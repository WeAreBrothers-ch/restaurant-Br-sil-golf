# Illustrations

- `source/` : les dessins d'origine (JPG ou PNG sur fond blanc ou gris). Non utilisés par le site.
- `dist/`   : les fichiers servis par le site, une seule couleur pilotée par le CSS.

Régénérer `dist/` depuis `source/` :

```
pip install Pillow numpy potracer
python3 tools/process_illustrations.py
```

Le script détoure le fond, retire les filigranes clairs et les taches, sort un
PNG transparent (le trait devient l'alpha) et, si le tracé est net, un SVG
`fill="currentColor"`. Il affiche à la fin les lignes CSS à coller dans
`css/style.css` pour chaque dessin.

Les six SVG actuellement dans `dist/` sont des dessins de substitution faits à la
main sur les mêmes sujets (golfeurs, clubs croisés, bouteille et verre, assiette
et couverts, chef à la cloche). Ils seront remplacés par les sorties du script
dès que les originaux seront dans `source/` : il suffit de garder les mêmes noms
de fichier, ou de mettre à jour les classes `.illu--*` dans le CSS.
