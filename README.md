# plaquette

Version sectorielle « Assurance » de la plaquette HelloLead (9 pages, 1440 × 810 pt).

## Livrables

- `Plaquette HelloLead - Assurance V3.pdf` — document final corrigé (page 3 revue), 9 pages. À utiliser en priorité.
- `Plaquette HelloLead - Assurance V2 (1).pdf` — version précédente, conservée pour comparaison (page 3 : cartes RCS à revoir).
- `Plaquette HelloLead - Assurance (modifiable).pptx` — 9 diapositives au format du PDF ; visuels figés en image de fond (180 dpi), texte des blocs « Modération & Enrichissement » et des fiches acheteur éditable (une zone de texte par ligne, placée sur la ligne de base d'origine). Diapositive 3 alignée sur la V3.
- `Rapport - Plaquette HelloLead Assurance.docx` (et `.md`) — cartographie, production, audit, écarts, doutes, corrections.

## Repères

- Pages 1, 2, 4, 8, 9 : strictement identiques à l'original (comparaison pixel à pixel des 9 pages : écart maximal = 0).
- Pages 3 (SMS – RCS), 5 (META Ads), 6 (CALL), 7 (Emailing) : visuel, formulaire, bloc de modération et fiche acheteur remplacés ; titres, puces, pictos, marques, légendes et cartes de fond inchangés.
- Contenus sectoriels : p3 = Assurance Protection Sociale Individuelle, p5 = IARD, p6 = Assurance Protection Sociale Collective, p7 = Gestion de Patrimoine.
- Toutes les données acheteur sont **fictives** ; contact, téléphone et e-mail restent masqués par les rectangles gris de l'original.

## Correction de la page 3 (V3)

Les deux cartes RCS (annonce SMS) ont été reconstruites et reposées sur la géométrie exacte des cartes d'origine : plus de bandes résiduelles de l'ancien visuel, texte qui ne passe plus sous le chevron, bouton d'action visible et contenu dans la carte, flèche « lien du RCS » repassée sous les cartes, titre « Des campagnes immersives et personnalisées » ramené à sa largeur d'origine. Détail dans le rapport, § 7.

## Régénération

Page 3 (V3) : `work/contenus_p3.py` (textes des cartes) → `work/build_cartes_p3.py` (visuels des deux cartes) → `work/build_p3.py` (PDF `… V3.pdf`) → `work/build_pptx_p3.py` (diapositive 3 du PPTX).

Pipeline V2 (pages 5 à 7) : `work/contenus.py` → `work/build_vis3.py`, `work/build_shots.py`, `work/build_vis5.py`, `work/build_vis7.py` (visuels) → `work/build_pdf_v2.py` (PDF) → `work/build_pptx.py` (PPTX).

Le PPTX utilise la police **Poppins** : l'installer sur le poste de travail pour un rendu identique au PDF.
