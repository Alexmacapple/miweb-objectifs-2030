# Matrice Slide IA Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

## État actuel - 2026-06-25

Ce plan est désormais une trace d’implémentation. Les tâches 1 à 5 ont été réalisées dans le dépôt courant :

- `matrice-slide-ai/build.py` existe et génère seulement le dossier du jeu ;
- `matrice-slide-ai/create_variant.py` crée un jeu autonome sans publier ;
- `matrice-slide-ai/publish_variant.py` publie explicitement un jeu vérifié sur l’accueil racine ;
- `matrice-slide-ai/published-versions.example.json` documente le catalogue racine ;
- `matrice-slide-ai/README.md` et `matrice-slide-ai/MODE-OPERATOIRE.md` documentent le workflow ;
- `matrice-slide-ai/tests/` couvre création, build, publication séparée et contrats de site.

Source opérationnelle actuelle : `matrice-slide-ai/README.md`, `matrice-slide-ai/MODE-OPERATOIRE.md`, `DEMARCHE-VERSIONS.md` et `GUIDE-REGENERATION-SITES-SLIDES.md`.

Les cases non cochées conservées ci-dessous appartiennent au plan initial et ne doivent plus être utilisées comme suivi d’avancement courant.

**But :** créer `matrice-slide-ai/`, matrice canonique permettant de générer puis publier séparément de nouveaux jeux de slides autonomes.

**Architecture actuelle :** `matrice-slide-ai/` contient un générateur copiable, un script de création de variante et un script de publication racine. Les jeux générés restent autonomes : ils embarquent leur propre `build.py` et leurs tests. Le sous-dossier `generator/` envisagé dans le plan initial n’a pas été retenu à date.

**Socle technique :** Python 3.12 standard library, HTML statique DSFR, `unittest`, `html-validate`, `vnu-jar`, GitHub Pages.

---

## Structure de fichiers

- Créer : `matrice-slide-ai/README.md` — rôle de la matrice et non-objectifs.
- Créer : `matrice-slide-ai/MODE-OPERATOIRE.md` — procédure création, test, publication.
- Créer : `matrice-slide-ai/create_variant.py` — crée un dossier autonome sans publier.
- Créer : `matrice-slide-ai/publish_variant.py` — publie un jeu validé sur l’accueil racine.
- Créer : `matrice-slide-ai/published-versions.example.json` — exemple de catalogue racine.
- Créer : `matrice-slide-ai/slides.example.json` — exemple de schéma `slides.json`.
- Non retenu à date : `matrice-slide-ai/generator/` — la matrice garde actuellement un `build.py` autonome copié dans les jeux.
- Créer : `matrice-slide-ai/tests/test_matrix_workflow.py` — tests de création/publication.
- Copier puis adapter : `matrice-slide-ai/build.py` depuis `miweb-offre-mutualisee-listes-diffusion-2026-longue/build.py`.
- Copier : `matrice-slide-ai/assets/favicons/favicon.ico`.
- Modifier : `docs/superpowers/specs/2026-06-25-matrice-slide-ai-design.md` seulement si l’implémentation révèle un écart de spec.

## Tâche 1 : tests de workflow de matrice

**Fichiers :**
- Créer : `matrice-slide-ai/tests/test_matrix_workflow.py`
- Créer : `matrice-slide-ai/__init__.py`

- [ ] **Étape 1 : créer le test de création autonome**

```python
def test_create_variant_copies_sources_without_publishing(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    target = tmp_path / "jeu-test"
    run([
        sys.executable, str(repo / "matrice-slide-ai" / "create_variant.py"),
        "--slug", str(target),
        "--title", "Jeu test",
        "--storyboard", str(repo / "miweb-offre-mutualisee-listes-diffusion-2026-longue" / "source" / "storyboard.md"),
        "--slides-dir", str(repo / "miweb-offre-mutualisee-listes-diffusion-2026-longue" / "assets" / "slides"),
    ], check=True)
    assert (target / "build.py").is_file()
    assert (target / "slides.json").is_file()
    assert (target / "source" / "storyboard.md").is_file()
    assert (target / "assets" / "slides" / "slide-01.png").is_file()
    assert "matrice-slide-ai" not in (target / "build.py").read_text(encoding="utf-8")
```

- [ ] **Étape 2 : créer le test de publication séparée**

```python
def test_publish_variant_requires_generated_outputs(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    result = run([
        sys.executable, str(repo / "matrice-slide-ai" / "publish_variant.py"),
        "--slug", str(tmp_path / "absent"),
    ], text=True, stderr=PIPE)
    assert result.returncode != 0
    assert "jeu non vérifiable" in result.stderr
```

- [ ] **Étape 3 : lancer les tests et constater l’échec attendu**

Commande : `python3 -m unittest discover -s matrice-slide-ai/tests`

Attendu : échec d’import ou fichiers absents, car les scripts n’existent pas encore.

## Tâche 2 : squelette de matrice depuis le jeu 6

**Fichiers :**
- Créer : `matrice-slide-ai/build.py`
- Créer : `matrice-slide-ai/tests/test_site_contracts.py`
- Créer : `matrice-slide-ai/assets/favicons/favicon.ico`
- Créer : `matrice-slide-ai/slides.example.json`
- Créer : `matrice-slide-ai/source/storyboard.example.md`

- [ ] **Étape 1 : copier les références stables**

```bash
mkdir -p matrice-slide-ai/assets/favicons matrice-slide-ai/source matrice-slide-ai/tests matrice-slide-ai/generator
cp miweb-offre-mutualisee-listes-diffusion-2026-longue/build.py matrice-slide-ai/build.py
cp miweb-offre-mutualisee-listes-diffusion-2026-longue/tests/test_site_contracts.py matrice-slide-ai/tests/test_site_contracts.py
cp miweb-offre-mutualisee-listes-diffusion-2026-longue/assets/favicons/favicon.ico matrice-slide-ai/assets/favicons/favicon.ico
cp miweb-offre-mutualisee-listes-diffusion-2026-longue/slides.json matrice-slide-ai/slides.example.json
cp miweb-offre-mutualisee-listes-diffusion-2026-longue/source/storyboard.md matrice-slide-ai/source/storyboard.example.md
```

- [ ] **Étape 2 : supprimer les caches copiés s’ils apparaissent**

Commande : `find matrice-slide-ai -name __pycache__ -o -name '*.pyc'`

Attendu : aucune sortie. Si une sortie apparaît, supprimer seulement ces caches.

## Tâche 3 : script `create_variant.py`

**Fichiers :**
- Créer : `matrice-slide-ai/create_variant.py`
- Modifier : `matrice-slide-ai/tests/test_matrix_workflow.py`

- [ ] **Étape 1 : écrire une CLI non destructive**

Le script doit accepter `--slug`, `--title`, `--storyboard`, `--slides-dir`, refuser un dossier existant, créer `assets/slides/`, `assets/downloads/`, `assets/favicons/`, `source/`, `tests/`, copier `build.py`, `tests/test_site_contracts.py`, `favicon.ico`, le storyboard et les images `slide-*.png`.

- [ ] **Étape 2 : initialiser `slides.json`**

Copier `slides.example.json`, puis remplacer seulement le titre public si le champ existe dans le générateur. Ne pas inventer d’alternatives textuelles.

- [ ] **Étape 3 : vérifier que le jeu généré construit réellement**

Commande :

```bash
tmpdir=$(mktemp -d)
python3 matrice-slide-ai/create_variant.py --slug "$tmpdir/jeu-test" --title "Jeu test" --storyboard miweb-offre-mutualisee-listes-diffusion-2026-longue/source/storyboard.md --slides-dir miweb-offre-mutualisee-listes-diffusion-2026-longue/assets/slides
python3 "$tmpdir/jeu-test/build.py"
python3 -m unittest discover -s "$tmpdir/jeu-test/tests"
```

Attendu : build OK et tests OK.

## Tâche 4 : catalogue et publication séparée

**Fichiers :**
- Créer : `matrice-slide-ai/publish_variant.py`
- Créer : `matrice-slide-ai/published-versions.example.json`
- Modifier : `matrice-slide-ai/tests/test_matrix_workflow.py`

- [ ] **Étape 1 : créer l’exemple de catalogue**

```json
[
  {
    "slug": "miweb-offre-mutualisee-listes-diffusion-2026-longue",
    "label": "Offre mutualisée listes de diffusion - version longue"
  }
]
```

- [ ] **Étape 2 : écrire `publish_variant.py`**

Le script doit refuser un slug absent, vérifier `index.html`, `alternatives.html`, `accessibilite.html`, `slides.json`, `assets/downloads/*-slides.zip`, puis mettre à jour `published-versions.json` et régénérer uniquement l’accueil racine.

- [ ] **Étape 3 : vérifier que `create_variant.py` ne publie pas**

Commande : `git diff -- index.html published-versions.json`

Attendu après création seule : aucune modification.

## Tâche 5 : documentation et validation complète

**Fichiers :**
- Créer : `matrice-slide-ai/README.md`
- Créer : `matrice-slide-ai/MODE-OPERATOIRE.md`
- Modifier : `README.md`
- Modifier : `DEMARCHE-VERSIONS.md`
- Modifier : `GUIDE-REGENERATION-SITES-SLIDES.md`

- [ ] **Étape 1 : documenter la séparation création/publication**

Inclure explicitement : `create_variant.py` ne publie jamais ; `publish_variant.py` est la seule commande autorisée à changer le catalogue et l’accueil.

- [ ] **Étape 2 : lancer les contrôles Markdown**

Commande :

```bash
bash /Users/alex/Claude/scripts/check-accents.sh README.md DEMARCHE-VERSIONS.md GUIDE-REGENERATION-SITES-SLIDES.md matrice-slide-ai/README.md matrice-slide-ai/MODE-OPERATOIRE.md
```

Attendu : aucune sortie.

- [ ] **Étape 3 : lancer la validation finale**

Commande :

```bash
python3 -m unittest discover -s matrice-slide-ai/tests
npx --yes html-validate index.html
npx --yes vnu-jar --errors-only index.html
git status --short
```

Attendu : tests OK, validateurs OK, seulement les fichiers de matrice/docs attendus modifiés.
