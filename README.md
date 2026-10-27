# plaquette

Version sectorielle « Assurance » de la plaquette HelloLead (9 pages, 1440 × 810 pt).

## Livrables

- `Plaquette HelloLead - Assurance.pdf` — document final, 9 pages.
- `Plaquette HelloLead - Assurance (modifiable).pptx` — 9 diapositives au format du PDF ; visuels figés en image de fond, texte des blocs « Modération & Enrichissement » et des fiches acheteur éditable (une zone par ligne).
- `Rapport - Plaquette HelloLead Assurance.docx` (et `.md`) — cartographie, production, audit, écarts, doutes.

## Repères

- Pages 1, 2, 4, 8, 9 : strictement identiques à l'original (comparaison pixel à pixel).
- Pages 3 (SMS – RCS), 5 (META Ads), 6 (CALL), 7 (Emailing) : visuel, formulaire, bloc de modération et fiche acheteur remplacés ; le reste est inchangé.
- Les contenus sectoriels sont **fictifs** (document CONTENUS non transmis) et centralisés dans `work/contenus.json` ; `work/build_pdf.py` régénère le PDF à l'identique après remplacement des valeurs.
