# Le 9 · Restaurant du Golf du Brésil

Site du restaurant Le 9, à Goumoens-le-Jux (VD). Six pages statiques, sans
framework ni étape de compilation : du HTML, du CSS et un fichier JavaScript.

## Les pages

| Fichier | Page | Composition |
|---|---|---|
| `index.html` | Accueil | Logo au centre, dessins autour, bandeau d'infos, quatre entrées en escalier |
| `le-restaurant.html` | Le restaurant | Titre sur deux colonnes, bande photo pleine largeur, récit en blocs alternés, portrait du chef, trois repères |
| `la-carte.html` | La carte | Fond sombre, sommaire collant à gauche, familles de plats sur deux colonnes |
| `les-plats.html` | Les plats | Mosaïque de douze photos en pleine largeur, visionneuse au clic |
| `la-terrasse.html` | La terrasse | Photo panoramique en tête, texte en deux colonnes façon journal, bande de photos qui défile |
| `contact.html` | Contact | Informations et plan côte à côte, horaires jour par jour, bloc réservation |

Chaque page a sa propre grille. Seuls l'en-tête, le pied de page et les dessins
en fond sont communs.

## Arborescence

```
css/base.css                   variables, typographie, en-tête, pied, dessins
css/pages.css                  la composition de chaque page
js/main.js                     menu, visionneuse, apparition au défilement
assets/illustrations/source/   les dessins d'origine
assets/illustrations/dist/     les dessins servis par le site (une seule couleur)
assets/photos/                 les photos (voir le README du dossier)
assets/logo/                   le logo Le 9 (à déposer)
tools/process_illustrations.py détourage, nettoyage et vectorisation
tools/illustrations.json       réglages par dessin
```

## Tester en local

```
python3 -m http.server 8000
```

puis http://localhost:8000. Ouvrir les fichiers directement (`file://`) fonctionne
aussi, sauf les dessins en fond : les masques CSS ont besoin d'un serveur.

## Changer la palette

Tout est dans le bloc `:root` de `css/base.css` :

| Variable | Rôle |
|---|---|
| `--c-cream`, `--c-cream-2`, `--c-cream-3` | fonds clairs et filets |
| `--c-green`, `--c-green-deep`, `--c-sage` | vert principal, sections sombres, dessins |
| `--c-brass` | accent : étiquettes, prix, liens |
| `--illu`, `--illu-opacity` | couleur et opacité des dessins en fond |

Les zones sombres (classe `dark`) ne font que redéfinir ces variables : changer
la palette suffit, il n'y a aucune couleur écrite en dur ailleurs.

## Les dessins

Six dessins au trait, dispersés en fond, tous dans la même couleur. Ils sont la
seule chose que le site partage avec L'Étoile, l'autre restaurant de la maison.

Pour les regénérer depuis les originaux :

```
pip install Pillow numpy potracer
python3 tools/process_illustrations.py
```

Le script détoure par écart à la couleur du fond (et non par simple noirceur),
ce qui traite aussi bien un trait noir sur blanc qu'une silhouette verte sur gris
ou un aplat blanc sur fond vert. Il retire les filigranes des banques d'images,
les liserés et les petites taches, puis sort un PNG transparent et un SVG en
`fill="currentColor"`. Les réglages par fichier sont dans `tools/illustrations.json`.

Placement dans les pages :

```html
<div class="illu i-chef" style="--x:5%; --y:58%; --w:170px; --r:3deg; --mx:0%; --my:77%"></div>
```

`--x` `--y` position, `--w` largeur, `--r` rotation, `--mx` `--my` position sur
mobile. `data-hide="lg"` retire le dessin sous 1180 px, `"md"` sous 860 px,
`"sm"` sous 620 px.

## Les photos

Voir `assets/photos/README.md` pour la liste des noms attendus. Tant qu'un
fichier manque, la page affiche un cadre qui indique le nom à déposer. Une fois
toutes les photos en place, remplacer `data-slots="show"` par `data-slots="hide"`
sur la balise `<body>` de chaque page : les cadres restants disparaîtront.

## Ce qu'il reste à compléter

Chercher `TODO` dans les fichiers HTML.

- **Logo** : déposer `assets/logo/le9.svg`, puis remplacer le bloc `.mono` du hero dans `index.html`.
- **Photos** : douze plats, trois vues de salle, quatre de terrasse, un portrait du chef.
- **Carte** : plats et prix relevés sur une fiche en ligne de 2024, à valider avec la cuisine.
- **Horaires** : les sources se contredisent sur le lundi, la grille est en « à confirmer ».
- **À vérifier** : nom du chef, capacité de la salle, terrasse couverte, parking, source de la citation presse, adresse du site de L'Étoile.
- **Numéro de téléphone** : la fiche de l'office du tourisme indique 021 732 26 46, le site utilise le 021 882 24 19 que vous m'avez donné.

## Mettre en ligne sur GitHub Pages

Le site est à la racine du dépôt et n'utilise que des chemins relatifs.

1. Fusionner la branche dans `main`.
2. Dans le dépôt : **Settings → Pages → Build and deployment → Source : GitHub Actions**.
3. Le workflow `.github/workflows/deploy-pages.yml` publie à chaque push sur `main`.

L'option « Deploy from a branch » (branche `main`, dossier `/`) fonctionne aussi.
Le fichier `.nojekyll` fait servir les fichiers tels quels.
