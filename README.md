# Le 9 · Restaurant du Golf du Brésil

Site vitrine statique du restaurant Le 9, à Goumoens-le-Jux (VD).
HTML, CSS et un peu de JavaScript, sans framework ni étape de build.

## Structure

```
index.html                     la page (sections : hero, restaurant, carte, terrasse, horaires, contact)
css/style.css                  toute la mise en forme ; les couleurs sont des variables en tête de fichier
js/main.js                     menu mobile, apparition au défilement, photos manquantes
assets/illustrations/source/   dessins d'origine (à déposer)
assets/illustrations/dist/     dessins servis par le site, une seule couleur pilotée par le CSS
assets/photos/                 photos (voir le README du dossier pour les noms attendus)
assets/logo/                   logo Le 9 (à déposer, voir ci-dessous)
tools/process_illustrations.py détourage, nettoyage et vectorisation des dessins
```

## Tester en local

Ouvrir `index.html` dans un navigateur suffit. Pour un serveur local :

```
python3 -m http.server 8000
```

puis http://localhost:8000.

## Changer la palette

Toutes les couleurs sont dans le bloc `:root` de `css/style.css` :

```css
--c-cream, --c-cream-2, --c-cream-3    fonds et filets clairs
--c-green, --c-green-deep, --c-green-soft   verts (texte fort, sections sombres, dessins)
--c-gold                               accent
--illu-color, --illu-opacity           couleur et opacité des dessins en fond
```

Les sections sombres (`.section--dark`) ne font que redéfinir ces variables.

## Illustrations

Déposer les JPG/PNG dans `assets/illustrations/source/` puis :

```
pip install Pillow numpy potracer
python3 tools/process_illustrations.py
```

Le script sort un PNG transparent par dessin (et un SVG `currentColor` si le
tracé est net) dans `dist/`, et affiche les lignes CSS à coller. Les dessins
sont placés dans `index.html` avec des variables inline :

```html
<div class="illu illu--chef" style="--x:4%; --y:54%; --w:165px; --r:3deg"></div>
```

`--x` / `--y` position, `--w` largeur, `--r` rotation, `--mx` / `--my` position
sur mobile. `data-hide="mobile"` masque le dessin sur mobile,
`data-hide="tablet"` dès la tablette.

## Ce qu'il reste à remplir

Chercher `TODO` dans `index.html`. En résumé :

- **Logo** : déposer `assets/logo/le9.svg` (ou .png) et remplacer le bloc `.logo` du hero.
- **Photos** : voir `assets/photos/README.md`.
- **Carte** : plats et prix relevés sur une fiche en ligne de 2024, à valider avec la cuisine.
- **Horaires** : les sources se contredisent (lundi ouvert ou fermé), la grille est en « à confirmer ».
- **À vérifier** : nom du chef, terrasse couverte, parking, source de la citation presse, lien vers L'Étoile.

## Déployer sur GitHub Pages

Le site est à la racine du dépôt et n'utilise que des chemins relatifs.

1. Fusionner la branche dans `main`.
2. Dans le dépôt GitHub : **Settings → Pages → Build and deployment → Source : GitHub Actions**.
3. Le workflow `.github/workflows/deploy-pages.yml` publie le site à chaque push sur `main`.

Sans le workflow, l'option « Deploy from a branch » (branche `main`, dossier `/`)
fonctionne aussi. Le fichier `.nojekyll` est là pour que GitHub serve les
fichiers tels quels.
