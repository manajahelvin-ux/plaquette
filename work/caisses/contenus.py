# -*- coding: utf-8 -*-
"""Contenus de la plaquette « Caisses enregistreuses tactiles ».

Tous les textes de secteur (pages 3 à 7) sont regroupés ici :
cartes RCS, maquettes (page de destination, formulaire META, CRM, emails),
blocs « Modération & Enrichissement » et fiches acheteur.

Règle de mise en page : chaque bloc reprend exactement le nombre de lignes de
l'original et se cale sur les mêmes lignes de base (voir la version solaire).

Public de la plaquette : les éditeurs et distributeurs de caisses tactiles
(CHR, boulangeries, restauration rapide, commerces alimentaires). Les fiches
acheteur décrivent donc des ACHETEURS finaux — un restaurant, une
boulangerie-pâtisserie, un commerce alimentaire — et jamais un éditeur de
caisse : aucun nom d'annonceur réel n'apparaît dans les fiches. Toutes les
données sont fictives ; téléphone et e-mail restent masqués dans la maquette.
"""

# --------------------------------------------------------------- page 3 (SMS - RCS)

CARTE_1 = {
    "kicker": ["CAISSES TACTILES", "RESTAURANTS, BARS & COMMERCES"],
    "bandeau": "DEVIS GRATUIT • SPÉCIALISTES CHR",
    "titre": "Caisses tactiles : encaissez plus vite",
    "texte": (
        "Comparez les caisses tactiles et les logiciels de gestion adaptés "
        "à votre établissement."
    ),
    "cta": "Ça m'intéresse !",
    "cta_couleur": (10, 91, 255),
    "cta_icone": "chevron",
}

CARTE_2 = {
    "kicker": [],
    "titre": "Boulangerie : fluidifiez votre caisse",
    "texte": (
        "Caisse tactile, imprimante à tickets et gestion des invendus : "
        "recevez des offres de votre région."
    ),
    "cta": "Obtenir une offre !",
    "cta_couleur": (17, 17, 17),
    "cta_icone": "cercle",
}

# Page de destination « hellodevis » (image de la page 3) : textes réécrits à
# l'identique en nombre de lignes.
P3_LANDING = {
    "titre": ["Trouvez le meilleur", "Partenaire", "pour votre caisse", "tactile !"],
    "intro": ["Comparez les caisses tactiles et les",
              "logiciels de gestion adaptés à votre",
              "point de vente."],
    "question": ["Concernant votre établissement,", "vous êtes :"],
    "choix": ["Commerce indépendant", "Chaîne ou franchise"],
}

# ------------------------------------------------------- colonnes de droite

# (texte, gras) — gras = étiquette bleue, sinon valeur noire.
# « mod » = qualification du besoin d'achat ; « fiche » = coordonnées de
# l'acheteur final (restaurant, boulangerie, commerce), pas de l'éditeur.
CAISSES = {
    3: {
        "mod": [
            ("Type d’équipement recherché :", True),
            ("Caisse tactile avec logiciel de", False),
            ("gestion intégré", False),
            ("Statut de l’acheteur :", True),
            ("Professionnel (CHR), exploitant", False),
            ("Type d’établissement :", True),
            ("Restaurant traditionnel, 80 couverts", False),
            ("Nombre de points de vente :", True),
            ("2 établissements à Lyon", False),
            ("Tickets encaissés par jour :", True),
            ("150 à 250 tickets", False),
            ("Budget envisagé :", True),
            ("2 000 € à 4 000 €", False),
            ("Sous quel délai souhaitez-vous être", True),
            ("équipé ?", True),
            ("Sous 1 mois", False),
        ],
        "fiche": [
            "Entreprise : LE BISTROT DES HALLES",
            "Siret : 91357924600026",
            "Activité : (Restauration traditionnelle,",
            "2 établissements en centre-ville)",
            "Contact :",
            "Adresse : 14 rue des Halles",
            "Ville : Lyon",
            "Code Postal : 69002",
            "Tél :",
            "Mail :",
        ],
    },
    4: {
        "mod": [
            ("Type d’équipement recherché :", True),
            ("Caisse tactile avec logiciel de gestion", False),
            ("et terminal de paiement", False),
            ("Type d’établissement :", True),
            ("Café-brasserie, 60 couverts", False),
            ("Échéance du projet :", True),
            ("Sous 1 mois", False),
        ],
        "fiche": [
            "Entreprise : CAFÉ DES ARCADES",
            "Siret : 90246813500019",
            "Activité : (Débit de boissons et",
            "restauration rapide sur place,",
            "terrasse 40 places)",
            "Contact : ",
            "Adresse : 3 place des Arcades",
            "Ville : Rennes",
            "Code postal : 35000",
            "Tél : ",
            "Mail : ",
        ],
    },
    5: {
        "mod": [
            ("Quel type d’équipement recherché ?", True),
            ("Caisse tactile et logiciel de gestion", False),
            ("Votre établissement :", True),
            ("Restaurant traditionnel (CHR)", False),
            ("Nombre de couverts en salle :", True),
            ("60 à 100 couverts", False),
            ("Nombre de points de vente :", True),
            ("2 établissements", False),
            ("Sous quel délai souhaitez-vous être", True),
            ("équipé ?", True),
            ("Sous 1 mois", False),
            ("Fonctions attendues :", True),
            ("Encaissement, commandes, stocks", False),
        ],
        "fiche": [
            "Entreprise : LA TABLE DES QUAIS",
            "Siret : 90482135700018",
            "Activité : (Restauration traditionnelle",
            "et traiteur, 2 points de vente)",
            "Contact :",
            "Adresse : 6 quai des Chartrons",
            "Ville : Bordeaux",
            "Code Postal : 33000",
            "Tél :",
            "Mail :",
        ],
    },
    6: {
        "mod": [
            ("Catégorie CRM du besoin :", True),
            ("Caisses enregistreuses tactiles,", False),
            ("restauration (CHR)", False),
            ("Type d’équipement et statut :", True),
            ("Caisse tactile, professionnel (CHR)", False),
            ("Nombre de points de vente :", True),
            ("3 établissements", False),
            ("Propriétaire du matériel :", True),
            ("Oui", False),
            ("Disponibilité pour un appel :", True),
            ("Demain à 11:00", False),
        ],
        "fiche": [
            "Entreprise : LE COMPTOIR DU MARCHÉ",
            "Siret : 90135792400026",
            "Activité : (Restauration rapide,",
            "3 points de vente en centre-ville)",
            "Contact :",
            "Adresse : 27 place du Marché",
            "Ville : Annecy",
            "Code Postal : 74000",
            "Tél :",
            "Mail :",
        ],
    },
    7: {
        "mod": [
            ("Êtes-vous déjà équipé d’une caisse tactile ?", True),
            ("Non, caisse traditionnelle", False),
            ("Type d’établissement à équiper :", True),
            ("Boulangerie-pâtisserie et salon de thé", False),
            ("Tickets encaissés par jour :", True),
            ("300 à 500 tickets", False),
            ("Budget envisagé pour l’équipement :", True),
            ("3 000 € à 6 000 €", False),
            ("Souhaitez-vous un logiciel de gestion", True),
            ("intégré (stocks, production) ?", True),
            ("Oui", False),
            ("Échéance du projet :", True),
            ("Sous 1 mois", False),
        ],
        "fiche": [
            "Entreprise : MAISON LORETTE",
            "Siret : 90579135700034",
            "Activité : (Boulangerie-pâtisserie et",
            "salon de thé, 4 boutiques en",
            "centre-ville)",
            "Contact :",
            "Adresse : 42 rue de la République",
            "Ville : Aix-en-Provence",
            "Code Postal : 13100",
            "Tél :",
            "Mail :",
        ],
    },
}

# ------------------------------------------------------------ maquettes (page 5)

P5_POSTE = {
    "nom": "Caisseo",
    "initiales": "CA",
    "ligne1": "CAISSES TACTILES 2026 — Le service, sans temps mort.",
    "ligne2": "La caisse tactile pensée pour les métiers de la restauration.",
}

P5_FORMULAIRE = {
    "marque": "Caisseo",
    "titre": "DEVIS CAISSE TACTILE",
    "sous_titre": "Plusieurs offres pour votre point de vente",
    "champs": [
        "Quel est votre métier ?",
        "Combien de points de vente ?",
        "Quand souhaitez-vous vous équiper ?",
    ],
}

# ------------------------------------------------------------ maquette (page 6)

P6_CRM = {
    "campagne": "Caisses tactiles",
    "titre_modale": "DEMANDE DE DEVIS : Caisse tactile",
    "q1": "Avez-vous un projet de caisse tactile dans les mois à venir ?",
    "q2": "Quel type d’équipement recherchez-vous ?",
    "o2": ["Caisse enregistreuse tactile", "Logiciel de gestion"],
    "q3": "Vous équipez votre établissement à titre :",
    "o3": ["personnel", "professionnel"],
    "q4": "Type d’équipement [Obligatoire]",
    "o4": ["Caisse tactile", "Logiciel de caisse", "Terminal de paiement",
           "Imprimante à tickets", "Borne de commande", "Autre"],
    "q5": "Nombre de points de vente [Obligatoire]",
    "o5": ["1 établissement", "2 à 5 établissements", "Plus de 5"],
    "q6": "Êtes-vous propriétaire du matériel ?",
    "q7": "Échéance du projet [Obligatoire]",
    "o7": ["Sous 1 mois", "1 à 3 mois", "Plus de 3 mois"],
    "matching_titre": "Résultat du matching :",
    "matching_valeur": "CAISSE TACTILE (CHR)",
    "soe": "LE COMPTOIR DU MARCHÉ",
    "siret": "90135792400026",
    "acheteur": "Monsieur THOMAS REY",
    "mail": "t.rey@comptoir-marche.example",
    "naf": "NAF 5610C : Restauration de type rapide",
    "naf2": "3 points de vente en centre-ville",
    "creation": "Date de création : Juin 2016",
    "historique": [
        "> 12/03/2026 11:00 - hellodevis_28",
        "projet caisse tactile, 3 établissements",
        "devis demandé : 3 fournisseurs",
        "",
        "relance prévue le 19/03",
    ],
}

# ------------------------------------------------------------ maquettes (page 7)

# Email 1 : colonne de gauche (image p7_img194).
P7_EMAIL_1 = {
    "titre": ["Caisses enregistreuses", "tactiles :", "quelle solution choisir ?"],
    "bouton": "COMPARER LES SOLUTIONS",
    "bloc_titre": "À chaque métier sa solution",
    "lignes": [
        ("La caisse tactile",
         "Un écran simple et des encaissements rapides, table par table."),
        ("Le logiciel de gestion",
         "Stocks, fiches techniques et statistiques consultables en direct."),
        ("Les bornes de commande",
         "Le client commande seul, la file d’attente au comptoir diminue."),
    ],
    "bandeau": ["Votre caisse tactile chiffrée en 1 minute,",
                "par des spécialistes du CHR !"],
    "bandeau_texte": "Trouvez la solution de caisse adaptée à votre établissement",
    "boutons": ["Je m’inscris", "Être rappelé par un conseiller"],
}

# Email 2 : colonne du milieu (image p7_img191).
P7_EMAIL_2 = {
    "titre": ["Équipez votre comptoir", "d’une caisse tactile"],
    "bouton": "Je compare",
    "bloc_titre": "BON À SAVOIR",
    "paras": [
        "Une caisse tactile réunit encaissement, prise de commande et suivi "
        "des stocks sur un seul écran.",
        "Le logiciel se choisit selon votre métier : restauration, boulangerie "
        "ou commerce alimentaire.",
        "Comparez plusieurs offres : matériel, abonnement logiciel et durée de "
        "garantie varient fortement.",
    ],
}
