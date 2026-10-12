import contextlib
import io
import json
import unittest
import urllib.error
from unittest.mock import patch

from pc_administration.api import APIError, Gmail, Moneybird, NoRedirect
from pc_administration.__main__ import main, search_query


class ReadOnlyTests(unittest.TestCase):
    def test_moneybird_check_does_not_require_gmail(self):
        output = io.StringIO()
        with patch.dict('os.environ', {'MONEYBIRD_API_TOKEN': 'test',
                                      'MONEYBIRD_ADMINISTRATION_ID': '123'}, clear=True):
            with patch.object(Moneybird, 'purchase_invoices', return_value=[]) as read:
                with patch.object(Gmail, '__init__', side_effect=AssertionError('Gmail')):
                    with contextlib.redirect_stdout(output):
                        self.assertEqual(main(['moneybird-check']), 0)
        read.assert_called_once()
        self.assertEqual(json.loads(output.getvalue())['purchase_invoice_count'], 0)

    def test_gmail_visits_all_pages(self):
        client = Gmail('test-token')
        with patch.object(client, '_get', side_effect=[
            {'messages': [{'id': 'a'}], 'nextPageToken': 'page2'},
            {'messages': [{'id': 'b'}]},
        ]) as get:
            self.assertEqual(len(client.candidates('label:Invoices')), 2)
            self.assertEqual(get.call_args_list[1].args[1]['pageToken'], 'page2')

    def test_gmail_limit_is_failure_not_partial_success(self):
        client = Gmail('test-token')
        with patch.object(client, '_get', return_value={'messages': [{'id': 'a'}, {'id': 'b'}]}):
            with self.assertRaises(APIError):
                client.candidates('label:Invoices', max_messages=1)

    def test_gmail_repeated_page_fails(self):
        client = Gmail('test-token')
        with patch.object(client, '_get', side_effect=[
            {'messages': [{'id': 'a'}], 'nextPageToken': 'page2'},
            {'messages': [{'id': 'a'}], 'nextPageToken': 'page2'},
        ]):
            with self.assertRaises(APIError):
                client.candidates('label:Invoices')

    def test_moneybird_reads_second_page_and_minimizes_content(self):
        client = Moneybird('test-token', '123')
        first = [{'id': str(i), 'reference': 'PRIVATE'} for i in range(100)]
        with patch.object(client, '_get', side_effect=[first, [{'id': '100'}]]) as get:
            records = client.purchase_invoices()
            self.assertEqual(len(records), 101)
            self.assertNotIn('PRIVATE', json.dumps(records))
            self.assertEqual(get.call_args_list[1].args[1]['page'], 2)

    def test_administration_cannot_inject_path(self):
        with self.assertRaises(APIError):
            Moneybird('test-token', '../other')

    def test_redirect_never_forwards_authorization(self):
        self.assertIsNone(NoRedirect().redirect_request(None, None, 302, '', {}, 'https://evil.example'))

    def test_http_error_is_redacted_and_method_is_get(self):
        client = Gmail('PRIVATE-TOKEN')
        error = urllib.error.HTTPError('https://example', 401, 'PRIVATE-TOKEN', {}, None)
        with patch.object(client._opener, 'open', side_effect=error) as opened:
            with self.assertRaises(APIError) as caught:
                client.candidates('label:Invoices')
            self.assertNotIn('PRIVATE', str(caught.exception))
            request = opened.call_args.args[0]
            self.assertEqual(request.get_method(), 'GET')
            self.assertTrue(request.full_url.startswith('https://gmail.googleapis.com/'))

    def test_label_cannot_escape_search(self):
        with self.assertRaises(APIError):
            search_query('2026-07-01', '2026-10-01', 'x" OR in:anywhere')

    def test_demo_never_contacts_accounts(self):
        output = io.StringIO()
        with patch.object(Gmail, 'candidates', side_effect=AssertionError('network')):
            with contextlib.redirect_stdout(output):
                self.assertEqual(main(['demo']), 0)
        report = json.loads(output.getvalue())
        self.assertFalse(report['quarter_ready'])
        self.assertEqual(report['mode'], 'demo_synthetisch')

    def test_failed_scan_has_no_success_report(self):
        output = io.StringIO()
        with patch.dict('os.environ', {'GMAIL_ACCESS_TOKEN': 'test',
                                      'MONEYBIRD_API_TOKEN': 'test',
                                      'MONEYBIRD_ADMINISTRATION_ID': '123'}):
            with patch.object(Gmail, 'candidates', side_effect=APIError('onvolledig')):
                with contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(main(['scan', '--start', '2026-07-01', '--end', '2026-10-01',
                                           '--label', 'Invoices']), 1)
        self.assertEqual(output.getvalue(), '')


if __name__ == '__main__':
    unittest.main()
