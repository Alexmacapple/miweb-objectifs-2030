# AGENTS.md - miweb-objectifs-2030

## Règle centrale

Toujours répondre et documenter en français.

Ce dépôt publie des variantes web statiques des slides MiWeb « Objectifs 2030 - accessibilité numérique » et des supports thématiques produits avec le même modèle. Le but n’est pas de créer un nouveau site éditorial, mais de rendre comparables des jeux de slides visuels en conservant la traçabilité des sources.

## Pourquoi

Chaque version doit permettre de répondre à quatre questions :

- quelle variante est publiée ;
- quelles images elle contient ;
- quelles alternatives textuelles décrivent ces images ;
- quel storyboard source a guidé la génération.

Toutes les versions publiées doivent rester comparables. Une version publiée ne doit pas être réécrite pour devenir une autre variante.

## Principe Saint-Exupéry

Appliquer le principe de sobriété : enlever ce qui ne sert pas la lecture, l’accessibilité, la comparaison ou la publication.

Concrètement :

- pas de fonctionnalité ajoutée sans usage réel ;
- pas de nouveau framework ;
- pas de composant décoratif ;
- pas de page supplémentaire si le contenu tient dans le README, `slides.json`, `DEMARCHE-VERSIONS.md` ou `GUIDE-REGENERATION-SITES-SLIDES.md` ;
- pas de duplication de texte long entre versions hors alternatives nécessaires.

## Structure à préserver

- `index.html` : accueil des versions publiées.
- `miweb-objectifs-2030-vN/` : une version autonome du diaporama Objectifs 2030.
- `miweb-offre-mutualisee-listes-diffusion-2026-condensee/` : support thématique condensé.
- `miweb-offre-mutualisee-listes-diffusion-2026-longue/` : support thématique long.
- `span-pan/` : support thématique SPAN / PAN.
- `mise-en-gouvernance-du-span/` : support thématique sur la gouvernance du SPAN.
- `checklist-span-operationnel/` : support thématique checklist SPAN opérationnel et dernière version publiée.
- `<dossier-jeu>/assets/slides/` : les images publiées de la variante.
- `<dossier-jeu>/source/` : storyboard et sources utiles de la variante.
- `<dossier-jeu>/slides.json` : source canonique des titres, alternatives, descriptions et messages.
- `<dossier-jeu>/build.py` : générateur autonome de la variante ; il ne doit générer que le dossier du jeu.
- `matrice-slide-ai/` : matrice canonique pour créer et publier séparément les futurs jeux.
- `published-versions.json` : catalogue racine, créé au premier publish ou mis à jour par `publish_variant.py`.
- `DEMARCHE-VERSIONS.md` : procédure de publication des variantes suivantes.
- `GUIDE-REGENERATION-SITES-SLIDES.md` : mode opératoire complet pour créer, vérifier, prévisualiser et publier un jeu.
- `docs/prd/` : cadrages fonctionnels historiques.
- `docs/prompts/` : prompts de génération et de correction conservés pour référence.
- `docs/goals/` : objectifs de chantier historiques.
- `scripts/validate_variant.sh` : vérification standard d’un jeu.
- `scripts/serve-local.sh` : serveur local standard.
- `scripts/push-pages.sh` : push non interactif vers GitHub Pages.

## Hiérarchie documentaire

Pour un agent ou un LLM qui reprend le dépôt :

- `AGENTS.md` fixe les règles de conduite et les interdits.
- `README.md` donne l’entrée courte et le chemin standard.
- `DEMARCHE-VERSIONS.md` détaille la procédure opérationnelle.
- `GUIDE-REGENERATION-SITES-SLIDES.md` sert de mode opératoire complet quand il faut inspecter, prévisualiser ou prouver.
- `docs/prd/`, `docs/prompts/` et `docs/goals/` sont des archives de cadrage ; ne pas les traiter comme procédure active si un document racine plus récent dit autre chose.

## Règles de variante

- Créer une nouvelle variante ou un nouveau support dans un nouveau dossier autonome avec `matrice-slide-ai/create_variant.py`.
- Si les images source sont préfixées, utiliser `--slide-prefix <prefixe>` au lieu de les renommer manuellement.
- Ne pas modifier les images ou alternatives d’une version déjà publiée pour fabriquer la suivante.
- Copier le storyboard source dans `source/`.
- Mettre à jour `slides.json` avant de générer les pages.
- Optimiser les images avant `build.py`. Si les images changent ensuite, relancer `build.py` pour reconstruire le ZIP.
- Lancer `python3 <dossier-jeu>/build.py` pour générer seulement le jeu.
- Publier sur l’accueil racine uniquement avec `python3 matrice-slide-ai/publish_variant.py --slug <dossier-jeu>`.
- Ne pas modifier `PUBLISHED_VERSIONS`, `LATEST_VERSION_SLUG` ou `ROOT_CATALOG_BOOTSTRAP` dans un `build.py` de variante pour publier l’accueil.
- Ne pas faire dépendre un jeu publié de `matrice-slide-ai/` à l’exécution.
- Ne pas publier d’image sans alternative textuelle.
- Ne pas inventer de chiffre, seuil, engagement, audit ou conformité absents de la note source.

## Vérifications attendues

Pour le jeu modifié :

```bash
scripts/validate_variant.sh <dossier-jeu>
```

Dans un environnement sandboxé, les validateurs `npx` peuvent demander un accès réseau. Le script reste la commande canonique ; relancer avec autorisation réseau si nécessaire.

Pour une modification commune :

```bash
python3 -m unittest discover -s matrice-slide-ai/tests
python3 -m unittest discover -s miweb-objectifs-2030-v1/tests
python3 -m unittest discover -s miweb-objectifs-2030-v2/tests
python3 -m unittest discover -s miweb-objectifs-2030-v3/tests
python3 -m unittest discover -s miweb-objectifs-2030-v4/tests
python3 -m unittest discover -s miweb-offre-mutualisee-listes-diffusion-2026-condensee/tests
python3 -m unittest discover -s miweb-offre-mutualisee-listes-diffusion-2026-longue/tests
python3 -m unittest discover -s span-pan/tests
python3 -m unittest discover -s mise-en-gouvernance-du-span/tests
python3 -m unittest discover -s checklist-span-operationnel/tests
```

Tester aussi en local :

```bash
scripts/serve-local.sh 8000
```

## Publication

Avant push :

- vérifier `git status --short` ;
- ne pas ajouter `.DS_Store`, caches, `test-results/` ou artefacts locaux ignorés ;
- vérifier le diff des fichiers racine, du catalogue et du dossier de jeu concerné ;
- vérifier que `published-versions.json` et `index.html` racine ne changent qu’après `publish_variant.py` ;
- vérifier que l’accueil racine pointe bien vers la dernière version publiée ;
- vérifier que le ZIP de la dernière version existe dans `assets/downloads/`.
- pousser avec `scripts/push-pages.sh` pour éviter un blocage silencieux sur une invite Git.

GitHub Pages publie depuis la branche du dépôt. Après push, vérifier l’URL publique de la version concernée.
