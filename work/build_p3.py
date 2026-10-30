# -*- coding: utf-8 -*-
"""Corrige la page 3 (SMS – RCS) de la plaquette V2.

Corrections apportées :
  * les deux cartes RCS sont reconstruites (work/build_cartes_p3.py) et posées
    exactement sur la géométrie des cartes d'origine : plus de bandes
    résiduelles de l'ancien visuel, plus de bas de carte fantôme, plus de texte
    coupé par le bord de la page de destination ;
  * le bouton d'action de chaque carte redevient visible et reste à l'intérieur
    de la carte (il était tronqué par la page de destination et par le bas de
    la carte) ;
  * la flèche « lien du RCS vers landing page » repasse sous les cartes (elle
    traversait le bouton de la 2e carte) ;
  * le titre « Des campagnes immersives et personnalisées » est ramené à la
    largeur de l'original (il touchait le bord du panneau de droite).

Le reste de la page (titres, puces, pictos, panneau « Modération &
Enrichissement », fiche acheteur, page de destination) est laissé intact : les
flux de contenu concernés ne sont pas touchés.
"""
import os

import pymupdf

ICI = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ICI, "assets")
SRC = os.path.join(ICI, "..", "Plaquette HelloLead - Assurance V2 (1).pdf")

# Repère des flux ajoutés par la V2 : ils sont dessinés comme si la page
# mesurait 817.92 pt de haut (et non 810) -> y_flux = 817.92 - y_page.
YC = 817.92

# Géométrie des cartes d'origine (points, origine en haut à gauche).
CARTE_1 = pymupdf.Rect(516.86, 140.58, 765.11, 439.82)
CARTE_2 = pymupdf.Rect(520.65, 441.18, 761.40, 740.42)   # même hauteur que la carte 1
CARTE_2_ORIG_BAS = 748.68                                # bas de l'ancienne carte 2

PANEL = (0.95686277, 0.9607843, 0.9843137)               # fond du panneau central
MARGE_ANTICRENELAGE = 1.5                                # recouvre les bords de l'ancien visuel

TITRE_TZ = 0.93771                                       # (1014.0 - 512.7) / (1047.3 - 512.7)


def _image(doc, chemin):
    """Ajoute un PNG comme XObject image et renvoie son xref."""
    pix = pymupdf.Pixmap(chemin)
    if pix.n != 3:
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    xref = doc.get_new_xref()
    doc.update_object(
        xref,
        "<</Type/XObject/Subtype/Image/Width %d/Height %d/ColorSpace/DeviceRGB"
        "/BitsPerComponent 8/Filter/FlateDecode/Interpolate true>>"
        % (pix.width, pix.height),
    )
    doc.update_stream(xref, pix.samples, compress=True)
    return xref


def _dessiner_image(rect, nom):
    return "q %.5f 0 0 %.5f %.5f %.5f cm /%s Do Q" % (
        rect.width, rect.height, rect.x0, YC - rect.y1, nom)


def _aplat(rect, couleur):
    return "q %.4f %.4f %.4f rg %.3f %.3f %.3f %.3f re f Q" % (
        couleur[0], couleur[1], couleur[2], rect.x0, YC - rect.y1,
        rect.width, rect.height)


def corriger_page3(doc):
    page = doc[2]
    flux = page.get_contents()
    assert len(flux) > 20, "structure de page inattendue"
    contenu = {x: doc.xref_stream(x).decode("latin-1") for x in flux}

    for nom, fichier in (("fzCarteA", "carte1.png"), ("fzCarteB", "carte2.png")):
        xref = _image(doc, os.path.join(ASSETS, fichier))
        doc.xref_set_key(page.xref, "Resources/XObject/" + nom, "%d 0 R" % xref)

    fond_1 = CARTE_1 + (-MARGE_ANTICRENELAGE, -MARGE_ANTICRENELAGE,
                        MARGE_ANTICRENELAGE, MARGE_ANTICRENELAGE)
    fond_2 = pymupdf.Rect(CARTE_2.x0 - MARGE_ANTICRENELAGE,
                          CARTE_2.y0 - MARGE_ANTICRENELAGE,
                          CARTE_2.x1 + MARGE_ANTICRENELAGE,
                          CARTE_2_ORIG_BAS + MARGE_ANTICRENELAGE)

    for x, s in contenu.items():
        t = " ".join(s.split())   # les flux d'origine sont écrits sur plusieurs lignes
        if t.startswith("q 529.6 404.41999 225.9 255.5 re h 1 1 1 rg f Q"):
            # fond de la carte 1 : on y place la flèche (sous les cartes) puis le fond
            doc.update_stream(x, (
                "q 143.24465 0 0 143.24465 738.16836 77.82623 cm /fzImg3 Do Q\n"
                + _aplat(fond_1, PANEL)).encode("latin-1"))
        elif t.startswith("q 520.5 69.21997 240.9 307.5 re h 1 1 1 rg f Q"):
            # fond de la carte 2, qui efface aussi le manteau résiduel
            doc.update_stream(x, _aplat(fond_2, PANEL).encode("latin-1"))
        elif "225.95041 0 0 255.49776 529.6238 404.41999 cm" in s:
            doc.update_stream(x, _dessiner_image(CARTE_1, "fzCarteA").encode("latin-1"))
        elif "240.8094 0 0 307.4951 520.5434 69.21997 cm" in s:
            doc.update_stream(x, _dessiner_image(CARTE_2, "fzCarteB").encode("latin-1"))
        elif "fzImg3 Do" in t:
            # la flèche est redessinée avec le fond de la carte 1
            doc.update_stream(x, b"q Q")
        elif (t.startswith("q 529.6 608.02 m")                 # cadre carte 1
              or t.startswith("q 529.6 404.41999 225.9 255.5 re h .82")   # bord carte 1
              or t.startswith("q 520.5 325.71998 m")           # cadre carte 2
              or t.startswith("q 520.5 69.21997 240.9 307.5 re h .82")):  # bord carte 2
            # les cadres et bordures sont désormais dessinés dans les visuels
            doc.update_stream(x, b"q Q")
        elif t.startswith("q\nBT\n1 0 0 1 512.7 709.42 Tm") or (
                "1 0 0 1 512.7 709.42 Tm" in s and "campagnes" not in s
                and len(s) < 600 and "/OS 25 Tf" in s):
            # titre « Des campagnes immersives et personnalisées » : largeur d'origine
            doc.update_stream(x, s.replace(
                "q\nBT\n",
                "q\n%.5f 0 0 1 %.4f 0 cm\nBT\n" % (TITRE_TZ, 512.7 * (1 - TITRE_TZ))
            ).encode("latin-1"))


def main():
    doc = pymupdf.open(SRC)
    corriger_page3(doc)
    sortie = os.path.join(ICI, "..", "Plaquette HelloLead - Assurance V3.pdf")
    doc.save(sortie, garbage=0, deflate=True)
    doc.close()
    print("écrit :", os.path.normpath(sortie))


if __name__ == "__main__":
    main()
