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

À côté de chaque fichier vit sa jumelle de 800 px, `<nom>-800.jpg`. Les pages
déclarent les deux et le navigateur choisit : la grande sur un écran
d'ordinateur, la petite au doigt. Les jumelles sont produites par
`tools/prepare_photos.py` — ne pas les modifier à la main, et **ne pas les
lister dans le tableau ci-dessous** : elles suivent leur aînée.

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
900 px de large, et n'en donne que 675 une fois recadrée. Elle a donc dû rester
dans le cadre sur la page « Le restaurant », là où la composition prévoyait de
la faire sortir jusqu'au bord de l'écran. Une vue en haute définition rendrait
ce débordement possible.

Idéalement : une vue de la salle vide, une table dressée à l'intérieur, et le
chef en cuisine.

## Légender une photo de la galerie

Ajouter `data-caption` sur la figure correspondante dans `les-plats.html` :

```html
<figure class="ph ph--z" data-file="plat-02.jpg" data-caption="Foie gras mi-cuit, chutney de pomme">
```

La légende s'affiche sur l'image et dans la visionneuse.
