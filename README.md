# Le 9 · Restaurant du Golf du Brésil

Site du restaurant Le 9, à Goumoens-le-Jux (VD). Six pages statiques, sans
framework ni étape de compilation : du HTML, du CSS et un fichier JavaScript.

## Les pages

| Fichier | Page | Composition |
|---|---|---|
| `index.html` | Accueil | Premier écran sombre : le sceau et huit dessins, rien d'autre. Puis le bandeau d'accès direct en quatre carrés, deux duos photographie-texte, et le mot de la fin. |
| `le-restaurant.html` | Le restaurant | Titre sur deux colonnes, bande photo pleine largeur, un diptyque puis un contrepoint, le chef, trois repères |
| `la-carte.html` | La carte | Fond sombre, familles de plats sur deux colonnes, trois photographies en respiration, chacune entre deux familles |
| `la-terrasse.html` | La terrasse | Photo panoramique en tête, chapô et trois colonnes de journal, une journée en trois heures |
| `contact.html` | Contact | Informations et plan côte à côte, horaires jour par jour, formulaire, bloc réservation |

Chaque page a sa propre grille. Seuls l'en-tête, le pied de page, les dessins
en fond et le duo (une photographie, un texte) sont communs.

## Pensé pour le téléphone

C'est là que le site sera lu. Tout part de l'écran étroit et monte ensuite.

- **Le premier écran est sombre, plein, et ne porte que le sceau.** Il occupe
  exactement la hauteur de l'écran : rien du bandeau d'en dessous n'y paraît.
  Il s'arrêtait quatre rem et demie plus haut au doigt pour laisser deviner la
  suite, mais un premier écran qui montre la case suivante n'en est plus un.
  Pas de phrase, pas de bouton :
  ce qu'on veut savoir tout de suite est dans le bandeau juste dessous, et le
  nom de la maison est déjà dans le sceau. La phrase qui situe le restaurant
  reste dans le document pour les moteurs et les lecteurs d'écran.
  Il est posé sur le socle, le vert le plus profond de la palette, et le sceau
  comme les huit dessins y passent en crème. Aucun dessin ne touche le sceau :
  la plus petite distance entre un trait et le cercle est de trente-deux
  pixels, mesurée sur douze formats. Le sceau est borné par la hauteur de
  l'écran autant que par sa largeur — c'est cette borne qui garantit les deux
  bandes libres où les dessins se rangent. La page bascule au crème sous le
  bandeau : cette coupure franche est la porte. C'est l'ouverture du site de
  L'Étoile, l'autre restaurant de la maison, dont le premier écran est noir.
  Sur grand écran, le sceau est une île au milieu et les dessins font le tour.
  Sur un téléphone il barre l'écran : il ne reste plus une couronne mais deux
  bandes, quatre dessins au-dessus et quatre en dessous, et aucun n'est coupé
  sur les côtés. **Chacun est posé à sa propre profondeur** — 16, 7, 19 et 10
  pour cent dans la bande du haut — comme chez L'Étoile, où aucun dessin n'est
  à la hauteur de son voisin. Alignés deux par deux, ils faisaient une frise.
- **Rien ne descend sous 13 px** au doigt. Les libellés en capitales espacées,
  les plus durs à lire, montent d'un cran sous 700 px.
- **Aucune cible tactile sous 44 px de haut.** Les liens de liste, les liens
  fléchés et les entrées de sommaire sont élargis là où le pointeur est
  grossier, sans rien changer là où l'on a une souris.
- **Les blocs se recomposent plutôt que de rétrécir.** Le bandeau d'accès
  direct devient quatre cellules sur deux lignes au lieu de quatre colonnes :
  on les voit d'un seul coup d'œil sous le sceau, au lieu de parcourir une
  liste. Elles ne sont pas carrées — elles l'ont été, et le carré creusait
  entre le libellé et sa réponse un trou de cent pixels que rien ne
  remplissait. Hauteur fixe et courte, contenu centré dedans, une flèche au
  bout du libellé : c'est le bandeau de L'Étoile, dans sa mécanique exacte.
  Les filets ne doublent jamais celui de la bande ni celui du bord, et les
  quatre réponses tiennent chacune sur une ligne — dès que l'une passe à la
  ligne, sa cellule décale son libellé et la rangée boite.
  Les repères chiffrés passent côte à côte. Le récit passe en colonne unique,
  titre avant photo. L'heure de la terrasse passe au-dessus de son titre.
- **Une barre d'appel reste au bas de l'écran** avec le numéro et l'itinéraire,
  les deux seules choses qu'on veut faire depuis un téléphone devant un site de
  restaurant. Elle monte une fois le premier écran passé et s'efface pendant la
  saisie d'un champ, pour ne pas se poser sur le clavier.
- **Le pied de page tient en trois temps**, comme celui de L'Étoile :
  l'enseigne et la phrase qui situe la maison, les coordonnées en colonnes à
  libellés, la mention légale. Deux filets séparent les trois. Il n'y a **pas
  de liste des pages** : elles sont dans l'en-tête, collé en haut de l'écran,
  et dans le menu du téléphone — personne ne descend au bas d'une page pour y
  chercher une navigation qui n'a jamais quitté l'écran. Il fait 646 px au
  doigt, contre 1148 à l'origine.
- **Le menu est un vrai `<dialog>`** ouvert en modal : le piégeage du focus, la
  touche Échap et le rôle de dialogue sont assurés par le navigateur. Il occupe
  tout l'écran, en vert profond, et les liens y sont composés dans le serif des
  titres, à la taille où on les lit sans viser.
- Vérifié à 360, 390 et 430 px de large.

## Les compositions photographiques

Une photographie posée à côté d'un paragraphe, répétée trois fois, c'est ce que
fait n'importe quel gabarit. Chaque page en a donc une qui lui est propre.

**Le diptyque** (page « Le restaurant », premier bloc). Une grande
photographie en paysage à droite du texte, et une seconde en portrait qui vient
mordre son angle inférieur gauche — un quart de sa largeur, pas plus — et pend
en dessous d'un quart de sa hauteur. Elle commence une gouttière après la
colonne de texte : elle mord la photographie, jamais un mot. Le liseré crème
autour de la petite la décolle de la grande ; sans lui les deux images se
touchent et l'œil ne sait plus laquelle il regarde.

**Le contrepoint** (page « Le restaurant », second bloc). Le titre est posé
dans le bas de la photographie, sur un aplat crème à sa taille : une entaille
dans l'image, pas une carte qui flotte dessus. Le texte suit en dessous, et
part de la colonne où pend la petite photographie du diptyque : les deux blocs
partagent un axe. C'est l'inverse exact du premier bloc : là le texte était à
côté, ici il est dedans.

**Le duo** (page « Accueil »). Une photographie et un texte côte à côte, la
photographie sur six colonnes, le texte sur cinq, et la gouttière du milieu
vide : c'est ce vide, et non un filet, qui les sépare. Les côtés s'inversent
d'un duo à l'autre.

C'est la disposition de L'Étoile, pas son nombre. Chez eux la page d'accueil
compte une quinzaine de photographies ; ici il y en a **deux**. L'accueil en
a porté neuf — un ruban, un duo, trois
cartes de plat, une paire, un second duo — et c'était une galerie. Jamais
deux images à la suite, jamais une grille : une image, un texte, et l'on
passe à autre chose.

Les deux sont choisies pour ce premier écran-là, pas pour ce qu'elles
montrent. L'assiette est sombre, vert et orange sur fond noir : elle prolonge
le socle du sceau. La terrasse porte le vert des chaises et la lumière du
soir. Les deux vivent dans la palette de la maison.

**Les heures** (page « La terrasse »). Une journée en trois temps, réglée
comme une grille horaire : un filet, l'heure dans la marge, le texte à côté,
la photographie au bout de la ligne. L'heure est un **chiffre de chapitre**,
le seul nombre écrit grand de tout le site : au corps d'un sous-titre, elle
laissait deux cents pixels de vide à gauche de chaque rangée.

L'heure et le texte se **centrent sur la photographie**, deux fois plus haute
qu'eux. Calés en haut, ils laissaient sous eux quatre cents pixels de vide
jusqu'au filet suivant ; poussé au bas de la colonne pour la tenir, le lien
se retrouvait seul, à deux cent quarante pixels de son paragraphe. Centrés,
le vide se partage au-dessus et au-dessous, et le filet du haut suffit à dire
où la rangée commence.

**Le cadre est celui de la photographie.** Les deux originaux sont en trois
quarts — 1400 sur 1867 et 1000 sur 1333. Le cadre était en cinq quarts : il
en retirait deux cent huit pixels, cent quatre en haut et cent quatre en bas,
c'est-à-dire la bouteille tranchée par le milieu et la garniture de
l'assiette. On ne voyait plus une photographie mais une photographie coupée.
Le cadre est maintenant exactement celui de l'image, et rien n'en est retiré.

**Au doigt, une photographie pleine largeur ne se sépare pas d'un bloc
pleine largeur par une bande de crème.** Elle en touche le bord. Sur
l'accueil, la première photographie commence au filet du bandeau d'accès
direct ; sur la terrasse, la dernière touche le panneau vert. Entre deux
aplats qui vont d'un bord à l'autre, les cinquante pixels de marge d'une
section ne se lisent pas comme une respiration mais comme une couture, et
l'on croit à un défaut d'affichage.

**Au doigt, la dernière photographie touche le vert.** Elle va d'un bord à
l'autre de l'écran et le panneau qui la suit aussi ; entre les deux restait
la marge basse de la section — cinquante pixels de crème sur toute la largeur
entre deux aplats pleine page. Ce n'est pas une respiration, c'est une
couture : on croit à un défaut d'affichage. Sur grand écran la photographie
tient dans ses colonnes et ne touche aucun bord, la marge y reste.

Celle du milieu n'a pas de photographie — mais une phrase prend sa place, à
l'endroit exact où les deux autres ont la leur. Vide, la moitié droite de la
rangée se lisait comme une image qui n'aurait pas chargé ; ainsi, la
respiration est voulue et elle se voit.

**Le chapô et les colonnes** (page « La terrasse »). Le texte d'ouverture
tenait dans une colonne étroite et centrée, avec une lettrine : sur un grand
écran il flottait au milieu de la page, sans rapport avec la grille des
heures juste en dessous. Il prend la même largeur qu'elle — une phrase
d'ouverture dans le corps des titres, puis trois colonnes de journal. La
lettrine est retirée : le chapô ouvre déjà le texte, et deux ouvertures l'une
sur l'autre n'en font aucune.

Il n'y a que **deux prises de vue de la terrasse** dans toute la maison : la
table sous le grand arbre, et la table ouverte sur le parcours. La page en
montrait trois à la suite, dont le bandeau du haut : on regardait trois fois
la même bouteille. Elle en montre maintenant deux, plus une assiette servie
dehors, chacune une seule fois. Avant d'ajouter une image ici, vérifier
qu'elle ne redit pas celle d'au-dessus.

**Rien ne défile sur le côté.** On ne demande pas à quelqu'un de faire glisser
une bande pour voir ce qu'on avait à lui montrer : tout est là du premier coup
d'œil. Au doigt, chaque composition garde son geste, en plus court : la grande
photographie du diptyque prend toute la largeur de l'écran, la petite sort par
la droite et mord son angle, et le lien vers la carte se pose dans l'angle
qu'elle laisse libre, calé sur son bord inférieur ; le titre de la salle
remonte sur la photographie depuis le bord de l'écran ; l'heure de la terrasse
passe au-dessus de son titre. Sur tablette, où les chevauchements manquent de
largeur, il ne reste que les décalages verticaux.

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
js/main.js                     menu, apparitions, filet de l'en-tête
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

Chercher `TODO` dans les fichiers HTML. **Rien n'est plus marqué à l'écran.**
Les étiquettes « à confirmer », « à valider », « à vérifier » et les notes qui
les accompagnaient sont retirées : le site se lit comme un site fini.

Ce qu'elles signalaient n'est pas résolu pour autant — le nom du chef, la
capacité de la salle, le parking, les prix de la carte et la source de la
citation de presse restent à valider. La liste est ci-dessous, et chaque
endroit porte un commentaire `TODO` dans le HTML, à l'aplomb de la ligne
concernée.

- **Formulaire de contact** : il poste vers un service de réception qui
  transmet le message par courriel. Remplacer l'adresse de l'attribut `action`
  dans `contact.html` par la vôtre (Formspree, Basin, Formcarry, ou un script
  sur votre hébergement). Tant que ce n'est pas fait, l'envoi échoue et le
  visiteur est renvoyé vers le téléphone.
- **Carte** : plats et prix relevés sur une fiche en ligne de 2024, à valider avec la cuisine.
- **Carte en PDF** : le lien est retiré de `la-carte.html` tant que le fichier
  n'existe pas — il menait à une page d'erreur. Déposer le PDF dans
  `assets/carte.pdf` et remettre la ligne indiquée dans le commentaire.
- **Citation de presse** : la page de la terrasse affirme que la maison est
  citée parmi les « 100 terrasses de rêve ». La source venait d'une fiche de
  l'office du tourisme et n'est pas confirmée. La mention « source à préciser »
  qui l'accompagnait est retirée : la phrase est donc affirmée sans réserve.
  À vérifier avant la mise en ligne, ou à supprimer.
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
