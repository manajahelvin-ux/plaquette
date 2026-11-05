# -*- coding: utf-8 -*-
"""Corrige le titre de la page 4 de la plaquette « Fournisseurs d'énergies ».

Le titre d'origine, hérité de la version Assurance, parlait de « ré-assurance »
(terme d'assurance) alors que la page présente une page de destination dont le
formulaire capte le lead. Il devient « LP : Visuels et messages de capture ».

La police est le sous-ensemble OpenSans-Regular embarqué dans la V3 (le seul
disponible : il couvre tous les caractères du nouveau titre). Le script est
idempotent : relancé sur un PDF déjà corrigé, il ne fait rien.
"""
import os

import pymupdf

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(RACINE, "Plaquette HelloLead - Energie - Finale (9 pages).pdf")
V3 = os.path.join(RACINE, "Plaquette HelloLead - Assurance V3.pdf")
POLICE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets",
                      "OpenSans-Regular-P4.ttf")

ANCIEN = "LP : Visuels et messages de ré-assurance"
NOUVEAU = "LP : Visuels et messages de capture"
XREF_OPENSANS = 233          # sous-ensemble OpenSans-Regular de la V3


def police():
    """Extrait (une fois) le sous-ensemble OpenSans de la V3."""
    if not os.path.exists(POLICE):
        os.makedirs(os.path.dirname(POLICE), exist_ok=True)
        src = pymupdf.open(V3)
        with open(POLICE, "wb") as fh:
            fh.write(src.extract_font(XREF_OPENSANS)[3])
        src.close()
    return POLICE


def main():
    doc = pymupdf.open(PDF)
    page = doc[3]

    cible = None
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if s["text"].strip() == ANCIEN:
                    cible = s
    if cible is None:
        print("titre déjà corrigé — rien à faire")
        return

    origine = tuple(cible["origin"])
    corps = cible["size"]
    c = cible["color"]
    couleur = (((c >> 16) & 255) / 255, ((c >> 8) & 255) / 255, (c & 255) / 255)

    # le texte est retiré du flux (pas seulement recouvert)
    page.add_redact_annot(pymupdf.Rect(cible["bbox"]).__add__((-1, -2, 1, 2)))
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                          graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                          text=pymupdf.PDF_REDACT_TEXT_REMOVE)

    page.insert_font(fontname="osr4", fontfile=police())
    page.insert_text(origine, NOUVEAU, fontname="osr4", fontsize=corps, color=couleur)

    tmp = PDF + ".tmp"
    doc.save(tmp, garbage=0, deflate=True)
    doc.close()
    os.replace(tmp, PDF)
    print("titre de la page 4 : %r → %r" % (ANCIEN, NOUVEAU))


if __name__ == "__main__":
    main()
