"""Construit la plaquette PowerPoint modifiable à partir du PDF final.

Principe (identique à la version Assurance) :
  * les pages 3, 5, 6 et 7 sont reprises en image de fond **sans leur texte**
    (fond_sans_texte.pdf, rendu 180 dpi) ;
  * chaque ligne du panneau « Modération & Enrichissement » et de la fiche
    acheteur est ajoutée en zone de texte éditable, calée sur la position
    exacte du PDF (x du span, y = haut de boîte du span − 3,12 pt) ;
  * les autres pages (1, 2, 4, 8, 9), strictement identiques, sont conservées
    telles quelles depuis le fichier PowerPoint d'origine.
"""
import io
import os
import shutil

import pymupdf
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PDF = os.path.join(RACINE, "Plaquette HelloLead - Panneaux solaires.pdf")
FOND = os.path.join(RACINE, "work", "solaire", "fond_sans_texte.pdf")
MODELE = os.path.join(RACINE, "Plaquette HelloLead - Assurance (modifiable).pptx")
SORTIE = os.path.join(RACINE, "Plaquette HelloLead - Panneaux solaires (modifiable).pptx")

PAGES = (3, 5, 6, 7)
BLEU = RGBColor(0x0A, 0x5B, 0xFF)
NOIR = RGBColor(0, 0, 0)
MARGE_HAUT = 3.12          # décalage constaté entre haut de span et haut de boîte
EMU = 12700                # 1 pt


def lignes_panneau(page):
    """(x, y_baseline, texte, gras) des lignes du panneau, dans l'ordre du flux."""
    out = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if s["bbox"][0] < 1080 or not s["text"].strip():
                    continue
                gras = "Bold" in s["font"] or "Semibold" in s["font"]
                out.append((s["origin"][0], s["bbox"][1], s["text"], gras))
    return out


def vider(slide):
    for sh in list(slide.shapes):
        sh._element.getparent().remove(sh._element)


def main():
    doc = pymupdf.open(PDF)
    fond = pymupdf.open(FOND)
    prs = Presentation(MODELE)
    largeur, hauteur = prs.slide_width, prs.slide_height

    for n in PAGES:
        slide = prs.slides[n - 1]
        vider(slide)

        pix = fond[n - 1].get_pixmap(dpi=180)
        img = io.BytesIO(pix.tobytes("png"))
        pic = slide.shapes.add_picture(img, 0, 0, width=largeur, height=hauteur)
        pic.name = "fond_p%d" % n

        for i, (x, haut, texte, gras) in enumerate(lignes_panneau(doc[n - 1])):
            tb = slide.shapes.add_textbox(Emu(int(x * EMU)),
                                          Emu(int((haut - MARGE_HAUT) * EMU)),
                                          Emu(400 * EMU), Emu(19.5 * EMU))
            tb.name = "txt_%d_%d" % (n, i)
            tf = tb.text_frame
            tf.word_wrap = False
            tf.margin_left = tf.margin_right = 0
            tf.margin_top = tf.margin_bottom = 0
            tf.vertical_anchor = MSO_ANCHOR.TOP
            p = tf.paragraphs[0]
            run = p.add_run()
            run.text = texte
            run.font.size = Pt(12.5)
            run.font.bold = gras
            run.font.name = "Poppins"
            run.font.color.rgb = BLEU if gras else NOIR
        print("page %d : %d zones de texte" % (n, len(lignes_panneau(doc[n - 1]))))

    prs.save(SORTIE)
    print("écrit :", SORTIE)


if __name__ == "__main__":
    main()
