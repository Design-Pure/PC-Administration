# PC Administration

Eerste basis voor Gmail-bonnetjes en voorbereiding van een Nederlandse btw-aangifte in Moneybird. Je dient zelf in via Moneybird.

## Hergebruik

We hebben twee connectorbestanden van [BirdGPT](https://github.com/janyksteenbeek/birdgpt) overgenomen als vastgelegde referentie. De oorspronkelijke MIT-licentie en herkomst staan in [third_party/birdgpt](third_party/birdgpt/PROVENANCE.md). De uitvoerbare Python-code is daarvan een aangepaste leesbasis. De upstream Go-bestanden worden niet uitgevoerd. Er is geen Go-toolchain nodig.

Automatische contacten/boekingen, externe AI-verwerking en lokale tokenbestanden uit het oorspronkelijke project zijn niet opgenomen.

## Starten

Python 3.12 of hoger; geen externe packages nodig. Werk vanuit de bestaande checkout; maak geen extra Git-worktree voor een cloudtaak.

```bash
cd /workspace/PC-Administration
python -m unittest discover -s tests -v
python -m pc_administration demo
```

De demo gebruikt uitsluitend synthetische bron-ID's. Dit bewijst geen verbinding met jouw accounts.

## Accountscan

Begin klein met alleen Moneybird. Nadat `MONEYBIRD_API_TOKEN` en `MONEYBIRD_ADMINISTRATION_ID` via beveiligde instellingen beschikbaar zijn:

```bash
python -m pc_administration moneybird-check
```

Deze controle leest de inkoopdocumenten en toont uitsluitend het aantal. Hij vereist geen Gmail-token en wijzigt niets. Een succes bewijst toegang tot de documentleesroute, geen volledige kwartaalcontrole.

Alleen uitvoeren nadat je toegang en gegevensopslag hebt ingericht. Injecteer deze variabelen via beveiligde instellingen, nooit via chat, een commit of een shellcommando met het token als argument:

- `MONEYBIRD_API_TOKEN`: persoonlijk token met de voor de documentleesroute vereiste scope `documents`.
- `MONEYBIRD_ADMINISTRATION_ID`: expliciet gekozen administratie-ID, alleen cijfers.
- `GMAIL_ACCESS_TOKEN`: reeds geautoriseerd toegangstoken met `gmail.readonly`.

De app doet uitsluitend GET-verzoeken. Moneybird-scopes kunnen zelf ook schrijven toelaten; leesbeperking in deze app is geen beperking van een gestolen token. Gmail-leesrechten omvatten de mailbox; het gekozen label beperkt de verwerking, niet de tokenrechten.

Vereiste HTTPS-bestemmingen voor deze scan: `moneybird.com` en `gmail.googleapis.com`. TLS-verificatie blijft actief en redirects worden geweigerd om tokenlekkage naar andere bestemmingen te voorkomen. Gebruik proxy-geïnjecteerde tokens alleen via hun geconfigureerde bestemming.

```bash
python -m pc_administration scan --start 2026-07-01 --end 2026-10-01 --label Administratie
```

De einddatum is exclusief, de zoekgrenzen zijn in UTC en de selectie gebruikt ontvangsttijd. Gebruik rond het kwartaal een ruimere periode; dit is nog geen selectie op fiscale documentdatum. De standaardlimiet is 500 berichten. Een overschreden limiet of onvolledige scan geeft een foutcode zonder succesrapport.

De JSON-uitvoer bevat Gmail-kandidaat-ID's en alle bestaande Moneybird-inkoopdocument-ID's. Geen mailinhoud, bijlagen of bedragen worden opgeslagen. Ook ID's zijn persoonsgegevens/administratieve metadata: deel of bewaar de uitvoer zorgvuldig. `source_scan_complete` betekent uitsluitend dat deze bronlijsten zijn opgehaald; `quarter_ready` blijft `false`.

## Nog te bouwen

Deze versie doet **nog geen** volledige OAuth-autorisatie of tokenvernieuwing, bijlagedownload, OCR, documentmatching, voorstellen met bedragen, import of btw-controle. Een verlopen token geeft een fout; er wordt niet naar credentials gevraagd of automatisch opnieuw geboekt.

Volgende stap: duurzame beveiligde OAuth en gecontroleerde documentverwerking met een importregister. Daarna een beoordeelde sandboximport en de kwartaalcontrole. Goedkeuring voor een algemene accountscan is geen goedkeuring voor latere boekingen.
