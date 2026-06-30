# Typage strict de slides.json Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** refuser tôt et clairement les `slides.json` dont les champs ont un type invalide.

**Architecture:** le contrat est porté par `load_slides()` dans `build.py`, car c'est le dernier point commun avant rendu HTML, Markdown et ZIP. Les variantes sont autonomes : la validation est donc copiée dans chaque `build.py` concerné, sans import runtime vers `matrice-slide-ai/`.

**Tech Stack:** Python standard library, `unittest`, scripts shell existants, validateurs HTML npm verrouillés.

---

## Structure de fichiers

- Modifier : `matrice-slide-ai/build.py` — ajouter la validation stricte des types dans `load_slides()`.
- Modifier : `matrice-slide-ai/tests/test_matrix_workflow.py` — ajouter les tests TDD invalides et positifs sur les types.
- Modifier : `matrice-slide-ai/tests/test_site_contracts.py` — renforcer le contrat des types sur la matrice.
- Modifier : `*/build.py` des variantes autonomes — propager le même garde sans dépendance vers la matrice.
- Modifier après implémentation : `CHANGELOG.MD` et le PRD associé si créé ensuite.

## Règles à figer

- `slides` doit être une liste non vide de dictionnaires.
- `numero` doit être un entier strict, pas une chaîne convertible, et pas un booléen.
- `titre`, `image`, `alt`, `description` et `message` doivent être des chaînes non vides, après suppression des espaces de bord.
- `textes_visibles` doit être une liste non vide de chaînes non vides.
- Les erreurs doivent être des `ValueError` contenant `slides.json` et le nom du champ fautif.
- Le garde de chemin image existant sous `assets/slides/` reste séparé et réutilisé.

## Task 1: Tests TDD sur les types invalides

**Files:**
- Modify: `matrice-slide-ai/tests/test_matrix_workflow.py`

- [ ] **Step 1: Add helper for one-field invalid slides**

Add this helper inside `MatrixWorkflowTest`, near the existing `create_temp_variant()` helper:

```python
    def write_first_slide_override(self, target, override):
        slides_path = target / "slides.json"
        slides = json.loads(slides_path.read_text(encoding="utf-8"))
        slides[0].update(override)
        slides_path.write_text(
            json.dumps(slides, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def run_variant_build(self, target):
        return run(
            [sys.executable, str(target / "build.py")],
            cwd=target,
            stdout=PIPE,
            stderr=PIPE,
            text=True,
        )

    def run_build_with_first_slide_override(self, override):
        repo = Path(__file__).resolve().parents[2]
        with TemporaryDirectory() as tmp_dir:
            target = self.create_temp_variant(repo, tmp_dir)
            self.write_first_slide_override(target, override)
            return self.run_variant_build(target)
```

- [ ] **Step 2: Add invalid type tests**

Add this test in `MatrixWorkflowTest`:

```python
    def test_variant_build_rejects_invalid_slides_root_type(self):
        repo = Path(__file__).resolve().parents[2]
        with TemporaryDirectory() as tmp_dir:
            target = self.create_temp_variant(repo, tmp_dir)
            (target / "slides.json").write_text(
                json.dumps({"numero": 1}, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            result = self.run_variant_build(target)

            self.assertNotEqual(0, result.returncode)
            self.assertIn("slides.json", result.stderr)
            self.assertIn("liste", result.stderr)

    def test_variant_build_rejects_invalid_slide_field_types(self):
        invalid_cases = [
            (None, "objet"),
            ({"numero": "1"}, "numero"),
            ({"numero": True}, "numero"),
            ({"titre": ["Titre"]}, "titre"),
            ({"titre": " "}, "titre"),
            ({"image": 42}, "image"),
            ({"image": " "}, "image"),
            ({"alt": None}, "alt"),
            ({"alt": " "}, "alt"),
            ({"description": 42}, "description"),
            ({"description": " "}, "description"),
            ({"textes_visibles": "texte au lieu de liste"}, "textes_visibles"),
            ({"textes_visibles": []}, "textes_visibles"),
            ({"textes_visibles": [""]}, "textes_visibles"),
            ({"message": {}}, "message"),
            ({"message": " "}, "message"),
        ]

        for override, field_name in invalid_cases:
            value = override if not isinstance(override, dict) else override[field_name]
            with self.subTest(field=field_name, value=value):
                if isinstance(override, dict):
                    result = self.run_build_with_first_slide_override(override)
                else:
                    repo = Path(__file__).resolve().parents[2]
                    with TemporaryDirectory() as tmp_dir:
                        target = self.create_temp_variant(repo, tmp_dir)
                        slides_path = target / "slides.json"
                        slides = json.loads(slides_path.read_text(encoding="utf-8"))
                        slides[0] = override
                        slides_path.write_text(
                            json.dumps(slides, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8",
                        )
                        result = self.run_variant_build(target)
                self.assertNotEqual(0, result.returncode)
                self.assertIn("slides.json", result.stderr)
                self.assertIn(field_name, result.stderr)
```

- [ ] **Step 3: Add positive type test**

Add this test in `MatrixWorkflowTest`:

```python
    def test_variant_build_accepts_valid_slide_field_types(self):
        repo = Path(__file__).resolve().parents[2]
        with TemporaryDirectory() as tmp_dir:
            target = self.create_temp_variant(repo, tmp_dir)
            self.write_first_slide_override(
                target,
                {
                    "numero": 1,
                    "titre": "Titre valide",
                    "image": "assets/slides/slide-01.png",
                    "alt": "Alternative valide.",
                    "description": "Description valide.",
                    "textes_visibles": ["Texte visible valide"],
                    "message": "Message valide.",
                },
            )

            result = self.run_variant_build(target)

            self.assertEqual(0, result.returncode, result.stderr)
            index_html = (target / "index.html").read_text(encoding="utf-8")
            self.assertIn('src="assets/slides/slide-01.png"', index_html)
```

- [ ] **Step 4: Run tests and verify failure before implementation**

Run:

```bash
python3 -m unittest discover -s matrice-slide-ai/tests -p 'test_matrix_workflow.py'
```

Expected before implementation:

```text
FAIL
```

At least one invalid case is currently accepted or fails with the wrong error contract.

## Task 2: Validation stricte dans build.py

**Files:**
- Modify: `matrice-slide-ai/build.py`
- Modify: all current variant `build.py` files matching `rg -l 'def load_slides' --glob build.py .`

- [ ] **Step 1: Add validation helpers in `matrice-slide-ai/build.py`**

Add these helpers above `load_slides()`:

```python
def require_non_empty_string(slide_number: object, field_name: str, value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(
            f"slides.json slide {slide_number} : champ {field_name} doit être une chaîne non vide."
        )
    return value


def require_visible_texts(slide_number: object, value: object) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError(
            f"slides.json slide {slide_number} : champ textes_visibles doit être une liste non vide."
        )
    for index, item in enumerate(value, start=1):
        if not isinstance(item, str) or not item.strip():
            raise ValueError(
                "slides.json slide "
                f"{slide_number} : textes_visibles[{index}] doit être une chaîne non vide."
            )
    return value


def validate_slide_contract(slide: object, expected_numero: int) -> dict:
    if not isinstance(slide, dict):
        raise ValueError(f"slides.json slide {expected_numero} doit être un objet.")
    required = {"numero", "titre", "image", "alt", "description", "textes_visibles", "message"}
    missing = required - set(slide)
    if missing:
        raise ValueError(
            f"slides.json slide {slide.get('numero', '?')} : champs manquants {sorted(missing)}."
        )
    if type(slide["numero"]) is not int:
        raise ValueError(
            f"slides.json slide {slide.get('numero', '?')} : champ numero doit être un entier."
        )
    if slide["numero"] != expected_numero:
        raise ValueError(
            f"Numéro de slide inattendu : {slide['numero']} au lieu de {expected_numero}."
        )
    for field_name in ("titre", "image", "alt", "description", "message"):
        require_non_empty_string(slide["numero"], field_name, slide[field_name])
    require_visible_texts(slide["numero"], slide["textes_visibles"])
    return slide


def validate_slides_root(slides: object) -> list[dict]:
    if not isinstance(slides, list) or not slides:
        raise ValueError("slides.json doit contenir une liste non vide de slides.")
    return slides
```

- [ ] **Step 2: Use the helper in `load_slides()`**

Replace the current required-field and `int(slide["numero"])` block with:

```python
    slides = validate_slides_root(slides)
    for expected_numero, slide in enumerate(slides, start=1):
        slide = validate_slide_contract(slide, expected_numero)
        resolve_slide_image_path(slide["image"], require_exists=require_image_files)
```

For V1/V2 style builds that keep `len(slides) == 10`, run `validate_slides_root(slides)` before the length check and preserve that length check before the loop.

- [ ] **Step 3: Run targeted tests**

Run:

```bash
python3 -m unittest discover -s matrice-slide-ai/tests -p 'test_matrix_workflow.py'
```

Expected:

```text
OK
```

- [ ] **Step 4: Remove remaining numeric coercion**

Replace any `int(slide["numero"])` or `int(slide['numero'])` usage with direct
use of the already validated integer. For example:

```python
def slide_id(slide: dict) -> str:
    return f"slide-{slide['numero']:02d}"
```

Run:

```bash
rg "int\\(slide\\[['\\\"]numero['\\\"]\\]\\)" --glob build.py .
```

Expected:

```text
no output
```

## Task 3: Propagation aux variantes autonomes

**Files:**
- Modify: `checklist-span-operationnel/build.py`
- Modify: `mise-en-gouvernance-du-span/build.py`
- Modify: `miweb-objectifs-2030-v1/build.py`
- Modify: `miweb-objectifs-2030-v2/build.py`
- Modify: `miweb-objectifs-2030-v3/build.py`
- Modify: `miweb-objectifs-2030-v4/build.py`
- Modify: `miweb-offre-mutualisee-listes-diffusion-2026-condensee/build.py`
- Modify: `miweb-offre-mutualisee-listes-diffusion-2026-longue/build.py`
- Modify: `span-pan/build.py`

- [ ] **Step 1: Copy the validation helpers into each autonomous `build.py`**

Copy the exact helpers from Task 2 into each `build.py`, next to `resolve_slide_image_path()`.

- [ ] **Step 2: Update each `load_slides()` loop**

Use the same pattern, adapting existing loops that currently do `for slide in slides` to `enumerate(slides, start=1)`:

```python
    slides = validate_slides_root(slides)
    for expected_numero, slide in enumerate(slides, start=1):
        slide = validate_slide_contract(slide, expected_numero)
        resolve_slide_image_path(slide["image"], require_exists=require_image_files)
```

For variants without `slides.example.json`, omit `require_exists=require_image_files` and call:

```python
        resolve_slide_image_path(slide["image"])
```

- [ ] **Step 3: Verify no runtime dependency was introduced**

Run:

```bash
rg -n 'matrice[-_]slide[-_]ai|matrice-slide-ai' --glob build.py .
```

Expected:

```text
no output
```

## Task 4: Contract tests and full local validation

**Files:**
- Modify: `matrice-slide-ai/tests/test_site_contracts.py`

- [ ] **Step 1: Strengthen site contract types**

In `test_slides_json_matches_images()`, add assertions:

```python
            self.assertIsInstance(slide["numero"], int)
            for field_name in ("titre", "image", "alt", "description", "message"):
                with self.subTest(field=field_name, slide=slide["numero"]):
                    self.assertIsInstance(slide[field_name], str)
                    self.assertTrue(slide[field_name].strip())
            self.assertIsInstance(slide["textes_visibles"], list)
            self.assertTrue(slide["textes_visibles"])
            for text in slide["textes_visibles"]:
                self.assertIsInstance(text, str)
                self.assertTrue(text.strip())
```

- [ ] **Step 2: Run matrix tests**

Run:

```bash
python3 -m unittest discover -s matrice-slide-ai/tests
```

Expected:

```text
OK
```

- [ ] **Step 3: Rebuild real folders after Alex validates**

Run only after explicit local rebuild approval:

```bash
for slug in miweb-objectifs-2030-v1 miweb-objectifs-2030-v2 miweb-objectifs-2030-v3 miweb-objectifs-2030-v4 miweb-offre-mutualisee-listes-diffusion-2026-condensee miweb-offre-mutualisee-listes-diffusion-2026-longue span-pan mise-en-gouvernance-du-span checklist-span-operationnel; do
  (cd "$slug" && python3 build.py)
done
```

Expected:

```text
exit code 0
```

- [ ] **Step 4: Validate all variants**

Run:

```bash
for slug in miweb-objectifs-2030-v1 miweb-objectifs-2030-v2 miweb-objectifs-2030-v3 miweb-objectifs-2030-v4 miweb-offre-mutualisee-listes-diffusion-2026-condensee miweb-offre-mutualisee-listes-diffusion-2026-longue span-pan mise-en-gouvernance-du-span checklist-span-operationnel; do
  scripts/validate_variant.sh "$slug"
done
```

Expected:

```text
OK for every variant
```

## Task 5: Commit boundaries

**Files:**
- All modified files from previous tasks.

- [ ] **Step 1: Commit code and tests**

Run:

```bash
git add checklist-span-operationnel/build.py matrice-slide-ai/build.py mise-en-gouvernance-du-span/build.py miweb-objectifs-2030-v1/build.py miweb-objectifs-2030-v2/build.py miweb-objectifs-2030-v3/build.py miweb-objectifs-2030-v4/build.py miweb-offre-mutualisee-listes-diffusion-2026-condensee/build.py miweb-offre-mutualisee-listes-diffusion-2026-longue/build.py span-pan/build.py matrice-slide-ai/tests/test_matrix_workflow.py matrice-slide-ai/tests/test_site_contracts.py
git commit -m "fix: Valide les types de slides.json"
```

- [ ] **Step 2: Commit regenerated artifacts separately if any**

Run:

```bash
git status --short
```

If only ZIP artifacts changed after real rebuild:

```bash
git add '*/assets/downloads/*-slides.zip'
git commit -m "build: Régénère les ZIP après validation slides"
```

## Self-review

- Spec coverage: invalid root type, invalid slide object type, invalid fields, positive case, autonomous variants, no runtime import, full local validation are each covered by a task.
- Placeholder scan: aucun marqueur de remplissage ni test non spécifié.
- Type consistency: helper names are stable: `require_non_empty_string`, `require_visible_texts`, `validate_slide_contract`, `resolve_slide_image_path`.
