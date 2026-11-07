#!/usr/bin/env python3
"""
Prépare les photos du site Le 9.

Les photos telles que fournies sont dans `assets/photos/source/`. Ce script en
tire les fichiers que le site utilise, dans `assets/photos/` : recadrés au bon
format, redimensionnés et compressés.

Pourquoi : deux photos de terrasse pèsent près de 6 Mo chacune en PNG. Servies
telles quelles, la page mettrait plusieurs secondes à s'afficher.

Netteté : plusieurs photos d'origine sont plus petites que l'espace qu'elles
occupent à l'écran (des photos de téléphone de 1000 px posées sur 1600 px de
large sur un écran Retina), ou sont des « HD » dont le détail réel est bien
plus petit que la taille annoncée. Pour celles-là, le script passe par
`tools/superresolution.py` (Real-ESRGAN) avant de ramener l'image à la taille
voulue. Sans onnxruntime ou sans réseau, il se rabat sur un redimensionnement
classique : rien ne casse, les photos sont juste un peu moins nettes.

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

from PIL import Image, ImageFilter, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parent))
import superresolution

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "photos" / "source"
OUT = ROOT / "assets" / "photos"

# (source, fichier produit, ratio, largeur finale, focus x, focus y[, rognage])
# Le rognage préalable est facultatif : (gauche, haut, droite, bas) en fraction
# de l'image. Il sert à retirer ce qui traîne sur les bords, par exemple les
# flèches de navigation présentes sur les captures d'écran d'origine.
DERIVES = [
    # --- Les plats : une entrée par photo, format portrait ---------------------
    # Largeurs choisies pour ce que l'écran demande réellement : la carte pose
    # une photo sur 820 px de large, soit 1640 px sur un écran Retina.
    ("nourriture.jpg",                   "plat-01.jpg", 3/4,  1600, .50, .55),
    ("nourriture 2.jpg",                 "plat-02.jpg", 3/4,  1600, .50, .55),
    ("caption.jpg",                      "plat-03.jpg", 3/4,  1400, .50, .50),
    ("viande.jpg",                       "plat-04.jpg", 3/4,  1600, .50, .48),
    ("img-20190316-wa0006-largejpg.jpg", "plat-05.jpg", 3/4,  1000, .50, .55),
    ("20180714-120531-largejpg.jpg",     "plat-06.jpg", 3/4,   653, .50, .48),

    # --- Le lieu et la terrasse ----------------------------------------------
    # La bande pleine largeur vient de la photo la mieux définie (2296 px).
    # Les deux bandeaux : cadrage large plutôt que serré. En 21/8 ils ne
    # gardaient qu'un tiers de la photo, et la vue sur le parcours — ce qu'on
    # vient voir — passait presque entièrement à la trappe.
    ("le9_barolo_terrasse_HD.png",         "lieu-pano.jpg",      2/1, 2880, .54, .58, (.045, 0, .01, 0)),
    ("le9_terrasse_coucher_soleil_HD.png", "terrasse-pano.jpg", 16/9, 2880, .48, .55, (.01, 0, .045, 0)),
    ("le9_barolo_terrasse_HD.png",         "terrasse-01.jpg",   3/4,  1400, .38, .55, (.045, 0, .01, 0)),
    ("le9_terrasse_coucher_soleil_HD.png", "terrasse-02.jpg",   3/4,  1400, .44, .55, (.01, 0, .045, 0)),
    ("le9_barolo_terrasse_HD.png",         "terrasse-03.jpg",   4/3,  1600, .56, .50, (.045, 0, .01, 0)),
    ("le9_terrasse_coucher_soleil_HD.png", "terrasse-04.jpg",   4/3,  1600, .53, .42, (.01, 0, .045, 0)),

    # --- Cadrages pour téléphone ----------------------------------------------
    # Sur un téléphone, le bandeau large est posé dans une boîte presque carrée
    # (« Le restaurant »), et le haut de « La terrasse » dans une boîte
    # PORTRAIT de 390 × 620. Un panorama 16/9 y est agrandi près de trois fois :
    # c'est ce qui le rendait flou. Ces deux cadrages sont servis à la place du
    # panorama sous 700 px (balise <picture>), à la forme exacte de la boîte.
    # Les originaux sont des captures Instagram : tampon « LE 9 » dans le coin bas-droit,
    # points de carrousel sur les bords et en bas au centre. Ce cadrage retire le coin
    # droit (le tampon) et s'arrête avant le bord bas (les points).
    ("le9_barolo_terrasse_HD.png",         "lieu-pano-m.jpg",    4/3, 1600, .36, .67, (.045, 0, .17, 0)),
    ("le9_terrasse_coucher_soleil_HD.png", "terrasse-pano-m.jpg", 5/8, 1300, .47, .50, (.01, 0, .045, 0)),

    # --- Image de partage -----------------------------------------------------
    # Ce qui s'affiche quand on envoie le lien par message ou sur un réseau :
    # 1200 × 630, sous 200 Ko (WhatsApp écarte les aperçus trop lourds).
    ("le9_terrasse_coucher_soleil_HD.png", "og.jpg", 1200/630, 1200, .48, .50, (.01, 0, .045, 0)),

    # --- La salle -------------------------------------------------------------
    # Photo d'origine en 900 px : agrandie par super-résolution, elle tient
    # sa place, mais une vraie photo en haute définition reste préférable.
    ("une-vue-imprenable-sur.jpg", "salle-01.jpg", 4/3, 1400, .50, .50),
]

# Sources dont le détail réel est bien plus petit que la taille annoncée : les
# deux « HD » de la terrasse font 2296 px mais ne portent guère plus de 600 px
# de détail (agrandies et recompressées avant d'arriver). On les ramène d'abord
# à ce détail réel, puis on agrandit : le modèle travaille sur du détail net,
# pas sur du flou étalé.
SOURCES_MOLLES = {
    "le9_barolo_terrasse_HD.png": 0.5,
    "le9_terrasse_coucher_soleil_HD.png": 0.5,
}

QUALITY = 82
MAX_KB = 620  # au-delà, on baisse la qualité par paliers

# --- LA VARIANTE LÉGÈRE ------------------------------------------------------
# Chaque grande photo a une jumelle de 1200 px, nommée « <nom>-1200.jpg ». Les
# pages déclarent les deux dans `srcset` et le navigateur choisit selon la
# largeur d'affichage : la grande sur un écran d'ordinateur, la jumelle au doigt.
#
# Pourquoi 1200 et pas moins : un téléphone récent affiche en 390 px CSS mais
# dispose de 1170 pixels physiques (×3). Une jumelle de 800 px y était étirée
# d'un tiers, c'est ce qui rendait les photos molles sur mobile. 1200 px
# couvre exactement un écran à ×3 pour un poids qui reste raisonnable.
VARIANTE_W = 1200
VARIANTE_MIN = 1350  # en dessous, la photo est déjà légère : pas de jumelle
VARIANTE_KB = 300    # la jumelle doit tenir sous ce poids, quitte à baisser la qualité


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


def mise_a_taille(im: Image.Image, width: int, mou=None, sr_ok=False):
    """Amène `im` à `width` px de large. Renvoie (image, agrandie_par_IA).

    - Photo assez grande : simple réduction (Lanczos), rien d'autre.
    - Photo trop petite pour la largeur demandée, ou source « molle » : si la
      super-résolution est disponible, on agrandit ×4 puis on réduit à la
      taille voulue ; sinon on agrandit classiquement, sans rien promettre.
    `mou` : facteur de réduction préalable pour une source dont le détail réel
    est plus petit que sa taille (voir SOURCES_MOLLES).
    """
    ratio = im.width / im.height
    besoin_ia = mou is not None or im.width < width * 0.98
    if besoin_ia and sr_ok:
        base = im
        if mou:
            base = im.resize((max(1, round(im.width * mou)), max(1, round(im.height * mou))), Image.LANCZOS)
        grande = superresolution.agrandir(base)
        out = grande.resize((width, int(round(width / ratio))), Image.LANCZOS)
        # Un voile de netteté très léger : la réduction ×4 → ×1,5 rend déjà les
        # bords francs, on ne cherche qu'à leur rendre le contraste perdu.
        out = out.filter(ImageFilter.UnsharpMask(radius=0.9, percent=30, threshold=3))
        return out, True
    if im.width > width:
        return im.resize((width, int(round(width / ratio))), Image.LANCZOS), False
    return im, False


def save_jpeg(im: Image.Image, path: Path, max_kb: int = None) -> int:
    """Écrit en JPEG, en baissant la qualité tant que le fichier est trop lourd."""
    max_kb = max_kb or MAX_KB
    for q in (QUALITY, 76, 70, 64, 58):
        im.save(path, "JPEG", quality=q, optimize=True, progressive=True, subsampling=1)
        kb = path.stat().st_size // 1024
        if kb <= max_kb:
            return kb
    return path.stat().st_size // 1024


def variantes(dossier: Path, montrer=False) -> list:
    """Écrit la jumelle de 800 px de chaque photo assez large pour en valoir une."""
    faits = []
    for src in sorted(dossier.glob("*.jpg")):
        if src.stem.endswith(f"-{VARIANTE_W}"):
            continue
        with Image.open(src) as im:
            if im.width < VARIANTE_MIN:
                continue
            cible = src.with_name(f"{src.stem}-{VARIANTE_W}.jpg")
            if montrer:
                faits.append(f"{cible.name}  {VARIANTE_W} px")
                continue
            petite = im.convert("RGB").resize(
                (VARIANTE_W, round(im.height * VARIANTE_W / im.width)), Image.LANCZOS)
            # Certaines photos d'origine sont bruitées : à qualité fixe, leur
            # jumelle pesait encore près de trois cents kilo-octets. On descend
            # par paliers jusqu'à ce qu'elle tienne dans le budget.
            for q in (80, 74, 68, 62):
                petite.save(cible, "JPEG", quality=q, optimize=True, progressive=True, subsampling=1)
                if cible.stat().st_size // 1024 <= VARIANTE_KB:
                    break
            faits.append(f"{cible.name}  {VARIANTE_W} px  {cible.stat().st_size // 1024} Ko")
    return faits


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true", help="montrer le plan sans rien écrire")
    ap.add_argument("--seulement", metavar="FICHIERS",
                    help="ne refaire que ces fichiers produits (séparés par des virgules), "
                         "par exemple --seulement lieu-pano.jpg,terrasse-pano.jpg")
    ap.add_argument("--sans-agrandissement", action="store_true",
                    help="ne pas utiliser la super-résolution (redimensionnement classique)")
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

    sr_ok = (not args.list) and (not args.sans_agrandissement) and superresolution.disponible()
    if not args.list and not sr_ok:
        print("  Super-résolution inactive : redimensionnement classique.\n")

    total = 0
    petites = []
    for entry in DERIVES:
        src, dst, ratio, width, fx, fy = entry[:6]
        if args.seulement and dst not in args.seulement.split(","):
            continue
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
        im, agrandie = mise_a_taille(im, width, SOURCES_MOLLES.get(src), sr_ok)
        if im.width < width:
            petites.append((dst, im.width, width))
        kb = save_jpeg(im, OUT / dst, 200 if dst == "og.jpg" else None)
        total += kb
        print(f"  ✓ {src[:34]:36s} -> {dst:20s} {im.width}×{im.height}  {kb} Ko{'  (super-résolution)' if agrandie else ''}")

    if not args.list:
        print("\nJumelles pour téléphone :")
        for ligne in variantes(OUT):
            print("  ✓", ligne)
        print(f"\nTotal des grandes images servies : {total} Ko")
        if petites:
            print("\nPlus petites que la largeur demandée (elles ne sont pas agrandies,")
            print("mais seront un peu molles si la page les affiche en grand) :")
            for nom, eu, voulu in petites:
                print(f"  {nom:20s} {eu} px au lieu de {voulu}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
