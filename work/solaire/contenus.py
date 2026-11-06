# -*- coding: utf-8 -*-
"""Contenus de la plaquette « Panneaux solaires ».

Tous les textes de secteur (pages 3 à 7) sont regroupés ici :
cartes RCS, maquettes (page de destination, formulaire META, CRM, emails),
blocs « Modération & Enrichissement » et fiches acheteur.

Règle de mise en page : chaque bloc reprend exactement le nombre de lignes de
l'original et se cale sur les mêmes lignes de base (voir panneaux_origine.json).

Les fiches décrivent des ACHETEURS de panneaux solaires (prospects finaux),
jamais des installateurs : quatre profils B2B (pages 3, 4, 6, 7) et un profil
B2C (page 5, dont les visuels et le formulaire sont orientés résidence
principale). Aucune donnée réelle : sociétés, SIRET, adresses et contacts sont
fictifs ; téléphone et e-mail restent masqués dans la maquette.
"""

# --------------------------------------------------------------- page 3 (SMS - RCS)

CARTE_1 = {
    "kicker": ["PHOTOVOLTAÏQUE", "ENTREPRISES & PROFESSIONNELS"],
    "bandeau": "DEVIS GRATUIT • INSTALLATEURS RGE",
    "titre": "Panneaux solaires : divisez votre facture",
    "texte": (
        "Réduisez la facture de votre site et comparez les installateurs "
        "agréés de votre région."
    ),
    "cta": "Ça m'intéresse !",
    "cta_couleur": (10, 91, 255),
    "cta_icone": "chevron",
}

CARTE_2 = {
    "kicker": [],
    "titre": "Solaire : faites le point sur votre projet",
    "texte": (
        "Toiture, ombrières, autoconsommation : recevez des offres "
        "d'installateurs agréés de votre secteur."
    ),
    "cta": "Obtenir une offre !",
    "cta_couleur": (17, 17, 17),
    "cta_icone": "cercle",
}

# Page de destination « hellodevis » (image de la page 3) : textes réécrits à
# l'identique en nombre de lignes.
P3_LANDING = {
    "titre": ["Trouvez le meilleur", "Partenaire", "pour votre projet", "photovoltaïque !"],
    "intro": ["Comparez les offres de panneaux", "solaires et d'autoconsommation",
              "adaptées à votre bâtiment."],
    "question": ["Concernant votre projet,", "vous êtes :"],
    "choix": ["Particulier", "Professionnel"],
}

# ------------------------------------------------------- colonnes de droite

# (texte, gras) — gras = étiquette bleue, sinon valeur noire.
# « mod » = qualification du besoin d'achat ; « fiche » = coordonnées de
# l'acheteur final (entreprise utilisatrice ou particulier), pas de l'installateur.
PANNEAUX = {
    3: {
        "mod": [
            ("Type de projet solaire :", True),
            ("Photovoltaïque en autoconsommation", False),
            ("avec revente du surplus", False),
            ("Statut de l’acheteur :", True),
            ("Professionnel (B2B), propriétaire", False),
            ("Type de bâtiment :", True),
            ("Entrepôt logistique, toiture bac acier", False),
            ("Surface de toiture disponible :", True),
            ("500 à 1 000 m²", False),
            ("Consommation annuelle d’électricité :", True),
            ("80 000 à 120 000 kWh", False),
            ("Budget envisagé :", True),
            ("70 000 € à 120 000 €", False),
            ("Sous quel délai souhaitez-vous être", True),
            ("équipé ?", True),
            ("Dans 3 à 6 mois", False),
        ],
        "fiche": [
            "Entreprise : DOCKS DE L’OUEST",
            "Siret : 91357924600018",
            "Activité : (Entreposage et logistique",
            "pour la distribution régionale)",
            "Contact :",
            "Adresse : 24 quai des Frégates",
            "Ville : Nantes",
            "Code Postal : 44200",
            "Tél :",
            "Mail :",
        ],
    },
    4: {
        "mod": [
            ("Type de projet solaire :", True),
            ("Photovoltaïque en autoconsommation", False),
            ("avec revente du surplus", False),
            ("Surface de toiture disponible :", True),
            ("250 à 500 m²", False),
            ("Échéance du projet :", True),
            ("Dans 3 à 6 mois", False),
        ],
        "fiche": [
            "Entreprise : HÔTEL DES EMBRUNS",
            "Siret : 90246813500027",
            "Activité : (Hôtellerie et restauration",
            "avec espace bien-être et",
            "parking couvert)",
            "Contact : ",
            "Adresse : 9 avenue du Littoral",
            "Ville : Saint-Malo",
            "Code postal : 35400",
            "Tél : ",
            "Mail : ",
        ],
    },
    5: {
        "mod": [
            ("Quel type de projet solaire ?", True),
            ("Photovoltaïque en autoconsommation", False),
            ("Vous envisagez cette installation :", True),
            ("à titre personnel (B2C)", False),
            ("Statut et type de bien :", True),
            ("Propriétaire occupant, maison", False),
            ("Surface de toiture disponible :", True),
            ("30 à 50 m²", False),
            ("Sous quel délai souhaitez-vous être", True),
            ("équipé ?", True),
            ("Sous 6 mois", False),
            ("Puissance de l’installation :", True),
            ("3 à 6 kWc", False),
        ],
        "fiche": [
            "Nom : MARTIN (exemple fictif)",
            "Siret : Sans objet (particulier)",
            "Projet : (Équipement de la",
            "résidence principale)",
            "Contact :",
            "Adresse : 16 rue des Tilleuls",
            "Ville : La Roche-sur-Yon",
            "Code Postal : 85000",
            "Tél :",
            "Mail :",
        ],
    },
    6: {
        "mod": [
            ("Catégorie CRM du besoin :", True),
            ("Panneaux photovoltaïques / EDF Solutions", False),
            ("solaires", False),
            ("Type de projet et statut :", True),
            ("Autoconsommation, professionnel (B2B)", False),
            ("Surface de toiture disponible :", True),
            ("1 000 à 5 000 m²", False),
            ("Propriétaire du bâtiment :", True),
            ("Oui", False),
            ("Disponibilité pour un appel :", True),
            ("Demain à 11:00", False),
        ],
        "fiche": [
            "Entreprise : BRASSERIE DES ALPES",
            "Siret : 90135792400035",
            "Activité : (Fabrication de bière et",
            "boissons artisanales)",
            "Contact :",
            "Adresse : 18 rue des Sources",
            "Ville : Annecy",
            "Code Postal : 74000",
            "Tél :",
            "Mail :",
        ],
    },
    7: {
        "mod": [
            ("Êtes-vous déjà équipé en solaire ?", True),
            ("Non", False),
            ("Type de bâtiment à équiper :", True),
            ("Siège social et entrepôt", False),
            ("Consommation annuelle d’électricité :", True),
            ("120 000 à 200 000 kWh", False),
            ("Budget envisagé pour l’installation :", True),
            ("100 000 € à 180 000 €", False),
            ("Souhaitez-vous l’autoconsommation", True),
            ("avec revente du surplus ?", True),
            ("Oui", False),
            ("Échéance du projet :", True),
            ("Dans 3 à 6 mois", False),
        ],
        "fiche": [
            "Entreprise : VERGERS DE PROVENCE",
            "Siret : 90579135700043",
            "Activité : (Culture et conditionnement",
            "de fruits, stockage et",
            "expédition)",
            "Contact :",
            "Adresse : 310 chemin des Vergers",
            "Ville : Aix-en-Provence",
            "Code Postal : 13100",
            "Tél :",
            "Mail :",
        ],
    },
}

# ------------------------------------------------------------ maquettes (page 5)

P5_POSTE = {
    "nom": "Solaris Énergie",
    "initiales": "SE",
    "ligne1": "SOLAIRE 2026 — La sérénité de votre toit, sans compromis.",
    "ligne2": "Installation photovoltaïque adaptée à votre logement.",
}

P5_FORMULAIRE = {
    "marque": "Solaris Énergie",
    "titre": "DEVIS PANNEAUX SOLAIRES",
    "sous_titre": "Plusieurs devis gratuits pour votre installation",
    "champs": [
        "Quel type de projet solaire ?",
        "Quel est votre type de bien ?",
        "Quand souhaitez-vous installer ?",
    ],
}

# ------------------------------------------------------------ maquette (page 6)

P6_CRM = {
    "campagne": "Panneaux solaires",
    "titre_modale": "DEMANDE DE DEVIS : Panneaux photovoltaïques",
    "q1": "Avez-vous un projet de panneaux solaires dans les mois à venir ?",
    "q2": "Quel type de projet recherchez-vous ?",
    "o2": ["Panneaux photovoltaïques", "Solutions solaires EDF"],
    "q3": "Vous envisagez cette installation à titre :",
    "o3": ["personnel", "professionnel"],
    "q4": "Type de projet [Obligatoire]",
    "o4": ["Panneaux photovoltaïques", "Ombrières et parkings",
           "Autoconsommation avec revente", "Chauffe-eau solaire",
           "Bornes de recharge", "Autre"],
    "q5": "Surface de toiture disponible [Obligatoire]",
    "o5": ["100 m² à 500 m²", "1 000 m² et plus", "Moins de 100 m²"],
    "q6": "Êtes-vous propriétaire du bâtiment ?",
    "q7": "Échéance du projet [Obligatoire]",
    "o7": ["Sous 3 mois", "3 à 6 mois", "Plus de 6 mois"],
    "matching_titre": "Résultat du matching :",
    "matching_valeur": "PANNEAUX PHOTOVOLTAÏQUES (B2B)",
    "soe": "BRASSERIE DES ALPES",
    "siret": "90135792400035",
    "acheteur": "Madame CLAIRE MOREL",
    "mail": "c.morel@brasserie-alpes.example",
    "naf": "NAF 1105Z : Fabrication de bière",
    "naf2": "Site de production et entrepôt",
    "creation": "Date de création : Juin 2016",
    "historique": [
        "> 12/03/2026 11:00 - hellodevis_28",
        "projet photovoltaïque, 1 800 m²",
        "devis demandé : 3 installateurs",
        "",
        "relance prévue le 19/03",
    ],
}

# ------------------------------------------------------------ maquettes (page 7)

# Email 1 : colonne de gauche (image p7_img194).
P7_EMAIL_1 = {
    "titre": ["Panneaux solaires et", "autoconsommation :", "quel projet choisir ?"],
    "bouton": "COMPARER LES SOLUTIONS",
    "bloc_titre": "À chaque toiture sa solution",
    "lignes": [
        ("Panneaux photovoltaïques",
         "Production d’électricité revendue ou autoconsommée."),
        ("Autoconsommation avec revente",
         "Le surplus injecté sur le réseau, valorisé chaque année."),
        ("Ombrières et parkings",
         "Production solaire sur ombrière, sans consommer de terrain."),
    ],
    "bandeau": ["Votre projet solaire chiffré en 1 minute,",
                "par des installateurs agréés RGE !"],
    "bandeau_texte": "Trouvez l’installateur solaire qui correspond à votre projet",
    "boutons": ["Je m’inscris", "Être rappelé par un installateur"],
}

# Email 2 : colonne du milieu (image p7_img191).
P7_EMAIL_2 = {
    "titre": ["Valorisez votre toiture", "avec une installation solaire"],
    "bouton": "Je compare",
    "bloc_titre": "BON À SAVOIR",
    "paras": [
        "Une installation photovoltaïque se dimensionne selon votre consommation, "
        "l’orientation et l’inclinaison de la toiture.",
        "Un installateur qualifié RGE réalise l’étude, le raccordement et les "
        "démarches administratives.",
        "Comparez plusieurs devis : matériel, puissance et durée de garantie "
        "varient fortement d’un installateur à l’autre.",
    ],
}
