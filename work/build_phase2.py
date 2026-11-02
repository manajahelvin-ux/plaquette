# -*- coding: utf-8 -*-
"""Phase 2 — plaquette complète « Fournisseurs d'énergies » (9 pages).

Base : la page 3 déjà validée (phase 1) dans « Plaquette HelloLead - Energie - Page 3 (validation).pdf ».
Pages 1, 2, 8, 9 : inchangées. Pages 4 à 7 : visuel, formulaire, bloc Modération & Enrichissement
et fiche acheteur remplacés ; titres, puces, pictos, marques, légendes et pieds de page conservés.

Sortie : « Plaquette HelloLead - Energie - Finale (9 pages).pdf »
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont
import pymupdf

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import contenus_phase2 as C  # noqa: E402

RACINE = os.path.join(ICI, "..")
ASSETS = os.path.join(ICI, "assets")
BASE = os.path.join(RACINE, "Plaquette HelloLead - Energie - Page 3 (validation).pdf")
V3 = os.path.join(RACINE, "Plaquette HelloLead - Assurance V3.pdf")
SORTIE = os.path.join(RACINE, "Plaquette HelloLead - Energie - Finale (9 pages).pdf")

K = 3  # pixels par point pour les visuels
PANEL = (244, 245, 251)
PANEL_CLAIR = (234, 241, 247)
BLEU = (10, 91, 255)
NOIR = (0, 0, 0)
GRIS_T = (110, 110, 115)
JAUNE = (255, 205, 40)
FOND_SOMBRE = (30, 30, 32)


def S(v):
    return int(round(v * K))


# ------------------------------------------------------------------ polices
def _extraire_polices():
    os.makedirs(ASSETS, exist_ok=True)
    doc = pymupdf.open(V3)
    out = {}
    for xref, nom in ((132, "Poppins-Regular.ttf"), (141, "Poppins-Bold.ttf")):
        chemin = os.path.join(ASSETS, nom)
        if not os.path.exists(chemin):
            _, _, _, buf = doc.extract_font(xref)
            open(chemin, "wb").write(buf)
        out[nom] = chemin
    doc.close()
    return out


FONTS = _extraire_polices()
POP_R = FONTS["Poppins-Regular.ttf"]
POP_B = FONTS["Poppins-Bold.ttf"]
DJ_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DJ_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def fnt(chemin, pt):
    return ImageFont.truetype(chemin, S(pt))


def tx(d, xy_pt, texte, chemin, pt, couleur, anchor="la"):
    d.text((S(xy_pt[0]), S(xy_pt[1])), texte, font=fnt(chemin, pt), fill=couleur, anchor=anchor)


def lignes(texte, chemin, pt, largeur_pt):
    f = fnt(chemin, pt)
    mots, out, cur = texte.split(), [], ""
    for m in mots:
        essai = (cur + " " + m).strip()
        if f.getlength(essai) <= S(largeur_pt) or not cur:
            cur = essai
        else:
            out.append(cur)
            cur = m
    if cur:
        out.append(cur)
    return out


def bloc(d, xy_pt, texte, chemin, pt, couleur, largeur_pt, pas_pt=None, anchor="la"):
    pas = pas_pt or pt * 1.32
    y = xy_pt[1]
    for l in lignes(texte, chemin, pt, largeur_pt):
        tx(d, (xy_pt[0], y), l, chemin, pt, couleur, anchor)
        y += pas
    return y


def rect(d, x0, y0, x1, y1, fill=None, outline=None, r=0, larg=1):
    box = [S(x0), S(y0), S(x1), S(y1)]
    if r:
        d.rounded_rectangle(box, radius=S(r), fill=fill, outline=outline, width=S(larg) if outline else 0)
    else:
        d.rectangle(box, fill=fill, outline=outline, width=S(larg) if outline else 0)


def cover(chemin, w_pt, h_pt, cx=0.5, cy=0.5, assombrir=0.0):
    src = Image.open(chemin).convert("RGB")
    W, H = S(w_pt), S(h_pt)
    r = max(W / src.width, H / src.height)
    src = src.resize((round(src.width * r), round(src.height * r)), Image.LANCZOS)
    x = round((src.width - W) * cx)
    y = round((src.height - H) * cy)
    im = src.crop((x, y, x + W, y + H))
    if assombrir:
        im = Image.blend(im, Image.new("RGB", im.size, (0, 0, 0)), assombrir)
    return im


def coins_arrondis(im, rayon_pt, fond):
    masque = Image.new("L", im.size, 0)
    ImageDraw.Draw(masque).rounded_rectangle([0, 0, im.width - 1, im.height - 1],
                                             radius=S(rayon_pt), fill=255)
    out = Image.new("RGB", im.size, fond)
    out.paste(im, (0, 0), masque)
    return out


def case(d, x, y, coche, taille=7.0):
    rect(d, x, y, x + taille, y + taille, fill=(255, 255, 255), outline=(120, 120, 125), r=1.5, larg=0.8)
    if coche:
        d.line([(S(x + 1.6), S(y + 3.6)), (S(x + 3.0), S(y + 5.2)), (S(x + 5.6), S(y + 1.8))],
               fill=(10, 91, 255), width=S(0.9), joint="curve")


def radio(d, x, y, coche, taille=7.0):
    d.ellipse([S(x), S(y), S(x + taille), S(y + taille)], fill=(255, 255, 255), outline=(120, 120, 125), width=S(0.8))
    if coche:
        d.ellipse([S(x + 1.8), S(y + 1.8), S(x + taille - 1.8), S(y + taille - 1.8)], fill=(10, 91, 255))


# ----------------------------------------------------------------- visuels
def visuel_lp_p4():
    """Page de destination SEA (483,89)-(956,440) : photo, carte de formulaire, bande de ré-assurance."""
    w, h = 473, 351
    im = Image.new("RGB", (S(w), S(h)), (255, 255, 255))
    im.paste(cover(f"{ASSETS}/p4_restaurant.jpg", w, 314, 0.5, 0.35), (0, 0))
    # voile sombre à gauche pour le titre
    voile = Image.new("L", im.size, 0)
    dv = ImageDraw.Draw(voile)
    for x in range(S(w)):
        t = max(0.0, 1 - x / S(w * 0.75))
        dv.line([(x, 0), (x, S(314))], fill=int(170 * t))
    im.paste(Image.new("RGB", im.size, (0, 0, 0)), (0, 0), voile)
    d = ImageDraw.Draw(im)
    tx(d, (22, 178), C.P4_LP_TITRE, POP_B, 19, (255, 255, 255))
    tx(d, (22, 204), C.P4_LP_SOUS[0], POP_R, 9.5, (255, 255, 255))
    tx(d, (22, 218), C.P4_LP_SOUS[1], POP_R, 9.5, (255, 255, 255))
    # carte de formulaire
    rect(d, 219, 53, 458, 287, fill=(255, 255, 255), r=8)
    tx(d, (233, 68), C.P4_CARTE_TITRE[0], POP_B, 9.5, BLEU)
    tx(d, (233, 82), C.P4_CARTE_TITRE[1], POP_B, 8.5, (20, 20, 25))
    tx(d, (233, 102), C.P4_CARTE_QUESTION, POP_R, 7.5, (60, 60, 60))
    y = 118
    for texte, coche in C.P4_CARTE_OPTIONS:
        case(d, 233, y, coche)
        tx(d, (246, y - 0.5), texte, POP_R, 7.5, (30, 30, 30))
        y += 21
    rect(d, 370, 250, 440, 268, fill=(33, 150, 214), r=3)
    tx(d, (405, 259), "Suivant", POP_B, 7.5, (255, 255, 255), anchor="mm")
    # bande de ré-assurance (sans logo)
    rect(d, 0, 314, w, h, fill=(255, 255, 255))
    tx(d, (w / 2, 333), C.P4_LP_STRIP, POP_B, 9, (60, 60, 66), anchor="mm")
    return im


def visuel_formulaire_p4():
    """Extrait du formulaire (477,496)-(963,756)."""
    w, h = 486, 260
    im = Image.new("RGB", (S(w), S(h)), PANEL_CLAIR)
    d = ImageDraw.Draw(im)
    rect(d, 16, 10, 470, 62, fill=(22, 50, 82), r=5)
    tx(d, (30, 20), C.P4_FORM_BARRE[0], POP_B, 12, (255, 255, 255))
    tx(d, (30, 42), C.P4_FORM_BARRE[1], POP_R, 8, (220, 228, 238))
    rect(d, 28, 74, 458, 252, fill=(255, 255, 255), r=6)
    tx(d, (44, 90), C.P4_FORM_QUESTION, POP_B, 9, BLEU)
    y = 114
    for texte, coche in C.P4_FORM_OPTIONS:
        case(d, 46, y, coche)
        tx(d, (62, y - 0.5), texte, POP_R, 8, (40, 40, 40))
        y += 19
    rect(d, 362, 212, 444, 232, fill=(33, 150, 214), r=3)
    tx(d, (403, 222), "Suivant", POP_B, 7.5, (255, 255, 255), anchor="mm")
    return im


def visuel_annonce_meta_p5():
    """Annonce sponsorisée (407.7,209.4)-(722.7,638.4)."""
    w, h = 315, 429
    im = Image.new("RGB", (S(w), S(h)), (255, 255, 255))
    d = ImageDraw.Draw(im)
    d.ellipse([S(12), S(12), S(34), S(34)], fill=(20, 20, 30))
    tx(d, (40, 13), C.P5_META_BRAND, POP_B, 8.5, (20, 20, 25))
    tx(d, (40, 26), "Sponsorisé · ", POP_R, 6.5, GRIS_T)
    bloc(d, (14, 46), C.P5_META_TEXTE, POP_R, 8, (40, 40, 40), 290, pas_pt=11)
    im.paste(cover(f"{ASSETS}/p5_artisan.jpg", w, 232, 0.5, 0.4), (0, S(100)))
    rect(d, 0, 332, w, 380, fill=(242, 243, 245))
    tx(d, (14, 340), "FORMULAIRE", POP_R, 5.5, GRIS_T)
    tx(d, (14, 352), C.P5_META_FOOT, POP_B, 8, (20, 20, 25))
    rect(d, 236, 348, 304, 368, fill=(228, 230, 234), r=3)
    tx(d, (270, 358), "En savoir plus", POP_B, 6.5, (30, 30, 30), anchor="mm")
    tx(d, (14, 392), "👍 Jaime · 💬 Commenter", POP_R, 6.5, GRIS_T)
    return im


def visuel_formulaire_meta_p5():
    """Formulaire instantané (710.5,172.4)-(1058.5,638.2)."""
    w, h = 348, 466
    im = cover(f"{ASSETS}/p5_artisan.jpg", w, h, 0.5, 0.5, assombrir=0.62)
    d = ImageDraw.Draw(im)
    rect(d, 22, 37, 326, 196, fill=(255, 255, 255), r=10)
    d.ellipse([S(156), S(18), S(192), S(54)], fill=(255, 255, 255), outline=(200, 200, 205), width=S(0.6))
    tx(d, (174, 36), "É", POP_B, 12, BLEU, anchor="mm")
    tx(d, (174, 70), C.P5_FORM_TITRE[0], POP_R, 8.5, (90, 90, 95), anchor="mm")
    tx(d, (174, 88), C.P5_FORM_TITRE[1], POP_B, 12.5, (20, 20, 25), anchor="mm")
    tx(d, (174, 104), C.P5_FORM_TITRE[2], POP_B, 12.5, (20, 20, 25), anchor="mm")
    bloc(d, (56, 122), C.P5_FORM_TEXTE, POP_R, 7.5, (90, 90, 95), 236, pas_pt=10)
    alpha = [(0.44, 0.56), (0.59, 0.72), (0.75, 0.87)]
    for (q, a), (f0, f1) in zip(C.P5_FORM_CARTES, alpha):
        rect(d, 22, f0 * h, 326, f1 * h, fill=(255, 255, 255), r=8)
        tx(d, (38, f0 * h + 9), q, POP_B, 8.5, (20, 20, 25))
        tx(d, (38, f0 * h + 27), a, POP_R, 7.5, (90, 90, 95))
    return im


def visuel_crm_p6():
    """Capture du CRM (410.8,163.5)-(1046.1,517.9) — maquette de l'interface."""
    w, h = 635, 354
    im = Image.new("RGB", (S(w), S(h)), (236, 238, 242))
    d = ImageDraw.Draw(im)
    rect(d, 0, 0, w, 16, fill=(60, 62, 68))
    tx(d, (6, 4), "hello", POP_B, 8, (255, 255, 255))
    tx(d, (38, 4.5), "lead", POP_B, 8, (244, 114, 43))
    tx(d, (420, 5), C.P6_CRM["campagne"], POP_R, 6.5, (230, 230, 230))
    rect(d, 0, 16, w, 27, fill=(30, 90, 150))
    for i, t in enumerate(["Paramétrage", "Statistiques", "Fichiers Agents", "Marché Hellolead"]):
        tx(d, (60 + i * 98, 19), t, POP_R, 5.8, (255, 255, 255))
    # colonnes société / acheteur
    tx(d, (6, 33), "Société", POP_B, 6.5, (30, 30, 30))
    tx(d, (150, 33), "Acheteur", POP_B, 6.5, (30, 30, 30))
    campos = ["Société : BOULANGERIE DES CHARMES", "Siret : 84123906500018",
              "Activité : Boulangerie-pâtisserie", "Adresse : 12 place du Marché", "Ville : Tours"]
    for i, t in enumerate(campos):
        tx(d, (6, 44 + i * 13), t, POP_R, 5.6, (50, 50, 50))
    for i, t in enumerate(["Contact : M. Lefèvre", "Fonction : Gérant", "Tél : (masqué)", "Mail : (masqué)"]):
        tx(d, (150, 44 + i * 13), t, POP_R, 5.6, (50, 50, 50))
    rect(d, 0, 124, 300, 136, fill=(229, 110, 40))
    tx(d, (6, 126), "Commentaires datés", POP_B, 6, (255, 255, 255))
    for i, t in enumerate(["02/11/2026 09:12 – Premier appel, messagerie.",
                           "02/11/2026 14:30 – Rappel demandé, créneau à confirmer."]):
        tx(d, (6, 142 + i * 11), t, POP_R, 5.6, (70, 70, 70))
    # voile sombre de la modale
    voile = Image.new("RGBA", im.size, (0, 0, 0, 120))
    im = Image.alpha_composite(im.convert("RGBA"), voile).convert("RGB")
    d = ImageDraw.Draw(im)
    rect(d, 100, 60, 540, 300, fill=(255, 255, 255), r=6)
    tx(d, (116, 70), C.P6_CRM["titre"], POP_B, 8.5, (200, 40, 40))
    rect(d, 116, 80, 300, 102, fill=(255, 255, 255), outline=(230, 130, 40), r=3, larg=1.2)
    tx(d, (122, 83), "Résultat du matching : Fournisseur partenaire (démo)", POP_B, 5.2, (30, 30, 30))
    tx(d, (122, 92), "Électricité et gaz", POP_R, 5.2, (30, 30, 30))
    questions = [
        (112, "Projet de changement ou de renouvellement de contrat énergie ?",
         [("Oui", True), ("Non", False)], "h"),
        (148, "Quelle(s) énergie(s) recherchez-vous ?",
         [("Électricité", True), ("Gaz", True), ("Les deux", False)], "c"),
        (184, "Consommation annuelle du site",
         [("< 5 000 kWh", False), ("5 000 à 20 000 kWh", False), ("20 000 à 50 000 kWh", True)], "r"),
        (220, "Contrat actuel",
         [("Oui, à renouveler", False), ("Oui, à renégocier", True), ("Non", False)], "r"),
    ]
    for y, q, opts, kind in questions:
        tx(d, (116, y), q, POP_B, 6.5, (30, 30, 30))
        x = 116
        for texte, coche in opts:
            if kind == "c":
                case(d, x, y + 14, coche, 6)
            else:
                radio(d, x, y + 14, coche, 6)
            tx(d, (x + 9, y + 14), texte, POP_R, 6, (50, 50, 50))
            x += 9 + fnt(POP_R, 6).getlength(texte) / K + 16
    rect(d, 116, 254, 300, 270, fill=(30, 130, 60), r=3)
    tx(d, (208, 262), "Besoin réel mais projet immature", POP_B, 6.5, (255, 255, 255), anchor="mm")
    rect(d, 310, 254, 524, 270, fill=(230, 110, 40), r=3)
    tx(d, (417, 262), "Besoin réel, projet à court terme", POP_B, 6.5, (255, 255, 255), anchor="mm")
    return im


def _logo_comparateur(d, x, y, taille, fond_clair=True):
    tx(d, (x, y), "Comparateur", POP_B, taille, (30, 30, 30) if fond_clair else (255, 255, 255))
    xp = x + fnt(POP_B, taille).getlength("Comparateur") / K
    tx(d, (xp, y), "pro", POP_B, taille, JAUNE)


def visuel_email_p7():
    """E-mail principal (432.6,88)-(724.4,792.2) avec mini-visuels."""
    w, h = 292, 704
    im = Image.new("RGB", (S(w), S(h)), (255, 255, 255))
    d = ImageDraw.Draw(im)
    _logo_comparateur(d, 20, 14, 13)
    tx(d, (20, 34), "Électricité, gaz : comparez les offres pour votre site professionnel", POP_R, 5.8, GRIS_T)
    tx(d, (20, 52), "Électricité et gaz : quelle offre choisir ?", POP_B, 9, (20, 20, 25))
    im.paste(cover(f"{ASSETS}/p7_gerante.jpg", w, 170, 0.5, 0.25), (0, S(74)))
    rect(d, 80, 258, 212, 278, fill=JAUNE, r=10)
    tx(d, (146, 268), C.P7_EMAIL["cta"], POP_B, 6.8, (30, 30, 30), anchor="mm")
    rect(d, 0, 292, w, 500, fill=(246, 246, 246))
    tx(d, (146, 304), "À chaque projet sa stratégie", POP_B, 8, (40, 40, 45), anchor="mm")
    thumbs = [f"{ASSETS}/p7_bureau.jpg", f"{ASSETS}/p5_artisan.jpg",
              f"{ASSETS}/p4_restaurant.jpg", f"{ASSETS}/p7_gerante.jpg"]
    for i, (t, chemin) in enumerate(zip(C.P7_EMAIL["lignes"], thumbs)):
        y = 322 + i * 44
        im.paste(cover(chemin, 52, 36, 0.5, 0.5), (S(12), S(y)))
        bloc(d, (72, y + 6), t, POP_R, 6.6, (40, 40, 45), 210, pas_pt=9)
    rect(d, 0, 500, w, 606, fill=FOND_SOMBRE)
    bloc(d, (16, 512), C.P7_EMAIL["bandeau"], POP_B, 8, JAUNE, 260, pas_pt=10, anchor="la")
    tx(d, (146, 552), C.P7_EMAIL["bandeau_sous"], POP_R, 6, (230, 230, 230), anchor="mm")
    rect(d, 18, 568, 138, 586, outline=JAUNE, r=9, larg=0.9)
    tx(d, (78, 577), C.P7_EMAIL["bouton_1"], POP_R, 6.3, JAUNE, anchor="mm")
    rect(d, 150, 568, 274, 586, fill=JAUNE, r=9)
    tx(d, (212, 577), C.P7_EMAIL["bouton_2"], POP_B, 5.9, (30, 30, 30), anchor="mm")
    y = 616
    for t in C.P7_EMAIL["legal"]:
        tx(d, (14, y), t, POP_R, 4.6, (120, 120, 125))
        y += 8
    return im


def visuel_email_bon_savoir_p7():
    """E-mail secondaire, bannière bureau (743.4,96.4)-(1003.6,516.4)."""
    w, h = 260, 420
    im = Image.new("RGB", (S(w), S(h)), (255, 255, 255))
    photo = cover(f"{ASSETS}/p7_bureau.jpg", w, 128, 0.5, 0.5)
    haut = photo.crop((0, 0, photo.width, S(52)))
    photo.paste(Image.blend(haut, Image.new("RGB", haut.size, (0, 0, 0)), 0.5), (0, 0))
    im.paste(photo, (0, 0))
    d = ImageDraw.Draw(im)
    _logo_comparateur(d, 16, 14, 11, fond_clair=False)
    tx(d, (16, 146), "Électricité et gaz : quelle offre choisir ?", POP_B, 8.6, (20, 20, 25))
    rect(d, 92, 168, 168, 186, fill=JAUNE, r=9)
    tx(d, (130, 177), "Je compare", POP_B, 6.5, (30, 30, 30), anchor="mm")
    tx(d, (16, 204), "BON À SAVOIR", POP_B, 6.8, (30, 30, 30))
    bloc(d, (16, 218),
         "Un comparatif d'énergie professionnelle permet de vérifier l'échéance de votre contrat, "
         "la puissance souscrite et le niveau de consommation de votre site.",
         POP_R, 5.8, (70, 70, 75), 228, pas_pt=8)
    bloc(d, (16, 262), "Chaque situation est unique : comparez avant de choisir.", POP_R, 5.8,
         (70, 70, 75), 228, pas_pt=8)
    y = 384
    for t in C.P7_EMAIL["legal"]:
        tx(d, (14, y), t, POP_R, 4.4, (130, 130, 135))
        y += 7
    return im


def visuel_bandeau_p7():
    """Bandeau sombre (743.4,521.7)-(1000.6,677) — 2 boutons."""
    w, h = 257, 155
    im = Image.new("RGB", (S(w), S(h)), FOND_SOMBRE)
    d = ImageDraw.Draw(im)
    bloc(d, (w / 2 - 110, 22), C.P7_EMAIL["bandeau"], POP_B, 8, JAUNE, 220, pas_pt=10)
    tx(d, (w / 2, 60), C.P7_EMAIL["bandeau_sous"], POP_R, 6.3, (235, 235, 235), anchor="mm")
    rect(d, 20, 78, 120, 98, outline=JAUNE, r=10, larg=0.9)
    tx(d, (70, 88), C.P7_EMAIL["bouton_1"], POP_R, 6.5, JAUNE, anchor="mm")
    rect(d, 132, 78, 240, 98, fill=JAUNE, r=10)
    tx(d, (186, 88), C.P7_EMAIL["bouton_2"], POP_B, 6, (30, 30, 30), anchor="mm")
    return im


def visuel_formulaire_p7_gauche():
    """Mini-formulaire (748.1,695.1)-(867.4,784.3)."""
    w, h = 119, 89
    im = Image.new("RGB", (S(w), S(h)), (255, 255, 255))
    d = ImageDraw.Draw(im)
    rect(d, 0.5, 0.5, w - 0.5, h - 0.5, outline=(220, 220, 225), r=3, larg=0.6)
    tx(d, (8, 8), "Quelle énergie recherchez-vous ?", POP_B, 5.6, (30, 30, 30))
    y = 26
    for t in ["Électricité", "Gaz", "Les deux", "Je ne sais pas encore"]:
        radio(d, 9, y, t == "Les deux", 5)
        tx(d, (18, y - 0.5), t, POP_R, 5.6, (50, 50, 50))
        y += 13
    return im


def visuel_formulaire_p7_droite():
    """Mini-formulaire (874.4,696)-(999.6,783.8) avec 4 vignettes."""
    w, h = 125, 88
    im = Image.new("RGB", (S(w), S(h)), (255, 255, 255))
    d = ImageDraw.Draw(im)
    rect(d, 0.5, 0.5, w - 0.5, h - 0.5, outline=(220, 220, 225), r=3, larg=0.6)
    tx(d, (8, 7), "Quel type de site ?", POP_B, 5.6, (30, 30, 30))
    vign = [(f"{ASSETS}/p7_bureau.jpg", "Bureau"), (f"{ASSETS}/p5_artisan.jpg", "Atelier"),
            (f"{ASSETS}/p4_restaurant.jpg", "Restaurant"), (f"{ASSETS}/p7_gerante.jpg", "Commerce")]
    for i, (chemin, lib) in enumerate(vign):
        x = 8 + (i % 2) * 58
        y = 18 + (i // 2) * 34
        im.paste(cover(chemin, 52, 24, 0.5, 0.5), (S(x), S(y)))
        tx(d, (x, y + 26), lib, POP_R, 5.2, (50, 50, 50))
    return im


# ------------------------------------------------------ mise en page (texte)
def _layout(items, chemin_r, chemin_b, pt, largeur, cible):
    """items: [(question, réponse)] → lignes [(texte, 'B'|'R')]. Ajuste le nombre de lignes."""
    fr = fnt(chemin_r, pt)
    fb = fnt(chemin_b, pt)
    n = len(items)
    inline = []
    for q, a in items:
        if fb.getlength(q + " ") + fr.getlength(a) <= S(largeur):
            inline.append(True)
        else:
            inline.append(False)
    lignes_par_item = [1 if inl else 2 for inl in inline]
    total = sum(lignes_par_item)
    # éclater les champs inline pour atteindre le nombre de lignes cible
    for i in range(n):
        if total >= cible:
            break
        if lignes_par_item[i] == 1:
            lignes_par_item[i] = 2
            total += 1
    assert total <= cible, "trop de lignes (%d > %d)" % (total, cible)
    out = []
    for (q, a), nb in zip(items, lignes_par_item):
        if nb == 1:
            out.append([(q + " ", "B"), (a, "R")])
        else:
            out.append([(q, "B")])
            out.append([(a, "R")])
    return out


def _lignes_fiche(textes, chemin_r, pt, largeur, cible):
    """Chaque texte est une ligne : on contrôle qu'il tient sur la largeur."""
    f = fnt(chemin_r, pt)
    out = []
    for t in textes:
        assert f.getlength(t) <= S(largeur), "ligne trop longue : " + t
        out.append([(t, "R")])
    assert len(out) <= cible, "fiche trop longue"
    return out


# ------------------------------------------------------------- PDF : pages
def _zone_efface(page, rect_zone):
    page.add_redact_annot(rect_zone)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                          graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)


def _ecrire(page, x, y, runs, fs, polices, couleurs):
    cx = x
    for texte, style in runs:
        if not texte:
            continue
        nom = polices["B" if style == "B" else "R"]
        page.insert_text((cx, y), texte, fontname=nom, fontsize=fs,
                         color=couleurs["B" if style == "B" else "R"])
        cx += pymupdf.Font(fontfile=polices["fichier_B" if style == "B" else "fichier_R"]).text_length(texte, fs)


def _bloc_pdf(page, x, premiere, pitch, lignes, fs, polices, couleurs):
    y = premiere
    for runs in lignes:
        _ecrire(page, x, y, runs, fs, polices, couleurs)
        y += pitch


def _supprimer_images(page, zones):
    """Retire les images dont le centre tombe dans une des zones (les flèches sont épargnées)."""
    retirees = []
    for info in page.get_image_info(xrefs=True):
        x0, y0, x1, y1 = info["bbox"]
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        if info["xref"] and any(z.contains(pymupdf.Point(cx, cy)) for z in zones):
            if info["xref"] not in retirees:
                page.delete_image(info["xref"])
                retirees.append(info["xref"])
    return retirees



def page_4(doc):
    page = doc[3]
    _zone_efface(page, pymupdf.Rect(1000, 448, 1340, 790))
    _supprimer_images(page, [pymupdf.Rect(483, 89, 956, 441), pymupdf.Rect(477, 495, 963, 757)])
    # textes cachés de l'ancien visuel agricole (sous les nouveaux visuels) : retirés
    page.add_redact_annot(pymupdf.Rect(477, 85, 963, 760))
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
    # ancien bandeau « Extrait du formulaire » (vectoriel + texte) entre la bande LP et le nouveau formulaire
    page.add_redact_annot(pymupdf.Rect(483, 441, 956, 496))
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
    page.draw_rect(pymupdf.Rect(483, 440, 956, 496), color=None,
                   fill=(234 / 255, 241 / 255, 247 / 255), overlay=True)
    # rectangles de la page : fond de l'extrait de formulaire et de la carte LP déjà en place
    page.insert_image(pymupdf.Rect(483.0, 89.0, 956.0, 440.0),
                      stream=_png(visuel_lp_p4()), overlay=True)
    page.insert_image(pymupdf.Rect(477.4, 495.8, 962.7, 756.1),
                      stream=_png(visuel_formulaire_p4()), overlay=True)
    polices = _polices_dejavu(page)
    couleurs = {"B": (23 / 255, 99 / 255, 246 / 255), "R": (0.09, 0.09, 0.09)}
    for y, style, texte in C.P4_MOD:
        _ecrire(page, 1011.0, y, [(texte, style)], 11.3 if style == "B" else 10.3, polices,
                {"B": couleurs["B"], "R": couleurs["R"]})
    for y, texte in C.P4_FICHE:
        _ecrire(page, 1011.0, y, [(texte, "R")], 10.3, polices, {"B": couleurs["B"], "R": couleurs["R"]})


def _polices_dejavu(page):
    page.insert_font(fontname="DJR", fontfile=DJ_R)
    page.insert_font(fontname="DJB", fontfile=DJ_B)
    return {"R": "DJR", "B": "DJB", "fichier_R": DJ_R, "fichier_B": DJ_B}


def _polices_poppins(page):
    page.insert_font(fontname="PR", fontfile=POP_R)
    page.insert_font(fontname="PB", fontfile=POP_B)
    return {"R": "PR", "B": "PB", "fichier_R": POP_R, "fichier_B": POP_B}


_BLEU_PDF = (10 / 255, 91 / 255, 255 / 255)
_NOIR_PDF = (0, 0, 0)
_COULEURS_POP = {"B": _BLEU_PDF, "R": _NOIR_PDF}


def _png(im):
    import io
    b = io.BytesIO()
    im.save(b, format="PNG", optimize=True)
    return b.getvalue()


def _masques_fiche(page, x, base_tel, base_mail, texte_tel, texte_mail):
    """Remplace les barres grises de la page par celles des lignes Tél. et Mail."""
    gris = (0.635, 0.6235, 0.6235)
    panneau = (244 / 255, 245 / 255, 251 / 255)
    for dr in page.get_drawings():
        r = dr["rect"]
        f = dr.get("fill")
        if f and r.x0 > 1000 and abs(f[0] - gris[0]) < 0.02 and abs(f[1] - gris[1]) < 0.02:
            page.draw_rect(pymupdf.Rect(r.x0 - 1, r.y0 - 1, r.x1 + 1, r.y1 + 1), color=None,
                           fill=panneau, overlay=True)
    fr = pymupdf.Font(fontfile=POP_R)
    for base, txt, larg, bas in ((base_tel, texte_tel, 92.0, 3.7), (base_mail, texte_mail, 188.0, 5.2)):
        x0 = x + fr.text_length(txt, 12.997)
        page.draw_rect(pymupdf.Rect(x0, base - 11.9, x0 + larg, base + bas),
                       color=None, fill=gris, overlay=True)


def _mod_et_fiche(page, mod_items, fiche, zone, x, base_mod, base_fiche, cible_mod, cible_fiche, pitch=19.5,
                  masques=None):
    _zone_efface(page, zone)
    pol = _polices_poppins(page)
    lignes_mod = _layout(mod_items, POP_R, POP_B, 12.997, 1380 - x, cible_mod)
    lignes_fiche = _lignes_fiche(fiche, POP_R, 12.997, 1380 - x, cible_fiche)
    if masques:  # masques d'abord : le texte doit rester au-dessus
        _masques_fiche(page, x, *masques)
    _bloc_pdf(page, x, base_mod, pitch, lignes_mod, 12.997, pol, _COULEURS_POP)
    _bloc_pdf(page, x, base_fiche, pitch, lignes_fiche, 12.997, pol, _COULEURS_POP)
    return lignes_mod, lignes_fiche


def page_5(doc):
    page = doc[4]
    _supprimer_images(page, [pymupdf.Rect(407, 209, 723, 639), pymupdf.Rect(710, 172, 1059, 639)])
    page.insert_image(pymupdf.Rect(407.7, 209.4, 722.7, 638.4), stream=_png(visuel_annonce_meta_p5()), overlay=True)
    page.insert_image(pymupdf.Rect(710.5, 172.4, 1058.5, 638.2), stream=_png(visuel_formulaire_meta_p5()), overlay=True)
    return _mod_et_fiche(page, C.P5_MOD, C.P5_FICHE, pymupdf.Rect(1085, 268, 1395, 760), 1091.2,
                         280.4, 564.8, 13, 10, masques=(720.8, 740.3, "Tél : ", "Mail : "))


def page_6(doc):
    page = doc[5]
    _supprimer_images(page, [pymupdf.Rect(410, 163, 1047, 518)])
    page.insert_image(pymupdf.Rect(410.8, 163.5, 1046.1, 517.9), stream=_png(visuel_crm_p6()), overlay=True)
    return _mod_et_fiche(page, C.P6_MOD, C.P6_FICHE, pymupdf.Rect(1075, 337, 1395, 790), 1082.2,
                         349.8, 601.2, 11, 10, masques=(757.2, 776.7, "Tél : ", "Mail : "))


def page_7(doc):
    page = doc[6]
    _supprimer_images(page, [pymupdf.Rect(432, 88, 725, 793), pymupdf.Rect(743, 96, 1004, 517),
                             pymupdf.Rect(743, 521, 1001, 678), pymupdf.Rect(748, 695, 1004, 785)])
    page.insert_image(pymupdf.Rect(432.6, 88.0, 724.4, 792.2), stream=_png(visuel_email_p7()), overlay=True)
    page.insert_image(pymupdf.Rect(743.4, 96.4, 1003.6, 516.4), stream=_png(visuel_email_bon_savoir_p7()), overlay=True)
    page.insert_image(pymupdf.Rect(743.4, 521.7, 1000.6, 677.0), stream=_png(visuel_bandeau_p7()), overlay=True)
    page.insert_image(pymupdf.Rect(748.1, 695.1, 867.4, 784.3), stream=_png(visuel_formulaire_p7_gauche()), overlay=True)
    page.insert_image(pymupdf.Rect(874.4, 696.0, 999.6, 783.8), stream=_png(visuel_formulaire_p7_droite()), overlay=True)
    return _mod_et_fiche(page, C.P7_MOD, C.P7_FICHE, pymupdf.Rect(1075, 290, 1395, 790), 1081.9,
                         307.9, 578.5, 13, 11, masques=(754.0, 773.5, "Tél : ", "Mail : "))


# ------------------------------------------------------------------ main
def construire():
    print("Phase 2 : fabrication de la plaquette complète")
    doc = pymupdf.open(BASE)
    rapports = {}
    # ordre : l'insertion d'images sur les pages n'interfère pas entre elles
    rapports[4] = page_4(doc)
    rapports[5] = page_5(doc)
    rapports[6] = page_6(doc)
    rapports[7] = page_7(doc)
    doc.save(SORTIE, garbage=3, deflate=True)
    doc.close()
    print("écrit :", os.path.normpath(SORTIE))
    for k in (5, 6, 7):
        m, f = rapports[k]
        print("  page %d : modération %d lignes, fiche %d lignes" % (k, len(m), len(f)))
    return rapports


if __name__ == "__main__":
    construire()
