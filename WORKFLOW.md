# Werkwijze

Deze repository bevat kleine hulpmiddelen voor administratie op verzoek via Codex. Moneybird blijft de centrale boekhouding. Er is geen permanente server of automatische verwerking.

## Huidige afspraak

- Werkadministratie: Pure Camper B.V.
- Q1 en Q2 2026 zijn volgens de gebruiker al ingediend.
- Nu voorbereiden: Q3 2026, 1 juli t/m 30 september.
- Volgende aangifte: Q4 2026, 1 oktober t/m 31 december.
- De gebruiker dient zelf in via Moneybird.

## Stappen

1. Controleer toegang zonder tokens te tonen. Gebruik de bestaande checkout.
2. Lees banktransacties voor de afgesproken rekening en periode. Een onverwerkte betaling bewijst niet dat een bon ontbreekt.
3. Vergelijk met bestaande documenten en lees relevante bijlagen voordat nieuwe boekingen worden voorgesteld. Mail-, betaal- en factuurdatum kunnen verschillen.
4. Leg ontbrekende documenten, mogelijke matches en afwijkingen voor. Een privébetaling wordt niet automatisch een zakelijke uitgave.
5. Wijzig Moneybird uitsluitend op concrete opdracht. Controleer factuurnummer, datum, valuta, btw-code, grootboekrekening en bronbestand. Herhaal een onzekere schrijfaanvraag niet blind.
6. Moneybird kan betalingen automatisch koppelen. Controleer de actuele toestand voordat een extra koppeling wordt toegevoegd en controleer daarna het open bedrag.
7. Maak een kwartaaloverzicht met de nog openstaande uitzonderingen. Dien geen aangifte in en voer geen bankbetalingen uit vanuit deze hulpmiddelen.

## Verplichte controle per factuur

Vergelijk vóór aanmaak of wijziging de ingevulde gegevens met de originele factuur. Een gelijk eindtotaal is geen voldoende controle: een onjuiste btw-code kan hetzelfde eindtotaal opleveren.

- Controleer leverancier, factuurnummer, factuurdatum, valuta, creditnota-status en of hetzelfde document al bestaat.
- Controleer afzonderlijk het bedrag exclusief btw, btw-bedrag en bedrag inclusief btw. Controleer of Moneybird op inclusief of exclusief staat en of prijs maal aantal, eventuele kortingen en afrondingen aansluiten.
- Kies de actieve inkoop-btw-code die overeenkomt met factuur én toepasselijke btw-behandeling. Neem nooit een standaardwaarde zoals vrijgesteld over zonder bewijs. Bij verlegging ook de aangifterubrieken controleren.
- Beschrijf de werkelijke aankoop of werkzaamheden. Neem geen omschrijving, termijnpercentage, orderreferentie of factuurregel van een eerdere factuur over.
- Onderbouw grootboekcategorie en project/caravan uit de factuur of bekende opdrachtcontext. Een eerder gebruikt project is geen bewijs. Laat een optioneel onbekend project leeg; blokkeer verwerking als noodzakelijke informatie ontbreekt.
- Controleer betalingstermijn en bestaande/geplande betalingen voordat een betaalopdracht wordt voorbereid. Betaalgegevens alleen uit gecontroleerde bronnen gebruiken.
- Sla een financiële wijziging niet op zolang een verschil of onzekere btw-behandeling onopgelost is. Vermeld precies wat nog moet worden vastgesteld.
- Lees na een wijziging de actuele opgeslagen boeking terug en vergelijk de bovenstaande velden en bedragen opnieuw. Gebruik waar nodig de synchronisatieleesroute in plaats van een mogelijk gecachet antwoord.

Bij een geconstateerde fout: beoordeel ook de andere facturen in dezelfde batch op dezelfde foutbron. Rapporteer gevonden afwijkingen; corrigeer bestaande boekingen alleen binnen de gegeven opdracht. Deze checklist is een werkinstructie, geen reeds ingebouwde automatische validatie.

## Gegevens en toegang

Tokens, IBANs, persoonlijke contactgegevens, bankexports, facturen en lokale verwerkingsverslagen horen niet in Git. Gebruik beveiligde omgevingsinstellingen en afgeschermde lokale opslag. Lokale administratiecontext staat in de huidige omgeving buiten de checkout; die wordt niet door een Git-clone hersteld. Controleer die beschikbaarheid bij een nieuwe omgeving.

De Moneybird-verbinding is in de huidige omgeving getest. Dat bewijst geen toegang in een nieuwe checkout. Gmail-tools zijn in de huidige chat niet beschikbaar; een vermelde Gmail-plugin of accountbrede ChatGPT-koppeling bewijst geen toegang vanuit Codex. Gebruik bestaande goedgekeurde toegang als die beschikbaar komt; vraag nooit om tokens in de chat.

De zeven afzonderlijke OpenAI-Q3-facturen zijn in de huidige Moneybird-administratie verwerkt. De import was een eenmalige handeling, geen functie van de CLI in deze repository. Voer geen nieuwe import uit zonder actuele controle op reeds aanwezige facturen. Gedetailleerde resultaten en rekeningmapping blijven buiten Git.
