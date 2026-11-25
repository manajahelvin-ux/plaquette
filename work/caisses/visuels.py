# -*- coding: utf-8 -*-
"""Outils de retouche des visuels raster de la plaquette.

Chaque visuel de maquette est une image placée sur la page. On la recharge à sa
résolution native, on y repeint les zones de texte / les photos, puis on repose
uniquement les zones retouchées à la même place et à la même échelle : tout le
reste de la page reste identique au pixel près.
"""
import io
import os

from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ICI, "assets")
REG = os.path.join(ASSETS, "Poppins-Regular.ttf")
GRAS = os.path.join(ASSETS, "Poppins-Bold.ttf")
PHOTOS = os.path.join(ICI, "photos")


def charger_image(doc, xref):
    import pymupdf
    pix = pymupdf.Pixmap(doc, xref)
    if pix.alpha or pix.n not in (3,):
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    return Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")


def taille_police(texte, chemin, largeur_cible, mini=8, maxi=400):
    """Taille de police pour que `texte` mesure `largeur_cible` pixels."""
    lo, hi = mini, maxi
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if ImageFont.truetype(chemin, mid).getlength(texte) <= largeur_cible:
            lo = mid
        else:
            hi = mid - 1
    return lo


def couper(texte, font, largeur):
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


class Visuel:
    """Image d'une maquette + ses retouches, reposées sur la page."""

    def __init__(self, doc, page, xref, rect, nom=""):
        self.doc = doc
        self.page = page
        self.rect = rect
        self.nom = nom or str(xref)
        self.img = charger_image(doc, xref)
        self.ech_x = rect.width / self.img.width
        self.ech_y = rect.height / self.img.height
        self.d = ImageDraw.Draw(self.img)
        self.zones = []

    # ---------------------------------------------------------------- primitives
    def pt_vers_px(self, x, y):
        return ((x - self.rect.x0) / self.ech_x, (y - self.rect.y0) / self.ech_y)

    def box_px(self, x0, y0, x1, y1):
        a = self.pt_vers_px(x0, y0)
        b = self.pt_vers_px(x1, y1)
        return (round(a[0]), round(a[1]), round(b[0]), round(b[1]))

    def effacer_box(self, box, couleur=(255, 255, 255)):
        self.d.rectangle(box, fill=couleur)
        self.zones.append(box)

    def effacer(self, x0, y0, x1, y1, couleur=(255, 255, 255)):
        """Efface une zone exprimée en points de la page."""
        box = self.box_px(x0, y0, x1, y1)
        self.effacer_box(box, couleur)
        return box

    def texte(self, xy_px, texte, chemin, taille, couleur, ancre="ls"):
        self.d.text(xy_px, texte, font=ImageFont.truetype(chemin, taille),
                    fill=couleur, anchor=ancre)

    def photo(self, chemin, x0, y0, x1, y1, cadrage=0.45):
        """Remplace une zone par une photo (recadrée, sans déformation)."""
        box = self.box_px(x0, y0, x1, y1)
        l, h = box[2] - box[0], box[3] - box[1]
        im = Image.open(chemin).convert("RGB")
        r = max(l / im.width, h / im.height)
        im = im.resize((max(l, round(im.width * r)) + 1, max(h, round(im.height * r)) + 1),
                       Image.LANCZOS)
        gx, gy = im.width - l, im.height - h
        im = im.crop((gx // 2, int(gy * cadrage), gx // 2 + l, int(gy * cadrage) + h))
        self.img.paste(im, (box[0], box[1]))
        self.zones.append(box)

    def zone(self, x0, y0, x1, y1):
        box = self.box_px(x0, y0, x1, y1)
        self.zones.append(box)

    def zone_px(self, box):
        """Déclare une zone à reposer, en pixels de l'image."""
        self.zones.append(tuple(box))

    # ------------------------------------------------------------------- sortie
    def poser(self, marge=1):
        """Repose les zones retouchées sur la page, à leur place exacte."""
        import pymupdf
        for box in self.zones:
            b = (max(0, box[0] - marge), max(0, box[1] - marge),
                 min(self.img.width, box[2] + marge), min(self.img.height, box[3] + marge))
            if b[2] - b[0] < 2 or b[3] - b[1] < 2:
                continue
            rect = pymupdf.Rect(self.rect.x0 + b[0] * self.ech_x,
                                self.rect.y0 + b[1] * self.ech_y,
                                self.rect.x0 + b[2] * self.ech_x,
                                self.rect.y0 + b[3] * self.ech_y)
            buf = io.BytesIO()
            self.img.crop(b).save(buf, "PNG", optimize=True)
            self.page.insert_image(rect, stream=buf.getvalue(), keep_proportion=False)

    def enregistrer(self, chemin):
        self.img.save(chemin)


class Region:
    """Zone de page rendue en raster : on retouche le rendu, puis on le repose.

    Utilisé pour les maquettes dont l'image est imbriquée dans un formulaire
    (le PDF applique des découpes) : le rendu garantit un calage exact.
    """

    def __init__(self, doc, page, rect, densite=4.5, nom=""):
        import pymupdf
        self.page = page
        self.rect = pymupdf.Rect(rect)
        self.nom = nom
        self.densite = densite
        pix = doc.get_page_pixmap(page.number, dpi=round(72 * densite), clip=self.rect)
        self.img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        self.ech = self.rect.width / self.img.width
        self.d = ImageDraw.Draw(self.img)
        self.zones = [None]      # une seule zone : tout le rendu

    def px(self, x_pt, y_pt):
        return ((x_pt - self.rect.x0) / self.ech, (y_pt - self.rect.y0) / self.ech)

    def effacer(self, x0, y0, x1, y1, couleur=(255, 255, 255)):
        a = self.px(x0, y0)
        b = self.px(x1, y1)
        self.d.rectangle([a[0], a[1], b[0], b[1]], fill=couleur)
        return a, b

    def texte(self, x_pt, y_pt_baseline, texte, chemin, taille_pt, couleur, ancre="ls"):
        """Texte dont la taille est exprimée en points de page."""
        a = self.px(x_pt, y_pt_baseline)
        self.d.text(a, texte, font=ImageFont.truetype(chemin, round(taille_pt / self.ech)),
                    fill=couleur, anchor=ancre)

    def texte_centre(self, cx_pt, y_pt_base, texte, chemin, taille_pt, couleur):
        self.texte(cx_pt, y_pt_base, texte, chemin, taille_pt, couleur, ancre="ms")

    def ajuster(self, texte, chemin, largeur_pt, mini=3, maxi=40):
        """Taille (en points) pour que le texte tienne dans `largeur_pt`."""
        lo, hi = mini, maxi
        while lo < hi:
            mid = (lo + hi + 1) / 2
            if len_texte(texte, chemin, mid / self.ech) <= largeur_pt / self.ech:
                lo = mid
            else:
                hi = mid - 0.5
        return lo

    def photo(self, chemin, x0, y0, x1, y1, cadrage=0.45):
        a = self.px(x0, y0)
        b = self.px(x1, y1)
        l, h = round(b[0] - a[0]), round(b[1] - a[1])
        im = Image.open(chemin).convert("RGB")
        r = max(l / im.width, h / im.height)
        im = im.resize((max(l, round(im.width * r)) + 1, max(h, round(im.height * r)) + 1),
                       Image.LANCZOS)
        gx, gy = im.width - l, im.height - h
        im = im.crop((gx // 2, int(gy * cadrage), gx // 2 + l, int(gy * cadrage) + h))
        self.img.paste(im, (round(a[0]), round(a[1])))

    def poser(self):
        buf = io.BytesIO()
        self.img.save(buf, "PNG", optimize=True)
        self.page.insert_image(self.rect, stream=buf.getvalue(), keep_proportion=False)

    def enregistrer(self, chemin):
        self.img.save(chemin)


def len_texte(texte, chemin, taille_px):
    return ImageFont.truetype(chemin, max(1, round(taille_px))).getlength(texte)


# ------------------------------------------- retouches exprimées en pixels image
def _regler_region(self, img_rect, W, H):
    import pymupdf
    self._img_rect = pymupdf.Rect(img_rect)
    self._W, self._H = W, H
    # facteur pixels image -> pixels de la région rendue
    self.f_ip = (self._img_rect.width / W) / self.ech


def _ipx(self, x, y):
    r = self._img_rect
    return self.px(r.x0 + x * r.width / self._W, r.y0 + y * r.height / self._H)


def _effacer_ip(self, x0, y0, x1, y1, couleur=None, point=None):
    a = self.ipx(x0, y0)
    b = self.ipx(x1, y1)
    if couleur is None:
        sx, sy = point or (x0 - 4, y0 - 3)
        p = self.ipx(sx, sy)
        couleur = self.img.getpixel((max(0, min(self.img.width - 1, int(p[0]))),
                                     max(0, min(self.img.height - 1, int(p[1])))))
    self.d.rectangle([a[0], a[1], b[0], b[1]], fill=couleur)
    return couleur


def _texte_ip(self, x, y, texte, chemin, taille, couleur, ancre="ls"):
    a = self.ipx(x, y)
    self.d.text(a, texte, font=ImageFont.truetype(chemin, max(1, round(taille * self.f_ip))),
                fill=couleur, anchor=ancre)


def _largeur_ip(self, texte, chemin, taille):
    return ImageFont.truetype(chemin, max(1, round(taille * self.f_ip))).getlength(texte) / self.f_ip


def _ajuster_ip(self, texte, chemin, largeur, mini=4, maxi=40):
    lo, hi = mini, maxi
    while lo < hi:
        mid = (lo + hi + 1) / 2
        if self.largeur_ip(texte, chemin, mid) <= largeur:
            lo = mid
        else:
            hi = mid - 0.5
    return max(lo, mini)


Region.regler = _regler_region
Region.ipx = _ipx
Region.effacer_ip = _effacer_ip
Region.texte_ip = _texte_ip
Region.largeur_ip = _largeur_ip
Region.ajuster_ip = _ajuster_ip


def _effacer_ip_degrade(self, x0, y0, x1, y1, cote="gauche"):
    """Efface en reprenant, ligne par ligne, la couleur du fond voisin.

    Indispensable sur les aplats dégradés (bandeaux sombres des emails) : un
    aplat uni laisserait un rectangle visible.
    """
    a = self.ipx(x0, y0)
    b = self.ipx(x1, y1)
    xa, xb = int(round(a[0])), int(round(b[0]))
    for y in range(int(round(a[1])), int(round(b[1])) + 1):
        if y < 0 or y >= self.img.height:
            continue
        xs = xa - 3 if cote == "gauche" else xb + 3
        xs = max(0, min(self.img.width - 1, xs))
        self.d.line([(xa, y), (xb, y)], fill=self.img.getpixel((xs, y)))


Region.effacer_ip_degrade = _effacer_ip_degrade
