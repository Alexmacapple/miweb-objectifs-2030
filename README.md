# Objectifs 2030 - accessibilité numérique

Site public : <https://alexmacapple.github.io/miweb-objectifs-2030/>

Ce dépôt publie des variantes web DSFR, statiques et accessibles des slides MiWeb « Objectifs 2030 - accessibilité numérique ».

## Pourquoi

Le site sert à comparer plusieurs variantes visuelles d’un même support sans perdre la traçabilité : chaque version garde ses images, ses alternatives textuelles, son storyboard source et son ZIP.

Le principe Saint-Exupéry s’applique ici : ne garder que ce qui sert la lecture, l’accessibilité, la comparaison des variantes et la publication. Une version ne doit pas accumuler de fonctionnalités ou de fichiers décoratifs.

## Versions

- Version 1 : <https://alexmacapple.github.io/miweb-objectifs-2030/miweb-objectifs-2030-v1/>
- Version 2 : <https://alexmacapple.github.io/miweb-objectifs-2030/miweb-objectifs-2030-v2/>
- Version 3 : <https://alexmacapple.github.io/miweb-objectifs-2030/miweb-objectifs-2030-v3/>

## Accès directs V3

- Présentation plein écran : <https://alexmacapple.github.io/miweb-objectifs-2030/miweb-objectifs-2030-v3/?projection=1#slide-01>
- Toutes les slides : <https://alexmacapple.github.io/miweb-objectifs-2030/miweb-objectifs-2030-v3/?slides=all#diaporama>
- Alternatives textuelles : <https://alexmacapple.github.io/miweb-objectifs-2030/miweb-objectifs-2030-v3/alternatives.html>
- Page accessibilité : <https://alexmacapple.github.io/miweb-objectifs-2030/miweb-objectifs-2030-v3/accessibilite.html>

## Organisation

- `index.html` : accueil des versions.
- `miweb-objectifs-2030-v1/` : diaporama V1, alternatives, page accessibilité et sources.
- `miweb-objectifs-2030-v2/` : diaporama V2, alternatives, page accessibilité et sources.
- `miweb-objectifs-2030-v3/` : diaporama V3, alternatives, page accessibilité et sources.
- `miweb-objectifs-2030-v1/source/storyboard-slides-accessibilite-2030.md` : storyboard source V1.
- `miweb-objectifs-2030-v2/source/storyboard-v2.md` : storyboard source V2.
- `miweb-objectifs-2030-v3/source/storyboard-v3.md` : storyboard source V3.
- `slides.json` dans chaque version : titres, alternatives textuelles, descriptions et messages.
- `build.py` dans chaque version : génération HTML, Markdown et ZIP.
- `DEMARCHE-VERSIONS.md` : procédure pour publier V3, V4, etc.

## Générer la dernière version

```bash
python3 miweb-objectifs-2030-v3/build.py
```

## Tester localement

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

URL locale V3 :

```text
http://127.0.0.1:8000/miweb-objectifs-2030-v3/
```

## Vérifier avant publication

```bash
python3 -m unittest discover -s miweb-objectifs-2030-v3/tests
npx --yes html-validate miweb-objectifs-2030-v3/index.html miweb-objectifs-2030-v3/alternatives.html miweb-objectifs-2030-v3/accessibilite.html index.html
npx --yes vnu-jar --errors-only miweb-objectifs-2030-v3/index.html miweb-objectifs-2030-v3/alternatives.html miweb-objectifs-2030-v3/accessibilite.html index.html
```

Pour une vérification complète après modification commune V1/V2/V3 :

```bash
python3 -m unittest discover -s miweb-objectifs-2030-v1/tests
python3 -m unittest discover -s miweb-objectifs-2030-v2/tests
python3 -m unittest discover -s miweb-objectifs-2030-v3/tests
npx --yes html-validate miweb-objectifs-2030-v1/index.html miweb-objectifs-2030-v1/alternatives.html miweb-objectifs-2030-v1/accessibilite.html miweb-objectifs-2030-v2/index.html miweb-objectifs-2030-v2/alternatives.html miweb-objectifs-2030-v2/accessibilite.html miweb-objectifs-2030-v3/index.html miweb-objectifs-2030-v3/alternatives.html miweb-objectifs-2030-v3/accessibilite.html index.html
npx --yes vnu-jar --errors-only miweb-objectifs-2030-v1/index.html miweb-objectifs-2030-v1/alternatives.html miweb-objectifs-2030-v1/accessibilite.html miweb-objectifs-2030-v2/index.html miweb-objectifs-2030-v2/alternatives.html miweb-objectifs-2030-v2/accessibilite.html miweb-objectifs-2030-v3/index.html miweb-objectifs-2030-v3/alternatives.html miweb-objectifs-2030-v3/accessibilite.html index.html
```

## Limite

Le site vise une publication accessible et a fait l’objet de vérifications techniques automatisées. Il ne vaut pas déclaration de conformité RGAA sans audit humain complet.
