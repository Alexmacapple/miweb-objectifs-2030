# Matrice slide IA

`matrice-slide-ai/` est la matrice canonique pour créer de nouveaux jeux de slides statiques et autonomes.

Elle n’est pas une variante publiée. Elle sert à copier le modèle de génération, les tests de contrat, le favicon et les exemples de sources dans un nouveau dossier de jeu.

## Règles

- `create_variant.py` crée un dossier autonome, mais ne publie jamais.
- `build.py` génère seulement les fichiers du dossier de jeu qui le contient.
- `publish_variant.py` est la seule commande autorisée à modifier `published-versions.json` et `index.html` racine.
- Un jeu publié ne doit pas importer de code depuis `matrice-slide-ai/`.
- Les variantes déjà publiées ne doivent pas être modifiées pour fabriquer un nouveau jeu.

## Création

Depuis la racine du dépôt :

```bash
python3 matrice-slide-ai/create_variant.py \
  --slug nouveau-jeu \
  --title "Titre public" \
  --storyboard chemin/storyboard.md \
  --slides-dir chemin/assets/slides
```

La commande crée `nouveau-jeu/`, copie les images `slide-*.png`, le storyboard, `slides.json`, `build.py`, les tests et les assets nécessaires.

## Génération

Après avoir vérifié ou complété `slides.json` :

```bash
python3 nouveau-jeu/build.py
python3 -m unittest discover -s nouveau-jeu/tests
```

Le build produit `index.html`, `alternatives.html`, `accessibilite.html`, `alternatives.md`, `README.md` et le ZIP dans `assets/downloads/`.

## Publication

Publier seulement après génération et vérifications :

```bash
python3 matrice-slide-ai/publish_variant.py --slug nouveau-jeu
```

La publication refuse un jeu non vérifiable. Si le jeu est valide, elle met à jour le catalogue racine `published-versions.json` puis régénère uniquement `index.html` à la racine.

Dans `build.py`, `ROOT_CATALOG_BOOTSTRAP` sert seulement de graine de compatibilité si `published-versions.json` n’existe pas encore. Cette constante ne doit pas être modifiée pour publier un jeu.

## Fichiers de référence

- `slides.example.json` : schéma complet de `slides.json`.
- `source/storyboard.example.md` : exemple de storyboard.
- `published-versions.example.json` : exemple de catalogue racine.
- `tests/test_matrix_workflow.py` : workflow de création, build et publication séparée.
- `tests/test_site_contracts.py` : contrat des pages générées.
