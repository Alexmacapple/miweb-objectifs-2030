# Objectifs 2030 - accessibilité numérique

Site public : <https://alexmacapple.github.io/miweb-objectifs-2030/>

Version 1 : <https://alexmacapple.github.io/miweb-objectifs-2030/miweb-objectifs-2030-v1/>

Ce dépôt publie une version web DSFR, statique et accessible des slides MiWeb « Objectifs 2030 - accessibilité numérique ».

## Contenu

- `index.html` : accueil des versions.
- `miweb-objectifs-2030-v1/` : diaporama, alternatives textuelles, page accessibilité et fichiers sources.
- `miweb-objectifs-2030-v1/slides.json` : contenu source des slides.
- `miweb-objectifs-2030-v1/build.py` : génération HTML et ZIP.

## Générer

```bash
python3 miweb-objectifs-2030-v1/build.py
```

## Vérifier

```bash
python3 -m unittest discover -s miweb-objectifs-2030-v1/tests
npx --yes html-validate miweb-objectifs-2030-v1/index.html miweb-objectifs-2030-v1/alternatives.html miweb-objectifs-2030-v1/accessibilite.html index.html
npx --yes vnu-jar --errors-only miweb-objectifs-2030-v1/index.html miweb-objectifs-2030-v1/alternatives.html miweb-objectifs-2030-v1/accessibilite.html index.html
```

## Limite

Le site est pré-audité techniquement, mais ne vaut pas déclaration de conformité RGAA sans revue humaine complète.
