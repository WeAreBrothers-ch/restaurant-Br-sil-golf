# Photos

Déposer les fichiers ici, avec exactement ces noms. Tant qu'un fichier manque,
la page affiche un cadre qui rappelle le nom attendu.

## Les plats — page « Les plats », mosaïque

| Fichier | Cadrage conseillé |
|---|---|
| `plat-01.jpg` | paysage, la plus large de la mosaïque |
| `plat-02.jpg` | portrait |
| `plat-03.jpg` | portrait |
| `plat-04.jpg` | carré |
| `plat-05.jpg` | portrait |
| `plat-06.jpg` | paysage |
| `plat-07.jpg` | paysage |
| `plat-08.jpg` | portrait |
| `plat-09.jpg` | paysage large |
| `plat-10.jpg` | carré |
| `plat-11.jpg` | carré |
| `plat-12.jpg` | panoramique |

`plat-01`, `plat-02` et `plat-03` servent aussi sur l'accueil et la page du
restaurant. `plat-09` réapparaît sur la page de la terrasse.

## La salle et le chef

| Fichier | Où | Cadrage |
|---|---|---|
| `salle-01.jpg` | accueil, première entrée | portrait 3:4 |
| `salle-02.jpg` | le restaurant, bande pleine largeur | panoramique, au moins 2000 px de large |
| `salle-03.jpg` | le restaurant, une table dressée | carré |
| `chef.jpg` | le restaurant, portrait rond | carré, le visage bien centré |

## La terrasse

| Fichier | Où | Cadrage |
|---|---|---|
| `terrasse-pano.jpg` | terrasse, photo de tête plein écran | panoramique, au moins 2000 px de large |
| `terrasse-01.jpg` | accueil, quatrième entrée | portrait 3:4 |
| `terrasse-02.jpg` | terrasse, bande de photos | portrait |
| `terrasse-03.jpg` | terrasse, bande de photos | paysage |
| `terrasse-04.jpg` | terrasse, bande de photos | portrait, facultatif |
| `parcours.jpg` | terrasse, bande de photos | paysage, facultatif |

Les fichiers marqués facultatifs disparaissent d'eux-mêmes s'ils sont absents.

## Conseils

JPG de qualité 80, 1600 px de large suffisent pour la plupart, 2400 px pour les
panoramiques. Viser moins de 400 Ko par image pour garder le site rapide.

Pour légender une photo de la mosaïque, ajouter l'attribut `data-caption` sur sa
balise `<figure>` dans `les-plats.html` :

```html
<figure class="ph ph--z" data-file="plat-04.jpg" data-caption="Foie gras mi-cuit, chutney de pomme">
```
