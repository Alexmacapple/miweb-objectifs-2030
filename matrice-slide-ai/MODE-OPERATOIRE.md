# Mode opératoire - créer et publier un jeu de slides

## Préparer

Réunir :

- un dossier contenant les images `slide-*.png` ;
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

La commande doit créer un nouveau dossier. Elle refuse d’écraser un dossier existant et ne modifie ni `index.html` racine ni `published-versions.json`.

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
python3 -m unittest discover -s nouveau-jeu/tests
npx --yes html-validate nouveau-jeu/index.html nouveau-jeu/alternatives.html nouveau-jeu/accessibilite.html index.html
npx --yes vnu-jar --errors-only nouveau-jeu/index.html nouveau-jeu/alternatives.html nouveau-jeu/accessibilite.html index.html
```

Inspecter aussi localement :

```bash
python3 -m http.server 8000 --bind 127.0.0.1
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
```

Cette commande est la seule étape qui modifie `published-versions.json` et `index.html` racine. Elle vérifie les pages générées, le ZIP et les tests du jeu avant d’écrire.

## Contrôler avant commit

```bash
git status --short
git diff --stat
git diff -- index.html published-versions.json nouveau-jeu/slides.json nouveau-jeu/build.py
```

Ne pas ajouter les caches, `.DS_Store`, captures temporaires ou sorties locales non liées au jeu publié.
