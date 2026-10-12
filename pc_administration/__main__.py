import argparse
import datetime as dt
import json
import os
import sys

from .api import APIError, Gmail, Moneybird


def search_query(start, end, label):
    try:
        first, last = dt.date.fromisoformat(start), dt.date.fromisoformat(end)
    except ValueError:
        raise APIError('Gebruik datums in YYYY-MM-DD.') from None
    if first >= last or (last - first).days > 370:
        raise APIError('Kies een periode van 1 tot 370 dagen; einddatum is exclusief.')
    if not label or len(label) > 100 or any(c in label for c in '"\r\n\\'):
        raise APIError('Gebruik een geldig Gmail-label zonder aanhalingstekens.')
    # Explicit UTC instants avoid Gmail date-string timezone ambiguity.
    start_epoch = int(dt.datetime.combine(first, dt.time(), dt.timezone.utc).timestamp())
    end_epoch = int(dt.datetime.combine(last, dt.time(), dt.timezone.utc).timestamp())
    return f'label:"{label}" after:{start_epoch} before:{end_epoch}'


def main(argv=None):
    parser = argparse.ArgumentParser(description='Gmail–Moneybird: uitsluitend lezen.')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('demo', help='Offline proef met synthetische bron-ID’s.')
    sub.add_parser('moneybird-check', help='Moneybird-verbinding testen zonder Gmail of wijzigingen.')
    scan = sub.add_parser('scan', help='Kandidaten en bestaande document-ID’s ophalen.')
    scan.add_argument('--start', required=True)
    scan.add_argument('--end', required=True, help='Exclusieve einddatum; selectie in UTC.')
    scan.add_argument('--label', required=True, help='Alleen dit Gmail-label verwerken.')
    scan.add_argument('--max-messages', type=int, default=500)
    args = parser.parse_args(argv)
    try:
        if args.command == 'moneybird-check':
            client = Moneybird(os.environ.get('MONEYBIRD_API_TOKEN', ''),
                               os.environ.get('MONEYBIRD_ADMINISTRATION_ID', ''))
            documents = client.purchase_invoices()
            print(json.dumps({'mode': 'alleen_lezen', 'moneybird_access': 'verified',
                              'purchase_invoice_count': len(documents),
                              'quarter_ready': False}, indent=2))
            return 0
        if args.command == 'demo':
            gmail = [{'gmail_message_id': 'demo-message-1', 'status': 'nog_te_beoordelen'}]
            moneybird = [{'moneybird_document_id': '1001', 'status': 'bestaand_document'}]
            mode, period = 'demo_synthetisch', None
        else:
            query = search_query(args.start, args.end, args.label)
            if not 1 <= args.max_messages <= 5000:
                raise APIError('Berichtenlimiet moet tussen 1 en 5000 liggen.')
            gmail_client = Gmail(os.environ.get('GMAIL_ACCESS_TOKEN', ''))
            moneybird_client = Moneybird(os.environ.get('MONEYBIRD_API_TOKEN', ''),
                                         os.environ.get('MONEYBIRD_ADMINISTRATION_ID', ''))
            gmail = gmail_client.candidates(query, args.max_messages)
            moneybird = moneybird_client.purchase_invoices()
            mode, period = 'alleen_lezen', {'start': args.start, 'end_exclusive': args.end,
                                          'selection_timezone': 'UTC'}
        print(json.dumps({'mode': mode, 'period': period,
                          'source_scan_complete': True,
                          'quarter_ready': False,
                          'gmail_candidates': gmail,
                          'moneybird_documents': moneybird,
                          'warning': 'Nog geen documentanalyse, matching of btw-controle.'}, indent=2))
        return 0
    except APIError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
