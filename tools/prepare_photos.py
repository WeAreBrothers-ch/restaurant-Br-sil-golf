#!/usr/bin/env python3
"""
Prépare les photos du site Le 9.

Les photos telles que fournies sont dans `assets/photos/source/`. Ce script en
tire les fichiers que le site utilise, dans `assets/photos/` : recadrés au bon
format, redimensionnés et compressés.

Pourquoi : deux photos de terrasse pèsent près de 6 Mo chacune en PNG. Servies
telles quelles, la page mettrait plusieurs secondes à s'afficher.

Usage :
  python3 tools/prepare_photos.py            # produit tous les fichiers
  python3 tools/prepare_photos.py --list     # montre seulement ce qui serait fait

Le plan de découpe est la liste DERIVES ci-dessous. Une même photo peut donner
plusieurs fichiers, cadrés différemment. Pour changer un cadrage, modifier
`focus` : c'est le point de l'image à garder au centre, en proportions de 0 à 1
(0.5, 0.5 = le centre ; 0.5, 0.7 = un peu plus bas).

Dépendances : Pillow (pip install Pillow)
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "photos" / "source"
OUT = ROOT / "assets" / "photos"

# (source, fichier produit, ratio, largeur finale, focus x, focus y[, rognage])
# Le rognage préalable est facultatif : (gauche, haut, droite, bas) en fraction
# de l'image. Il sert à retirer ce qui traîne sur les bords, par exemple les
# flèches de navigation présentes sur les captures d'écran d'origine.
DERIVES = [
    # --- Les plats : une entrée par photo, format portrait ---------------------
    ("nourriture.jpg",                   "plat-01.jpg", 3/4,  1000, .50, .55),
    ("nourriture 2.jpg",                 "plat-02.jpg", 3/4,  1000, .50, .55),
    ("caption.jpg",                      "plat-03.jpg", 3/4,  1000, .50, .50),
    ("viande.jpg",                       "plat-04.jpg", 3/4,  1400, .50, .48),
    ("img-20190316-wa0006-largejpg.jpg", "plat-05.jpg", 3/4,  1000, .50, .55),
    ("20180714-120531-largejpg.jpg",     "plat-06.jpg", 3/4,   653, .50, .48),

    # --- Le lieu et la terrasse ----------------------------------------------
    # La bande pleine largeur vient de la photo la mieux définie (2296 px).
    # Les deux bandeaux : cadrage large plutôt que serré. En 21/8 ils ne
    # gardaient qu'un tiers de la photo, et la vue sur le parcours — ce qu'on
    # vient voir — passait presque entièrement à la trappe.
    ("le9_barolo_terrasse_HD.png",         "lieu-pano.jpg",      2/1, 2170, .54, .58, (.045, 0, .01, 0)),
    ("le9_terrasse_coucher_soleil_HD.png", "terrasse-pano.jpg", 16/9, 2170, .48, .55, (.01, 0, .045, 0)),
    ("le9_barolo_terrasse_HD.png",         "terrasse-01.jpg",   3/4,  1400, .38, .55, (.045, 0, .01, 0)),
    ("le9_terrasse_coucher_soleil_HD.png", "terrasse-02.jpg",   3/4,  1400, .44, .55, (.01, 0, .045, 0)),
    ("le9_barolo_terrasse_HD.png",         "terrasse-03.jpg",   4/3,  1600, .56, .50, (.045, 0, .01, 0)),
    ("le9_terrasse_coucher_soleil_HD.png", "terrasse-04.jpg",   4/3,  1600, .53, .42, (.01, 0, .045, 0)),

    # --- La salle -------------------------------------------------------------
    # Photo d'origine en 900 px : réservée à un cadre de taille modeste.
    ("une-vue-imprenable-sur.jpg", "salle-01.jpg", 4/3, 675, .50, .50),
]

QUALITY = 82
MAX_KB = 420  # au-delà, on baisse la qualité par paliers


def trim_black_bars(im: Image.Image, tol: int = 22) -> Image.Image:
    """Retire les bandes noires d'une image en boîte aux lettres."""
    g = im.convert("L")
    w, h = g.size
    px = g.load()

    def row_dark(y):
        return sum(px[x, y] for x in range(0, w, max(1, w // 60))) / max(1, len(range(0, w, max(1, w // 60)))) < tol

    def col_dark(x):
        return sum(px[x, y] for y in range(0, h, max(1, h // 60))) / max(1, len(range(0, h, max(1, h // 60)))) < tol

    top = 0
    while top < h - 1 and row_dark(top): top += 1
    bot = h - 1
    while bot > top and row_dark(bot): bot -= 1
    left = 0
    while left < w - 1 and col_dark(left): left += 1
    right = w - 1
    while right > left and col_dark(right): right -= 1
    if (top, left, right, bot) == (0, 0, w - 1, h - 1):
        return im
    return im.crop((left, top, right + 1, bot + 1))


def crop_to_ratio(im: Image.Image, ratio: float, fx: float, fy: float) -> Image.Image:
    """Recadre au ratio demandé en gardant le point (fx, fy) au centre."""
    w, h = im.size
    cur = w / h
    if abs(cur - ratio) < 1e-3:
        return im
    if cur > ratio:                      # trop large : on coupe sur les côtés
        nw, nh = int(round(h * ratio)), h
    else:                                # trop haute : on coupe en haut et en bas
        nw, nh = w, int(round(w / ratio))
    cx, cy = fx * w, fy * h
    x = int(round(min(max(cx - nw / 2, 0), w - nw)))
    y = int(round(min(max(cy - nh / 2, 0), h - nh)))
    return im.crop((x, y, x + nw, y + nh))


def save_jpeg(im: Image.Image, path: Path) -> int:
    """Écrit en JPEG, en baissant la qualité tant que le fichier est trop lourd."""
    for q in (QUALITY, 76, 70, 64):
        im.save(path, "JPEG", quality=q, optimize=True, progressive=True, subsampling=1)
        kb = path.stat().st_size // 1024
        if kb <= MAX_KB:
            return kb
    return path.stat().st_size // 1024


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true", help="montrer le plan sans rien écrire")
    args = ap.parse_args(argv)

    if not SRC.exists():
        print(f"Dossier introuvable : {SRC}")
        print("Y déposer les photos telles que fournies, puis relancer.")
        return 1

    missing = sorted({s for s, *_ in DERIVES} - {p.name for p in SRC.iterdir()})
    if missing:
        print("Photos absentes de source/ :")
        for m in missing:
            print("  -", m)
        print()

    total = 0
    petites = []
    for entry in DERIVES:
        src, dst, ratio, width, fx, fy = entry[:6]
        inset = entry[6] if len(entry) > 6 else (0, 0, 0, 0)
        sp = SRC / src
        if not sp.exists():
            continue
        if args.list:
            print(f"  {src:38s} -> {dst:20s} ratio {ratio:.2f}  {width} px")
            continue
        im = Image.open(sp)
        im = ImageOps.exif_transpose(im).convert("RGB")
        im = trim_black_bars(im)
        if any(inset):
            w, h = im.size
            l, t, r, b = inset
            im = im.crop((int(w * l), int(h * t), int(w * (1 - r)), int(h * (1 - b))))
        im = crop_to_ratio(im, ratio, fx, fy)
        if im.width > width:
            im = im.resize((width, int(round(width / ratio))), Image.LANCZOS)
        if im.width < width:
            petites.append((dst, im.width, width))
        kb = save_jpeg(im, OUT / dst)
        total += kb
        print(f"  ✓ {src[:34]:36s} -> {dst:20s} {im.width}×{im.height}  {kb} Ko")

    if not args.list:
        print(f"\nTotal des images servies : {total} Ko")
        if petites:
            print("\nPlus petites que la largeur demandée (elles ne sont pas agrandies,")
            print("mais seront un peu molles si la page les affiche en grand) :")
            for nom, eu, voulu in petites:
                print(f"  {nom:20s} {eu} px au lieu de {voulu}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
