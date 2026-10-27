# plaquette

Version sectorielle « Assurance » de la plaquette HelloLead (9 pages, 1440 × 810 pt).

## Livrables

- `Plaquette HelloLead - Assurance.pdf` — document final, 9 pages.
- `Plaquette HelloLead - Assurance (modifiable).pptx` — 9 diapositives au format du PDF ; visuels figés en image de fond (180 dpi), texte des blocs « Modération & Enrichissement » et des fiches acheteur éditable (une zone de texte par ligne, placée sur la ligne de base d'origine).
- `Rapport - Plaquette HelloLead Assurance.docx` (et `.md`) — cartographie, production, audit, écarts, doutes.

## Repères

- Pages 1, 2, 4, 8, 9 : strictement identiques à l'original (comparaison pixel à pixel des 9 pages : écart maximal = 0).
- Pages 3 (SMS – RCS), 5 (META Ads), 6 (CALL), 7 (Emailing) : visuel, formulaire, bloc de modération et fiche acheteur remplacés ; titres, puces, pictos, marques, légendes et cartes de fond inchangés.
- Contenus sectoriels : p3 = Assurance Protection Sociale Individuelle, p5 = IARD, p6 = Assurance Protection Sociale Collective, p7 = Gestion de Patrimoine.
- Toutes les données acheteur sont **fictives** ; contact, téléphone et e-mail restent masqués par les rectangles gris de l'original.

## Régénération

`work/contenus.py` (textes des blocs) → `work/build_vis3.py`, `work/build_shots.py`, `work/build_vis5.py`, `work/build_vis7.py` (visuels) → `work/build_pdf_v2.py` (PDF) → `work/build_pptx.py` (PPTX).

Le PPTX utilise la police **Poppins** : l'installer sur le poste de travail pour un rendu identique au PDF.
