# -*- coding: utf-8 -*-
"""Cartes RCS de la page 3 — version « panneaux solaires ».

Même géométrie et même langage graphique que les cartes reconstruites en V3
(work/build_cartes_p3.py) : photo en haut, titre, texte, chevron, bouton
d'action. Les visuels sont opaques et calés sur les rects d'origine du PDF.

Sortie : work/solaire/assets/carte1.png, carte2.png
"""
import os

from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ICI, "assets")
PHOTOS = os.path.join(ICI, "photos")
FONTS = os.path.join(ICI, "assets")

ECHELLE = 3.142
CARTE_1_PT = (248.25, 299.24)
CARTE_2_PT = (240.75, 290.25)

PANEL_BG = (244, 245, 251)
CARTE_BG = (237, 237, 239)
TITRE = (17, 17, 17)
TEXTE = (133, 133, 138)
CHEVRON = (178, 178, 184)
BORDURE = (219, 219, 224)
PILL_BG = (255, 255, 255)

REG = os.path.join(FONTS, "Poppins-Regular.ttf")
GRAS = os.path.join(FONTS, "Poppins-Bold.ttf")


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


def _chevron(d, x, y, taille, epaisseur, couleur):
    d.line([(x, y - taille / 2), (x + taille * 0.62, y), (x, y + taille / 2)],
           fill=couleur, width=epaisseur, joint="curve")


def _pastille(d, boite, carte, font_cta):
    x0, y0, x1, y1 = boite
    d.rounded_rectangle([x0, y0, x1, y1], radius=(y1 - y0) / 2,
                        fill=PILL_BG, outline=BORDURE, width=2)
    texte = carte["cta"]
    bb = d.textbbox((0, 0), texte, font=font_cta)
    d.text((x0 + 46, (y0 + y1) / 2 - (bb[1] + bb[3]) / 2),
           texte, font=font_cta, fill=carte["cta_couleur"])
    cx, cy = x1 - 46, (y0 + y1) / 2
    if carte["cta_icone"] == "cercle":
        r = 22
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(108, 108, 114))
        d.line([(cx - 9, cy), (cx + 9, cy)], fill=(255, 255, 255), width=4)
        d.line([(cx + 3, cy - 7), (cx + 9, cy), (cx + 3, cy + 7)],
               fill=(255, 255, 255), width=4, joint="curve")
    else:
        _chevron(d, cx - 6, cy, 22, 4, (170, 170, 176))


def _bandeau(img, y0, y1, lignes, tailles, marge=30, opacite=118):
    """Bande sombre translucide sur la photo, texte blanc (haut-gauche)."""
    couche = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(couche)
    d.rectangle([0, y0, img.size[0], y1], fill=(12, 16, 28, opacite))
    y = y0 + 10
    for ligne, taille in zip(lignes, tailles):
        f = ImageFont.truetype(GRAS, taille)
        d.text((marge, y), ligne, font=f, fill=(255, 255, 255, 255))
        y += round(taille * 1.34)
    return Image.alpha_composite(img.convert("RGBA"), couche).convert("RGB")


def _photo(chemin, largeur, hauteur):
    im = Image.open(chemin).convert("RGB")
    r = max(largeur / im.width, hauteur / im.height)
    im = im.resize((round(im.width * r) + 1, round(im.height * r) + 1), Image.LANCZOS)
    g = im.width - largeur
    h = im.height - hauteur
    # cadrage : un peu au-dessus du centre (toiture / visages)
    im = im.crop((g // 2, int(h * 0.42), g // 2 + largeur, int(h * 0.42) + hauteur))
    return im


def construire(carte, taille_pt, photo, hauteur_photo, sortie):
    largeur = round(taille_pt[0] * ECHELLE)
    hauteur = round(taille_pt[1] * ECHELLE)
    marge = round(0.073 * largeur)
    largeur_texte = largeur - marge - round(0.128 * largeur)

    f_titre = ImageFont.truetype(GRAS, round(0.0692 * largeur))
    f_texte = ImageFont.truetype(REG, round(0.0487 * largeur))
    f_cta = ImageFont.truetype(GRAS, round(0.0487 * largeur))
    interligne_titre = round(1.11 * f_titre.size)
    interligne_texte = round(1.30 * f_texte.size)

    lignes_titre = _couper(carte["titre"], f_titre, largeur_texte)
    lignes_texte = _couper(carte["texte"], f_texte, largeur_texte)

    img = Image.new("RGB", (largeur, hauteur), CARTE_BG)
    ph = photo.crop((0, 0, largeur, hauteur_photo)).resize(
        (largeur, hauteur_photo), Image.LANCZOS)
    if carte.get("kicker"):
        tailles = [round(0.0265 * largeur), round(0.0205 * largeur)]
        ph = _bandeau(ph, 0, round(0.019 * largeur) + sum(
            round(t * 1.34) for t in tailles), carte["kicker"], tailles)
    if carte.get("bandeau"):
        f = ImageFont.truetype(GRAS, round(0.0195 * largeur))
        h = round(f.size * 1.9)
        ph = _bandeau(ph, hauteur_photo - h, hauteur_photo, [carte["bandeau"]],
                      [f.size], marge=30, opacite=150)
    img.paste(ph, (0, 0))
    d = ImageDraw.Draw(img)

    haut_texte = hauteur_photo + round(0.0436 * hauteur)
    y = haut_texte
    for ligne in lignes_titre:
        d.text((marge, y), ligne, font=f_titre, fill=TITRE)
        y += interligne_titre
    bas_titre = y - interligne_titre + f_titre.size * 0.72

    y += round(0.021 * hauteur)
    for ligne in lignes_texte:
        d.text((marge, y), ligne, font=f_texte, fill=TEXTE)
        y += interligne_texte
    bas_desc = y - interligne_texte + f_texte.size * 0.72

    _chevron(d, largeur - marge - round(0.030 * largeur),
             (haut_texte + bas_desc) / 2, round(0.037 * largeur),
             max(3, round(0.0064 * largeur)), CHEVRON)

    h_pill = round(0.115 * largeur)
    bas_pill = hauteur - round(0.067 * hauteur)
    _pastille(d, (round(0.049 * largeur), bas_pill - h_pill,
                  largeur - round(0.049 * largeur), bas_pill), carte, f_cta)

    assert bas_pill <= hauteur - 8, "bouton hors carte"
    assert bas_desc <= bas_pill - 12, "texte qui touche le bouton"
    print("    %s %dx%d | titre %s | texte %s | libre %d px" % (
        os.path.basename(sortie), largeur, hauteur, lignes_titre, lignes_texte,
        bas_pill - bas_desc))

    d.rectangle([0, 0, largeur - 1, hauteur - 1], outline=BORDURE, width=2)
    masque = Image.new("L", (largeur, hauteur), 0)
    ImageDraw.Draw(masque).rounded_rectangle([0, 0, largeur - 1, hauteur - 1],
                                             radius=round(0.031 * largeur), fill=255)
    fond = Image.new("RGB", (largeur, hauteur), PANEL_BG)
    fond.paste(img, (0, 0), masque)
    fond.save(sortie, optimize=True)


def main():
    import contenus
    os.makedirs(ASSETS, exist_ok=True)
    p1 = _photo(os.path.join(PHOTOS, "maison.jpg"),
                round(CARTE_1_PT[0] * ECHELLE), 400)
    p2 = _photo(os.path.join(PHOTOS, "couple.jpg"),
                round(CARTE_2_PT[0] * ECHELLE), 370)
    construire(contenus.CARTE_1, CARTE_1_PT, p1, 400,
               os.path.join(ASSETS, "carte1.png"))
    construire(contenus.CARTE_2, CARTE_2_PT, p2, 370,
               os.path.join(ASSETS, "carte2.png"))


if __name__ == "__main__":
    main()
