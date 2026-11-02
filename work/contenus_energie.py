# -*- coding: utf-8 -*-
"""Contenus « Fournisseurs d'énergies » (fictifs) — page 3 (SMS – RCS).

Source unique pour le PDF et le PPTX. Aucun nom, logo, tarif ni offre réel.
"""

# Cartes RCS (annonce SMS)
CARTE_1 = {
    "kicker": ["ÉNERGIE PROFESSIONNELLE", "ÉLECTRICITÉ & GAZ", "COMPAREZ LES OFFRES"],
    "accroche": "Contrat énergie à renouveler ?",
    "titre": "Contrat énergie à renouveler ?",
    "texte": ("Électricité ou gaz pour votre site professionnel : recevez des offres "
              "adaptées à votre activité."),
    "cta": "Ça m'intéresse !",
    "cta_couleur": (10, 91, 255),
    "cta_icone": "chevron",
}

CARTE_2 = {
    "kicker": [],
    "titre": "Facture trop élevée ? Faites le point",
    "texte": ("Maîtrisez votre facture : recevez des offres de fournisseurs d'énergie "
              "adaptées à votre consommation."),
    "cta": "Obtenir une offre !",
    "cta_couleur": (17, 17, 17),
    "cta_icone": "cercle",
}

# Page de destination (formulaire)
LANDING = {
    "titre_1": "Trouvez le meilleur partenaire",
    "titre_2": "pour votre énergie professionnelle !",
    "sous_titre": ("Comparez des offres d'électricité ou de gaz adaptées à votre "
                   "site professionnel."),
    "q1": "Énergie recherchée :",
    "q1_options": ["Électricité", "Gaz", "Les deux"],
    "q2": "Type de site :",
    "q2_options": ["Bureau", "Commerce", "Atelier ou entrepôt"],
}

# Bloc « Modération & Enrichissement » : (question, réponse), 16 lignes max
MODERATION = [
    ("Énergie recherchée :", "Électricité et gaz"),
    ("Type de site :", "Commerce de proximité"),
    ("Contrat actuel :", "Oui, à renouveler"),
    ("Date d'échéance du contrat :", "15/03/2027"),
    ("Consommation annuelle :", "5 000 à 20 000 kWh"),
    ("Puissance souscrite :", "9 à 18 kVA"),
    ("Nombre de sites :", "1 site"),
    ("Échéance du projet :", "Sous 3 mois"),
    ("Disponibilité pour un appel :", "le matin"),
    ("Heure de préférence (HH:MM) :", "10:00"),
]

# Fiche acheteur (fictive) : 10 lignes max. Tél. et Mail restent masqués.
FICHE = [
    "Entreprise : BOULANGERIE DES CHARMES",
    "Siret : 84123906500018",
    "Activité : (Fabrication de pain et de pâtisserie)",
    "Contact : M. Lefèvre",
    "Adresse : 12 place du Marché",
    "Ville : Tours",
    "Code Postal : 37000",
    "Tél : ",
    "Mail : ",
]
