# Plaquette HelloLead — version sectorielle « Assurance »

## Rapport de production et d'audit

**Document source :** `Plaquette HelloLead.pdf` — 9 pages, 1440 × 810 pt (20 × 11,25 in), paysage.
**Document livré :** `Plaquette HelloLead - Assurance.pdf` — 9 pages, même format, mêmes polices, même mise en page.
**Fichier de travail :** `Plaquette HelloLead - Assurance (modifiable).pptx` — 9 diapositives au format du PDF, visuels figés en image de fond, texte des blocs remplacés éditable.

---

## 0. Résumé

| Point | Résultat |
|---|---|
| Pages conservées strictement identiques | 1, 2, 4, 8, 9 — **pixel-identique** (comparaison `numpy.array_equal` sur rendu 120 dpi) |
| Pages modifiées | 3 (SMS – RCS), 5 (META Ads), 6 (CALL), 7 (Emailing) |
| Rubriques effectivement modifiées | uniquement les 4 autorisées : visuel · formulaire / page de destination · bloc « Modération & Enrichissement » · fiche acheteur |
| Rubriques non touchées | titres, sous-titres, puces, pictos, flèches, marques, légendes, cartes de fond, filets, rectangles de masquage |
| Nombre de lignes de texte par bloc | 16/13/11/13 (modération) et 10/10/10/11 (fiche) — **identique à l'original page par page** |
| Coordonnées du texte | première et dernière ligne de base identiques à l'original au 1/10 pt sur les 4 pages |
| Données réelles | aucune : entreprises, SIRET, adresses, téléphones, e-mails et marques d'annonceurs sont fictifs |

---

## 1. Étape 1 — Cartographie

Légende : les positions sont données en points PDF (origine en haut à gauche). « Remplacé ? » = **oui** uniquement pour les quatre rubriques autorisées.

### 1.1 Page 3 — SMS – RCS — secteur « Assurance Protection Sociale Individuelle »

| Élément | Position / géométrie (pt) | Style | Remplacé ? |
|---|---|---|---|
| Carte de fond gauche | (44,7 ; 10,3) → (465,9 ; 706,3) | aplat `#F4F5FC`, coins arrondis | non |
| Titre « SMS – RCS » | x = 61,4 ; y = 36,6 | Poppins Bold, bleu `#0A5BFF`, 29,99 pt | non |
| Sous-titre « Un contact direct et immédiat sur mobile » | x = 61,4 ; y = 92,9 (2 lignes) | Open Sans, 25 pt, bleu | non |
| 6 puces d'argumentaire | x = 85,2 ; 1re à y = 174,6 ; pas de 48 pt | Poppins Regular, 13,99 pt | non |
| Capture de l'interface HelloLead | xref 64, (61,4 ; 477,3) → (452,2 ; 679,0) | image, coins arrondis | non |
| Carte centrale + titre « Des campagnes immersives et personnalisées » | (483,0 ; 40,3) → (1064,9 ; 760,8) ; titre 29,99 pt | — | carte non, visuel oui |
| Visuel annonce RCS | xref 65, (516,9 ; 140,6) → (765,1 ; 439,8) | image 410 × 494 | **oui** |
| Visuel landing page / formulaire | xref 67, (520,7 ; 441,2) → (761,4 ; 748,7) | image 398 × 508 | **oui** |
| Visuel page hellodevis | xref 57, (755,1 ; 150,6) → (1041,6 ; 617,9) | image 540 × 881 | **oui** |
| Pictos complementaires (58, 64) + flèches bleues | (738,2 ; 596,8) → (881,4 ; 740,1) ; deux flèches | vectoriel | non |
| Carte droite | (1080,2 ; 166,3) → (1395,3 ; 800,2) | aplat `#F4F5FC` | non |
| Titre « Modération & Enrichissement » | x = 1098,9 ; y = 178,1 à 241,4 | Open Sans, 25 pt, bleu, 2 lignes | non |
| Questions / réponses de modération | x = 1098,9 ; première ligne de base y = 251,7 | Poppins Bold 13 bleu (questions) / Regular 13 noir (réponses), interligne 19,5 | **oui** |
| Fiche acheteur | x = 1098,9 ; première ligne de base y = 585,6 | Poppins Regular 13, interligne 19,5 | **oui** |
| Rectangles gris de masquage (contact, tél, mail) | (1158,3 ; 665,1) (1124,6 ; 743,4) (1132,1 ; 764,2) | aplat `#A29F9F` 15,6 pt de haut | non |

### 1.2 Page 5 — META Ads — secteur « IARD »

| Élément | Position / géométrie (pt) | Style | Remplacé ? |
|---|---|---|---|
| Carte de fond gauche | (51,8 ; 37,3) → (381,1 ; 609,8) | aplat `#F4F5FC` | non |
| Titre « META Ads » / sous-titre | x = 72,4 (y = 54,1 / 110,9) | Poppins Bold 29,99 / Open Sans 25, bleu | non |
| Paragraphe + 5 puces | paragraphe x = 72,4 ; puces x = 92,0 | Poppins Regular 13,99 | non |
| Carte centrale + titre « Formulaire instantané META ou redirection LP » | (396,4 ; 93,6) → (1056,8 ; 684,7) | — | carte non, visuel oui |
| Capture de l'annonce Meta | xref 174, (407,7 ; 209,4) → (722,7 ; 638,4) | image 519 × 707 | **oui** |
| Formulaire instantané Meta | xref 173, (710,5 ; 172,4) → (1058,5 ; 638,2) | image 393 × 526 | **oui** |
| Carte droite | (1073,1 ; 164,4) → (1388,2 ; 765,1) | aplat `#F4F5FC` | non |
| Titre « Modération & Enrichissement » | x = 1091,2 ; y = 187,0 à 250,3 | Open Sans 25 bleu, 2 lignes | non |
| Questions / réponses de modération | x = 1091,2 ; y = 266,8 | Poppins 13 / interligne 19,5 | **oui** |
| Fiche acheteur | x = 1091,2 ; première ligne de base y = 551,2 | Poppins Regular 13 | **oui** |
| Rectangles gris de masquage | (1151,0 ; 630,7) (1117,1 ; 708,2) (1124,7 ; 729,6) | aplat `#A29F9F` | non |

### 1.3 Page 6 — CALL — secteur « Assurance Protection Sociale Collective »

| Élément | Position / géométrie (pt) | Style | Remplacé ? |
|---|---|---|---|
| Carte de fond gauche | (44,7 ; 13,5) → (374,0 ; 559,0) | aplat `#F4F5FC` | non |
| Titre « CALL » / sous-titre / paragraphe / puces | x = 66,4 (titre y = 23,8) ; sous-titre 70,6 ; puces 88,1 | Poppins Bold 29,99 · Open Sans 25 · Poppins 13,99 | non |
| Carte centrale + titre « Précision du discours et richesse de l'échange » | (389,3 ; 96,0) → (1049,8 ; 746,3) | — | carte non, visuel oui |
| Capture du CRM HelloLead | xref 202, (410,8 ; 163,5) → (1046,1 ; 517,9) | image 1411 × 786 | **oui** |
| Photo du plateau téléphonique | xref 208, (349,1 ; 531,7) → (1096,1 ; 717,7) | image | non |
| Carte droite | (1066,0 ; 243,0) → (1395,3 ; 796,2) | aplat `#F4F5FC` | non |
| Titre « Modération & Enrichissement » | x = 1082,2 ; y = 256,0 à 319,3 | Open Sans 25 bleu, 2 lignes | non |
| Questions / réponses de modération | x = 1082,2 ; y = 336,1 | Poppins 13 / interligne 19,5 | **oui** |
| Fiche acheteur | x = 1082,2 ; première ligne de base y = 587,5 | Poppins Regular 13 | **oui** |
| Rectangles gris de masquage | (1141,9 ; 666,3) (1108,1 ; 746,4) (1116,4 ; 765,3) | aplat `#A29F9F` | non |

### 1.4 Page 7 — Emailing — secteur « Gestion de Patrimoine »

| Élément | Position / géométrie (pt) | Style | Remplacé ? |
|---|---|---|---|
| Carte de fond gauche | (44,7 ; 7,8) → (374,0 ; 545,5) | aplat `#F4F5FC` | non |
| Titre « Emailing » / sous-titre / paragraphe / puces | x = 68,2 (titre y = 23,8) ; puces x = 91,1 | Poppins Bold 29,99 · Open Sans 25 · Poppins 13,99 | non |
| Carte centrale + titre « Une diffusion portée par un message sur-mesure » | (389,3 ; 7,8) → (1050,7 ; 801,0) | — | carte non, visuel oui |
| E-mail ComparateurPro (gestion de patrimoine) | xref 239, (432,6 ; 88,0) → (724,4 ; 792,2) | image 328 × 791 | **oui** |
| E-mail ComparateurPro (bannière villa) | xref 236, (743,4 ; 96,4) → (1003,6 ; 516,4) | image 405 × 652 | **oui** |
| Bandeau ComparateurPro « 8h de temps » | xref 237, (743,4 ; 521,7) → (1000,6 ; 677,0) | image 562 × 339 | **oui** |
| Deux formulaires ComparateurPro | xref 238 (874,4 ; 696,0) → (999,6 ; 783,8) et 240 (748,1 ; 695,1) → (867,4 ; 784,3) | images 240 × 169 / 240 × 179 | **oui** |
| Carte droite | (1065,7 ; 194,4) → (1395,1 ; 802,9) | aplat `#F4F5FC` | non |
| Titre « Modération & Enrichissement » | x = 1081,9 ; y = 209,5 à 272,8 | Open Sans 25 bleu, 2 lignes | non |
| Questions / réponses de modération | x = 1081,9 ; y = 294,2 | Poppins 13 / interligne 19,5 | **oui** |
| Fiche acheteur | x = 1081,9 ; première ligne de base y = 564,8 | Poppins Regular 13 | **oui** |
| Rectangles gris de masquage | (1141,6 ; 662,7) (1107,8 ; 742,1) (1115,4 ; 763,1) | aplat `#A29F9F` | non |

### 1.5 Pages 1, 2, 4, 8, 9

Cartographie inchangée : aucun élément n'est listé comme remplaçable par le brief, ces pages n'ont donc fait l'objet d'aucune modification (voir § 4, contrôle pixel-identique).

---

## 2. Étape 2 — Production

**Principe technique.** Le PDF d'origine est repris tel quel, page par page. Sur les pages 3, 5, 6 et 7 :

1. les images des visuels sont remplacées par des images de **mêmes dimensions et même rapport** (`page.replace_image`, coins arrondis conservés par le masque alpha d'origine) ;
2. seule la zone de droite porteuse de texte est « nettoyée » (suppression du texte uniquement — les images et le trait/les aplats ne sont pas touchés, donc les rectangles gris de masquage restent exactement à leur place) ;
3. les blocs « Modération & Enrichissement » et fiche acheteur sont réécrits à position, corps et interligne identiques (Poppins 13 pt, interligne 19,5 pt), avec la même hiérarchie question en gras bleu `#0A5BFF` / réponse en noir ;
4. les pages 1, 2, 4, 8, 9 ne sont jamais ouvertes en écriture.

**Contenus sectoriels produits** (tous fictifs, voir § 6) :

| Page | Secteur | Entreprise (fictive) | Adresse / Ville / CP |
|---|---|---|---|
| 3 | Assurance Protection Sociale Individuelle | ATELIER DUVERGER | 9 rue des Lilas · Nantes · 44000 |
| 5 | IARD | MENUISERIE KLAAS | 8 rue des Chênes · Vichy · 03 200 |
| 6 | Assurance Protection Sociale Collective | BATIPRO SERVICES | 584 chemin des Vignes · Toulon · 83200 |
| 7 | Gestion de Patrimoine | HD PATRIMOINE | 114 rue de Flandre · Paris · 75019 |

SIRET fictifs (14 chiffres, même encombrement que l'original) : 81234567800019 / 81234567800027 / 81234567800035 / 81234567800043.

**Visuels reconstruits.** Maquettes redessinées à l'identique en géométrie (mêmes rectangles, mêmes rayons, mêmes couleurs de marque) : annonce RCS et page de destination hellodevis (p3) ; annonce et formulaire instantané Meta (p5, photo d'en-tête, carte de présentation puis trois cartes de questions et barre de validation au même emplacement, la troisième carte étant rognée par la barre comme dans l'original) ; CRM HelloLead (p6) ; deux e-mails, bandeau et deux formulaires ComparateurPro, palette jaune `#FFCD28` conservée (p7). Le message sombre de la page 7 reprend la structure de l'original (bandeau photo assombri, « BON À SAVOIR », paragraphes, encart illustration) et s'arrête sur un fond blanc, sans y ajouter de mentions. Les photos d'ambiance ont été générées pour l'occasion (voir § 6.4).

**Régénération.** Tout est reproductible : `contenus.json` (une entrée par valeur remplaçable) → `build_pdf.py` (assemblage) → `build_pptx.py` (version éditable). `check_lines.py` vérifie que le nombre de lignes de chaque bloc reste celui de l'original avant chaque export.

---

## 3. Étape 3 — Audit contre l'original

Méthode : rendu comparatif à 110, 120, 150, 180 et 600 dpi ; extraction des spans (position, corps, couleur) des deux documents ; mesure des encres ; comptage de lignes ; relevé des aplats et des images.

| Contrôle | Original | Livré | Verdict |
|---|---|---|---|
| Nombre de pages / format | 9 · 1440 × 810 pt | 9 · 1440 × 810 pt | conforme |
| p3 — lignes de modération | 16 | 16 | conforme |
| p3 — lignes de fiche | 10 | 10 | conforme |
| p5 — modération / fiche | 13 / 10 | 13 / 10 | conforme |
| p6 — modération / fiche | 11 / 10 | 11 / 10 | conforme |
| p7 — modération / fiche | 13 / 11 | 13 / 11 | conforme |
| p3 — 1re / dernière ligne de base | 251,7 / 761,1 | 251,7 / 761,1 | identique |
| p5 — 1re / dernière ligne de base | 266,8 / 726,7 | 266,8 / 726,6 | écart 0,1 pt (arrondi) |
| p6 — 1re / dernière ligne de base | 336,1 / 763,0 | 336,1 / 763,0 | identique |
| p7 — 1re / dernière ligne de base | 294,2 / 759,8 | 294,1 / 759,8 | écart 0,1 pt (arrondi) |
| Abscisse des blocs de droite | 1098,9 / 1091,2 / 1082,2 / 1081,9 | identique | identique |
| Corps de texte | 13,0 pt | 13,0 pt | identique |
| Interligne | 19,5 pt | 19,5 pt | identique |
| Couleur des questions | `#0A5BFF` | `#0A5BFF` | identique |
| Rectangles gris de masquage | 3 (p3, p5, p7) / 4 (p6) | mêmes rectangles, mêmes coordonnées | identique |
| Titres de blocs, titres de pages, puces | — | non modifiés, non redessinés | identique |
| Cadres / cartes de fond | 3 cartes par page | inchangés | identique |

Écarts corrigés pendant l'audit (et non des écarts résiduels) :

- **Décalage vertical de la fiche de la page 3** : la fiche était placée 13,7 pt trop haut, les rectangles gris tombaient alors sur la ligne « Adresse ». La ligne de base a été recalée à 599,3 pt (soit un sommet de glyphe à 585,6 pt, exactement comme l'original) ; le défaut a disparu et les 10 lignes retrouvent leur place.
- **Troncature du titre « Modération & Enrichissement »** : la zone de nettoyage démarrait trop haut et effaçait le titre. Elle commence désormais juste sous le titre, page par page (246 / 249 / 318 / 271 pt).
- **Traces de données réelles** dans une version intermédiaire (anciennes raisons sociales, adresses, SIRET, téléphones) : toutes remplacées ; contrôle par recherche plein texte sur les 9 pages, aucune occurrence résiduelle.

---

## 4. Étape 4 — Contrôle final

| Critère | Statut |
|---|---|
| 9 pages | ✔ |
| Pages 1, 2, 4, 8, 9 strictement identiques | ✔ rendu 120 dpi comparé octet à octet (`array_equal` = True sur les 5 pages) |
| Aucun débordement ni troncature | ✔ dernière ligne de chaque bloc au-dessus du bas de carte (p3 : 761,1 < 800,2 ; p5 : 726,6 < 765,1 ; p6 : 763,0 < 796,2 ; p7 : 759,8 < 802,9) ; aucun texte hors des cartes à droite |
| Valeurs des contenus reprises mot pour mot | ✔ contrôle automatique : toutes les valeurs des blocs « modération » et « fiche » sont retrouvées dans le texte du PDF ; seules les 3 valeurs masquées par page (contact, tél, mail) sont volontairement absentes |
| Aucune donnée réelle | ✔ entreprises, SIRET, adresses, téléphones, e-mails, marques d'annonceurs fictifs ; aucun logo d'assureur ; aucune mention réglementaire ajoutée |
| Polices, corps, couleurs, marges | ✔ Poppins / Open Sans, 13 pt, 19,5 pt d'interligne, `#0A5BFF`, abscisses d'origine |
| Marques de l'original conservées | ✔ HelloLead, hellodevis, ComparateurPro |
| Version modifiable | ✔ PPTX 9 diapositives au format du PDF, texte des deux blocs éditable |

---

## 5. Tableau récapitulatif, page par page

| Page | Titre | Statut | Détail |
|---|---|---|---|
| 1 | Couverture | **identique** | page non ouverte en écriture |
| 2 | Sommaire / présentation | **identique** | idem |
| 3 | SMS – RCS | **modifié** | visuel, formulaire/page de destination, modération, fiche |
| 4 | Assurance agricole | **identique** | idem |
| 5 | META Ads | **modifié** | visuel, formulaire instantané, modération, fiche |
| 6 | CALL | **modifié** | capture CRM, modération, fiche (photo du plateau conservée) |
| 7 | Emailing | **modifié** | e-mails, bannière, formulaires, modération, fiche |
| 8 | (page d'origine) | **identique** | idem |
| 9 | (page de clôture) | **identique** | idem |

---

## 6. Doutes et décisions appliquées

**6.1 Le document CONTENUS n'a pas été transmis.** Aucun texte sectoriel d'origine n'était donc disponible. Décision appliquée (règle « en cas de doute, s'aligner sur l'original ») : produire une trame complète, cohérente et **fictive** par secteur, en conservant strictement la structure, le nombre de questions et la longueur des blocs de l'original. Chaque valeur est isolée dans `contenus.json` et peut être remplacée champ par champ, la mise en page étant régénérée automatiquement à l'identique. **Tous les contenus sectoriels sont donc à valider / remplacer par les contenus définitifs.**

**6.2 Interprétation de « Modération et Enrichissement ».** Le bloc ne contient, dans l'original, que le titre et une liste de questions/réponses de qualification de l'acheteur. Le titre est conservé mot pour mot ; seules les questions/réponses sont adaptées au secteur. Aucun autre texte n'a été ajouté dans le bloc.

**6.3 Questions trop longues pour la zone.** Règle appliquée : reformuler plus court, jamais réduire le corps, jamais déplacer l'élément. Cas rencontrés : p7 Q1 « Êtes-vous déjà accompagné par un conseiller en gestion de patrimoine ? » ; p3 Q7 « Recherchez-vous une garantie optique et dentaire ? » ; les libellés longs p5 Q2, p5 Q5, p6 Q1 ont été calés pour tenir en 1 ou 2 lignes exactement comme l'original.

**6.4 Photographies.** Aucune banque d'images n'était fournie : les photos d'ambiance (famille en salle d'attente p3, atelier de menuiserie p5, intérieur de villa p7) ont été générées par IA, avec le même cadrage, le même rapport et les mêmes coins arrondis que l'original. Elles sont réalistes, sans texte ni logo, mais **ne sont pas les photos d'origine** : à remplacer si une iconothèque est imposée.

**6.5 Noms d'annonceurs dans les maquettes.** Les captures de l'original affichaient des annonceurs réels. Pour ne citer aucun tiers, une marque fictive unique (« AssurDevis ») a été utilisée dans les maquettes reconstruites. Les marques propres à l'original (HelloLead, hellodevis, ComparateurPro) sont conservées.

**6.6 Données de la fiche acheteur.** Entreprise, SIRET, activité, adresse, ville et code postal sont fictifs (SIRET en 812 345 678 000xx, téléphones en 06 00 xx xx xx). Contact, téléphone et e-mail restent masqués par les rectangles gris, exactement comme dans l'original : ces trois informations ne sont donc pas lisibles, et les valeurs correspondantes ne sont pas imprimées.

**6.7 Coquille de l'original conservée.** Le libellé « Auto-entrepeneur / micro-entrepreneur » (p6) comporte la même faute que l'original ; conformément à la consigne « ne rien corriger spontanément », il n'a pas été rectifié.

**6.8 Version PowerPoint.** La mise en page et les visuels sont figés dans l'image de fond (aucun objet déplaçable) ; le texte des blocs « Modération & Enrichissement » et des fiches est éditable, **une zone de texte par ligne** afin de garantir un rendu identique au PDF. Conséquence : en modifiant la longueur d'une ligne, il faut réajuster manuellement les lignes voisines. Le PDF reste le document de référence.
