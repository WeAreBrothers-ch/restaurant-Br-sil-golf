# Le 9 · Restaurant du Golf du Brésil

Site du restaurant Le 9, à Goumoens-le-Jux (VD). Six pages statiques, sans
framework ni étape de compilation : du HTML, du CSS et un fichier JavaScript.

## Les pages

| Fichier | Page | Composition |
|---|---|---|
| `index.html` | Accueil | Le premier écran ne porte que le sceau et huit dessins, rien d'autre. Puis un bandeau d'accès direct et trois entrées en escalier. |
| `le-restaurant.html` | Le restaurant | Titre sur deux colonnes, bande photo pleine largeur, un diptyque puis un contrepoint, le chef, trois repères |
| `la-carte.html` | La carte | Fond sombre, sommaire collant à gauche, familles de plats sur deux colonnes, trois photographies en respiration |
| `la-terrasse.html` | La terrasse | Photo panoramique en tête, texte en deux colonnes façon journal, trois photos en salon |
| `contact.html` | Contact | Informations et plan côte à côte, horaires jour par jour, formulaire, bloc réservation |

Chaque page a sa propre grille. Seuls l'en-tête, le pied de page et les dessins
en fond sont communs.

## Pensé pour le téléphone

C'est là que le site sera lu. Tout part de l'écran étroit et monte ensuite.

- **Le premier écran ne porte que le sceau.** Pas de phrase, pas de bouton :
  ce qu'on veut savoir tout de suite est dans le bandeau juste dessous, et le
  nom de la maison est déjà dans le sceau. La phrase qui situe le restaurant
  reste dans le document pour les moteurs et les lecteurs d'écran.
  Sur grand écran, le sceau est une île au milieu et les dessins font le tour.
  Sur un téléphone il barre l'écran : il ne reste plus une couronne mais deux
  bandes, quatre dessins au-dessus et quatre en dessous, en quinconce, et aucun
  n'est coupé sur les côtés.
- **Rien ne descend sous 13 px** au doigt. Les libellés en capitales espacées,
  les plus durs à lire, montent d'un cran sous 700 px.
- **Aucune cible tactile sous 44 px de haut.** Les liens de liste, les liens
  fléchés et les entrées de sommaire sont élargis là où le pointeur est
  grossier, sans rien changer là où l'on a une souris.
- **Les blocs se recomposent plutôt que de rétrécir.** Le bandeau d'accès
  direct devient quatre carrés en deux lignes au lieu de quatre bandes
  empilées. Les trois entrées de l'accueil prennent une vignette carrée à
  gauche et le texte à droite, au lieu de trois photos plein cadre. Les repères
  chiffrés passent côte à côte. Le sommaire de la carte devient une rangée de
  pastilles. Le récit passe en colonne unique, titre avant photo.
- **Une barre d'appel reste au bas de l'écran** avec le numéro et l'itinéraire,
  les deux seules choses qu'on veut faire depuis un téléphone devant un site de
  restaurant. Elle monte une fois le premier écran passé et s'efface pendant la
  saisie d'un champ, pour ne pas se poser sur le clavier.
- **Le pied de page tient en trois temps** à toutes les tailles : la maison,
  les coordonnées, les pages. L'adresse et le contact restent côte à côte même
  sur un téléphone, et les pages sont une simple ligne de liens. Il portait
  quatre colonnes qui devenaient quatre pavés empilés : 1148 px de défilement
  pour une adresse et un numéro, contre 653 aujourd'hui.
- **Le menu est un vrai `<dialog>`** ouvert en modal : le piégeage du focus, la
  touche Échap et le rôle de dialogue sont assurés par le navigateur. Il occupe
  tout l'écran, en vert profond, et les liens y sont composés dans le serif des
  titres, à la taille où on les lit sans viser.
- Vérifié à 360, 390 et 430 px de large.

## Les compositions photographiques

Une photographie posée à côté d'un paragraphe, répétée trois fois, c'est ce que
fait n'importe quel gabarit. Chaque page en a donc une qui lui est propre.

**Le diptyque** (page « Le restaurant », premier bloc). Une grande
photographie en paysage, et une seconde en portrait qui vient la mordre par en
dessous. Elle commence après la colonne de texte : elle mord la photographie,
jamais un mot. Le liseré crème autour de la petite la décolle de la grande ;
sans lui les deux images se touchent et l'œil ne sait plus laquelle il regarde.

**Le contrepoint** (page « Le restaurant », second bloc). Le texte est posé
par-dessus le bas de la photographie, sur un aplat crème. C'est l'inverse exact
du premier bloc : là le texte était à côté, ici il est dedans.

**Le salon** (page « La terrasse »). Deux colonnes dont la seconde démarre plus
bas : c'est ce seul décalage qui fait la composition. Aucune image n'en recouvre
une autre, aucune ne recouvre un mot. Un mot posé entre deux images, à la place
d'une troisième, empêche l'ensemble de se lire comme une planche-contact.

**Rien ne défile sur le côté.** On ne demande pas à quelqu'un de faire glisser
une bande pour voir ce qu'on avait à lui montrer : tout est là du premier coup
d'œil. Au doigt, les chevauchements disparaissent — ils demandent de la largeur
— et il ne reste que les décalages verticaux.

## Le mouvement

Trois mécaniques, toutes désactivées si le système demande un mouvement réduit.

**Le premier écran.** Tout tient dans un seul nombre, `--p`, l'avancée du
premier défilement de 0 à 1. Le script `js/hero.js` ne fait qu'écrire ce nombre ;
c'est la feuille de style qui en tire la chute et la vrille de chacun des huit
dessins. Une écriture par image de rendu, pas huit, et le navigateur compose sur
la carte graphique. Passé le premier écran, plus rien n'est écrit.

Le même nombre sert à l'arrivée : les dessins entrent depuis `--p: -0.35`, un
peu plus haut et penchés dans l'autre sens, avec un retard échelonné. Le geste
d'arrivée et le geste de départ sont le même mouvement joué à l'envers.

Chaque dessin porte cinq réglages et rien d'autre : sa position, sa largeur, sa
pente au repos, sa chute et sa vrille. Chute et vrille changent de valeur et de
signe d'un dessin à l'autre : c'est ce qui donne l'impression d'un désordre
alors que chaque position est choisie.

**Les apparitions.** Un bloc marqué `data-reveal` monte de quelques millimètres
et se révèle une seule fois, quand son haut atteint le bas de l'écran. Le script
`js/amorce.js`, seul fichier chargé sans `defer`, pose l'attribut `data-js`
avant le premier affichage : sans lui les blocs apparaîtraient une fois en
clair avant de sauter à leur position de départ.

**La dérive.** Les dessins posés dans le flux descendent lentement pendant qu'on
les dépasse et se redressent en chemin ; les grandes photographies suivent le
doigt dans leur cadre. C'est tenu par le défilement lui-même, sans JavaScript.
Là où le navigateur ne connaît pas encore cette mécanique, tout est simplement
immobile.

## Arborescence## Arborescence

```
css/base.css                   variables, typographie, en-tête, pied, dessins
css/pages.css                  la composition de chaque page
js/amorce.js                   pose data-js avant le premier affichage
js/main.js                     menu, apparitions, sommaire actif
js/hero.js                     le mouvement du premier écran
js/barre.js                    la barre d'appel du téléphone
js/formulaire.js               validation et envoi du formulaire de contact
assets/illustrations/source/   les dessins d'origine
assets/illustrations/dist/     les dessins servis par le site (une seule couleur)
assets/photos/source/          les photos d'origine
assets/photos/                 les photos servies, produites par le script
assets/logo/                   le sceau Le 9, en courbes et en source modifiable
tools/process_illustrations.py détourage, nettoyage et vectorisation des dessins
tools/illustrations.json       réglages par dessin
tools/prepare_photos.py        recadrage, redimensionnement et compression des photos
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

### Les placer dans une page

Deux façons, selon l'endroit.

**Posé librement**, quelque part dans la section :

```html
<div class="illu i-clubs" style="--x:20%; --y:80%; --w:115px; --r:-9deg"></div>
```

**Accroché au bord de la colonne de texte**, ce qui le fait mordre le bord de
page sur les écrans étroits et le laisse entier dans la marge sur les larges :

```html
<div class="illu i-chef" data-side="l" style="--y:58%; --w:170px; --in:0px"></div>
```

| Variable | Rôle |
|---|---|
| `--x` `--y` | position, en pourcentage de la section |
| `--w` | largeur |
| `--r` | rotation |
| `--mx` `--my` | position sur mobile, si elle doit différer |
| `--in` | de combien le dessin mord sur la colonne de texte, avec `data-side` |

`data-side="l"` ou `"r"` accroche le dessin au bord gauche ou droit du contenu.
`data-hide="lg"` le retire sous 1180 px, `"md"` sous 860 px, `"sm"` sous 620 px.

### Les rendre plus ou moins présents

Deux réglages, dans `css/base.css` :

- `--illu-opacity` : 0,45 sur fond clair, 0,26 sur fond sombre, 0,16 dans le pied.
- `thicken` dans `tools/illustrations.json` : épaissit le trait à la source. Les
  trois dessins au trait fin sont à 2 px ; au-delà leurs boucles se referment.

### Vérifier qu'aucun dessin ne passe sous un texte

Un dessin est du décor : il ne doit jamais gêner la lecture. Le contrôle a été
fait à 390, 430, 620, 760, 900, 1024, 1280, 1440 et 1920 px, en mesurant les
rectangles de chaque dessin et de chaque bloc de texte. Après un déplacement,
refaire cette vérification à plusieurs largeurs.

## Les photos

Voir `assets/photos/README.md` pour la liste des noms attendus. Tant qu'un
fichier manque, la page affiche un cadre qui indique le nom à déposer. Une fois
toutes les photos en place, remplacer `data-slots="show"` par `data-slots="hide"`
sur la balise `<body>` de chaque page : les cadres restants disparaîtront.

## Le logo

Le sceau du hero a été redessiné d'après le filigrane visible sur les photos de
la maison, puis converti en courbes : il est net à toutes les tailles et prend
la couleur du contexte. Voir `assets/logo/README.md`. Si le fichier vectoriel
d'origine existe quelque part, il suffit de le mettre à la place de
`assets/logo/le9.svg`.

## Ce qu'il reste à compléter

Chercher `TODO` dans les fichiers HTML.

- **Formulaire de contact** : il poste vers un service de réception qui
  transmet le message par courriel. Remplacer l'adresse de l'attribut `action`
  dans `contact.html` par la vôtre (Formspree, Basin, Formcarry, ou un script
  sur votre hébergement). Tant que ce n'est pas fait, l'envoi échoue et le
  visiteur est renvoyé vers le téléphone.
- **Carte** : plats et prix relevés sur une fiche en ligne de 2024, à valider avec la cuisine.
- **Horaires** : les sources se contredisent sur le lundi, la grille est en « à confirmer ».
- **Photos manquantes** : le chef, une vraie photo de salle en haute définition, quelques plats de plus. Voir `assets/photos/README.md`.
- **À vérifier** : nom du chef, capacité de la salle, terrasse couverte, parking, source de la citation presse, adresse du site de L'Étoile.
- **Numéro de téléphone** : la fiche de l'office du tourisme indique 021 732 26 46, le site utilise le 021 882 24 19 que vous m'avez donné.
- **Droits des dessins** : ils viennent de banques d'images, vérifier que les licences couvrent l'usage sur le site.

## Mettre en ligne sur GitHub Pages

Le site est à la racine du dépôt et n'utilise que des chemins relatifs.

1. Fusionner la branche dans `main`.
2. Dans le dépôt : **Settings → Pages → Build and deployment → Source : GitHub Actions**.
3. Le workflow `.github/workflows/deploy-pages.yml` publie à chaque push sur `main`.

L'option « Deploy from a branch » (branche `main`, dossier `/`) fonctionne aussi.
Le fichier `.nojekyll` fait servir les fichiers tels quels.
