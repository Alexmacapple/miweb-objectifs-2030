# Mode opératoire - créer et publier un jeu de slides

Ce document détaille la procédure propre à `matrice-slide-ai/`. En cas de tension avec les documents racine, suivre d’abord `AGENTS.md`, puis le README racine, `DEMARCHE-VERSIONS.md` et `GUIDE-REGENERATION-SITES-SLIDES.md`.

## Préparer

Réunir :

- un dossier contenant les images `slide-*.png`, ou des images préfixées comme `checklist-span-slide-01.png` ;
- un storyboard source ;
- le titre public du jeu ;
- le slug public du dossier, en minuscules et sans espace.

## Créer le jeu autonome

```bash
python3 matrice-slide-ai/create_variant.py \
  --slug nouveau-jeu \
  --title "Titre public" \
  --storyboard chemin/storyboard.md \
  --slides-dir chemin/assets/slides
```

La commande doit créer un nouveau dossier. Elle refuse d’écraser un dossier existant et ne change ni `index.html` racine ni `published-versions.json`.

Si le lot source utilise un préfixe, le déclarer au lieu de renommer manuellement :

```bash
python3 matrice-slide-ai/create_variant.py \
  --slug nouveau-jeu \
  --title "Titre public" \
  --storyboard chemin/storyboard.md \
  --slides-dir chemin/assets/slides \
  --slide-prefix checklist-span-
```

La matrice copie alors `checklist-span-slide-01.png` vers `assets/slides/slide-01.png`.

## Compléter les transcriptions

Ouvrir `nouveau-jeu/slides.json` et vérifier chaque entrée :

- `numero` ;
- `titre` ;
- `image` ;
- `alt` ;
- `description` ;
- `textes_visibles` ;
- `message`.

Ne pas publier d’image sans alternative textuelle et description.

## Générer

Optimiser les images avant cette étape. Si les images sont remplacées ou optimisées après génération, relancer `python3 nouveau-jeu/build.py` pour reconstruire le ZIP.

```bash
python3 nouveau-jeu/build.py
```

Sorties attendues :

- `nouveau-jeu/index.html` ;
- `nouveau-jeu/alternatives.html` ;
- `nouveau-jeu/accessibilite.html` ;
- `nouveau-jeu/alternatives.md` ;
- `nouveau-jeu/assets/downloads/nouveau-jeu-slides.zip`.

## Vérifier

```bash
scripts/validate_variant.sh nouveau-jeu
```

Ce script lance les tests du jeu, `html-validate` et `vnu-jar`. Dans un environnement sandboxé, `npx` peut nécessiter une relance avec accès réseau.

Inspecter aussi localement :

```bash
scripts/serve-local.sh 8000
```

Pages à ouvrir :

```text
http://127.0.0.1:8000/nouveau-jeu/
http://127.0.0.1:8000/nouveau-jeu/?projection=1#slide-01
http://127.0.0.1:8000/nouveau-jeu/?slides=all#diaporama
http://127.0.0.1:8000/nouveau-jeu/alternatives.html
```

## Publier sur l’accueil

Après validation :

```bash
python3 matrice-slide-ai/publish_variant.py --slug nouveau-jeu
scripts/validate_variant.sh nouveau-jeu
```

Cette commande est la seule étape qui change `published-versions.json` et `index.html` racine. Elle vérifie les pages générées, le ZIP et les tests du jeu avant d’écrire.

## Contrôler avant commit

```bash
git status --short
git diff --stat
git diff -- README.md DEMARCHE-VERSIONS.md GUIDE-REGENERATION-SITES-SLIDES.md index.html published-versions.json nouveau-jeu
```

Ne pas ajouter les caches, `.DS_Store`, captures temporaires ou sorties locales non liées au jeu publié.

Pour pousser sans blocage silencieux sur une invite Git, utiliser :

```bash
scripts/push-pages.sh
```
