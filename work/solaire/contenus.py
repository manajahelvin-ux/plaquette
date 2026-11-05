# -*- coding: utf-8 -*-
"""Contenus de la plaquette « Panneaux solaires ».

Tous les textes de secteur (pages 3, 5, 6, 7) sont regroupés ici :
cartes RCS, maquettes (page de destination, formulaire META, CRM, emails),
blocs « Modération & Enrichissement » et fiches acheteur.

Règle de mise en page : chaque bloc reprend exactement le nombre de lignes de
l'original et se cale sur les mêmes lignes de base (voir panneaux_origine.json).
Aucune donnée réelle : installateurs, SIRET, adresses et contacts sont fictifs.
"""

# --------------------------------------------------------------- page 3 (SMS - RCS)

CARTE_1 = {
    "kicker": ["PHOTOVOLTAÏQUE", "PARTICULIERS & PROFESSIONNELS"],
    "bandeau": "DEVIS GRATUIT • INSTALLATEURS RGE",
    "titre": "Panneaux solaires : divisez votre facture",
    "texte": (
        "Estimez vos économies et comparez les installateurs agréés "
        "de votre région."
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
              "adaptées à votre logement."],
    "question": ["Concernant votre projet,", "vous êtes :"],
    "choix": ["Particulier", "Professionnel"],
}

# ------------------------------------------------------- colonnes de droite

# (texte, gras) — gras = étiquette bleue, sinon valeur noire.
PANNEAUX = {
    3: {
        "mod": [
            ("Type de projet solaire :", True),
            ("Photovoltaïque en autoconsommation", False),
            ("avec revente du surplus", False),
            ("Statut de l’acheteur :", True),
            ("Particulier propriétaire", False),
            ("Type de bien :", True),
            ("Maison individuelle, toiture en tuiles", False),
            ("Surface de toiture disponible :", True),
            ("30 à 50 m²", False),
            ("Consommation annuelle d’électricité :", True),
            ("3 500 à 5 000 kWh", False),
            ("Budget envisagé :", True),
            ("10 000 € à 14 999 €", False),
            ("Sous quel délai souhaitez-vous être", True),
            ("équipé ?", True),
            ("Sous 3 mois", False),
        ],
        "fiche": [
            "Entreprise : SOLARIS ÉNERGIE",
            "Siret : 81234567800027",
            "Activité : (Installation de panneaux",
            "photovoltaïques)",
            "Contact :",
            "Adresse : 12 rue des Ateliers",
            "Ville : Nantes",
            "Code Postal : 44000",
            "Tél :",
            "Mail :",
        ],
    },
    5: {
        "mod": [
            ("Quel type de projet solaire ?", True),
            ("Photovoltaïque en autoconsommation", False),
            ("Vous envisagez cette installation :", True),
            ("professionnel", False),
            ("Secteur d’activité de l’entreprise :", True),
            ("Industrie et logistique", False),
            ("Surface de toiture disponible :", True),
            ("500 m² à 1 000 m²", False),
            ("Sous quel délai souhaitez-vous être", True),
            ("équipé ?", True),
            ("Immédiat", False),
            ("Puissance de l’installation :", True),
            ("36 à 100 kWc", False),
        ],
        "fiche": [
            "Entreprise : AXSOL ENR",
            "Siret : 81234567800035",
            "Activité : (Installation de panneaux",
            "photovoltaïques)",
            "Contact :",
            "Adresse : 27 avenue de la Gare",
            "Ville : Montpellier",
            "Code Postal : 34000",
            "Tél :",
            "Mail :",
        ],
    },
    6: {
        "mod": [
            ("Catégorie CRM du besoin :", True),
            ("Panneaux photovoltaïques / EDF Solutions", False),
            ("solaires", False),
            ("Volume de leads recherché :", True),
            ("50 à 99 par mois", False),
            ("Zone géographique des interventions :", True),
            ("Auvergne-Rhône-Alpes", False),
            ("Disponibilité de l’acheteur pour un appel :", True),
            ("le matin", False),
            ("Avez-vous une heure de préférence :", True),
            ("11:00", False),
        ],
        "fiche": [
            "Entreprise : HELIOS INSTALLATION",
            "Siret : 81234567800043",
            "Activité : (Travaux d’installation",
            "électrique)",
            "Contact :",
            "Adresse : 584 chemin des Vignes",
            "Ville : Toulon",
            "Code Postal : 83200",
            "Tél :",
            "Mail :",
        ],
    },
    7: {
        "mod": [
            ("Êtes-vous déjà équipé en solaire ?", True),
            ("Non", False),
            ("Type de bien à équiper :", True),
            ("Maison individuelle", False),
            ("Consommation annuelle d’électricité :", True),
            ("3 500 à 5 000 kWh", False),
            ("Budget envisagé pour l’installation :", True),
            ("10 000 € à 14 999 €", False),
            ("Souhaitez-vous l’autoconsommation", True),
            ("avec revente du surplus ?", True),
            ("Oui", False),
            ("Échéance du projet :", True),
            ("Sous 3 mois", False),
        ],
        "fiche": [
            "Entreprise : SUNWATT FRANCE",
            "Siret : 81234567800051",
            "Activité : (Installation de panneaux",
            "photovoltaïques, autoconsommation,",
            "bornes de recharge)",
            "Contact :",
            "Adresse : 114 rue de Flandre",
            "Ville : Paris",
            "Code Postal : 75019",
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
    "soe": "SOLARIS ÉNERGIE",
    "acheteur": "Monsieur VASSEUR",
    "mail": "m.vasseur@solaris-energie.fr",
    "tel": "750771600010",
    "naf": "NAF 4321A : Installation électrique",
    "naf2": "et travaux d’installation photovoltaïque",
    "creation": "Date de création : Avril 2012",
    "historique": [
        "> 11/03/2026 15:12 - hellodevis_28",
        "projet photovoltaïque, 62 m²",
        "devis demandé : 3 installateurs",
        "",
        "relance prévue le 18/03",
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
    "bandeau": ["Gagnez du temps dans vos recherches,",
                "on vous répond en moins d’une minute !"],
    "bandeau_texte": "Trouvez l’installateur solaire de votre région et comparez.",
    "boutons": ["Je m’inscris", "Être rappelé"],
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
