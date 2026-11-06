# -*- coding: utf-8 -*-
"""Assemble la plaquette « Panneaux solaires » à partir du PDF d'origine.

Pages 3, 5, 6 et 7 : seuls les quatre blocs autorisés changent (visuel,
formulaire / page de destination, bloc « Modération & Enrichissement », fiche
acheteur). Titres, sous-titres, puces, pictos, flèches, marques et cartes de
fond ne sont pas touchés : les flux de contenu correspondants restent intacts,
les retouches de visuels se limitent aux zones de texte et aux photos.

Sortie : Plaquette HelloLead - Panneaux solaires.pdf (racine du dépôt).
"""
import io
import json
import os

import pymupdf
from PIL import Image, ImageDraw

import contenus as C
from visuels import GRAS, REG, PHOTOS, Region, Visuel, taille_police

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(os.path.join(ICI, "..", ".."))
SRC = os.path.join(RACINE, "Plaquette HelloLead - Assurance.pdf")
SORTIE = os.path.join(RACINE, "Plaquette HelloLead - Panneaux solaires.pdf")
SORTIE_FOND = os.path.join(RACINE, "work", "solaire", "fond_sans_texte.pdf")
SANS_TEXTE = os.environ.get("FOND") == "1"
ASSETS = os.path.join(ICI, "assets")

BLEU = (10, 91, 255)
NOIR = (17, 17, 17)


def _c(couleur):
    return tuple(v / 255.0 for v in couleur)
GRIS = (133, 133, 138)
PANEL = (244 / 255, 245 / 255, 252 / 255)
MASQUE = (0.6353, 0.6235, 0.6235)

CARTE_1 = pymupdf.Rect(516.86, 140.58, 765.11, 439.82)
# La carte 2 d'origine est découpée par le PDF : on ne pose que la partie visible.
CARTE_2 = pymupdf.Rect(520.65, 449.81, 761.40, 740.06)
LANDING = pymupdf.Rect(755.11, 150.61, 1041.61, 617.86)

# Les visuels de la colonne centrale sont recouverts par la page de destination
# (page 3) : on ne pose donc les cartes que jusqu'à son bord gauche.
CLIP_X = 758.58   # découpe d'origine de la carte 1


# --------------------------------------------------------------------- outils
def poser_png(page, chemin, rect, clip_x=None):
    """Pose un PNG (carte RCS) sur `rect`, éventuellement rogné à `clip_x`."""
    im = Image.open(chemin).convert("RGB")
    ech = rect.width / im.width
    if clip_x is not None and clip_x < rect.x1:
        garde = round((clip_x - rect.x0) / ech)
        im = im.crop((0, 0, garde, im.height))
        rect = pymupdf.Rect(rect.x0, rect.y0, clip_x, rect.y1)
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    page.insert_image(rect, stream=buf.getvalue(), keep_proportion=False)


LIGNES_PANNEAU = []


def panneau_lateral(page, pno, ecrire=True):
    """Réécrit le bloc « Modération & Enrichissement » et la fiche acheteur.

    Les lignes sont posées sur les lignes de base d'origine : même rythme, même
    encombrement, même style (étiquettes bleu gras / valeurs noires).
    """
    spans = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if s["bbox"][0] > 1080 and 12.5 < s["size"] < 13.5:
                    spans.append(s)
    lignes = C.PANNEAUX[pno]
    attendu = len(lignes["mod"]) + len(lignes["fiche"])
    assert len(spans) == attendu, "page %d : %d lignes au lieu de %d" % (
        pno, len(spans), attendu)

    cadre = [dr["rect"] for dr in page.get_drawings()
             if dr.get("fill") and abs(dr["fill"][0] - 0.9569) < 0.005
             and dr["rect"].x0 > 1050][0]

    x0 = min(s["bbox"][0] for s in spans) - 4
    x1 = cadre.x1 - 10
    y0 = spans[0]["bbox"][1] - 4
    y1 = spans[-1]["bbox"][3] + 4
    # l'ancien texte est retiré du flux (pas seulement masqué) : il ne doit pas
    # réapparaître au copier-coller ni à l'extraction
    page.add_redact_annot(pymupdf.Rect(x0, y0, x1, y1))
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                          graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                          text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    page.draw_rect(pymupdf.Rect(x0, y0, x1, y1), color=None, fill=PANEL)

    page.insert_font(fontname="popR", fontfile=REG)
    page.insert_font(fontname="popB", fontfile=GRAS)

    textes = list(lignes["mod"]) + [(t, False) for t in lignes["fiche"]]
    f_r = pymupdf.Font(fontfile=REG)
    f_b = pymupdf.Font(fontfile=GRAS)
    limite = x1 - spans[0]["origin"][0]
    for texte, gras in textes:
        largeur = (f_b if gras else f_r).text_length(texte, 13.0)
        assert largeur <= limite, "page %d : ligne trop large (%.1f > %.1f) %r" % (
            pno, largeur, limite, texte)
    for (texte, gras), s in zip(textes, spans):
        if ecrire:
            page.insert_text((s["origin"][0], s["origin"][1]), texte,
                             fontname="popB" if gras else "popR", fontsize=13.0,
                             color=_c(BLEU) if gras else (0, 0, 0))
        LIGNES_PANNEAU.append(dict(page=pno, x=round(s["origin"][0], 2),
                                   haut=round(s["bbox"][1], 2), texte=texte,
                                   gras=bool(gras), taille=13.0))

    # masques gris de la fiche (Contact / Tél / Mail)
    for dr in page.get_drawings():
        f = dr.get("fill")
        r = dr["rect"]
        if not f or abs(f[0] - MASQUE[0]) > 0.01:
            continue
        if r.x0 < 1080 or r.y1 < y0 or r.y0 > y1:
            continue
        page.draw_rect(r, color=None, fill=MASQUE)
    return len(spans)


def largeur_max(page):
    spans = [s for b in page.get_text("dict")["blocks"] for l in b.get("lines", [])
             for s in l["spans"] if s["bbox"][0] > 1080 and 12.5 < s["size"] < 13.5]
    return max(s["bbox"][2] for s in spans)


# ------------------------------------------------------------------- page 3
def page3(doc):
    page = doc[2]
    poser_png(page, os.path.join(ASSETS, "carte1.png"), CARTE_1, clip_x=CLIP_X)
    poser_png(page, os.path.join(ASSETS, "carte2.png"), CARTE_2)

    v = Visuel(doc, page, 52, LANDING, "landing")
    ech = v.ech_x
    # --- titre : 2 lignes bleues + 2 lignes noires, centré sur la carte blanche
    cx = 280
    v.effacer_box((96, 146, 478, 322))
    t1 = taille_police("Trouvez le meilleur", GRAS, 227 * (0.5306 / ech))
    for texte, couleur, base in zip(C.P3_LANDING["titre"],
                                    (BLEU, BLEU, NOIR, NOIR),
                                    (186, 224, 263, 301)):
        v.texte((cx, base), texte, GRAS, t1, couleur, ancre="ms")

    # --- intro
    v.effacer_box((104, 340, 470, 424))
    t2 = taille_police("Comparez les offres de", REG, 204 * (0.5306 / ech))
    for texte, base in zip(C.P3_LANDING["intro"], (364, 389, 414)):
        v.texte((112, base), texte, REG, t2, NOIR)

    # --- question + choix
    v.effacer_box((104, 498, 470, 552))
    t3 = taille_police("Concernant votre situation,", REG, 256 * (0.5306 / ech))
    for texte, base in zip(C.P3_LANDING["question"], (518, 543)):
        v.texte((112, base), texte, REG, t3, NOIR)
    from PIL import ImageDraw
    for y_haut, y_bas, texte, base in ((564, 603, C.P3_LANDING["choix"][0], 588),
                                       (636, 675, C.P3_LANDING["choix"][1], 660)):
        v.effacer_box((115, y_haut, 464, y_bas))
        centre = (y_haut + y_bas) // 2
        v.d.ellipse([122, centre - 8, 138, centre + 8], outline=(152, 156, 161), width=2)
        v.texte((144, base), texte, REG, t3, NOIR)
    v.poser()
    v.enregistrer(os.path.join(ASSETS, "apercu_landing.png"))

    panneau_lateral(page, 3, ecrire=not SANS_TEXTE)
    return page


# ---------------------------------------------------------------------- main
def main():
    doc = pymupdf.open(SRC)
    page3(doc)
    page4(doc, ecrire=not SANS_TEXTE)
    page5(doc)
    page6(doc)
    page7(doc)
    doc.save(SORTIE_FOND if SANS_TEXTE else SORTIE, garbage=0, deflate=True)
    doc.close()
    if not SANS_TEXTE:
        import json
        with open(os.path.join(ASSETS, "lignes_panneau.json"), "w") as fh:
            json.dump(LIGNES_PANNEAU, fh, ensure_ascii=False, indent=1)
    print("écrit :", SORTIE_FOND if SANS_TEXTE else SORTIE)




# ------------------------------------------------------------------- page 5
DJ = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DJB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def page5(doc):
    page = doc[4]

    # ---- publication META (image 156, 519 x 707)
    p = Visuel(doc, page, 156, pymupdf.Rect(407.68, 209.44, 722.68, 638.44), "post")
    # avatar
    p.d.ellipse([25, 57, 75, 107], fill=(31, 36, 48))
    p.zone_px((24, 56, 76, 108))
    p.texte((50, 86), C.P5_POSTE["initiales"], DJB, 16, (255, 255, 255), ancre="mm")
    # nom + mention
    p.effacer_box((74, 60, 300, 80))
    p.texte((78, 75), C.P5_POSTE["nom"], DJB, 13, (54, 54, 56))
    p.effacer_box((74, 81, 300, 99))
    p.texte((79, 92), "Sponsorisé", DJ, 11, (140, 140, 142))
    # texte de la publication
    p.effacer_box((24, 112, 505, 158))
    p.texte((30, 128), C.P5_POSTE["ligne1"], DJ, 12, (24, 25, 28))
    p.texte((30, 150), C.P5_POSTE["ligne2"], DJ, 12, (24, 25, 28))
    # visuel
    r = p.rect
    p.photo(os.path.join(PHOTOS, "installateurs.jpg"),
            r.x0 + 21 * p.ech_x, r.y0 + 165 * p.ech_y,
            r.x0 + 497 * p.ech_x, r.y0 + 637 * p.ech_y, cadrage=0.5)
    p.poser()
    p.enregistrer(os.path.join(ASSETS, "apercu_post.png"))

    # ---- formulaire instantané (image 155, 393 x 526)
    f = Visuel(doc, page, 155, pymupdf.Rect(710.48, 172.41, 1058.48, 638.16), "form")
    from PIL import Image as _Im
    masque = _Im.new("L", f.img.size, 0)
    _md = ImageDraw.Draw(masque)
    _md.ellipse([164, 16, 224, 76], fill=255)
    _md.rectangle([0, 0, f.img.width, 42], fill=0)      # zone découpée par le PDF
    f.img = _Im.composite(_Im.new("RGB", f.img.size, (31, 36, 48)), f.img, masque)
    f.d = ImageDraw.Draw(f.img)
    f.zone_px((160, 42, 228, 90))
    f.texte((194, 61), "Solaris", DJB, 9, (255, 255, 255), ancre="ms")
    f.effacer_box((120, 86, 280, 103))
    f.texte((196, 99), C.P5_FORMULAIRE["marque"], DJ, 13, (127, 127, 131), ancre="ms")
    f.effacer_box((44, 118, 352, 146))
    t = taille_police(C.P5_FORMULAIRE["titre"], DJB, 296)
    print("    titre formulaire : %d px" % t)
    f.texte((196, 140), C.P5_FORMULAIRE["titre"], DJB, t, (17, 17, 17), ancre="ms")
    f.effacer_box((44, 147, 352, 169))
    t2 = taille_police(C.P5_FORMULAIRE["sous_titre"], DJ, 296)
    print("    sous-titre formulaire : %d px" % t2)
    f.texte((196, 161), C.P5_FORMULAIRE["sous_titre"], DJ, t2, (48, 48, 52), ancre="ms")
    for texte, (x0, y0, x1, base) in zip(
            C.P5_FORMULAIRE["champs"],
            ((50, 234, 350, 249), (50, 337, 350, 352), (50, 442, 350, 456))):
        f.effacer_box((x0, y0, x1, base + 2))
        f.texte((65, base), texte, DJB, 14, (17, 17, 17))
    f.poser()
    f.enregistrer(os.path.join(ASSETS, "apercu_form.png"))

    panneau_lateral(page, 5, ecrire=not SANS_TEXTE)
    return page


# ------------------------------------------------------------------- page 6
def _ligne(v, box, runs, base, bg=None, point=None, x=None):
    """Efface une zone (pixels image) et y réécrit une suite de fragments."""
    v.effacer_ip(box[0], box[1], box[2], box[3], couleur=bg, point=point)
    curseur = box[0] + (x or 0)
    for texte, gras, taille, couleur in runs:
        chemin = DJB if gras else DJ
        v.texte_ip(curseur, base, texte, chemin, taille, couleur)
        curseur += v.largeur_ip(texte, chemin, taille)


def _radio(v, cx, cy, selected):
    """Redessine un bouton radio de la modale CRM (coordonnées image native)."""
    a = v.ipx(cx, cy)
    r = 5.2 * v.f_ip
    v.d.rectangle([a[0] - r - 3, a[1] - r - 3, a[0] + r + 3, a[1] + r + 3],
                  fill=(255, 255, 255))
    v.d.ellipse([a[0] - r, a[1] - r, a[0] + r, a[1] + r],
                outline=(125, 125, 128), width=max(1, round(1.1 * v.f_ip)))
    if selected:
        rr = 2.6 * v.f_ip
        v.d.ellipse([a[0] - rr, a[1] - rr, a[0] + rr, a[1] + rr], fill=(35, 35, 38))


def page6(doc):
    page = doc[5]
    v = Region(doc, page, (410.75, 163.51, 1028.5, 517.89), densite=2.2208, nom="crm")
    v.regler((410.75, 163.51, 1046.09, 517.89), 1411, 786)
    BLANC = (255, 255, 255)
    T = (35, 35, 38)         # texte courant
    ROUGE = (194, 39, 17)    # titre de la fiche
    GRIS = (70, 70, 72)
    SOMME = (45, 45, 45)     # panneau de gauche (déjà assombri par la modale)

    # ---- bandeau de campagne
    _ligne(v, (440, 50, 700, 74), [("Campagne : ", False, 11, T),
                                   (C.P6_CRM["campagne"], False, 11, T)], 69, bg=None,
           point=(660, 50))
    # ---- modale
    _ligne(v, (562, 88, 1000, 106),
           [(C.P6_CRM["titre_modale"], True, 12, ROUGE)], 102, BLANC)
    _ligne(v, (562, 132, 1005, 149),
           [(C.P6_CRM["q1"], False, 11, T)], 145, BLANC)
    _ligne(v, (632, 196, 900, 211),
           [(C.P6_CRM["q2"], True, 11, T)], 208, BLANC)
    _ligne(v, (653, 232, 900, 248),
           [("Panneaux photovoltaïques", False, 11, T)], 244, BLANC, x=2)
    _ligne(v, (653, 252, 900, 266),
           [("Solutions solaires EDF", False, 11, T)], 263, BLANC, x=2)
    _ligne(v, (562, 314, 930, 330),
           [(C.P6_CRM["q3"], True, 11, T),
            (" [Obligatoire]", False, 11, GRIS)], 326, BLANC)
    _ligne(v, (562, 384, 800, 400),
           [("Type de projet", True, 11, T), (" [Obligatoire]", False, 11, GRIS)],
           396, BLANC)
    for (y0, y1, base, texte) in ((403, 415, 412, "Panneaux photovoltaïques"),
                                  (422, 434, 431, "Ombrières et parkings"),
                                  (441, 456, 452, "Autoconsommation et revente"),
                                  (462, 474, 471, "Chauffe-eau solaire"),
                                  (482, 494, 491, "Bornes de recharge")):
        _ligne(v, (583, y0, 900, y1), [(texte, False, 11, T)], base, BLANC, x=3)
    _ligne(v, (562, 528, 800, 543),
           [("Surface de toiture", True, 11, T), (" [Obligatoire]", False, 11, GRIS)],
           539, BLANC)
    for (y0, y1, base, texte) in ((546, 560, 556, "100 m² à 500 m²"),
                                  (566, 580, 576, "1 000 m² et plus"),
                                  (586, 600, 596, "Moins de 100 m²")):
        _ligne(v, (583, y0, 900, y1), [(texte, False, 11, T)], base, BLANC, x=3)
    _ligne(v, (562, 610, 800, 626),
           [("Êtes-vous propriétaire du bâtiment ?", True, 11, T)], 622, BLANC)
    _ligne(v, (1000, 162, 1290, 181),
           [("\u2611", True, 12, (96, 96, 96)),
            ("  " + C.P6_CRM["matching_valeur"], True, 11, T)],
           176, BLANC, x=22)

    # ---- colonne de gauche (fiche société acheteuse, assombrie par la modale)
    for y0, y1, base in ((214, 228, 225), (241, 255, 252), (268, 282, 279)):
        _ligne(v, (14, y0, 300, y1), [(C.P6_CRM["soe"], False, 10, SOMME)], base,
               bg=None, point=(200, 205))
    _ligne(v, (14, 296, 300, 310), [("74000", False, 10, SOMME)], 306, bg=None,
           point=(200, 205))
    _ligne(v, (14, 322, 300, 336), [("ANNECY", False, 10, SOMME)], 332, bg=None,
           point=(200, 205))
    _ligne(v, (14, 348, 300, 362), [(C.P6_CRM["siret"], False, 10, SOMME)], 359,
           bg=None, point=(200, 345))
    _ligne(v, (14, 402, 340, 417),
           [(C.P6_CRM["naf"], False, 9, SOMME)], 413, bg=None,
           point=(300, 398))
    _ligne(v, (14, 419, 340, 434),
           [(C.P6_CRM["naf2"], False, 9, SOMME)], 430, bg=None,
           point=(300, 398))
    _ligne(v, (14, 436, 334, 450), [(C.P6_CRM["creation"], False, 9, SOMME)], 447,
           bg=None, point=(300, 440))
    _ligne(v, (14, 458, 334, 472), [("Effectif 50 à 99", False, 10, SOMME)], 468,
           bg=None, point=(300, 462))
    for y0, y1, base, texte in ((214, 230, 226, "Madame"), (241, 257, 253, "CLAIRE"),
                                (268, 284, 280, "MOREL")):
        _ligne(v, (370, y0, 540, y1), [(texte, False, 10, SOMME)], base, bg=None,
               point=(540, 205))
    _ligne(v, (370, 322, 552, 340),
           [(C.P6_CRM["mail"], False, 9, SOMME)], 336, bg=None,
           point=(500, 325))
    # ---- historique
    _ligne(v, (16, 584, 340, 598), [(C.P6_CRM["historique"][0], False, 9, SOMME)],
           594, bg=None, point=(300, 580))
    _ligne(v, (16, 604, 340, 616), [(C.P6_CRM["historique"][1], False, 9, SOMME)],
           612, bg=None, point=(300, 600))
    _ligne(v, (16, 622, 340, 634), [(C.P6_CRM["historique"][2], False, 9, SOMME)],
           630, bg=None, point=(300, 640))

    # ---- cohérence des réponses CRM avec le profil acheteur B2B
    _radio(v, 575, 552, False)   # surface : 100 à 500 m² -> non
    _radio(v, 575, 572, True)    # surface : 1 000 m² et plus -> oui
    _radio(v, 575, 636, True)    # propriétaire du bâtiment : Oui
    _radio(v, 575, 655, False)   # propriétaire du bâtiment : Non
    _radio(v, 575, 700, False)   # échéance : sous 3 mois -> non
    _radio(v, 575, 720, True)    # échéance : 3 à 6 mois -> oui

    v.poser()
    v.enregistrer(os.path.join(ASSETS, "apercu_crm.png"))
    panneau_lateral(page, 6, ecrire=not SANS_TEXTE)
    return page


# ------------------------------------------------------------------- page 7
def page7(doc):
    page = doc[6]
    # ---- email 1 (colonne de gauche)
    e1 = Region(doc, page, (439.39, 97.35, 724.37, 791.85), densite=1.1244, nom="email1")
    e1.regler((432.62, 87.97, 724.37, 792.22), 328, 791)
    BLANC = (255, 255, 255)
    T = (34, 34, 34)
    GRIS_C = (150, 150, 155)
    SOMBRE = (58, 58, 60)
    JAUNE = (234, 203, 58)

    e1.effacer_ip(8, 52, 272, 70, BLANC)
    e1.effacer_ip(8, 70, 272, 87, BLANC)
    t = e1.ajuster_ip("Installation de panneaux solaires", DJ, 258, maxi=12)
    e1.texte_ip(11, 68, "Installation de panneaux solaires", DJB, t, T)
    e1.texte_ip(11, 83, "Quel projet choisir ?", DJB, t, T)
    # titre de section
    e1.effacer_ip(60, 292, 275, 310, BLANC)
    t = e1.ajuster_ip("À chaque toiture sa solution", DJ, 200, maxi=12)
    e1.texte_ip(163, 306, "À chaque toiture sa solution", DJ, t, T, ancre="ms")
    # trois blocs
    for (yt, ys, titre, sous) in (
            (331, 342, "L’étude de votre toiture",
             "Un relevé précis de votre toit, pour dimensionner l’installation."),
            (389, 400, "L’autoconsommation",
             "La production solaire consommée sur place, au fil de la journée."),
            (445, 456, "La revente du surplus",
             "Le surplus injecté sur le réseau et valorisé par votre fournisseur.")):
        e1.effacer_ip(66, yt - 10, 278, yt + 3, BLANC)
        e1.effacer_ip(66, ys - 9, 300, ys + 3, BLANC)
        t1 = e1.ajuster_ip(titre, DJB, 200, maxi=11)
        e1.texte_ip(71, yt, titre, DJB, t1, T)
        t2 = e1.ajuster_ip(sous, DJ, 205, maxi=8)
        e1.texte_ip(71, ys, sous, DJ, t2, GRIS_C)
    # accroche du bandeau sombre (deux lignes jaunes d'origine)
    for (box, base, texte) in (
            ((24, 528, 306, 544), 539, "Votre projet solaire chiffré en 1 minute,"),
            ((24, 543, 306, 559), 553, "par des installateurs agréés RGE !")):
        e1.effacer_ip(*box, couleur=SOMBRE)
        t = e1.ajuster_ip(texte, DJ, 270, maxi=8)
        e1.texte_ip(163, base, texte, DJ, t, JAUNE, ancre="ms")
    # sous-titre du bandeau sombre
    e1.effacer_ip(28, 563, 302, 580, SOMBRE)
    t = e1.ajuster_ip("Trouvez l’installateur solaire qui correspond à votre projet",
                      DJ, 250, maxi=9)
    e1.texte_ip(163, 576, "Trouvez l’installateur solaire qui correspond à votre projet",
                DJ, t, (172, 172, 174), ancre="ms")
    # bouton « être rappelé »
    e1.effacer_ip(152, 588, 300, 606, SOMBRE)
    e1.texte_ip(157, 600, "Être rappelé par un installateur", DJ, 6.5, JAUNE)
    # visuel
    e1.photo(os.path.join(PHOTOS, "acheteurs_b2b_email.jpg"), 439.39 + 18 * e1.ech * e1.f_ip,
             87.97 + 92 * e1.ech * e1.f_ip,
             439.39 + 310 * e1.ech * e1.f_ip, 87.97 + 225 * e1.ech * e1.f_ip,
             cadrage=0.30)
    e1.poser()
    e1.enregistrer(os.path.join(ASSETS, "apercu_email1.png"))

    # ---- email 2 (colonne du milieu)
    e2 = Region(doc, page, (743.39, 104.88, 1000.64, 503.88), densite=1.5560, nom="email2")
    e2.regler((743.39, 96.37, 1003.64, 516.37), 405, 652)
    def fond(x0, y0):
        a = e2.ipx(x0, y0)
        return e2.img.getpixel((int(a[0]), int(a[1])))

    # la marque est conservée à l'identique : on la découpe avant de changer la
    # photo de bannière, puis on la repose au même endroit
    a = e2.ipx(0, 33)
    b = e2.ipx(232, 57)
    coin = (int(a[0]), int(a[1]), int(b[0]), int(b[1]))
    bande = e2.img.crop(coin)
    masque = bande.convert("L").point(lambda v: 255 if v > 130 else 0)
    pas = e2.ech * e2.f_ip
    e2.photo(os.path.join(PHOTOS, "toit_crepuscule.jpg"),
             743.39, 96.37 + 19 * pas, 743.39 + 405 * pas, 96.37 + 300 * pas,
             cadrage=0.5)
    e2.img.paste(bande, coin[:2], masque)
    # vignette « € » de la version patrimoine : sans objet ici
    e2.effacer_ip(316, 336, 404, 440, (255, 255, 255))
    # titre sur la bannière (l'ancien texte a disparu avec la photo)
    e2.texte_ip(23, 91, "Valorisez votre toiture", DJB, 13.5, (255, 255, 255))
    e2.texte_ip(23, 109, "avec une installation solaire", DJB, 13.5, (255, 255, 255))
    # corps
    for (box, base, texte) in (
            ((18, 346, 344, 358), 355,
             "Une installation photovoltaïque se dimensionne selon votre consommation,"),
            ((18, 358, 344, 369), 365,
             "l’orientation et l’inclinaison de la toiture."),
            ((18, 374, 344, 392), 387,
             "Un installateur qualifié RGE réalise l’étude, le raccordement et les"),
            ((18, 392, 344, 403), 400, "démarches administratives."),
            ((18, 412, 344, 426), 421,
             "Comparez plusieurs devis : matériel, puissance et durée de garantie"),
            ((18, 426, 344, 437), 432, "varient fortement d’un installateur à l’autre.")):
        e2.effacer_ip(*box, couleur=(255, 255, 255))
        t = e2.ajuster_ip(texte, DJ, 300, maxi=8)
        e2.texte_ip(box[0] + 2, base, texte, DJ, t, T)
    e2.poser()
    e2.enregistrer(os.path.join(ASSETS, "apercu_email2.png"))


    # ---- email 3 (bandeau + deux vignettes + formulaire)
    e3 = Region(doc, page, (743.39, 521.73, 1000.64, 676.98), densite=2.1845, nom="email3")
    e3.regler((743.39, 521.73, 1000.64, 676.98), 562, 339)
    BLANC = (255, 255, 255)
    CLAIR = (222, 226, 235)

    if True:
        for (box, base, texte, taille, graisse, couleur) in (
                ((10, 8, 300, 20), 17,
                 "L’installateur solaire qui correspond à votre projet, c’est par ici !",
                 6, False, CLAIR),
                ((10, 28, 470, 46), 44,
                 "Optimisez votre toiture et préparez votre installation", 11, True, BLANC),
                ((10, 46, 470, 62), 61,
                 "avec un installateur solaire de votre région", 11, True, BLANC),
                ((10, 70, 500, 84), 80,
                 "Vous cherchez à réduire votre facture, produire votre électricité ou revendre votre surplus ? Un installateur",
                 6.5, False, CLAIR),
                ((10, 84, 500, 95), 92,
                 "solaire vous aide à dimensionner l’installation adaptée à votre toiture.",
                 6.5, False, CLAIR),
                ((10, 240, 285, 253), 251,
                 "L’installation photovoltaïque", 7.5, True, BLANC),
                ((10, 253, 285, 264), 261,
                 "Une étude de votre toiture et un dimensionnement adapté à votre consommation.",
                 5.5, False, CLAIR),
                ((288, 240, 555, 253), 251,
                 "L’autoconsommation", 7.5, True, BLANC),
                ((288, 253, 555, 264), 261,
                 "La production solaire consommée sur place, au fil de la journée.",
                 5.5, False, CLAIR)):
            e3.effacer_ip_degrade(*box)
            t = e3.ajuster_ip(texte, DJB if graisse else DJ, box[2] - box[0] - 8,
                              maxi=taille)
            e3.texte_ip(box[0] + 4, base, texte, DJB if graisse else DJ, t, couleur)
        e3.photo(os.path.join(PHOTOS, "installateurs.jpg"), 743.39 + 14 * 0.4572,
                 521.73 + 125 * 0.4572, 743.39 + 280 * 0.4572, 521.73 + 235 * 0.4572,
                 cadrage=0.45)
        e3.photo(os.path.join(PHOTOS, "maison.jpg"), 743.39 + 290 * 0.4572,
                 521.73 + 125 * 0.4572, 743.39 + 545 * 0.4572, 521.73 + 235 * 0.4572,
                 cadrage=0.5)
        e3.poser()
        e3.enregistrer(os.path.join(ASSETS, "apercu_email3.png"))

    # ---- étapes de formulaire (deux vignettes)
    for (xref, rect, W, H, question, options) in (
            (193, (874.36, 696.05, 999.61, 783.8), 240, 169,
             "Quel type d’installation recherchez-vous ?",
             ("PHOTOVOLTAÏQUE", "AUTOCONSOMMATION")),
            (195, (748.11, 695.09, 867.36, 784.34), 240, 179,
             "Quel budget prévoyez-vous ?", None)):
        r = Region(doc, page, rect, densite=1.92, nom="etape%d" % xref)
        r.regler(rect, W, H)
        r.effacer_ip(30, 20, W - 30, 34, (255, 255, 255))
        t = r.ajuster_ip(question, DJB, W - 70, maxi=8)
        r.texte_ip(W // 2, 31, question, DJB, t, (40, 40, 45), ancre="ms")
        if options:
            r.effacer_ip(50, 114, 114, 128, (255, 255, 255))
            r.effacer_ip(130, 114, 196, 128, (255, 255, 255))
            t = r.ajuster_ip(options[0], DJB, 62, maxi=7)
            r.texte_ip(81, 125, options[0], DJB, t, (40, 40, 45), ancre="ms")
            t = r.ajuster_ip(options[1], DJB, 62, maxi=7)
            r.texte_ip(162, 125, options[1], DJB, t, (40, 40, 45), ancre="ms")
        r.poser()
        r.enregistrer(os.path.join(ASSETS, "apercu_etape%d.png" % xref))

    panneau_lateral(page, 7, ecrire=not SANS_TEXTE)
    return page


# ------------------------------------------------------------------- page 4
# DejaVu complet (les fichiers extraits du PDF n'ont plus de table de caractères)
DJ = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DJB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Visuel de la page de destination (page 4) : mêmes 12 lignes, mêmes origines.
P4_LP = [
    "Panneaux solaires",
    "Des offres adaptées",
    "à votre site professionnel",
    "Comparez les offres",
    "pour votre projet solaire",
    "Quels équipements recherchez-vous ?",
    "Panneaux photovoltaïques",
    "Ombrières et parkings",
    "Autoconsommation et revente",
    "Chauffe-eau solaire",
    "Bornes de recharge",
    "Suivant",
]
# Extrait de formulaire : mêmes 11 lignes.
P4_FORM = [
    "Extrait du formulaire",
    "Étape 2 · Préciser la surface de toiture",
    "Quelle est la surface de votre toiture ?",
    "Moins de 100 m²",
    "100 à 250 m²",
    "250 à 500 m²",
    "500 à 1 000 m²",
    "1 000 à 5 000 m²",
    "5 000 à 10 000 m²",
    "10 000 m² et plus",
    "Suivant",
]
# Bande de ré-assurance : les logos d'assureurs sont remplacés par une mention.
P4_BANDE = "Particuliers · Professionnels · Toitures et ombrières"
# Le titre de la page venait de la version Assurance (« ré-assurance ») : il décrit
# maintenant la page de destination et son formulaire.
P4_TITRE = "LP : Visuels et messages de capture"
# Panneau : 18 lignes d'origine (7 modération + 11 fiche).
# Source unique : contenus.PANNEAUX[4] (acheteur final B2B, pas un installateur).
P4_PANNEAU = ([texte for texte, _ in C.PANNEAUX[4]["mod"]]
              + list(C.PANNEAUX[4]["fiche"]))


def police_titre():
    """Sous-ensemble OpenSans-Regular du PDF d'origine (aucun OpenSans système).

    Les sous-ensembles embarqués ne contiennent que les caractères réellement
    utilisés : on prend le premier qui couvre toutes les lettres du nouveau titre.
    """
    chemin = os.path.join(ASSETS, "OpenSans-Regular-P4.ttf")
    if os.path.exists(chemin):
        return chemin
    src = pymupdf.open(SRC)
    vus = set()
    for pno in range(src.page_count):
        for xref, ext, typ, base, ref, enc in src.get_page_fonts(pno):
            if "OpenSans-Regular" not in base or xref in vus:
                continue
            vus.add(xref)
            buf = src.extract_font(xref)[3]
            essai = "/tmp/_os_%d.ttf" % xref
            open(essai, "wb").write(buf)
            if all(pymupdf.Font(fontfile=essai).has_glyph(ord(c)) for c in P4_TITRE):
                open(chemin, "wb").write(buf)
                src.close()
                return chemin
    src.close()
    raise RuntimeError("aucun sous-ensemble OpenSans ne couvre le titre")


def _spans_zone(page, zone):
    """Spans dont l'origine tombe dans `zone`, dans l'ordre de lecture."""
    out = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if s["text"].strip() and zone.contains(pymupdf.Point(s["origin"])):
                    out.append(s)
    # ordre de lecture : colonne (x) puis ligne (y) — les textes de la carte de
    # formulaire sont à droite de ceux de la photo, pas en dessous
    out.sort(key=lambda s: (round(s["origin"][0]), round(s["origin"][1], 1)))
    return out


def _reecrire(page, zone, textes, ecrire=True):
    """Remplace les textes de `zone` en conservant origine, corps, couleur et graisse."""
    spans = _spans_zone(page, zone)
    assert len(spans) == len(textes), "page 4 : %d lignes au lieu de %d" % (
        len(spans), len(textes))
    infos = [dict(origine=tuple(s["origin"]), taille=s["size"], couleur=s["color"],
                  haut=s["bbox"][1], x=s["bbox"][0], gras="Bold" in s["font"])
             for s in spans]
    page.add_redact_annot(zone)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                          graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                          text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    if ecrire:
        page.insert_font(fontname="djr4", fontfile=DJ)
        page.insert_font(fontname="djb4", fontfile=DJB)
        for info, texte in zip(infos, textes):
            c = info["couleur"]
            rgb = (((c >> 16) & 255) / 255, ((c >> 8) & 255) / 255, (c & 255) / 255)
            page.insert_text(info["origine"], texte,
                             fontname="djb4" if info["gras"] else "djr4",
                             fontsize=info["taille"], color=rgb)
    return infos


def page4(doc, ecrire=True):
    page = doc[3]

    # 1. photo de la page de destination (même cadre, même définition)
    im = Image.open(os.path.join(PHOTOS, "chantier_b2b.jpg")).convert("RGB")
    # on recadre le ciel pour garder le bâtiment et l'installateur au centre
    im = im.crop((int(im.width * 0.06), int(im.height * 0.20),
                  int(im.width * 0.94), im.height))
    ech = max(1419 / im.width, 942 / im.height)
    im = im.resize((round(im.width * ech) + 1, round(im.height * ech) + 1), Image.LANCZOS)
    gx, gy = im.width - 1419, im.height - 942
    im = im.crop((gx // 2, round(gy * 0.45), gx // 2 + 1419, round(gy * 0.45) + 942))
    # voile sombre en bas à gauche : le titre blanc doit rester lisible
    voile = Image.new("L", im.size, 0)
    dv = ImageDraw.Draw(voile)
    for y in range(im.height):
        t = max(0.0, (y - im.height * 0.45) / (im.height * 0.55))
        dv.line([(0, y), (im.width, y)], fill=int(150 * t))
    im = Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, voile)
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    page.replace_image(136, stream=buf.getvalue())

    # 2. titre de la page (hérité de la version Assurance)
    titres = _spans_zone(page, pymupdf.Rect(465, 18, 970, 82))
    assert len(titres) == 1, "page 4 : %d titre(s)" % len(titres)
    t = titres[0]
    origine, corps, c = tuple(t["origin"]), t["size"], t["color"]
    page.add_redact_annot(pymupdf.Rect(t["bbox"]).__add__((-1, -2, 1, 2)))
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                          graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                          text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    page.insert_font(fontname="osr4", fontfile=police_titre())
    page.insert_text(origine, P4_TITRE, fontname="osr4", fontsize=corps,
                     color=(((c >> 16) & 255) / 255, ((c >> 8) & 255) / 255, (c & 255) / 255))

    # 3. bande de ré-assurance : retrait des logos d'assureurs
    for info in page.get_image_info(xrefs=True):
        if info["xref"] and 400 < info["bbox"][1] < 445 and 480 < info["bbox"][0] < 960:
            page.delete_image(info["xref"])
    page.insert_font(fontname="djb4", fontfile=DJB)
    largeur = pymupdf.Font(fontfile=DJB).text_length(P4_BANDE, 9.0)
    page.insert_text((719.5 - largeur / 2, 429), P4_BANDE, fontname="djb4",
                     fontsize=9.0, color=(0.235, 0.235, 0.259))

    # 4. textes de la page de destination et de l'extrait de formulaire
    # les textes des visuels restent dans le fond (seul le panneau est éditable)
    _reecrire(page, pymupdf.Rect(483, 85, 962, 403), P4_LP)
    _reecrire(page, pymupdf.Rect(477, 460, 963, 760), P4_FORM)

    # 5. bloc « Modération & Enrichissement » et fiche acheteur
    infos = _reecrire(page, pymupdf.Rect(1000, 448, 1340, 790), P4_PANNEAU, ecrire)
    for info, texte in zip(infos, P4_PANNEAU):
        LIGNES_PANNEAU.append(dict(page=4, x=round(info["x"], 2),
                                   haut=round(info["haut"], 2), texte=texte,
                                   gras=info["gras"], taille=round(info["taille"], 2)))
    return page


if __name__ == "__main__":
    main()
