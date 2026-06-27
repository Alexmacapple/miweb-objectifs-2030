# Objectifs 2030 - accessibilité numérique

Site public : <https://alexmacapple.github.io/miweb-objectifs-2030/>

Ce dépôt publie des jeux de slides web statiques, accessibles et comparables. Il contient les variantes MiWeb « Objectifs 2030 - accessibilité numérique » et des supports thématiques produits avec le même modèle.

![Flux de publication : contribuer, créer un jeu autonome, vérifier, publier l’accueil racine puis servir le public avec GitHub Pages.](flux-de-publication.png)

## Règle à retenir

Un jeu de slides est un dossier autonome. Il contient ses images, ses alternatives textuelles, son storyboard source, son générateur et son ZIP.

La génération du jeu et la publication sur l’accueil racine sont deux actions séparées :

- `python3 <dossier-jeu>/build.py` génère seulement le dossier du jeu ;
- `python3 matrice-slide-ai/publish_variant.py --slug <dossier-jeu>` met à jour `published-versions.json` et `index.html` racine.

Ne pas modifier une version déjà publiée pour fabriquer la suivante. Créer un nouveau dossier avec la matrice.

## Publier un nouveau jeu de slides

Depuis la racine du dépôt, créer le dossier autonome :

```bash
python3 matrice-slide-ai/create_variant.py \
  --slug nouveau-jeu \
  --title "Titre public" \
  --storyboard chemin/storyboard.md \
  --slides-dir chemin/assets/slides
```

Si les images source sont préfixées, déclarer le préfixe au lieu de les renommer :

```bash
python3 matrice-slide-ai/create_variant.py \
  --slug nouveau-jeu \
  --title "Titre public" \
  --storyboard chemin/storyboard.md \
  --slides-dir chemin/assets/slides \
  --slide-prefix prefixe-
```

Compléter ensuite `nouveau-jeu/slides.json`. Ce fichier est la source canonique des titres, alternatives courtes, descriptions complètes, textes visibles et messages.

Optimiser les images avant la génération, puis lancer :

```bash
python3 nouveau-jeu/build.py
scripts/validate_variant.sh nouveau-jeu
```

Publier seulement après vérification :

```bash
python3 matrice-slide-ai/publish_variant.py --slug nouveau-jeu
scripts/validate_variant.sh nouveau-jeu
```

Avant de pousser :

```bash
git status --short
git diff -- README.md DEMARCHE-VERSIONS.md GUIDE-REGENERATION-SITES-SLIDES.md index.html published-versions.json nouveau-jeu
scripts/push-pages.sh
```

Après le push, vérifier l’URL publique :

```text
https://alexmacapple.github.io/miweb-objectifs-2030/nouveau-jeu/
```

## Contrat d’un jeu publié

Chaque jeu publié doit contenir :

- `index.html` : présentation web et mode projection ;
- `alternatives.html` : alternatives textuelles complètes ;
- `alternatives.md` : version Markdown des alternatives ;
- `accessibilite.html` : état d’accessibilité du support ;
- `assets/slides/` : images publiées ;
- `assets/downloads/` : ZIP généré ;
- `source/` : storyboard et sources utiles ;
- `slides.json` : transcriptions et messages ;
- `build.py` : générateur autonome ;
- `tests/` : tests de contrat.

Le HTML généré, le Markdown généré et le ZIP ne se corrigent pas à la main. Corriger la source, puis relancer `build.py`.

## Points de vigilance

- Ne pas publier d’image sans alternative textuelle.
- Ne pas inventer de chiffre, seuil, engagement, audit ou conformité absent de la source.
- Ne pas déclarer une conformité RGAA sans audit dédié.
- Ne pas faire dépendre un jeu publié de `matrice-slide-ai/` à l’exécution.
- Ne pas modifier `PUBLISHED_VERSIONS`, `LATEST_VERSION_SLUG` ou `ROOT_CATALOG_BOOTSTRAP` dans un `build.py` pour publier l’accueil.
- Relancer `build.py` si les images changent après optimisation, afin de reconstruire le ZIP.
- Conserver la navigation clavier, le mode projection, les alternatives et le swipe horizontal tactile.

## Versions publiées

- Version 1 : <https://alexmacapple.github.io/miweb-objectifs-2030/miweb-objectifs-2030-v1/>
- Version 2 : <https://alexmacapple.github.io/miweb-objectifs-2030/miweb-objectifs-2030-v2/>
- Version 3 : <https://alexmacapple.github.io/miweb-objectifs-2030/miweb-objectifs-2030-v3/>
- Version 4 : <https://alexmacapple.github.io/miweb-objectifs-2030/miweb-objectifs-2030-v4/>
- Offre mutualisée de listes de diffusion, version condensée : <https://alexmacapple.github.io/miweb-objectifs-2030/miweb-offre-mutualisee-listes-diffusion-2026-condensee/>
- Offre mutualisée de listes de diffusion, version longue : <https://alexmacapple.github.io/miweb-objectifs-2030/miweb-offre-mutualisee-listes-diffusion-2026-longue/>
- SPAN / PAN - accessibilité numérique : <https://alexmacapple.github.io/miweb-objectifs-2030/span-pan/>
- Mise en gouvernance du SPAN : <https://alexmacapple.github.io/miweb-objectifs-2030/mise-en-gouvernance-du-span/>
- Checklist SPAN opérationnel : <https://alexmacapple.github.io/miweb-objectifs-2030/checklist-span-operationnel/>

Dernière version publiée : `checklist-span-operationnel/`.

Accès directs :

- présentation plein écran : <https://alexmacapple.github.io/miweb-objectifs-2030/checklist-span-operationnel/?projection=1#slide-01>
- toutes les slides : <https://alexmacapple.github.io/miweb-objectifs-2030/checklist-span-operationnel/?slides=all#diaporama>
- alternatives textuelles : <https://alexmacapple.github.io/miweb-objectifs-2030/checklist-span-operationnel/alternatives.html>
- page accessibilité : <https://alexmacapple.github.io/miweb-objectifs-2030/checklist-span-operationnel/accessibilite.html>

## Documents utiles

- `AGENTS.md` : règles projet pour les agents.
- `DEMARCHE-VERSIONS.md` : procédure courte de publication des variantes.
- `GUIDE-REGENERATION-SITES-SLIDES.md` : mode opératoire complet, avec contrôles et inspection locale.
- `docs/architecture.md` : vue d’architecture légère du dépôt et du flux de publication.
- `matrice-slide-ai/README.md` : fonctionnement de la matrice canonique.
- `docs/prd/` : cadrages fonctionnels historiques.
- `docs/prompts/` : prompts de génération et de correction conservés pour référence.
- `docs/goals/` : objectifs de chantier historiques.

En cas de tension, suivre d’abord les documents racine dans cet ordre : `AGENTS.md`, `README.md`, `DEMARCHE-VERSIONS.md`, puis `GUIDE-REGENERATION-SITES-SLIDES.md`. Les dossiers `docs/` servent de contexte historique.

## Développement local

Régénérer la dernière version publiée :

```bash
python3 checklist-span-operationnel/build.py
```

Tester un jeu :

```bash
scripts/validate_variant.sh checklist-span-operationnel
```

Servir le site localement :

```bash
scripts/serve-local.sh 8000
```

URL locale :

```text
http://127.0.0.1:8000/checklist-span-operationnel/
```

Dans un environnement sandboxé, les validateurs `npx` peuvent demander un accès réseau.
