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
| `plat-01.jpg` | nourriture.jpg | galerie, page carte sur l'accueil |
| `plat-02.jpg` | nourriture 2.jpg | galerie, accueil |
| `plat-03.jpg` | caption.jpg | galerie, terrasse |
| `plat-04.jpg` | viande.jpg | galerie, le restaurant |
| `plat-05.jpg` | img-20190316… | galerie |
| `plat-06.jpg` | 20180714… | galerie |
| `lieu-pano.jpg` | le9_barolo_terrasse | bande large de la page « Le restaurant » |
| `terrasse-pano.jpg` | le9_terrasse_coucher_soleil | photo de tête de la page « La terrasse » |
| `terrasse-01.jpg` | le9_barolo_terrasse | accueil, bande de la terrasse |
| `terrasse-02.jpg` | le9_terrasse_coucher_soleil | accueil, bande de la terrasse |
| `terrasse-03.jpg` | le9_barolo_terrasse | bande de la terrasse |
| `terrasse-04.jpg` | le9_terrasse_coucher_soleil | bande de la terrasse |
| `salle-01.jpg` | une-vue-imprenable-sur | page « Le restaurant », la vue depuis la salle |

## Ce qui manque encore

Ces emplacements existent dans les pages mais restent invisibles tant que le
fichier n'est pas là. Déposer les photos dans `source/`, ajouter la ligne
correspondante dans `tools/prepare_photos.py`, relancer le script.

| Fichier attendu | Où | Cadrage |
|---|---|---|
| `chef.jpg` | le restaurant, portrait rond | carré, visage centré |
| `plat-07.jpg` à `plat-10.jpg` | galerie | portrait ou paysage |
| `parcours.jpg` | bande de la terrasse | paysage |

Une vraie photo de la salle serait utile : la seule dont nous disposons fait
900 px de large, ce qui est juste pour un grand format. Idéalement une vue de la
salle vide, une table dressée à l'intérieur, et le chef en cuisine.

## Légender une photo de la galerie

Ajouter `data-caption` sur la figure correspondante dans `les-plats.html` :

```html
<figure class="ph ph--z" data-file="plat-02.jpg" data-caption="Foie gras mi-cuit, chutney de pomme">
```

La légende s'affiche sur l'image et dans la visionneuse.
