# -*- coding: utf-8 -*-
"""Reconstruit les deux cartes RCS de la page 3 (visuels « SMS » de la colonne centrale).

Le visuel de chaque carte est un PNG opaque, calé exactement sur la géométrie des
cartes d'origine du PDF (voir work/build_p3.py), de sorte qu'il recouvre
intégralement l'ancien visuel et se raccorde au fond du panneau (#F4F5FB).

Sortie : work/assets/carte1.png, work/assets/carte2.png
"""
import io
import os

from PIL import Image, ImageDraw, ImageFont
import pymupdf

ICI = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ICI, "assets")
SRC_PDF = os.path.join(ICI, "..", "Plaquette HelloLead - Assurance V2 (1).pdf")

# ---------------------------------------------------------------- géométrie
# 3.142 px/pt : même échelle pour les deux cartes, donc mêmes tailles de texte
# en points une fois posées dans la page.
ECHELLE = 3.142
CARTE_1_PT = (248.25, 299.24)
CARTE_2_PT = (240.75, 299.24)

PANEL_BG = (244, 245, 251)        # fond du panneau central
CARTE_BG = (237, 237, 239)        # fond de la zone texte des cartes
TITRE = (17, 17, 17)
TEXTE = (133, 133, 138)
CHEVRON = (178, 178, 184)
BORDURE = (219, 219, 224)
PILL_BG = (255, 255, 255)


def _fonts():
    """Poppins Regular/Bold, extraits du PDF (polices complètes, non sous-ensemblées)."""
    doc = pymupdf.open(SRC_PDF)
    chemins = {}
    for xref, nom in ((132, "Poppins-Regular.ttf"), (141, "Poppins-Bold.ttf")):
        chemin = os.path.join(ASSETS, nom)
        if not os.path.exists(chemin):
            _, _, _, buf = doc.extract_font(xref)
            with open(chemin, "wb") as fh:
                fh.write(buf)
        chemins[nom] = chemin
    return chemins["Poppins-Regular.ttf"], chemins["Poppins-Bold.ttf"]


def _photos():
    """Photos des cartes V2 (recadrées) : on ne touche pas aux visuels, on les réutilise."""
    doc = pymupdf.open(SRC_PDF)
    pix1 = pymupdf.Pixmap(doc, 116)   # carte 1 (photo + accroches déjà incrustées)
    pix2 = pymupdf.Pixmap(doc, 122)   # carte 2 (photo nue)
    img1 = Image.open(io.BytesIO(pix1.tobytes("png"))).convert("RGB")
    img2 = Image.open(io.BytesIO(pix2.tobytes("png"))).convert("RGB")
    return img1, img2


def _nettoyer_coins(img, taille=36):
    """Les visuels V2 ont les coins hauts noirs (fond transparent rendu en noir).

    On les comble par symétrie du contenu voisin, sinon l'arc noir dépasse du
    coin arrondi de la carte.
    """
    import numpy as np

    a = np.asarray(img).copy()
    h, w, _ = a.shape
    noir = a.max(axis=2) < 30
    if not noir[:taille].any():
        return img
    coins = [
        (slice(0, taille), slice(0, taille), slice(taille, 2 * taille)),
        (slice(0, taille), slice(w - taille, w), slice(w - 2 * taille, w - taille)),
    ]
    for lignes, cols, voisin in coins:
        m = noir[lignes, cols]
        if m.any():
            a[lignes, cols][m] = np.fliplr(a[lignes, voisin])[m]
    return Image.fromarray(a, "RGB")


def _couper(texte, font, largeur):
    """Découpe en lignes qui tiennent dans `largeur` (césure aux espaces)."""
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
    """Bouton d'action arrondi, texte à gauche, icône à droite."""
    x0, y0, x1, y1 = boite
    d.rounded_rectangle([x0, y0, x1, y1], radius=(y1 - y0) / 2,
                        fill=PILL_BG, outline=BORDURE, width=2)
    texte = carte["cta"]
    haut_texte = d.textbbox((0, 0), texte, font=font_cta)
    d.text((x0 + 46, (y0 + y1) / 2 - (haut_texte[1] + haut_texte[3]) / 2),
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


def construire(carte, taille_pt, photo, hauteur_photo, surf, sortie,
               reg_font, gras_font):
    """Assemble une carte : photo en haut, puis titre / texte / bouton."""
    largeur = round(taille_pt[0] * ECHELLE)
    hauteur = round(taille_pt[1] * ECHELLE)
    marge = round(0.073 * largeur)                  # 57 px pour 780
    largeur_texte = largeur - marge - round(0.128 * largeur)   # colonne + place du chevron

    f_titre = ImageFont.truetype(gras_font, round(0.0692 * largeur))
    f_texte = ImageFont.truetype(reg_font, round(0.0487 * largeur))
    f_cta = ImageFont.truetype(gras_font, round(0.0487 * largeur))
    interligne_titre = round(1.11 * f_titre.size)
    interligne_texte = round(1.30 * f_texte.size)

    lignes_titre = _couper(carte["titre"], f_titre, largeur_texte)
    lignes_texte = _couper(carte["texte"], f_texte, largeur_texte)

    img = Image.new("RGB", (largeur, hauteur), CARTE_BG)
    # photo
    ph = _nettoyer_coins(photo).crop((0, 0, largeur, hauteur_photo))
    if ph.size[0] != largeur:
        ph = ph.resize((largeur, hauteur_photo), Image.LANCZOS)
    img.paste(ph, (0, 0))
    # L'accroche blanche sur la photo est déjà incrustée dans le visuel d'origine :
    # on ne la redessine pas (elle serait dédoublée).
    d = ImageDraw.Draw(img)

    # titre
    haut_texte = hauteur_photo + round(0.0436 * hauteur)
    y = haut_texte
    for ligne in lignes_titre:
        d.text((marge, y), ligne, font=f_titre, fill=TITRE)
        y += interligne_titre
    bas_titre = y - interligne_titre + f_titre.size * 0.72

    # texte courant
    y += round(0.021 * hauteur)
    haut_desc = y
    for ligne in lignes_texte:
        d.text((marge, y), ligne, font=f_texte, fill=TEXTE)
        y += interligne_texte
    bas_desc = y - interligne_texte + f_texte.size * 0.72

    # chevron, centré sur le bloc titre + texte
    _chevron(d, largeur - marge - round(0.030 * largeur),
             (haut_texte + bas_desc) / 2, round(0.037 * largeur),
             max(3, round(0.0064 * largeur)), CHEVRON)

    # bouton d'action
    h_pill = round(0.115 * largeur)
    bas_pill = hauteur - round(0.067 * hauteur)
    _pastille(d, (round(0.049 * largeur), bas_pill - h_pill,
                  largeur - round(0.049 * largeur), bas_pill), carte, f_cta)

    # contrôles : rien ne doit déborder, ni toucher le bouton
    assert bas_pill <= hauteur - 8, "bouton hors carte"
    assert bas_desc <= bas_pill - 12, (
        "texte qui touche le bouton : bas_desc=%s bas_pill=%s" % (bas_desc, bas_pill))
    print("    bloc texte: %d -> %d, bouton %d -> %d, marge libre %d px" % (
        haut_texte, bas_desc, bas_pill - h_pill, bas_pill, bas_pill - bas_desc))

    # bordure fine + coins arrondis couleur panneau
    d.rectangle([0, 0, largeur - 1, hauteur - 1], outline=BORDURE, width=2)
    masque = Image.new("L", (largeur, hauteur), 0)
    ImageDraw.Draw(masque).rounded_rectangle([0, 0, largeur - 1, hauteur - 1],
                                             radius=round(0.031 * largeur), fill=255)
    fond = Image.new("RGB", (largeur, hauteur), PANEL_BG)
    fond.paste(img, (0, 0), masque)
    fond.save(sortie, optimize=True)
    print("%s  %dx%d  titre=%s  texte=%s" % (
        os.path.basename(sortie), largeur, hauteur,
        lignes_titre, lignes_texte))
    return lignes_titre, lignes_texte


def main():
    os.makedirs(ASSETS, exist_ok=True)
    reg, gras = _fonts()
    photo1, photo2 = _photos()
    import contenus_p3 as contenus
    construire(contenus.CARTE_1, CARTE_1_PT, photo1, 370,
               None, os.path.join(ASSETS, "carte1.png"), reg, gras)
    construire(contenus.CARTE_2, CARTE_2_PT, photo2.crop((12, 0, 768, 966)), 360,
               None, os.path.join(ASSETS, "carte2.png"), reg, gras)


if __name__ == "__main__":
    import sys
    sys.path.insert(0, ICI)
    main()
