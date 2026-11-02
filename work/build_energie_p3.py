# -*- coding: utf-8 -*-
"""Page 3 (SMS – RCS) déclinée « Fournisseurs d'énergies ».

Entrée : « Plaquette HelloLead - Assurance V3.pdf » (page 3), utilisée comme
référence de mise en page. Ses calques cachés (textes et visuels des secteurs
précédents) sont retirés ; les blocs « Modération & Enrichissement » et « fiche
acheteur » sont réécrits à la géométrie d'origine (13 pt, pas 19,5 pt,
lignes de base 265,35 et 599,30).

Sorties :
  - work/assets/*.png|jpg        visuels reconstruits (intermédiaires)
  - work/assets/page3_fond.png   fond de page sans texte modifiable (pour le PPTX)
  - Plaquette HelloLead - Energie - Page 3 (validation).pdf
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont
import pymupdf

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import contenus_energie as C  # noqa: E402

RACINE = os.path.join(ICI, "..")
ASSETS = os.path.join(ICI, "assets")
SRC = os.path.join(RACINE, "Plaquette HelloLead - Assurance V3.pdf")
SORTIE = os.path.join(RACINE, "Plaquette HelloLead - Energie - Page 3 (validation).pdf")
REG = os.path.join(ASSETS, "Poppins-Regular.ttf")
GRAS = os.path.join(ASSETS, "Poppins-Bold.ttf")

PANEL = (244, 245, 251)
BLEU = (10, 91, 255)
NOIR = (0, 0, 0)
BORDURE_OPT = (156, 199, 234)
BTN_G = (46, 151, 212)
BTN_D = (143, 192, 228)

# Géométrie d'origine (points)
CARTE_1_RECT = pymupdf.Rect(516.86, 140.58, 765.11, 439.82)
CARTE_2_RECT = pymupdf.Rect(520.65, 441.18, 761.40, 740.42)
LANDING_RECT = pymupdf.Rect(755.11, 150.61, 1041.61, 617.86)
X_TXT = 1098.92
FS = 12.997
LH = 19.5
BASE_MOD = 265.35
BASE_FICHE = 599.30
MAX_X = 1392.0
MAX_LIGNES_MOD = 16
MAX_LIGNES_FICHE = 10

# ------------------------------------------------------------------ polices
F_REG = pymupdf.Font(fontfile=REG)
F_GRAS = pymupdf.Font(fontfile=GRAS)


def _pil(chemin, taille):
    return ImageFont.truetype(chemin, max(1, round(taille)))


def _couper(texte, font, largeur):
    mots, lignes, courant = texte.split(), [], ""
    for mot in mots:
        essai = (courant + " " + mot).strip()
        if font.getlength(essai) <= largeur or not courant:
            courant = essai
        else:
            lignes.append(courant)
            courant = mot
    if courant:
        lignes.append(courant)
    return lignes


# ------------------------------------------------------------- visuels
def _fond_panneau(w, h):
    return Image.new("RGB", (w, h), PANEL)


def _chevron(d, x, y, taille, epaisseur, couleur):
    d.line([(x, y - taille / 2), (x + taille * 0.62, y), (x, y + taille / 2)],
           fill=couleur, width=epaisseur, joint="curve")


def _pastille(d, boite, carte, font_cta):
    x0, y0, x1, y1 = boite
    d.rounded_rectangle([x0, y0, x1, y1], radius=(y1 - y0) / 2,
                        fill=(255, 255, 255), outline=(219, 219, 224), width=2)
    haut = d.textbbox((0, 0), carte["cta"], font=font_cta)
    d.text((x0 + 46, (y0 + y1) / 2 - (haut[1] + haut[3]) / 2), carte["cta"],
           font=font_cta, fill=carte["cta_couleur"])
    cx, cy = x1 - 46, (y0 + y1) / 2
    if carte["cta_icone"] == "cercle":
        r = 22
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(108, 108, 114))
        d.line([(cx - 9, cy), (cx + 9, cy)], fill=(255, 255, 255), width=4)
        d.line([(cx + 3, cy - 7), (cx + 9, cy), (cx + 3, cy + 7)],
               fill=(255, 255, 255), width=4, joint="curve")
    else:
        _chevron(d, cx - 6, cy, 22, 4, (170, 170, 176))


def _photo_couverture(chemin, w, h, recadrage=(0.5, 0.5)):
    src = Image.open(chemin).convert("RGB")
    r = max(w / src.width, h / src.height)
    src = src.resize((round(src.width * r), round(src.height * r)), Image.LANCZOS)
    x = round((src.width - w) * recadrage[0])
    y = round((src.height - h) * recadrage[1])
    return src.crop((x, y, x + w, y + h))


def carte_rcs(carte, taille_pt, photo_chemin, hauteur_photo, recadrage, sortie):
    """Carte RCS : photo en haut, titre, texte, bouton. Même échelle que la V3."""
    echelle = 3.142
    w = round(taille_pt[0] * echelle)
    h = round(taille_pt[1] * echelle)
    marge = round(0.073 * w)
    larg_txt = w - marge - round(0.128 * w)
    f_titre = _pil(GRAS, 0.0692 * w)
    f_texte = _pil(REG, 0.0487 * w)
    f_cta = _pil(GRAS, 0.0487 * w)
    inter_titre = round(1.11 * f_titre.size)
    inter_texte = round(1.30 * f_texte.size)

    img = _fond_panneau(w, h)
    photo = _photo_couverture(photo_chemin, w, hauteur_photo, recadrage)
    img.paste(photo, (0, 0))
    d = ImageDraw.Draw(img)

    if carte["kicker"]:
        # dégradé sombre en bas de photo, pour la lisibilité des accroches
        dg = Image.new("L", (w, hauteur_photo), 0)
        dd = ImageDraw.Draw(dg)
        for yy in range(hauteur_photo):
            if yy > hauteur_photo * 0.45:
                t = (yy - hauteur_photo * 0.45) / (hauteur_photo * 0.55)
                dd.line([(0, yy), (w, yy)], fill=int(150 * t))
        noir = Image.new("RGB", (w, hauteur_photo), (0, 0, 0))
        img.paste(noir, (0, 0), dg)
        d = ImageDraw.Draw(img)
        f_acc = _pil(GRAS, 0.0487 * w)
        f_kick = _pil(GRAS, 0.0235 * w)
        for i, ligne in enumerate(_couper(carte["accroche"], f_acc, w * 0.62)[:2]):
            d.text((marge * 0.6, round(0.07 * hauteur_photo) + i * round(1.1 * f_acc.size)),
                   ligne, font=f_acc, fill=(255, 255, 255))
        yk = hauteur_photo - round(0.06 * hauteur_photo) - len(carte["kicker"]) * round(1.35 * f_kick.size)
        for ligne in carte["kicker"]:
            d.text((marge * 0.6, yk), ligne, font=f_kick, fill=(255, 255, 255))
            yk += round(1.35 * f_kick.size)

    y = hauteur_photo + round(0.0436 * h)
    haut_titre = y
    lignes_titre = _couper(carte["titre"], f_titre, larg_txt)
    for ligne in lignes_titre:
        d.text((marge, y), ligne, font=f_titre, fill=(17, 17, 17))
        y += inter_titre
    bas_titre = y - inter_titre + f_titre.size * 0.72

    y += round(0.021 * h)
    haut_desc = y
    lignes_texte = _couper(carte["texte"], f_texte, larg_txt)
    for ligne in lignes_texte:
        d.text((marge, y), ligne, font=f_texte, fill=(133, 133, 138))
        y += inter_texte
    bas_desc = y - inter_texte + f_texte.size * 0.72

    _chevron(d, w - marge - round(0.030 * w), (haut_titre + bas_desc) / 2,
             round(0.037 * w), max(3, round(0.0064 * w)), (178, 178, 184))

    h_pill = round(0.115 * w)
    bas_pill = h - round(0.067 * h)
    _pastille(d, (round(0.049 * w), bas_pill - h_pill, w - round(0.049 * w), bas_pill),
              carte, f_cta)

    # contrôles : rien ne déborde, le texte ne touche pas le bouton
    assert bas_pill <= h - 8, "bouton hors carte"
    assert bas_desc <= bas_pill - 12, "texte trop long : touche le bouton"
    assert len(lignes_titre) <= 2, "titre trop long"

    d.rectangle([0, 0, w - 1, h - 1], outline=(219, 219, 224), width=2)
    masque = Image.new("L", (w, h), 0)
    ImageDraw.Draw(masque).rounded_rectangle([0, 0, w - 1, h - 1],
                                             radius=round(0.031 * w), fill=255)
    fond = _fond_panneau(w, h)
    fond.paste(img, (0, 0), masque)
    fond.save(sortie, optimize=True)
    print("  %s %dx%d titre=%s texte=%d lignes" % (
        os.path.basename(sortie), w, h, lignes_titre, len(lignes_texte)))


# ------------------------------------------------------ page de destination
def _ajuster(texte, font_chemin, largeur_cible):
    """Taille PIL telle que la chaîne fasse la largeur cible (référence d'origine)."""
    for taille in range(10, 80):
        if ImageFont.truetype(font_chemin, taille).getlength(texte) > largeur_cible:
            return taille - 1
    return 40


def page_destination(sortie):
    W, H = 958, 1562
    doc = pymupdf.open(SRC)
    ref_pix = pymupdf.Pixmap(doc, 124)
    ref_img = Image.frombytes("RGB", (ref_pix.width, ref_pix.height), ref_pix.samples) \
        if ref_pix.n == 3 else Image.frombytes("RGB", (ref_pix.width, ref_pix.height),
                                               pymupdf.Pixmap(pymupdf.csRGB, ref_pix).samples)
    img = Image.new("RGB", (W, H), (255, 255, 255))
    # en-tête : logo « hellodevis » conservé tel quel (marque)
    img.paste(ref_img.crop((300, 20, 660, 130)), (300, 20))
    # photo d'ambiance sous l'en-tête
    haut_photo = 158
    photo = _photo_couverture("%s/photo_bureau.jpg" % ASSETS, W, H - haut_photo, (0.5, 0.5))
    img.paste(photo, (0, haut_photo))
    d = ImageDraw.Draw(img)
    # carte blanche arrondie
    d.rounded_rectangle([22, 255, 939, 1257], radius=34, fill=(255, 255, 255))

    f_t1 = _pil(GRAS, _ajuster("Trouvez le meilleur partenaire", GRAS, 491))
    f_t2 = _pil(GRAS, _ajuster("pour votre protection sociale !", GRAS, 462))
    f_sub = _pil(REG, _ajuster("Sécurisez vos revenus et votre santé avec une couverture adaptée à", REG, 752))
    f_lab = _pil(REG, _ajuster("Concernant votre activité, vous êtes :", REG, 411))
    f_opt = _pil(REG, _ajuster("Travailleur indépendant (TNS)", REG, 313))

    d.text((480, 327), C.LANDING["titre_1"], font=f_t1, fill=BLEU, anchor="mm")
    d.text((480, 381), C.LANDING["titre_2"], font=f_t2, fill=(17, 17, 17), anchor="mm")

    lignes_sub = _couper(C.LANDING["sous_titre"], f_sub, 810)
    assert len(lignes_sub) <= 2, "sous-titre trop long"
    for i, ligne in enumerate(lignes_sub):
        d.text((76, 450 + 31 * i), ligne, font=f_sub, fill=(62, 62, 66), anchor="lm")

    def groupe(label, options, y_label, y_opts):
        d.text((76, y_label), label, font=f_lab, fill=(43, 43, 46), anchor="lm")
        for k, texte in enumerate(options):
            top = y_opts[k]
            d.rounded_rectangle([76, top, 885, top + 65], radius=12, fill=(255, 255, 255),
                                outline=BORDURE_OPT, width=2)
            cy = top + 32
            d.ellipse([96, cy - 9, 114, cy + 9], outline=(140, 140, 140), width=2)
            d.text((126, cy), texte, font=f_opt, fill=(51, 51, 51), anchor="lm")

    groupe(C.LANDING["q1"], C.LANDING["q1_options"], 563, [593, 672, 751])
    groupe(C.LANDING["q2"], C.LANDING["q2_options"], 860, [890, 969, 1048])

    # boutons de navigation (identiques à l'original)
    d.rounded_rectangle([76, 1165, 174, 1218], radius=6, fill=BTN_G)
    d.text((125, 1192), "«", font=_pil(GRAS, 26), fill=(255, 255, 255), anchor="mm")
    d.rounded_rectangle([787, 1165, 885, 1218], radius=6, fill=BTN_D)
    d.text((836, 1192), "»", font=_pil(GRAS, 26), fill=(255, 255, 255), anchor="mm")

    img.save(sortie, optimize=True)
    print("  landing.png %dx%d" % (W, H))


# ------------------------------------------------------------ mise en page
def _runs_modération():
    """Retourne une liste de lignes ; chaque ligne = [(texte, 'B'|'R'), ...]."""
    lignes = []
    for i, (q, a) in enumerate(C.MODERATION):
        # six premiers champs : question et réponse sur deux lignes (hauteur d'origine : 16 lignes)
        if i >= 6 and F_GRAS.text_length(q + " ", FS) + F_REG.text_length(a, FS) <= MAX_X - X_TXT:
            lignes.append([(q + " ", "B"), (a, "R")])
        else:
            lignes.append([(q, "B")])
            mots, courant = a.split(), ""
            for m in mots:
                essai = (courant + " " + m).strip()
                if F_REG.text_length(essai, FS) <= MAX_X - X_TXT or not courant:
                    courant = essai
                else:
                    lignes.append([(courant, "R")])
                    courant = m
            if courant:
                lignes.append([(courant, "R")])
    return lignes


def _lignes_fiche():
    lignes = []
    for texte in C.FICHE:
        mots, courant = texte.split(), ""
        for m in mots:
            essai = (courant + " " + m).strip()
            if F_REG.text_length(essai, FS) <= MAX_X - X_TXT or not courant:
                courant = essai
            else:
                lignes.append([(courant, "R")])
                courant = m
        if courant:
            lignes.append([(courant, "R")])
    return lignes


def _ecrire_ligne(page, y, runs):
    x = X_TXT
    for texte, style in runs:
        if not texte:
            continue
        nom = "PB" if style == "B" else "PR"
        couleur = BLEU if style == "B" else NOIR
        page.insert_text((x, y), texte, fontname=nom, fontsize=FS,
                         color=tuple(c / 255 for c in couleur))
        x += (F_GRAS if style == "B" else F_REG).text_length(texte, FS)


def construire():
    print("Construction de la page 3 « Fournisseurs d'énergies »")
    os.makedirs(ASSETS, exist_ok=True)

    # 1. visuels
    carte_rcs(C.CARTE_1, (248.25, 299.24), "%s/photo_commerce.jpg" % ASSETS, 370,
              (0.5, 0.45), "%s/carte1.png" % ASSETS)
    carte_rcs(C.CARTE_2, (240.75, 299.24), "%s/photo_bureau.jpg" % ASSETS, 360,
              (0.5, 0.35), "%s/carte2.png" % ASSETS)
    page_destination("%s/landing.png" % ASSETS)

    # 2. nettoyage : texte des blocs de droite (y compris calques cachés) et visuels
    doc = pymupdf.open(SRC)
    page = doc[2]
    zone_texte = pymupdf.Rect(1090, 244, 1410, 800)
    page.add_redact_annot(zone_texte)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                          graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
    for xref in (58, 124, 67, 69, 540, 541):      # visuels (anciens et calques V3)
        page.delete_image(xref)
    page.insert_image(CARTE_1_RECT, filename="%s/carte1.png" % ASSETS, overlay=True)
    page.insert_image(CARTE_2_RECT, filename="%s/carte2.png" % ASSETS, overlay=True)
    page.insert_image(LANDING_RECT, filename="%s/landing.png" % ASSETS, overlay=True)

    # masquage Tél. / Mail : barres grises d'origine (même position, même teinte).
    # Les trois barres résiduelles de la V3 (vers 665-707 pt) sont recouvertes par le fond.
    page.draw_rect(pymupdf.Rect(1110, 655, 1330, 715), color=None,
                   fill=(244 / 255, 245 / 255, 251 / 255), overlay=True)
    for r in ((1124.6, 743.4, 1216.8, 759.0), (1132.1, 764.2, 1319.9, 779.8)):
        page.draw_rect(pymupdf.Rect(*r), color=None, fill=(0.635, 0.6235, 0.6235), overlay=True)

    # fond sans texte pour le PPTX (visuels et grisés inclus)
    fond = pymupdf.open()
    fond.insert_pdf(doc, from_page=2, to_page=2)
    fond_pix = fond[0].get_pixmap(dpi=150)
    fond_pix.save("%s/page3_fond.png" % ASSETS)
    fond.close()

    # 3. texte réécrit à la géométrie d'origine
    page.insert_font(fontname="PR", fontfile=REG)
    page.insert_font(fontname="PB", fontfile=GRAS)
    lignes_mod = _runs_modération()
    lignes_fiche = _lignes_fiche()
    print("  modération : %d lignes (max %d)" % (len(lignes_mod), MAX_LIGNES_MOD))
    print("  fiche      : %d lignes (max %d)" % (len(lignes_fiche), MAX_LIGNES_FICHE))
    assert len(lignes_mod) <= MAX_LIGNES_MOD, "modération : trop de lignes"
    assert len(lignes_fiche) <= MAX_LIGNES_FICHE, "fiche : trop de lignes"
    for i, runs in enumerate(lignes_mod):
        _ecrire_ligne(page, BASE_MOD + i * LH, runs)
    for i, runs in enumerate(lignes_fiche):
        _ecrire_ligne(page, BASE_FICHE + i * LH, runs)

    doc.save(SORTIE, garbage=3, deflate=True)
    doc.close()
    print("écrit :", os.path.normpath(SORTIE))
    return lignes_mod, lignes_fiche


if __name__ == "__main__":
    mod, fiche = construire()
    for r in mod:
        print("  M |", "".join(t for t, _ in r))
    for r in fiche:
        print("  F |", "".join(t for t, _ in r))
