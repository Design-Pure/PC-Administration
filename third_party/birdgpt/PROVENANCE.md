# Herkomst

Bron: https://github.com/janyksteenbeek/birdgpt

Versie: commit 3d0d644 (17 november 2024). Zie LICENSE voor de oorspronkelijke MIT-licentie van Janyk Steenbeek.

De twee Go-bestanden zijn ongewijzigde referenties, geen uitvoerbare onderdelen van onze applicatie. De Python-connectors gebruiken de API-opbouw en Gmail-selectie van dit project als uitgangspunt. Ze vervangen automatische boekingen door expliciet begrensde leesverzoeken. Er wordt geen upstream-code uitgevoerd, geen OpenAI-call gedaan en geen OAuth-token op schijf opgeslagen.

De Python-versie is een aangepaste basis, geen complete fork van BirdGPT. Gmail-paginering, foutafhandeling, vaste bestemmingen en het rapport zonder mailinhoud zijn opnieuw uitgewerkt. Authentiseren gebeurt voorlopig uitsluitend met reeds verkregen tokens via de procesomgeving. Duurzame OAuth-autorisatie en documentimport zijn volgende stappen.
