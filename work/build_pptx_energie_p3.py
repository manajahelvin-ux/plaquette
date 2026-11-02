# -*- coding: utf-8 -*-
"""PPTX modifiable de la page 3 « Fournisseurs d'énergies ».

Fond = page 3 rendue sans texte modifiable (visuels inclus) ; blocs
« Modération & Enrichissement » et fiche acheteur = zones de texte, une par ligne,
posées sur les lignes de base d'origine (13 pt, pas 19,5 pt).
Police : Poppins (à installer pour un rendu identique au PDF).
"""
import os
import sys

from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import build_energie_p3 as B  # noqa: E402

PT = 12700  # EMU par point
SORTIE = os.path.join(ICI, "..", "Plaquette HelloLead - Energie - Page 3 (validation).pptx")


def _zone(slide, x, baseline, runs):
    # ascent approximatif de Poppins (≈ 1,05 em) pour placer la ligne de base
    top = baseline - 1.05 * B.FS
    tb = slide.shapes.add_textbox(Emu(int(x * PT)), Emu(int(top * PT)),
                                  Emu(int(300 * PT)), Emu(int(B.FS * 1.6 * PT)))
    tf = tb.text_frame
    tf.word_wrap = False
    for attr in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, attr, 0)
    p = tf.paragraphs[0]
    for texte, style in runs:
        if not texte:
            continue
        r = p.add_run()
        r.text = texte
        f = r.font
        f.name = "Poppins"
        f.size = Pt(B.FS)
        f.bold = style == "B"
        f.color.rgb = RGBColor(10, 91, 255) if style == "B" else RGBColor(0, 0, 0)


def construire():
    lignes_mod = B._runs_modération()
    lignes_fiche = B._lignes_fiche()
    prs = Presentation()
    prs.slide_width = Emu(int(1440 * PT))
    prs.slide_height = Emu(int(810 * PT))
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.shapes.add_picture(os.path.join(B.ASSETS, "page3_fond.png"), 0, 0,
                             prs.slide_width, prs.slide_height)
    for i, runs in enumerate(lignes_mod):
        _zone(slide, B.X_TXT, B.BASE_MOD + i * B.LH, runs)
    for i, runs in enumerate(lignes_fiche):
        _zone(slide, B.X_TXT, B.BASE_FICHE + i * B.LH, runs)
    prs.save(SORTIE)
    print("écrit :", os.path.normpath(SORTIE))


if __name__ == "__main__":
    construire()
