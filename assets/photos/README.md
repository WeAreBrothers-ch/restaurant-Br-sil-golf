# Photos

> **Ne pas supprimer les fichiers `.jpg` de ce dossier.** Ce sont ceux que le
> site affiche : recadrés, redimensionnés et compressés à partir des originaux.
> Les originaux, eux, vivent dans `source/` et ne sont jamais servis au visiteur.
> Pour ajouter une photo, la déposer dans `source/`, ajouter sa ligne dans
> `tools/prepare_photos.py`, puis relancer le script.

Deux dossiers :

- `source/` : les photos telles que vous les avez fournies. On n'y touche pas.
- ce dossier : les fichiers que le site affiche, produits à partir de `source/`.

## Regénérer les fichiers du site

```
pip install Pillow
python3 tools/prepare_photos.py
```

Le script recadre au bon format, redimensionne et compresse. Les deux photos de
terrasse pesaient près de 6 Mo chacune en PNG ; le site sert au total moins de
4 Mo pour treize images. Il retire aussi les bandes noires et les flèches de
navigation qui traînaient sur les bords des captures d'origine.

Pour changer un cadrage, modifier la liste `DERIVES` en tête du script : chaque
ligne indique le format voulu et le point de l'image à garder au centre.

## Chaque photo existe en deux tailles

À côté de chaque grande photo vit sa jumelle de 1200 px, `<nom>-1200.jpg`. Les
pages déclarent les deux dans `srcset` et le navigateur choisit : la grande sur
un écran d'ordinateur, la jumelle au doigt. Les jumelles sont produites par
`tools/prepare_photos.py` — ne pas les modifier à la main, et **ne pas les
lister dans le tableau ci-dessous** : elles suivent leur aînée.

**Pourquoi 1200 px.** Un téléphone récent affiche en 390 px CSS mais possède
1170 pixels physiques (écran ×3). Une jumelle de 800 px y était étirée d'un
tiers. Et les valeurs de `sizes` doivent dire la vérité : un `sizes="62vw"` sur
une photo qui occupe toute la largeur de l'écran fait choisir au navigateur
un fichier trop petit. Les pages portent maintenant la largeur réellement
occupée (`100vw` au doigt, la part de la grille sur ordinateur).

## Des photos nettes : la super-résolution

Plusieurs photos d'origine sont plus petites que la place qu'elles occupent :
des photos de téléphone de 1000 px posées sur 1640 px de large sur un écran
Retina, une vue de la salle de 900 px, et deux « HD » de terrasse annoncées à
2296 px mais dont le détail réel ne dépasse guère 600 px.

`tools/prepare_photos.py` les agrandit avec Real-ESRGAN (`tools/superresolution.py`,
modèle de 4,8 Mo téléchargé au premier lancement dans `tools/.modeles/`, non
versionné), qui nettoie au passage les carrés de compression, puis les ramène
à la taille voulue. Sans `onnxruntime` ou sans réseau, le script se rabat sur un
redimensionnement classique : rien ne casse.

```
pip install Pillow onnxruntime numpy
python3 tools/prepare_photos.py                              # tout
python3 tools/prepare_photos.py --seulement plat-02.jpg      # une seule photo
python3 tools/prepare_photos.py --sans-agrandissement        # sans super-résolution
```

Ce que ça ne fait pas : inventer du détail qui n'a pas été photographié. Un
arrière-plan flou à la prise de vue reste flou, mais lissé proprement. Une vraie
photo en haute définition restera toujours préférable (voir « Ce qui manque »).

## Deux cadrages pour téléphone

Sur un téléphone, deux bandeaux posent un panorama dans une boîte qui n'a pas sa
forme : « La terrasse » dans une boîte **portrait** de 390 × 620, « Le restaurant »
dans une boîte presque carrée. Le panorama y était agrandi près de trois fois.
Ils ont donc chacun un cadrage dédié, servi sous 700 px par une balise
`<picture>` :

| Fichier | Remplace, sur téléphone | Forme |
|---|---|---|
| `terrasse-pano-m.jpg` | `terrasse-pano.jpg` | portrait 5/8 |
| `lieu-pano-m.jpg` | `lieu-pano.jpg` | 4/3 |

## Ce que le site utilise aujourd'hui

| Fichier | Vient de | Où il apparaît |
|---|---|---|
| `plat-01.jpg` | nourriture.jpg | accueil (premier duo), carte, le restaurant |
| `plat-02.jpg` | nourriture 2.jpg | carte |
| `plat-03.jpg` | caption.jpg | terrasse, l'heure du déjeuner |
| `plat-04.jpg` | viande.jpg | carte, le restaurant |
| `plat-05.jpg` | img-20190316… | en réserve, plus affichée |
| `plat-06.jpg` | 20180714… | en réserve, plus affichée |
| `lieu-pano.jpg` | le9_barolo_terrasse | bande large de la page « Le restaurant » |
| `terrasse-pano.jpg` | le9_terrasse_coucher_soleil | photo de tête de la page « La terrasse » |
| `terrasse-01.jpg` | le9_barolo_terrasse | terrasse, l'heure du soir |
| `terrasse-02.jpg` | le9_terrasse_coucher_soleil | en réserve, plus affichée |
| `terrasse-03.jpg` | le9_barolo_terrasse | en réserve, plus affichée |
| `terrasse-04.jpg` | le9_terrasse_coucher_soleil | accueil (second duo) |
| `salle-01.jpg` | une-vue-imprenable-sur | le restaurant, la vue depuis la salle |
| `terrasse-pano-m.jpg` | le9_terrasse_coucher_soleil | cadrage téléphone de « La terrasse » (voir plus haut) |
| `lieu-pano-m.jpg` | le9_barolo_terrasse | cadrage téléphone de « Le restaurant » (voir plus haut) |

## L'accueil n'affiche que deux photographies

C'est voulu. Le sceau et les huit dessins du premier écran sont son image ;
les quatre autres pages portent le reste. Les deux qui y figurent sont
choisies pour la palette du premier écran — `plat-01` est sombre, vert et
orange sur fond noir, `terrasse-04` porte le vert des chaises et la lumière
du soir. Avant d'en ajouter une troisième, se demander si la page en a besoin
ou si c'est la page de destination qui doit la porter.

## Le cadre d'affichage doit suivre le cadrage de la photo

Toutes les photos servies sont en **trois quarts** (portrait) ou en paysage
selon leur ligne du tableau ci-dessus. Un cadre CSS plus large que la photo
la recadre par le centre et lui retire le haut et le bas : sur la page de la
terrasse, un cadre en cinq quarts tranchait la bouteille par le milieu. Avant
de changer un `--ar`, comparer avec le format du fichier.

## Attention : il n'y a que deux prises de vue de la terrasse

`terrasse-pano`, `terrasse-02` et `terrasse-04` sont **la même table** vue de
trois façons ; `terrasse-01`, `terrasse-03` et `lieu-pano` sont **la même
bouteille sous le même arbre**. Ce sont deux photographies, pas six. Avant de
poser l'une d'elles dans une page, vérifier qu'aucune de ses jumelles ne s'y
trouve déjà — c'est ce qui donnait à la page « La terrasse » l'air de répéter
la même image trois fois.

## Ce qui manque encore

Ces emplacements existent dans les pages mais restent invisibles tant que le
fichier n'est pas là. Déposer les photos dans `source/`, ajouter la ligne
correspondante dans `tools/prepare_photos.py`, relancer le script.

| Fichier attendu | Où il irait | Cadrage |
|---|---|---|
| `chef.jpg` | le restaurant, portrait rond à côté du texte « En cuisine » | carré, visage centré |
| `parcours.jpg` | bande de photos de la terrasse | paysage |
| plats supplémentaires | respirations de la carte, entrées du site | portrait ou paysage |

Ces emplacements ne sont pas dans le code : un cadre qui pointe vers un fichier
absent déclenche une requête en échec à chaque visite. Déposez la photo dans
`source/`, ajoutez sa ligne dans `tools/prepare_photos.py`, relancez le script,
et dites-le-moi : je remets l'emplacement dans la page.

Une vraie photo de la salle serait utile : la seule dont nous disposons fait
900 px de large, et n'en donne que 675 une fois recadrée. La super-résolution la
rend propre à la taille où elle est posée, mais elle a dû rester dans le cadre
sur la page « Le restaurant », là où la composition prévoyait de la faire sortir
jusqu'au bord de l'écran. Une vue en haute définition rendrait ce débordement
possible.

Idéalement : une vue de la salle vide, une table dressée à l'intérieur, et le
chef en cuisine.

## Légender une photo de la galerie

Ajouter `data-caption` sur la figure correspondante dans `les-plats.html` :

```html
<figure class="ph ph--z" data-file="plat-02.jpg" data-caption="Foie gras mi-cuit, chutney de pomme">
```

La légende s'affiche sur l'image et dans la visionneuse.
