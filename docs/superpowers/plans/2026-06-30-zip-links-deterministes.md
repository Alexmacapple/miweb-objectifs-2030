# Contrat ZIP et liens de téléchargement Implementation Plan

> PDG-LARGE-FILE-JUSTIFICATION: plan agentique détaillé nécessaire pour cadrer TDD, séparation des ZIPs générés, propagation multi-variantes et preuves de non-régression sans ambiguïté.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** rendre les ZIPs de slides fidèles, déterministes et toujours liés vers un fichier existant.

**Decision Source:** `prd-meta-workflow/PRD-006-zip-deterministes-liens-telechargement.MD`.

**Architecture:** le contrat se corrige dans les générateurs `build.py`, car les ZIPs et les liens HTML sont des sorties générées. La matrice porte le modèle des futures variantes, et les variantes autonomes actuelles reçoivent la même correction locale sans import runtime vers `matrice-slide-ai/`. Les ZIPs déjà régénérés localement après `PRD-005` doivent rester séparés du commit de code.

**Tech Stack:** Python standard library, `unittest`, `zipfile.ZipInfo`, scripts shell existants, validateurs HTML npm verrouillés.

---

## Root Cause

| Alerte | Source ouverte | Verdict | Impact |
|--------|----------------|---------|--------|
| `G-Z4-002` | `miweb-offre-mutualisee-listes-diffusion-2026-condensee/build.py:21` et `:832-839` | Confirmé | Le footer racine de `render_root()` combine le slug de la variante longue avec le nom ZIP de la variante condensée. Chemin produit : `miweb-offre-mutualisee-listes-diffusion-2026-longue/assets/downloads/miweb-offre-mutualisee-listes-diffusion-2026-condensee-slides.zip`. |
| `SG-Z4-003` | Comparaison locale du ZIP `span-pan` avec `assets/slides` | Résolu par rebuild local non commité | Les entrées `slide-*.png` du ZIP régénéré correspondent aux images courantes. Il faut conserver la preuve par test pour éviter la régression. |
| `SG-Z4-004` | Comparaison locale du ZIP `mise-en-gouvernance-du-span` avec `assets/slides` | Résolu par rebuild local non commité | Les entrées `slide-*.png` du ZIP régénéré correspondent aux images courantes. Il faut conserver la preuve par test pour éviter la régression. |
| `SG-Z2-004` | Rebuild de `span-pan` en copie temporaire, deux SHA-256 différents | Confirmé | `zipfile.ZipFile.write()` reprend les métadonnées de fichiers. Deux builds sans changement de contenu peuvent produire des ZIPs binaires différents. |

## État de départ à préserver

- Le dépôt est actuellement `main...origin/main [ahead 10]`.
- Les 9 ZIPs de variantes sont modifiés localement par le rebuild réel du `PRD-005`.
- Ces 9 ZIPs doivent être commités séparément ou explicitement laissés hors commit avant d'implémenter ce plan.
- Aucun push n'est autorisé sans validation d'Alex.

## Structure de fichiers

- Modifier : `matrice-slide-ai/build.py` — rendre `write_zip()` déterministe pour les futures variantes.
- Modifier : les 9 `build.py` autonomes actuels — appliquer le même helper ZIP déterministe.
- Modifier : `miweb-offre-mutualisee-listes-diffusion-2026-condensee/build.py` — corriger le lien ZIP du footer racine.
- Modifier : `miweb-offre-mutualisee-listes-diffusion-2026-longue/build.py` — figer le même contrat explicite côté variante longue.
- Modifier : `matrice-slide-ai/tests/test_matrix_workflow.py` — ajouter le test de ZIP déterministe sur variante temporaire.
- Modifier : `matrice-slide-ai/tests/test_site_contracts.py` — garder le test de fidélité ZIP comme contrat modèle.
- Modifier : `span-pan/tests/test_site_contracts.py` et `mise-en-gouvernance-du-span/tests/test_site_contracts.py` — ajouter le test de fidélité ZIP qui aurait capturé `SG-Z4-003` et `SG-Z4-004`.
- Modifier : `miweb-offre-mutualisee-listes-diffusion-2026-condensee/tests/test_site_contracts.py` et `miweb-offre-mutualisee-listes-diffusion-2026-longue/tests/test_site_contracts.py` — ajouter le test de liens racine vers ZIP existant.
- Modifier après implémentation : `CHANGELOG.MD` et, si un PRD est créé ensuite, son changelog.

## Task 0: Séparer les ZIPs déjà régénérés

**Files:**
- Inspect: `git status --short`
- Commit possible: les 9 fichiers `*/assets/downloads/*-slides.zip`

- [ ] **Step 1: Inspecter l'état Git**

Run:

```bash
git status --short --branch
```

Expected before implementation:

```text
## main...origin/main [ahead 10]
 M checklist-span-operationnel/assets/downloads/checklist-span-operationnel-slides.zip
 M mise-en-gouvernance-du-span/assets/downloads/mise-en-gouvernance-du-span-slides.zip
 M miweb-objectifs-2030-v1/assets/downloads/miweb-objectifs-2030-v1-slides.zip
 M miweb-objectifs-2030-v2/assets/downloads/miweb-objectifs-2030-v2-slides.zip
 M miweb-objectifs-2030-v3/assets/downloads/miweb-objectifs-2030-v3-slides.zip
 M miweb-objectifs-2030-v4/assets/downloads/miweb-objectifs-2030-v4-slides.zip
 M miweb-offre-mutualisee-listes-diffusion-2026-condensee/assets/downloads/miweb-offre-mutualisee-listes-diffusion-2026-condensee-slides.zip
 M miweb-offre-mutualisee-listes-diffusion-2026-longue/assets/downloads/miweb-offre-mutualisee-listes-diffusion-2026-longue-slides.zip
 M span-pan/assets/downloads/span-pan-slides.zip
```

- [ ] **Step 2: Poser un tag local avant la nouvelle implémentation**

Run:

```bash
git tag backup/zip-liens-deterministes-20260630 HEAD
git show-ref --tags backup/zip-liens-deterministes-20260630
```

Expected:

```text
<sha-du-head> refs/tags/backup/zip-liens-deterministes-20260630
```

- [ ] **Step 3: Ne pas mélanger les ZIPs déjà sales avec le code**

If Alex validates the current rebuild before implementation, commit only the ZIPs:

```bash
git add '*/assets/downloads/*-slides.zip'
git commit -m "build: Régénère les ZIP après validation slides"
```

If Alex does not validate this commit, stop before editing code.

## Task 1: Tests TDD pour le footer racine

**Files:**
- Modify: `miweb-offre-mutualisee-listes-diffusion-2026-condensee/tests/test_site_contracts.py`
- Modify: `miweb-offre-mutualisee-listes-diffusion-2026-longue/tests/test_site_contracts.py`

- [ ] **Step 1: Ajouter le parseur de liens si absent**

Add next to `ImageParser`:

```python
class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            values = {key: value or "" for key, value in attrs}
            if values.get("href"):
                self.links.append(values["href"])
```

- [ ] **Step 2: Ajouter le test de lien ZIP racine existant**

Add in `SiteContractsTest`:

```python
    def test_root_download_links_target_existing_zip_files(self):
        parser = LinkParser()
        parser.feed(self.root_html)
        zip_links = [
            href
            for href in parser.links
            if "assets/downloads/" in href and href.endswith(".zip")
        ]

        self.assertTrue(zip_links, "Le footer racine doit exposer un lien ZIP.")
        for href in zip_links:
            with self.subTest(href=href):
                self.assertTrue(
                    (ROOT.parent / href).is_file(),
                    msg=f"Le lien ZIP racine doit pointer vers un fichier existant : {href}",
                )
```

- [ ] **Step 3: Vérifier le rouge avant correction**

Run:

```bash
python3 -m unittest discover -s miweb-offre-mutualisee-listes-diffusion-2026-condensee/tests -p 'test_site_contracts.py'
```

Expected before implementation:

```text
FAIL
```

The failing href must be:

```text
miweb-offre-mutualisee-listes-diffusion-2026-longue/assets/downloads/miweb-offre-mutualisee-listes-diffusion-2026-condensee-slides.zip
```

## Task 2: Tests TDD pour ZIP déterministe

**Files:**
- Modify: `matrice-slide-ai/tests/test_matrix_workflow.py`

- [ ] **Step 1: Ajouter les imports**

Add near the existing imports:

```python
import hashlib
import os
```

- [ ] **Step 2: Ajouter le helper SHA-256**

Add inside `MatrixWorkflowTest`:

```python
    def file_sha256(self, path):
        return hashlib.sha256(path.read_bytes()).hexdigest()
```

- [ ] **Step 3: Ajouter le test de déterminisme**

Add inside `MatrixWorkflowTest`:

```python
    def test_variant_build_generates_deterministic_zip(self):
        repo = Path(__file__).resolve().parents[2]
        with TemporaryDirectory() as tmp_dir:
            target = self.create_temp_variant(repo, tmp_dir)

            first_build = self.run_variant_build(target)
            self.assertEqual(0, first_build.returncode, first_build.stderr)
            zip_path = target / "assets" / "downloads" / "jeu-test-slides.zip"
            first_sha = self.file_sha256(zip_path)

            first_slide = target / "assets" / "slides" / "slide-01.png"
            os.utime(first_slide, (946684800, 946684800))

            second_build = self.run_variant_build(target)
            self.assertEqual(0, second_build.returncode, second_build.stderr)
            second_sha = self.file_sha256(zip_path)

            self.assertEqual(first_sha, second_sha)
```

- [ ] **Step 4: Vérifier le rouge avant correction**

Run:

```bash
python3 -m unittest discover -s matrice-slide-ai/tests -p 'test_matrix_workflow.py'
```

Expected before implementation:

```text
FAIL
```

The deterministic ZIP test must fail because `archive.write()` preserves source file timestamps.

## Task 3: Tests de fidélité ZIP pour les variantes signalées

**Files:**
- Modify: `span-pan/tests/test_site_contracts.py`
- Modify: `mise-en-gouvernance-du-span/tests/test_site_contracts.py`

- [ ] **Step 1: Ajouter le test ZIP courant**

Add in each `SiteContractsTest`:

```python
    def test_download_zip_matches_current_slides(self):
        import zipfile

        zip_path = ROOT / "assets" / "downloads" / f"{ROOT.name}-slides.zip"
        self.assertTrue(zip_path.is_file(), zip_path)
        slide_paths = sorted((ROOT / "assets" / "slides").glob("slide-*.png"))
        with zipfile.ZipFile(zip_path) as archive:
            self.assertEqual(
                [path.name for path in slide_paths] + ["alternatives.md"],
                archive.namelist(),
            )
            for slide_path in slide_paths:
                with self.subTest(slide=slide_path.name):
                    self.assertEqual(
                        slide_path.read_bytes(),
                        archive.read(slide_path.name),
                        msg=(
                            "Le ZIP doit être régénéré après optimisation "
                            f"ou remplacement de {slide_path.name}."
                        ),
                    )
```

- [ ] **Step 2: Vérifier le vert actuel après rebuild local**

Run:

```bash
python3 -m unittest discover -s span-pan/tests -p 'test_site_contracts.py'
python3 -m unittest discover -s mise-en-gouvernance-du-span/tests -p 'test_site_contracts.py'
```

Expected after the already executed local rebuild:

```text
OK
```

## Task 4: Corriger le lien ZIP racine

**Files:**
- Modify: `miweb-offre-mutualisee-listes-diffusion-2026-condensee/build.py`
- Modify: `miweb-offre-mutualisee-listes-diffusion-2026-longue/build.py`

- [ ] **Step 1: Ajouter le nom ZIP de la dernière version**

Add after `LATEST_VERSION_SLUG`:

```python
LATEST_VERSION_ZIP_NAME = f"{LATEST_VERSION_SLUG}-slides.zip"
```

- [ ] **Step 2: Utiliser ce nom en contexte racine**

Replace in `footer()`:

```python
"Télécharger les slides": f"assets/downloads/{ZIP_NAME}" if version_context else f"{LATEST_VERSION_SLUG}/assets/downloads/{ZIP_NAME}",
```

with:

```python
"Télécharger les slides": f"assets/downloads/{ZIP_NAME}" if version_context else f"{LATEST_VERSION_SLUG}/assets/downloads/{LATEST_VERSION_ZIP_NAME}",
```

- [ ] **Step 3: Vérifier le vert**

Run:

```bash
python3 -m unittest discover -s miweb-offre-mutualisee-listes-diffusion-2026-condensee/tests -p 'test_site_contracts.py'
python3 -m unittest discover -s miweb-offre-mutualisee-listes-diffusion-2026-longue/tests -p 'test_site_contracts.py'
```

Expected:

```text
OK
```

## Task 5: Rendre `write_zip()` déterministe

**Files:**
- Modify: `matrice-slide-ai/build.py`
- Modify: `checklist-span-operationnel/build.py`
- Modify: `mise-en-gouvernance-du-span/build.py`
- Modify: `miweb-objectifs-2030-v1/build.py`
- Modify: `miweb-objectifs-2030-v2/build.py`
- Modify: `miweb-objectifs-2030-v3/build.py`
- Modify: `miweb-objectifs-2030-v4/build.py`
- Modify: `miweb-offre-mutualisee-listes-diffusion-2026-condensee/build.py`
- Modify: `miweb-offre-mutualisee-listes-diffusion-2026-longue/build.py`
- Modify: `span-pan/build.py`

- [ ] **Step 1: Ajouter la date ZIP stable**

Add near `ZIP_PATH`:

```python
ZIP_TIMESTAMP = (2026, 1, 1, 0, 0, 0)
```

- [ ] **Step 2: Ajouter le helper d'entrée ZIP**

Add before `write_zip()`:

```python
def write_zip_entry(archive: zipfile.ZipFile, source_path: Path, archive_name: str) -> None:
    info = zipfile.ZipInfo(archive_name, ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    archive.writestr(info, source_path.read_bytes())
```

- [ ] **Step 3: Remplacer les écritures ZIP**

Replace the body of `write_zip()`:

```python
def write_zip(slides: list[dict]) -> None:
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for slide in slides:
            image_path = resolve_slide_image_path(slide["image"])
            archive.write(image_path, image_path.name)
        archive.write(ROOT / "alternatives.md", "alternatives.md")
```

with:

```python
def write_zip(slides: list[dict]) -> None:
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for slide in slides:
            image_path = resolve_slide_image_path(slide["image"])
            write_zip_entry(archive, image_path, image_path.name)
        write_zip_entry(archive, ROOT / "alternatives.md", "alternatives.md")
```

- [ ] **Step 4: Vérifier qu'aucun `archive.write()` ne reste**

Run:

```bash
rg "archive\\.write\\(" --glob build.py .
```

Expected:

```text
no output
```

## Task 6: Validation locale complète

**Files:**
- All modified files from previous tasks.

- [ ] **Step 1: Lancer la suite matrice**

Run:

```bash
python3 -m unittest discover -s matrice-slide-ai/tests
```

Expected:

```text
OK
```

- [ ] **Step 2: Lancer les tests des 9 variantes**

Run:

```bash
for slug in miweb-objectifs-2030-v1 miweb-objectifs-2030-v2 miweb-objectifs-2030-v3 miweb-objectifs-2030-v4 miweb-offre-mutualisee-listes-diffusion-2026-condensee miweb-offre-mutualisee-listes-diffusion-2026-longue span-pan mise-en-gouvernance-du-span checklist-span-operationnel; do
  python3 -m unittest discover -s "$slug/tests" || exit 1
done
```

Expected:

```text
OK for every variant
```

- [ ] **Step 3: Rebuild réel après validation Alex**

Run only after explicit local rebuild approval:

```bash
for slug in miweb-objectifs-2030-v1 miweb-objectifs-2030-v2 miweb-objectifs-2030-v3 miweb-objectifs-2030-v4 miweb-offre-mutualisee-listes-diffusion-2026-condensee miweb-offre-mutualisee-listes-diffusion-2026-longue span-pan mise-en-gouvernance-du-span checklist-span-operationnel; do
  (cd "$slug" && python3 build.py) || exit 1
done
```

Expected:

```text
exit code 0
```

- [ ] **Step 4: Valider les 9 variantes**

Run:

```bash
for slug in miweb-objectifs-2030-v1 miweb-objectifs-2030-v2 miweb-objectifs-2030-v3 miweb-objectifs-2030-v4 miweb-offre-mutualisee-listes-diffusion-2026-condensee miweb-offre-mutualisee-listes-diffusion-2026-longue span-pan mise-en-gouvernance-du-span checklist-span-operationnel; do
  scripts/validate_variant.sh "$slug" || exit 1
done
```

Expected:

```text
OK for every variant
```

- [ ] **Step 5: Vérifier le déterminisme en copie temporaire**

Run:

```bash
tmp_root=$(mktemp -d)
cp -R span-pan "$tmp_root/span-pan"
(cd "$tmp_root/span-pan" && python3 build.py)
sha1=$(shasum -a 256 "$tmp_root/span-pan/assets/downloads/span-pan-slides.zip" | awk '{print $1}')
touch -t 200001010000 "$tmp_root/span-pan/assets/slides/slide-01.png"
(cd "$tmp_root/span-pan" && python3 build.py)
sha2=$(shasum -a 256 "$tmp_root/span-pan/assets/downloads/span-pan-slides.zip" | awk '{print $1}')
test "$sha1" = "$sha2"
```

Expected:

```text
exit code 0
```

- [ ] **Step 6: Contrôler les liens racine ZIP avec `curl`**

Run while the local server is active on port `8000`:

```bash
for path in \
  /miweb-offre-mutualisee-listes-diffusion-2026-longue/assets/downloads/miweb-offre-mutualisee-listes-diffusion-2026-longue-slides.zip \
  /miweb-offre-mutualisee-listes-diffusion-2026-condensee/assets/downloads/miweb-offre-mutualisee-listes-diffusion-2026-condensee-slides.zip \
  /span-pan/assets/downloads/span-pan-slides.zip \
  /mise-en-gouvernance-du-span/assets/downloads/mise-en-gouvernance-du-span-slides.zip
do
  code=$(/usr/bin/curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:8000${path}")
  printf '%s %s\n' "$code" "$path"
  test "$code" = "200" || exit 1
done
```

Expected:

```text
200 for every ZIP route
```

## Task 7: Commit boundaries

**Files:**
- All modified code and tests.
- ZIP artifacts only after rebuild.

- [ ] **Step 1: Commit code and tests separately**

Run:

```bash
git add matrice-slide-ai/build.py matrice-slide-ai/tests/test_matrix_workflow.py matrice-slide-ai/tests/test_site_contracts.py \
  checklist-span-operationnel/build.py mise-en-gouvernance-du-span/build.py span-pan/build.py \
  miweb-objectifs-2030-v1/build.py miweb-objectifs-2030-v2/build.py miweb-objectifs-2030-v3/build.py miweb-objectifs-2030-v4/build.py \
  miweb-offre-mutualisee-listes-diffusion-2026-condensee/build.py miweb-offre-mutualisee-listes-diffusion-2026-condensee/tests/test_site_contracts.py \
  miweb-offre-mutualisee-listes-diffusion-2026-longue/build.py miweb-offre-mutualisee-listes-diffusion-2026-longue/tests/test_site_contracts.py \
  span-pan/tests/test_site_contracts.py mise-en-gouvernance-du-span/tests/test_site_contracts.py CHANGELOG.MD
git commit -m "fix: Stabilise les ZIP et liens de téléchargement"
```

- [ ] **Step 2: Commit les ZIPs régénérés séparément**

Run after real rebuild and validation:

```bash
git status --short
git add '*/assets/downloads/*-slides.zip'
git commit -m "build: Régénère les ZIP déterministes"
```

## PDG pass

- Trigger decision: oui, le plan sera exécuté par un agent et touche des générateurs, des artefacts ZIP et des liens publics.
- Skill invocation pass: `superpowers:writing-plans` lu, `superpowers:systematic-debugging` lu, PDG lu. Une réponse courte est insuffisante parce que les alertes mêlent code, artefacts binaires déjà sales, tests manquants et génération réelle.
- Artifacts inspected: `build.py` matrice et variantes concernées, tests `test_site_contracts.py`, `test_matrix_workflow.py`, ZIPs `span-pan` et `mise-en-gouvernance-du-span`, `visual-tests/_results/audit-results.json`.
- Overlap findings: réutiliser `write_zip()` existant au lieu de créer un nouveau pipeline ; étendre les tests `unittest` existants ; éviter toute écriture racine hors `publish_variant.py`.
- Known knowns: footer condensé racine cassé dans `render_root()` ; ZIPs `span-pan` et `mise-en-gouvernance-du-span` actuellement cohérents après rebuild local ; ZIPs non déterministes avec `archive.write()`.
- Known unknowns: validation humaine requise avant de commiter les 9 ZIPs déjà régénérés ; ShipGuard devra être régénéré ensuite pour refléter l'état corrigé.
- Unknown knowns: `render_root()` n'est pas écrit par `main()`, mais reste testé et peut être appelé par un agent ; il doit donc rester correct.
- Unknown unknowns: d'autres ZIPs peuvent être cohérents aujourd'hui mais manquer de test de fidélité ; le plan limite le correctif obligatoire aux alertes signalées et à la matrice.
- Bad implementation path: corriger uniquement les ZIPs binaires sans rendre `write_zip()` déterministe ; supprimer `render_root()` ; modifier l'accueil racine à la main.
- Guardrail added: tests sur lien ZIP existant, ZIP fidèle aux images, ZIP déterministe.
- Preserved behavior: autonomie des variantes, génération locale par `python3 build.py`, validation par `scripts/validate_variant.sh`, absence d'import runtime vers la matrice.
- Forbidden shortcuts: pas de hand-edit des ZIPs ; pas de mélange silencieux entre ZIPs déjà sales et code ; pas de push sans validation Alex.

## Self-review

- Spec coverage: les quatre alertes `G-Z4-002`, `SG-Z4-003`, `SG-Z4-004`, `SG-Z2-004` ont une tâche de test, une tâche de correction ou une décision explicite.
- Placeholder scan: aucun marqueur de remplissage ni étape sans commande ou code quand un changement est demandé.
- Type consistency: helper stable `write_zip_entry(archive: zipfile.ZipFile, source_path: Path, archive_name: str)` ; constante stable `ZIP_TIMESTAMP`.
