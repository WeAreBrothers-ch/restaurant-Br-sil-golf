#!/usr/bin/env python3
"""
Traitement des illustrations pour le site Le 9.

Pour chaque image de `assets/illustrations/source/` (JPG ou PNG, dessin au trait
sur fond blanc ou gris) :

  1. détoure le fond et sort un PNG transparent (le trait devient l'alpha) ;
  2. si le tracé est net, vectorise en SVG avec fill="currentColor" ;
  3. nettoie ce qui traîne : filigranes clairs, liseré blanc, petites taches.

Le PNG produit est noir sur transparent : la couleur est donnée par le CSS
(`mask-image` + `background-color`), jamais dans le fichier.

Usage :
  python3 tools/process_illustrations.py                 # tout le dossier source
  python3 tools/process_illustrations.py chef.jpg -t 110 # un fichier, seuil manuel
  python3 tools/process_illustrations.py --no-svg        # PNG uniquement

Le détourage se fait par écart à la couleur du fond (déduite du pourtour), pas
par simple noirceur : un trait noir sur blanc, une silhouette verte sur gris et
un aplat blanc sur fond vert sont donc traités correctement.

Options par fichier (facultatif) dans tools/illustrations.json :
  { "chef.jpg": { "threshold": 40, "min_area": 60, "svg": false },
    "autre.png": { "mode": "luminance" },
    "encore.png": { "background": [255, 255, 255] } }

Dépendances : Pillow, numpy, potracer (pip install Pillow numpy potracer)
"""
import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

try:
    import potrace  # potracer (pure Python)
except ImportError:  # pragma: no cover
    potrace = None

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "assets" / "illustrations" / "source"
OUT_DIR = ROOT / "assets" / "illustrations" / "dist"
CONFIG = ROOT / "tools" / "illustrations.json"
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tif", ".tiff"}


# ----------------------------------------------------------------------------
# Lecture et mesure
# ----------------------------------------------------------------------------
def load_rgb(path: Path) -> np.ndarray:
    """Image aplatie sur blanc, en RGB float32 (0..255)."""
    im = Image.open(path).convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    bg.alpha_composite(im)
    return np.asarray(bg.convert("RGB"), dtype=np.float32)


def luminance(rgb: np.ndarray) -> np.ndarray:
    return 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]


def background_color(rgb: np.ndarray, border: int = 6) -> np.ndarray:
    """
    Couleur du fond : médiane des pixels du pourtour. Robuste au fond blanc,
    gris, ou coloré (le golfeur sur fond vert), et à une texture légère.
    """
    h, w, _ = rgb.shape
    b = max(1, min(border, h // 4, w // 4))
    edge = np.concatenate([
        rgb[:b, :, :].reshape(-1, 3), rgb[-b:, :, :].reshape(-1, 3),
        rgb[:, :b, :].reshape(-1, 3), rgb[:, -b:, :].reshape(-1, 3),
    ])
    return np.median(edge, axis=0)


def ink_distance(rgb: np.ndarray, bg: np.ndarray) -> np.ndarray:
    """
    Distance de chaque pixel à la couleur de fond, ramenée sur 0..255.
    C'est cette distance qui définit l'encre : tout ce qui s'écarte du fond est
    du dessin, quelle que soit sa couleur (trait noir, silhouette verte, et le
    pantalon blanc du golfeur sur fond vert, que la luminance seule perdait).
    """
    d = np.sqrt(((rgb - bg.reshape(1, 1, 3)) ** 2).sum(axis=2))
    return np.clip(d / np.sqrt(3.0), 0, 255).astype(np.float32)


def otsu(values: np.ndarray) -> float:
    """Seuil d'Otsu sur un tableau de valeurs 0..255."""
    hist, _ = np.histogram(values, bins=256, range=(0, 256))
    hist = hist.astype(np.float64)
    total = hist.sum()
    if total == 0:
        return 128.0
    prob = hist / total
    omega = np.cumsum(prob)
    mu = np.cumsum(prob * np.arange(256))
    mu_t = mu[-1]
    with np.errstate(divide="ignore", invalid="ignore"):
        sigma = (mu_t * omega - mu) ** 2 / (omega * (1 - omega))
    sigma[~np.isfinite(sigma)] = 0
    return float(np.argmax(sigma))


def auto_threshold(dist: np.ndarray) -> float:
    """
    Seuil sur la distance au fond.
    Otsu sépare le fond (distance ~0) du reste. S'il subsiste dans ce reste
    deux amas nettement séparés — filigrane pâle et trait franc — un second
    Otsu les départage et on garde le trait. Sinon on descend au ras du fond
    pour conserver l'anticrénelage.
    """
    t1 = otsu(dist)
    fg = dist[dist > t1]
    if fg.size < 50:
        return max(t1, 10.0)
    t2 = otsu(fg)
    low, high = fg[fg < t2], fg[fg >= t2]
    if low.size and high.size and fg.var() > 1e-6:
        between = (low.size * high.size) / float(fg.size ** 2) * (low.mean() - high.mean()) ** 2
        sep = float(between / fg.var())
        # un filigrane est pâle ET occupe une bonne part du "premier plan"
        if sep > 0.55 and (high.mean() - low.mean()) > 45 and low.size > 0.15 * fg.size:
            return float(t2 + 0.25 * (high.mean() - t2))
    return float(max(t1 * 0.6, 8.0))


# ----------------------------------------------------------------------------
# Masque d'encre et nettoyage
# ----------------------------------------------------------------------------
def ink_alpha(dist: np.ndarray, threshold: float, softness: float = 18.0) -> np.ndarray:
    """
    Alpha 0..1 sur la distance au fond : 0 en deçà de `threshold`, 1 au-delà de
    `threshold + softness`, rampe douce entre les deux. La rampe conserve
    l'anticrénelage du trait ; le seuil élimine fond et filigranes pâles.
    """
    a = (dist - threshold) / max(softness, 1e-6)
    return np.clip(a, 0.0, 1.0).astype(np.float32)


def remove_small_components(mask: np.ndarray, min_area: int) -> np.ndarray:
    """
    Supprime les composantes connexes (8-voisinage) de moins de `min_area`
    pixels. Implémentation par "runs" horizontaux + union-find : rapide en
    Python pur même sur des images de plusieurs mégapixels.
    """
    h, w = mask.shape
    parent = []
    size = []

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]

    prev_runs = []  # (x0, x1, label) de la ligne précédente
    runs_by_row = []
    for y in range(h):
        row = mask[y]
        if not row.any():
            prev_runs = []
            runs_by_row.append([])
            continue
        d = np.diff(np.concatenate(([0], row.astype(np.int8), [0])))
        starts = np.flatnonzero(d == 1)
        ends = np.flatnonzero(d == -1)  # exclusif
        cur = []
        j = 0
        for x0, x1 in zip(starts, ends):
            lab = len(parent)
            parent.append(lab)
            size.append(int(x1 - x0))
            # chevauchement (8-voisinage : on tolère un pixel de diagonale)
            while j < len(prev_runs) and prev_runs[j][1] < x0 - 1:
                j += 1
            k = j
            while k < len(prev_runs) and prev_runs[k][0] <= x1:
                union(lab, prev_runs[k][2])
                k += 1
            cur.append((int(x0), int(x1), lab))
        prev_runs = cur
        runs_by_row.append(cur)

    if not parent:
        return mask
    root_size = {}
    for lab in range(len(parent)):
        r = find(lab)
        root_size[r] = root_size.get(r, 0) + size[lab]
    out = mask.copy()
    for y, runs in enumerate(runs_by_row):
        for x0, x1, lab in runs:
            if root_size[find(lab)] < min_area:
                out[y, x0:x1] = False
    return out


def bbox(mask: np.ndarray, pad: int):
    ys, xs = np.nonzero(mask)
    if ys.size == 0:
        return None
    h, w = mask.shape
    return (max(int(xs.min()) - pad, 0), max(int(ys.min()) - pad, 0),
            min(int(xs.max()) + pad + 1, w), min(int(ys.max()) + pad + 1, h))


def sharpness(alpha: np.ndarray) -> float:
    """Part des pixels d'encre franchement opaques : ~1 = trait net, ~0.5 = flou."""
    ink = alpha > 0.05
    if ink.sum() == 0:
        return 0.0
    return float((alpha[ink] > 0.85).mean())


# ----------------------------------------------------------------------------
# Sorties
# ----------------------------------------------------------------------------
def write_png(alpha: np.ndarray, out: Path, max_size: int):
    h, w = alpha.shape
    rgba = np.zeros((h, w, 4), dtype=np.uint8)
    rgba[..., 3] = np.round(alpha * 255).astype(np.uint8)
    im = Image.fromarray(rgba, "RGBA")
    if max(w, h) > max_size:
        s = max_size / max(w, h)
        im = im.resize((max(1, round(w * s)), max(1, round(h * s))), Image.LANCZOS)
    im.save(out, optimize=True)
    return im.size


def _fmt(v: float) -> str:
    return f"{v:.1f}".rstrip("0").rstrip(".")


def write_svg(binary: np.ndarray, out: Path, turdsize: int = 3, alphamax: float = 1.0,
              opttolerance: float = 0.25) -> int:
    """Trace le masque binaire (True = encre) en un seul <path fill=currentColor>."""
    bm = potrace.Bitmap(np.logical_not(binary))  # potracer inverse son entrée
    path = bm.trace(turdsize=turdsize, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY,
                    alphamax=alphamax, opticurve=True, opttolerance=opttolerance)
    def pt(p):
        x, y = (p.x, p.y) if hasattr(p, "x") else (p[0], p[1])
        return f"{_fmt(x)} {_fmt(y)}"

    parts = []
    for curve in path:
        parts.append("M" + pt(curve.start_point))
        for seg in curve:
            if seg.is_corner:
                parts.append("L" + pt(seg.c) + "L" + pt(seg.end_point))
            else:
                parts.append("C" + pt(seg.c1) + " " + pt(seg.c2) + " " + pt(seg.end_point))
        parts.append("Z")
    h, w = binary.shape
    d = "".join(parts)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
           f'role="img" aria-hidden="true" focusable="false">\n'
           f'  <path fill="currentColor" d="{d}"/>\n</svg>\n')
    out.write_text(svg, encoding="utf-8")
    return len(path)


# ----------------------------------------------------------------------------
# Pipeline
# ----------------------------------------------------------------------------
def process(path: Path, out_dir: Path, opts: dict, want_svg: bool, verbose=True):
    rgb = load_rgb(path)
    h, w, _ = rgb.shape

    mode = opts.get("mode", "color")
    if mode == "luminance":
        # Repli : le dessin est simplement ce qui est sombre (fond clair garanti).
        metric = 255.0 - luminance(rgb)
    else:
        bg = np.array(opts["background"], dtype=np.float32) if "background" in opts \
            else background_color(rgb)
        metric = ink_distance(rgb, bg)

    thr = opts.get("threshold")
    thr = float(thr) if thr is not None else auto_threshold(metric)
    softness = float(opts.get("softness", 18))
    alpha = ink_alpha(metric, thr, softness)

    # Bords : un liseré (cadre, ombre de scan) collé au bord est retiré
    edge = int(opts.get("edge", 2))
    if edge > 0:
        alpha[:edge, :] = 0; alpha[-edge:, :] = 0; alpha[:, :edge] = 0; alpha[:, -edge:] = 0

    # Nettoyage des taches et restes de filigrane
    solid = alpha > 0.5
    min_area = int(opts.get("min_area", max(24, (w * h) // 40000)))
    keep = remove_small_components(solid, min_area)
    # on étend légèrement le masque conservé pour garder l'anticrénelage du trait
    keep_img = Image.fromarray((keep * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3))
    keep = np.asarray(keep_img) > 0
    alpha = np.where(keep, alpha, 0.0).astype(np.float32)

    box = bbox(alpha > 0.05, pad=int(opts.get("pad", 8)))
    if box is None:
        print(f"  ! {path.name}: aucun trait détecté (seuil {thr:.0f}), ignoré")
        return None
    x0, y0, x1, y1 = box
    alpha = alpha[y0:y1, x0:x1]

    stem = slugify(path.stem)
    out_dir.mkdir(parents=True, exist_ok=True)
    png = out_dir / f"{stem}.png"
    size = write_png(alpha, png, int(opts.get("max_size", 1200)))

    sharp = sharpness(alpha)
    do_svg = want_svg and opts.get("svg", sharp >= float(opts.get("svg_min_sharpness", 0.55)))
    svg_path = None
    ncurves = 0
    if do_svg:
        if potrace is None:
            print("  ! potracer manquant : pip install potracer (SVG ignoré)")
        else:
            binary = remove_small_components(alpha > 0.5, min_area)
            svg_path = out_dir / f"{stem}.svg"
            ncurves = write_svg(binary, svg_path, turdsize=int(opts.get("turdsize", 3)),
                                alphamax=float(opts.get("alphamax", 1.0)),
                                opttolerance=float(opts.get("opttolerance", 0.25)))

    if verbose:
        ah, aw = alpha.shape
        msg = (f"  ✓ {path.name:26s} {mode:9s} seuil {thr:5.1f}  netteté {sharp:.2f}  "
               f"→ {png.name} {size[0]}×{size[1]}")
        if svg_path:
            msg += f"  + {svg_path.name} ({ncurves} contours)"
        elif want_svg:
            msg += "  (tracé trop flou pour un SVG propre : PNG seulement)"
        print(msg)
    ah, aw = alpha.shape
    return {"stem": stem, "png": png, "svg": svg_path, "w": aw, "h": ah}


def slugify(s: str) -> str:
    import re, unicodedata
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s or "illustration"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", help="fichiers à traiter (défaut : tout le dossier source)")
    ap.add_argument("--src", type=Path, default=SRC_DIR)
    ap.add_argument("--out", type=Path, default=OUT_DIR)
    ap.add_argument("-t", "--threshold", type=float, help="seuil de luminance 0..255 (défaut : automatique)")
    ap.add_argument("--min-area", type=int, help="taille minimale d'une tache conservée, en pixels")
    ap.add_argument("--no-svg", action="store_true", help="ne pas vectoriser")
    ap.add_argument("--force-svg", action="store_true", help="vectoriser même si le tracé est flou")
    args = ap.parse_args(argv)

    cfg = {}
    if CONFIG.exists():
        cfg = json.loads(CONFIG.read_text(encoding="utf-8"))

    if args.files:
        files = [Path(f) if Path(f).exists() else args.src / f for f in args.files]
    else:
        files = sorted(p for p in args.src.iterdir() if p.suffix.lower() in EXTS) if args.src.exists() else []
    if not files:
        print(f"Aucune image dans {args.src}. Déposez-y les JPG/PNG puis relancez.")
        return 1

    print(f"{len(files)} fichier(s) → {args.out}")
    results = []
    for f in files:
        opts = dict(cfg.get(f.name, {}))
        if args.threshold is not None:
            opts["threshold"] = args.threshold
        if args.min_area is not None:
            opts["min_area"] = args.min_area
        if args.force_svg:
            opts["svg"] = True
        try:
            r = process(f, args.out, opts, want_svg=not args.no_svg)
        except Exception as e:  # on continue avec les autres fichiers
            print(f"  ! {f.name}: {e}")
            r = None
        if r:
            results.append(r)

    if results:
        print("\nÀ coller dans css/style.css (une classe par dessin, ratio = largeur / hauteur) :")
        for r in results:
            target = r["svg"] or r["png"]
            try:
                src = target.relative_to(ROOT)
            except ValueError:
                src = Path(os.path.relpath(target, ROOT))
            print(f'.illu--{r["stem"]:<12} {{ --src: url("../{src.as_posix()}"); --ar: {r["w"]} / {r["h"]}; }}')
    return 0


if __name__ == "__main__":
    sys.exit(main())
