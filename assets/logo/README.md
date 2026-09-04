# Logo

| Fichier | Rôle |
|---|---|
| `le9.svg` | ce que le site affiche : texte converti en courbes, aucune dépendance à une police |
| `le9-source.svg` | la version modifiable, avec du vrai texte |

Le sceau a été redessiné d'après le filigrane qui apparaît sur les photos de la
maison (`assets/photos/source/le9_*.png`). Si le restaurant fournit un jour son
fichier vectoriel d'origine, le mettre à la place de `le9.svg` : le site le
reprendra sans autre changement, à condition qu'il n'y ait pas de couleur écrite
en dur dedans.

## Couleur

Aucune couleur dans le fichier. Le logo est affiché en masque CSS, donc il prend
la couleur du contexte : vert sur les fonds crème, crème sur les fonds verts.

## Régénérer le9.svg après avoir modifié la source

1. Ouvrir `le9-source.svg` dans un navigateur, avec la police Cormorant Garamond
   chargée, et l'exporter en PNG à 1800 px sur fond blanc.
2. Placer ce PNG dans un dossier, puis :

```
python3 tools/process_illustrations.py --src <ce dossier> --out <sortie> --force-svg
```

3. Copier le SVG obtenu sur `le9.svg`.

C'est la même chaîne que pour les illustrations : elle convertit un rendu en
courbes et retire tout ce qui n'est pas le dessin.
