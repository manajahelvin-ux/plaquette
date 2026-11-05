# plaquette

Versions sectorielles de la plaquette HelloLead (9 pages, 1440 × 810 pt).

| Secteur | PDF de référence | Companion modifiable | Rapport |
| --- | --- | --- | --- |
| Assurance | `Plaquette HelloLead - Assurance V3.pdf` | `Plaquette HelloLead - Assurance (modifiable).pptx` | `Rapport - Plaquette HelloLead Assurance.docx` |
| Panneaux solaires | `Plaquette HelloLead - Panneaux solaires.pdf` | `Plaquette HelloLead - Panneaux solaires (modifiable).pptx` | `Rapport - Plaquette HelloLead Panneaux solaires.docx` |

## Version « Panneaux solaires »

Déclinaison solaire construite sur la même trame : pages sectorielles p3 (SMS – RCS), p5 (META
Ads), p6 (CALL) et p7 (Emailing) ; toutes les autres pages sont strictement identiques à
l'original.

- Segments retenus, d'après les rubriques CRM `id_rubrique=2019809` (EDF Solutions solaires) et
  `id_rubrique=2017948` (Panneaux photovoltaïques) :
  p3 = installation photovoltaïque résidentielle (comparateur d'installateurs),
  p4 = page de destination professionnelle (toiture d'entreprise, autoconsommation),
  p5 = SOLARIS ÉNERGIE, devis panneaux solaires,
  p6 = fiche CRM d'un projet photovoltaïque B2B,
  p7 = séquence e-mailing installateur solaire.
- Sur chaque page sectorielle, seules quatre rubriques sont modifiées : visuel, formulaire / page
  de destination, bloc « Modération & Enrichissement » et fiche acheteur. Titres, puces, pictos,
  flèches, marques, légendes et cartes de fond sont inchangés ; le nombre de lignes de chaque
  bloc est identique à l'original.
- Contrôle pixel à pixel (rendu 100 dpi) : pages 1, 2, 8, 9 **identiques** (0 pixel d'écart) ;
  pages 3, 4, 5, 6, 7 modifiées uniquement dans les zones autorisées (visuel, formulaire, panneau
  de modération, fiche acheteur) — les colonnes de titres et de puces de gauche ne bougent pas.
- Page 4 : les six logos d'assureurs de la bande de ré-assurance (Gan, Allianz, Groupama, AXA,
  MACIF, Hiscox) sont retirés et remplacés par une mention neutre ; aucun logo d'installateur
  n'est inventé.
- Direction artistique solaire assumée : pavillon équipé de panneaux, toiture au crépuscule,
  installateurs sur le toit. Les visuels de la page 7 (e-mails) ont été repris pour que la page
  ne se lise plus comme une page « patrimoine » — photo d'accroche, bannière, accroche du
  bandeau sombre et suppression de la vignette « € » (voir rapport, § 7 bis).
- Toutes les données acheteur sont **fictives** ; contact, téléphone et e-mail restent masqués par
  les rectangles gris de l'original.
- Régénération : `work/solaire/contenus.py` (textes) → `build_cartes.py` (cartes SMS) →
  `build_pdf.py` (PDF de référence ; `FOND=1` produit les fonds sans texte) → `build_pptx.py`
  (PPTX modifiable). Voir le rapport, § 10.

## Version « Assurance »

- `Plaquette HelloLead - Assurance V3.pdf` — document final corrigé (page 3 revue), 9 pages. À utiliser en priorité.
- `Plaquette HelloLead - Assurance V2 (1).pdf` — version précédente, conservée pour comparaison (page 3 : cartes RCS à revoir).
- `Plaquette HelloLead - Assurance (modifiable).pptx` — 9 diapositives au format du PDF ; visuels figés en image de fond (180 dpi), texte des blocs « Modération & Enrichissement » et des fiches acheteur éditable (une zone de texte par ligne, placée sur la ligne de base d'origine). Diapositive 3 alignée sur la V3.
- `Rapport - Plaquette HelloLead Assurance.docx` (et `.md`) — cartographie, production, audit, écarts, doutes, corrections.
- Pages 1, 2, 4, 8, 9 : strictement identiques à l'original.
- Contenus sectoriels : p3 = Assurance Protection Sociale Individuelle, p5 = IARD, p6 = Assurance Protection Sociale Collective, p7 = Gestion de Patrimoine.
- Correction de la page 3 (V3) : les deux cartes RCS (annonce SMS) ont été reconstruites et reposées sur la géométrie exacte des cartes d'origine — plus de bandes résiduelles, texte qui ne passe plus sous le chevron, bouton d'action contenu dans la carte, flèche « lien du RCS » repassée sous les cartes, titre « Des campagnes immersives et personnalisées » ramené à sa largeur d'origine.
- Régénération : `work/contenus_p3.py` → `work/build_cartes_p3.py` → `work/build_p3.py` (`… V3.pdf`) → `work/build_pptx_p3.py` (diapositive 3 du PPTX). Pipeline V2 (pages 5 à 7) : `work/contenus.py` → `work/build_vis3.py`, `build_shots.py`, `build_vis5.py`, `build_vis7.py` → `work/build_pdf_v2.py` → `work/build_pptx.py`.

Les deux PPTX utilisent la police **Poppins** : l'installer sur le poste de travail pour un rendu
identique au PDF.
