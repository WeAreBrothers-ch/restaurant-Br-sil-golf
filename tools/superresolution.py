#!/usr/bin/env python3
"""
Super-résolution des photos du site Le 9.

Agrandit une photo ×4 avec Real-ESRGAN (« general x4v3 », licence BSD-3) en
nettoyant au passage les carrés de compression JPEG, puis `prepare_photos.py`
la ramène à la taille voulue. Résultat : un bord net là où un simple
agrandissement donne un escalier flou.

Ce que ça ne fait pas : inventer ce qui n'a pas été photographié. Un arrière-plan
flou à la prise de vue (le parcours derrière la table) reste flou ; il est
seulement lissé proprement, sans pixels visibles.

Le modèle (4,8 Mo) n'est pas dans le dépôt. Il est téléchargé une fois dans
`tools/.modeles/` (ignoré par git) au premier lancement.

Dépendances : onnxruntime, numpy, Pillow   (pip install onnxruntime numpy Pillow)
Sans elles, ou sans réseau pour le modèle, `prepare_photos.py` retombe sur un
redimensionnement classique : rien ne casse, la photo est juste moins nette.
"""
import sys
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image

MODELE_URL = ("https://huggingface.co/tamnvcc/Real-ESRGAN-General-x4v3_float/"
              "resolve/main/onnx/model.onnx")
DOSSIER = Path(__file__).resolve().parent / ".modeles"
MODELE = DOSSIER / "realesrgan-general-x4v3.onnx"
ECHELLE = 4
MARGE = 10  # pixels de recouvrement entre deux tuiles, pour ne laisser aucune couture


def disponible() -> bool:
    """Vrai si l'agrandissement peut tourner (onnxruntime présent, modèle récupérable)."""
    try:
        import onnxruntime  # noqa: F401
    except ImportError:
        return False
    if MODELE.exists():
        return True
    try:
        DOSSIER.mkdir(exist_ok=True)
        print(f"  Téléchargement du modèle (4,8 Mo) : {MODELE_URL}")
        urllib.request.urlretrieve(MODELE_URL, MODELE)
        return MODELE.exists() and MODELE.stat().st_size > 1_000_000
    except Exception as e:  # pas de réseau, hôte bloqué…
        print(f"  Modèle indisponible ({e}) : redimensionnement classique.")
        MODELE.unlink(missing_ok=True)
        return False


_session = None


def _session_onnx():
    global _session
    if _session is None:
        import onnxruntime as ort
        opts = ort.SessionOptions()
        _session = ort.InferenceSession(str(MODELE), opts, providers=["CPUExecutionProvider"])
    return _session


def agrandir(im: Image.Image) -> Image.Image:
    """Agrandit ×4 par tuiles (le modèle prend une entrée fixe de 128×128)."""
    sess = _session_onnx()
    entree = sess.get_inputs()[0]
    tuile = entree.shape[2] if isinstance(entree.shape[2], int) else 128
    coeur = tuile - 2 * MARGE
    a = np.asarray(im.convert("RGB"), dtype=np.float32) / 255.0
    h, w, _ = a.shape
    # Marge réfléchie autour de l'image, et de quoi remplir la dernière tuile.
    ap = np.pad(a, ((MARGE, MARGE + coeur), (MARGE, MARGE + coeur), (0, 0)), mode="reflect")
    sortie = np.zeros((h * ECHELLE, w * ECHELLE, 3), dtype=np.float32)
    for y in range(0, h, coeur):
        for x in range(0, w, coeur):
            t = np.ascontiguousarray(ap[y:y + tuile, x:x + tuile].transpose(2, 0, 1)[None])
            o = sess.run(None, {entree.name: t})[0][0].transpose(1, 2, 0)
            hh, ww = min(coeur, h - y), min(coeur, w - x)
            sortie[y * ECHELLE:(y + hh) * ECHELLE, x * ECHELLE:(x + ww) * ECHELLE] = \
                o[MARGE * ECHELLE:(MARGE + hh) * ECHELLE, MARGE * ECHELLE:(MARGE + ww) * ECHELLE]
    return Image.fromarray((np.clip(sortie, 0, 1) * 255 + 0.5).astype(np.uint8))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage : python3 tools/superresolution.py entree.jpg sortie.png")
        sys.exit(1)
    if not disponible():
        sys.exit("Agrandissement indisponible.")
    agrandir(Image.open(sys.argv[1])).save(sys.argv[2])
