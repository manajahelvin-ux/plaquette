# -*- coding: utf-8 -*-
"""Aligne la diapositive 3 du PPTX sur la page 3 corrigée (V3).

Le PPTX « modifiable » a un visuel figé par diapositive (180 dpi) plus une zone
de texte par ligne pour le bloc « Modération & Enrichissement » et la fiche
acheteur. Pour la diapositive 3, ce visuel et ces textes étaient restés ceux de
la V1 (cartes « mutuelle » et fiche ATELIER DUVERGER).

Le script :
  * régénère le visuel de fond à partir de la page 3 du PDF V3, textes du
    panneau de droite masqués (ils restent éditables) ;
  * réécrit les zones de texte du panneau avec le contenu « prévoyance / kiné »
    de la V2, aux mêmes positions que dans le PDF.
"""
import io
import os
import re
import shutil
import zipfile

import pymupdf
from lxml import etree
from PIL import Image

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(os.path.join(ICI, ".."))
PDF_V3 = os.path.join(RACINE, "Plaquette HelloLead - Assurance V3.pdf")
PPTX = os.path.join(RACINE, "Plaquette HelloLead - Assurance (modifiable).pptx")
PPTX_SORTIE = os.path.join(ICI, "assets", "Plaquette HelloLead - Assurance (modifiable).pptx")
DIAPO = "ppt/slides/slide3.xml"

NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "p": "http://schemas.openxmlformats.org/presentationml/2006/main"}

BLEU = "0A5BFF"
NOIR = "000000"
ECHELLE_EMU = 12700            # 1 pt


# --------------------------------------------------------------- visuel de fond
def rendre_fond(chemin_png, dpi=180):
    """Rend la page 3 sans les textes du panneau « Modération & Enrichissement »."""
    doc = pymupdf.open(PDF_V3)
    page = doc[2]
    for xref in page.get_contents():
        s = doc.xref_stream(xref).decode("latin-1")
        if "13 Tf" in s:                      # lignes du bloc de modération / fiche
            doc.update_stream(xref, b"q Q")
    pix = page.get_pixmap(dpi=dpi)
    pix.save(chemin_png)
    doc.close()
    print("fond :", pix.width, "x", pix.height)


# ------------------------------------------------------------------ zones de texte
def lignes_panneau():
    """Lignes du panneau de droite (texte + graisse) telles qu'elles sont dans le PDF."""
    doc = pymupdf.open(PDF_V3)
    page = doc[2]
    lignes = {}
    for bloc in page.get_text("dict")["blocks"]:
        for ligne in bloc.get("lines", []):
            for span in ligne["spans"]:
                x0, y0 = span["bbox"][0], round(span["bbox"][1], 1)
                if x0 < 1080 or abs(span["size"] - 12.7) > 0.2:
                    continue                    # hors panneau, ou ancien texte masqué
                if not span["text"].strip():
                    continue
                gras = "Bold" in span["font"]
                lignes.setdefault(y0, []).append((gras, span["text"]))
    doc.close()
    return [(y, lignes[y]) for y in sorted(lignes)]


def construire_formes(lignes):
    """Une zone de texte par ligne, comme dans le PPTX d'origine."""
    modeles = []
    for i, (y, runs) in enumerate(lignes):
        paragraphes = []
        precedent = ""
        for gras, texte in runs:
            if precedent and not precedent.endswith(" ") and not texte.startswith(" "):
                texte = " " + texte          # le PDF sépare libellé et valeur par une espace
            precedent = texte
            couleur = BLEU if gras else NOIR
            paragraphes.append(
                '<a:r><a:rPr sz="1250" b="%d"><a:solidFill><a:srgbClr val="%s"/>'
                '</a:solidFill><a:latin typeface="Poppins"/></a:rPr><a:t>%s</a:t></a:r>'
                % (1 if gras else 0, couleur, _echapper(texte)))
        modeles.append(
            '<p:sp><p:nvSpPr><p:cNvPr id="%d" name="TextBox %d"/><p:cNvSpPr txBox="1"/>'
            '<p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="%d" y="%d"/>'
            '<a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/>'
            '</a:prstGeom><a:noFill/></p:spPr><p:txBody><a:bodyPr wrap="none" anchor="t" '
            'lIns="0" rIns="0" tIns="0" bIns="0"><a:noAutofit/></a:bodyPr><a:lstStyle/>'
            '<a:p>%s</a:p></p:txBody></p:sp>'
            % (3 + i, 2 + i,
               round(1098.9 * ECHELLE_EMU), round((y - 3.12) * ECHELLE_EMU),
               round(400 * ECHELLE_EMU), round(19.5 * ECHELLE_EMU),
               "".join(paragraphes)))
    return modeles


def _echapper(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# ------------------------------------------------------------------------- main
def main():
    os.makedirs(os.path.join(ICI, "assets"), exist_ok=True)
    fond = os.path.join(ICI, "assets", "diapo3_fond.png")
    rendre_fond(fond)

    # largeur du corps de diapositive pour la taille de police voulue
    lignes = lignes_panneau()
    print("%d lignes de texte dans le panneau" % len(lignes))

    with zipfile.ZipFile(PPTX) as zin:
        xml = zin.read(DIAPO).decode("utf-8")

    # on retire les zones de texte existantes, on garde l'image de fond
    xml = re.sub(r"<p:sp>.*?</p:sp>", "", xml, flags=re.S)
    xml = xml.replace("</p:spTree>", "".join(construire_formes(lignes)) + "</p:spTree>")
    xml = re.sub(r"\n\s*\n", "\n", xml)

    with zipfile.ZipFile(PPTX) as zin, zipfile.ZipFile(PPTX_SORTIE, "w",
                                                     zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == DIAPO:
                data = xml.encode("utf-8")
            elif item.filename == "ppt/media/image3.png":
                data = open(fond, "rb").read()
            zout.writestr(item, data)
    print("écrit :", PPTX_SORTIE)


if __name__ == "__main__":
    main()
