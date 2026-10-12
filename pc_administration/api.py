"""API structure adapted from BirdGPT; see third_party/birdgpt/LICENSE.

No generic API path or write operation is exposed.
"""

import json
import re
import urllib.error
import urllib.parse
import urllib.request


class APIError(RuntimeError):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Do not forward credentials to a redirect destination.
        return None


class ReadOnlyAPI:
    MAX_RESPONSE = 8 * 1024 * 1024

    def __init__(self, token, base):
        if not token or any(c in token for c in '\r\n'):
            raise APIError('Een geldig toegangstoken ontbreekt.')
        self._token = token
        self._base = base
        self._opener = urllib.request.build_opener(NoRedirect())

    def _get(self, path, params=None):
        url = self._base + path
        if params:
            url += '?' + urllib.parse.urlencode(params)
        request = urllib.request.Request(
            url, method='GET', headers={
                'Authorization': 'Bearer ' + self._token,
                'Accept': 'application/json',
            })
        try:
            with self._opener.open(request, timeout=30) as response:
                body = response.read(self.MAX_RESPONSE + 1)
        except urllib.error.HTTPError as exc:
            raise APIError(f'API-verzoek geweigerd (HTTP {exc.code}); scan afgebroken.') from None
        except (urllib.error.URLError, TimeoutError, OSError):
            raise APIError('Netwerkfout; scan is niet volledig.') from None
        if len(body) > self.MAX_RESPONSE:
            raise APIError('API-antwoord is te groot; scan afgebroken.')
        try:
            return json.loads(body)
        except (ValueError, UnicodeError):
            raise APIError('Ongeldig API-antwoord; scan afgebroken.') from None


class Gmail(ReadOnlyAPI):
    def __init__(self, token):
        super().__init__(token, 'https://gmail.googleapis.com/gmail/v1/users/me/')

    def candidates(self, query, max_messages=500):
        records, seen, page = [], set(), None
        while True:
            params = {'q': query, 'maxResults': min(100, max_messages)}
            if page:
                params['pageToken'] = page
            result = self._get('messages', params)
            if not isinstance(result, dict):
                raise APIError('Onverwacht Gmail-antwoord.')
            for message in result.get('messages', []):
                ident = message.get('id', '')
                if not re.fullmatch(r'[A-Za-z0-9_-]+', ident):
                    raise APIError('Ongeldig Gmail-bericht-ID.')
                if ident in seen:
                    raise APIError('Dubbel bericht in paginering; scan afgebroken.')
                seen.add(ident)
                records.append({'gmail_message_id': ident, 'status': 'nog_te_beoordelen'})
                if len(records) > max_messages:
                    raise APIError('Berichtenlimiet bereikt; verklein de zoekperiode.')
            next_page = result.get('nextPageToken')
            if not next_page:
                return records
            if next_page == page or not result.get('messages'):
                raise APIError('Gmail-paginering stagneert; scan afgebroken.')
            page = next_page


class Moneybird(ReadOnlyAPI):
    def __init__(self, token, administration_id):
        if not re.fullmatch(r'[0-9]+', administration_id or ''):
            raise APIError('Moneybird-administratie-ID moet uit cijfers bestaan.')
        super().__init__(token, 'https://moneybird.com/api/v2/' + administration_id + '/')

    def purchase_invoices(self, max_documents=10000):
        records, seen = [], set()
        for page in range(1, max_documents // 100 + 2):
            result = self._get('documents/purchase_invoices.json', {'page': page, 'per_page': 100})
            if not isinstance(result, list):
                raise APIError('Onverwacht Moneybird-antwoord.')
            for item in result:
                ident = str(item.get('id', ''))
                if not re.fullmatch(r'[0-9]+', ident) or ident in seen:
                    raise APIError('Ongeldig of herhaald document-ID; scan afgebroken.')
                seen.add(ident)
                # Do not persist invoice content, names, descriptions or amounts yet.
                records.append({'moneybird_document_id': ident, 'status': 'bestaand_document'})
                if len(records) > max_documents:
                    raise APIError('Documentenlimiet bereikt; scan afgebroken.')
            if len(result) < 100:
                return records
        raise APIError('Paginering onvolledig; scan afgebroken.')
