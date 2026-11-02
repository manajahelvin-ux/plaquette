# -*- coding: utf-8 -*-
"""PPTX modifiable de la plaquette complète (9 diapositives).

Fond = chaque page rendue sans ses blocs « Modération & Enrichissement » et « fiche acheteur »
(visuels inclus). Ces blocs sont repris en zones de texte éditables, une par ligne, à partir du PDF final.
Pages 1, 2, 8, 9 : image pleine page (texte non éditable, inchangé).
"""
import io
import os
import sys

import pymupdf
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Emu, Pt

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.join(ICI, "..")
PDF = os.path.join(RACINE, "Plaquette HelloLead - Energie - Finale (9 pages).pdf")
PPTX = os.path.join(RACINE, "Plaquette HelloLead - Energie - Finale (9 pages).pptx")
PT = 12700

# zones éditables (page index → rect), au-dessus des titres (inchangés)
ZONES = {
    2: pymupdf.Rect(1090, 244, 1410, 800),
    3: pymupdf.Rect(1000, 448, 1340, 790),
    4: pymupdf.Rect(1085, 268, 1395, 790),
    5: pymupdf.Rect(1075, 337, 1395, 800),
    6: pymupdf.Rect(1075, 290, 1395, 800),
}


def _lignes(page, zone):
    out = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            ox, oy = l["spans"][0]["origin"]
            if zone.contains(pymupdf.Point(ox, oy)):
                spans = []
                for s in l["spans"]:
                    if s["text"]:
                        spans.append((s["text"], s["font"], s["size"], s["color"]))
                out.append((oy, ox, spans))
    return sorted(out, key=lambda t: (round(t[0], 1), t[1]))


def _police(nom):
    return "DejaVu Sans" if "DejaVu" in nom else "Poppins"


def _gras(nom):
    return "Bold" in nom


def _couleur(c):
    return RGBColor((c >> 16) & 255, (c >> 8) & 255, c & 255)


def construire():
    doc = pymupdf.open(PDF)
    prs = Presentation()
    prs.slide_width = Emu(int(1440 * PT))
    prs.slide_height = Emu(int(810 * PT))
    for i in range(doc.page_count):
        page = doc[i]
        lignes = _lignes(page, ZONES[i]) if i in ZONES else []
        # fond : copie de la page sans les blocs éditables
        fond = pymupdf.open()
        fond.insert_pdf(doc, from_page=i, to_page=i)
        if i in ZONES:
            fond[0].add_redact_annot(ZONES[i])
            fond[0].apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                                     graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
        pix = fond[0].get_pixmap(dpi=150)
        fond.close()
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        slide.shapes.add_picture(io.BytesIO(pix.tobytes("jpg", jpg_quality=92)), 0, 0,
                                 prs.slide_width, prs.slide_height)
        for oy, ox, spans in lignes:
            taille = spans[0][2]
            tb = slide.shapes.add_textbox(Emu(int(ox * PT)), Emu(int((oy - 1.05 * taille) * PT)),
                                          Emu(int(330 * PT)), Emu(int(taille * 1.6 * PT)))
            tf = tb.text_frame
            tf.word_wrap = False
            for att in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
                setattr(tf, att, 0)
            p = tf.paragraphs[0]
            for texte, nom, tailleS, couleur in spans:
                r = p.add_run()
                r.text = texte
                r.font.name = _police(nom)
                r.font.size = Pt(tailleS)
                r.font.bold = _gras(nom)
                r.font.color.rgb = _couleur(couleur)
        print("diapositive %d : %d ligne(s) éditables" % (i + 1, len(lignes)))
    doc.close()
    prs.save(PPTX)
    print("écrit :", os.path.normpath(PPTX))


if __name__ == "__main__":
    construire()
