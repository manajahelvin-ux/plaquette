# -*- coding: utf-8 -*-
"""Contenus « Fournisseurs d'énergies » — pages 4 à 7 (fictifs).

Aucun nom, logo, tarif ni offre réel. Structure des blocs = structure d'origine
(nombre de lignes et positions de chaque page).
"""

# ---------------------------------------------------------------- page 4 (SEA)
P4_MOD = [  # (baseline, style, texte) — police DejaVu d'origine
    (465.3, "B", "Énergie recherchée :"),
    (484.3, "R", "Électricité et gaz"),
    (522.3, "B", "Nombre de sites :"),
    (541.3, "R", "1 site"),
    (561.3, "B", "Échéance du projet :"),
    (580.3, "R", "Sous 3 mois"),
]
P4_FICHE = [
    (604.3, "Entreprise : BOULANGERIE DES CHARMES"),
    (621.3, "Siret : 84123906500018"),
    (638.3, "Activité : (Boulangerie et pâtisserie"),
    (653.3, "artisanale, fabrication de pain et de"),
    (668.3, "viennoiseries)"),
    (687.3, "Contact :"),
    (704.3, "Adresse : 12 place du Marché"),
    (721.3, "Ville : Tours"),
    (738.3, "Code postal : 37 000"),
    (755.3, "Tél :"),
    (772.3, "Mail :"),
]
P4_LP_STRIP = "Électricité · Gaz · Sites professionnels"
P4_LP_TITRE = "Électricité et gaz"
P4_LP_SOUS = ["Des offres adaptées", "à votre site professionnel"]
P4_CARTE_TITRE = ["Comparez les offres", "pour votre site professionnel"]
P4_CARTE_QUESTION = "Quelles énergies recherchez-vous ?"
P4_CARTE_OPTIONS = [("Électricité", True), ("Gaz", True),
                    ("Maintenance des installations", False),
                    ("Efficacité énergétique", False)]
P4_FORM_BARRE = ("Extrait du formulaire", "Étape 2 · Préciser la consommation annuelle")
P4_FORM_QUESTION = "Quelle est la consommation annuelle de votre site ?"
P4_FORM_OPTIONS = [("Moins de 5 000 kWh", False), ("5 000 à 20 000 kWh", True),
                   ("20 000 à 50 000 kWh", False), ("Plus de 50 000 kWh", False)]

# ------------------------------------------------------------ page 5 (Meta Ads)
P5_MOD = [
    ("Énergie recherchée :", "Électricité et gaz"),
    ("Type de site :", "Atelier artisanal"),
    ("Contrat actuel :", "Oui, à renouveler"),
    ("Date d'échéance du contrat :", "31/12/2026"),
    ("Consommation annuelle :", "5 000 à 20 000 kWh"),
    ("Puissance souscrite :", "9 à 18 kVA"),
    ("Nombre de sites :", "1 site"),
    ("Échéance du projet :", "Sous 1 mois"),
    ("Disponibilité pour un appel :", "le matin"),
    ("Heure de préférence (HH:MM) :", "10:00"),
]
P5_FICHE = [
    "Entreprise : MENUISERIE DES TILLEULS",
    "Siret : 83012945700026",
    "Activité : (Fabrication de menuiseries",
    "en bois pour le bâtiment)",
    "Contact : M. Girard",
    "Adresse : 27 avenue du Général Leclerc",
    "Ville : Toulouse",
    "Code Postal : 31000",
    "Tél : ",
    "Mail : ",
]
P5_META_BRAND = "ÉnergiePro Entreprises"
P5_META_TEXTE = ("Sites professionnels, consommation, contrat : votre énergie est-elle "
                 "bien négociée ? Comparez plusieurs devis adaptés à votre activité.")
P5_META_FOOT = "Devis énergie pro. Simple. Rapide."
P5_FORM_TITRE = ["ÉnergiePro Entreprises", "DEVIS ÉNERGIE", "PROFESSIONNELLE"]
P5_FORM_TEXTE = "Recevez plusieurs devis adaptés à votre site professionnel"
P5_FORM_CARTES = [
    ("Quelle énergie recherchez-vous ?", "Électricité et gaz"),
    ("Quel est votre type de site ?", "Commerce, artisanat ou restaurant"),
    ("Quand souhaitez-vous souscrire ?", "Sous 1 mois"),
]

# ------------------------------------------------------------ page 6 (Call)
P6_MOD = [
    ("Énergie recherchée :", "Électricité et gaz"),
    ("Type de site :", "Atelier"),
    ("Contrat actuel :", "Oui, à renégocier"),
    ("Date d'échéance du contrat :", "01/01/2027"),
    ("Consommation annuelle :", "20 000 à 50 000 kWh"),
    ("Puissance souscrite :", "18 à 36 kVA"),
    ("Nombre de sites :", "2 sites"),
    ("Échéance du projet :", "Sous 3 mois"),
    ("Disponibilité pour un appel :", "l'après-midi"),
    ("Heure de préférence (HH:MM) :", "15:30"),
]  # 11 lignes : 1 champ sur 2 lignes
P6_FICHE = [
    "Entreprise : ÉLEC SERVICES 84",
    "Siret : 90886739300013",
    "Activité : (Travaux d'installation électrique",
    "dans les bâtiments)",
    "Contact : Mme Lecuru",
    "Adresse : 14 rue des Artisans",
    "Ville : Lille",
    "Code Postal : 59000",
    "Tél : ",
    "Mail : ",
]
P6_CRM = {
    "campagne": "Campagne : Énergie - Électricité et gaz pro",
    "titre": "DEMANDE DE DEVIS : Fourniture énergie professionnelle",
    "matching": "Fournisseur partenaire (démo) – Électricité et gaz",
}

# ------------------------------------------------------------ page 7 (Emailing)
P7_MOD = [
    ("Objectif(s) du projet :", "Comparer les offres du marché"),
    ("Consommation annuelle :", "20 000 à 50 000 kWh"),
    ("Puissance souscrite :", "18 à 36 kVA"),
    ("Statut professionnel :", "Gérant de commerce"),
    ("Contrat actuel :", "Oui, à renouveler"),
    ("Échéance du projet :", "Sous 3 mois"),
    ("Disponibilité de l'acheteur pour un appel :", "le soir"),
    ("Heure de préférence (HH:MM) :", "18:30"),
]  # 13 lignes
P7_FICHE = [
    "Entreprise : PÂTISSERIE LE FOURNIL",
    "Siret : 39284567100045",
    "Activité : (Fabrication de pain et de",
    "pâtisserie fraîche,",
    "vente en magasin)",
    "Contact : Mme Dubois",
    "Adresse : 18 rue du Port",
    "Ville : Bordeaux",
    "Code Postal : 33000",
    "Tél : ",
    "Mail : ",
]  # 11 lignes (ligne vide de respiration retirée si besoin)
P7_EMAIL = {
    "sujet": "Électricité et gaz : quelle offre choisir pour votre site ?",
    "bandeau": "Gagnez du temps dans vos recherches : trouvez le fournisseur adapté à votre site.",
    "bandeau_sous": "Trouvez le conseiller qui correspond à votre situation.",
    "bouton_1": "J'en profite ✓",
    "bouton_2": "Faire le point sur mon énergie",
    "cta": "COMPARER LES OFFRES",
    "lignes": [
        "Renouvellement : anticipez l'échéance de votre contrat.",
        "Renégociation : comparez les offres du marché.",
        "Puissance : adaptez votre contrat à votre site.",
        "Consommation : suivez et maîtrisez votre facture.",
    ],
    "legal": [
        "Vous recevez ce message car votre adresse e-mail professionnelle figure dans nos fichiers.",
        "Pour ne plus recevoir nos messages, cliquez ici.",
    ],
}
