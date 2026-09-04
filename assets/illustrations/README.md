# Illustrations

- `source/` : les dessins d'origine, tels que fournis. Non utilisés par le site.
- `dist/` : ce que le site sert. Une seule couleur, donnée par le CSS.

Six dessins : deux golfeurs, des clubs croisés, une bouteille et un verre, une
assiette dressée, un chef à la cloche.

## Régénérer dist/

```
pip install Pillow numpy potracer
python3 tools/process_illustrations.py
```

Le script sort pour chaque dessin un PNG transparent et, si le tracé est net, un
SVG en `fill="currentColor"`, puis affiche les lignes CSS correspondantes.

## Ce qu'il fait

1. **Détourage** par écart à la couleur du fond, déduite du pourtour de l'image.
   C'est ce qui permet de traiter aussi bien un trait noir sur blanc qu'une
   silhouette verte sur gris, ou le golfeur en noir et blanc sur fond vert dont
   le pantalon aurait disparu avec un simple seuil de noirceur.
2. **Nettoyage** : les filigranes des banques d'images (123RF, Adobe Stock), les
   liserés blancs de sticker et les petites taches sont retirés.
3. **Recolorisation** : le fichier ne contient aucune couleur. Le PNG est du noir
   sur transparent utilisé en masque, le SVG est en `currentColor`. La couleur
   vient de la variable `--illu` dans `css/base.css`.

## Réglages

`tools/illustrations.json` contient un réglage par fichier quand le réglage
automatique ne suffit pas :

| Clé | Effet |
|---|---|
| `threshold` | écart minimal à la couleur du fond, de 0 à 255 |
| `min_area` | taille minimale d'une tache conservée, en pixels ; c'est ce qui efface les mentions des banques d'images |
| `softness` | douceur du bord, pour garder l'anticrénelage |
| `mode` | `color` (défaut) ou `luminance` |
| `background` | forcer la couleur du fond, par exemple `[255, 255, 255]` |
| `svg` | forcer ou empêcher la vectorisation |

Après un ajout ou un changement de dessin, reporter les lignes affichées par le
script dans `css/base.css` (bloc `.i-*`) et vérifier le ratio.

## Provenance

Les dessins viennent de banques d'images. Vérifier que les licences couvrent
l'usage commercial sur le site avant la mise en ligne, en particulier pour les
fichiers qui portaient un filigrane.
