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

## Ce que le site utilise aujourd'hui

| Fichier | Vient de | Où il apparaît |
|---|---|---|
| `plat-01.jpg` | nourriture.jpg | accueil (ruban), carte, le restaurant |
| `plat-02.jpg` | nourriture 2.jpg | accueil (carte de plat), carte |
| `plat-03.jpg` | caption.jpg | accueil (ruban), terrasse |
| `plat-04.jpg` | viande.jpg | accueil (carte de plat), carte, le restaurant |
| `plat-05.jpg` | img-20190316… | accueil, duo « la cuisine » |
| `plat-06.jpg` | 20180714… | accueil, carte de plat « burger du chef » |
| `lieu-pano.jpg` | le9_barolo_terrasse | bande large de la page « Le restaurant » |
| `terrasse-pano.jpg` | le9_terrasse_coucher_soleil | photo de tête de la page « La terrasse » |
| `terrasse-01.jpg` | le9_barolo_terrasse | terrasse, l'heure du soir |
| `terrasse-02.jpg` | le9_terrasse_coucher_soleil | accueil, second duo |
| `terrasse-03.jpg` | le9_barolo_terrasse | accueil (paire) |
| `terrasse-04.jpg` | le9_terrasse_coucher_soleil | en réserve, plus affichée |
| `salle-01.jpg` | une-vue-imprenable-sur | accueil (paire), le restaurant |

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
