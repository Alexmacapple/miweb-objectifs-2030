# Nettoyage du paramètre slides=all Implementation Plan

> PDG-LARGE-FILE-JUSTIFICATION: plan agentique détaillé nécessaire pour cadrer TDD, propagation multi-variantes, rebuild généré et preuve navigateur sans ambiguïté.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** retirer `slides=all` de l'URL dès que le diaporama revient à une slide unique, sans supprimer les autres paramètres utiles.

**Architecture:** la correction se fait dans le script `MAIN_JS` embarqué par chaque `build.py`. La matrice corrige les futures variantes ; les 9 variantes autonomes reçoivent le même helper local, puis leurs `index.html` sont régénérés.

**Tech Stack:** Python standard library, `unittest`, JavaScript navigateur embarqué, Playwright via `visual-tests` pour le smoke local, scripts shell existants.

---

## PDG pass

Trigger decision: oui, le livrable est un plan exécuté par un agent et change un contrat d'URL utilisateur.

Skill invocation pass: `prd`, `superpowers:writing-plans` et `progressive-disclosure-guard` ont été lus. Réponse légère insuffisante car le bug est dupliqué dans la matrice et 9 variantes autonomes, avec génération HTML à préserver.

Artifacts inspected:
- `miweb-objectifs-2030-v1/build.py`
- `miweb-objectifs-2030-v1/tests/test_site_contracts.py`
- `matrice-slide-ai/tests/test_site_contracts.py`
- recherche `rg` sur `slides=all`, `setUrl`, `window.location.search` et `showSlide`
- `visual-tests/package.json`

Overlap findings: `reuse` du script existant ; `extend` de `setUrl()` par un helper ; `avoid` pour tout nouveau routeur ou nouveau mode de navigation.

| Claim | Source | Verdict | Impact |
|-------|--------|---------|--------|
| V1 conserve `slides=all` en sortie de mode toutes slides | `miweb-objectifs-2030-v1/build.py`, fonction `setUrl()` | Confirmé | L'URL partagée ou rechargée réactive un mode visible obsolète. |
| Le défaut est commun aux variantes | `rg` sur les 10 `build.py` | Confirmé | Corriger seulement V1 laisserait des variantes et la matrice incohérentes. |
| Les tests existants sont surtout des contrats statiques HTML/JS | `miweb-objectifs-2030-v1/tests/test_site_contracts.py`, `matrice-slide-ai/tests/test_site_contracts.py` | Confirmé | Ajouter des assertions statiques ciblées est cohérent avec le style local. |
| Un smoke navigateur est possible sans dépendance racine nouvelle | `visual-tests/package.json` | Confirmé | Playwright peut servir de preuve locale si `visual-tests` est installé. |

Known knowns: `?slides=all` ouvre toutes les slides ; `showSlide()` quitte le mode toutes slides ; `setUrl()` conserve actuellement toute la query string.

Known unknowns: l'environnement peut ne pas avoir les navigateurs Playwright installés ; dans ce cas, installer via `npm ci --prefix visual-tests` puis `npx --prefix visual-tests playwright install chromium`.

Forbidden shortcuts: ne pas supprimer toute la query string ; ne pas corriger seulement V1 ; ne pas modifier l'accueil racine à la main ; ne pas commiter les ZIPs de `PRD-006` dans le commit de navigation.

Regression proof required: tests rouges puis verts, rebuild des variantes, validation standard, smoke navigateur ou blocage explicitement documenté.

PDG self-check, not independent review.

## File Structure

- Modify: `miweb-objectifs-2030-v1/tests/test_site_contracts.py` - contrat V1 qui reproduit l'alerte ShipGuard.
- Modify: `matrice-slide-ai/tests/test_site_contracts.py` - contrat modèle pour les futures variantes.
- Modify: `matrice-slide-ai/build.py` - source modèle du helper d'URL.
- Modify: 9 variant `build.py` files - propagation autonome du helper.
- Generated after rebuild: 9 `*/index.html` files - script embarqué et hash CSP mis à jour.
- Do not stage: `*/assets/downloads/*-slides.zip` unless a separate ZIP commit is explicitly being made.
- Update after implementation: `CHANGELOG.MD` and `prd-meta-workflow/PRD-007-nettoyage-parametre-slides-all.MD`.

## Task 0: Isoler l'état Git

**Files:**
- Inspect: `git status --short --branch`

- [ ] **Step 1: Vérifier les fichiers sales**

Run:

```bash
git status --short --branch
```

Expected before implementation if `PRD-006` ZIPs are still pending:

```text
 M */assets/downloads/*-slides.zip
```

- [ ] **Step 2: Décider du sort des ZIPs avant de coder**

If the 9 ZIPs are still dirty, either commit them separately:

```bash
git add '*/assets/downloads/*-slides.zip'
git commit -m "build: Régénère les ZIP déterministes"
```

or stop and ask Alex. Do not start implementation with ZIPs mixed into the navigation diff.

## Task 1: Ajouter les tests TDD

**Files:**
- Modify: `miweb-objectifs-2030-v1/tests/test_site_contracts.py`
- Modify: `matrice-slide-ai/tests/test_site_contracts.py`

- [ ] **Step 1: Ajouter le test V1**

Add inside `SiteContractsTest`:

```python
    def test_single_slide_url_removes_all_slides_query(self):
        self.assertIn("function slideUrl(index)", self.index_html)
        self.assertIn('params.delete("slides");', self.index_html)
        self.assertIn("const query = params.toString();", self.index_html)
        self.assertIn(
            'return `${window.location.pathname}${query ? `?${query}` : ""}${hash}`;',
            self.index_html,
        )
        self.assertIn("const url = slideUrl(index);", self.index_html)
        self.assertIn(
            "if (window.location.hash === hash && !hasSlidesQuery()) return;",
            self.index_html,
        )
        self.assertNotIn(
            "const url = `${window.location.pathname}${window.location.search}${hash}`;",
            self.index_html,
        )
```

- [ ] **Step 2: Ajouter le même contrat dans la matrice**

Add inside `matrice-slide-ai/tests/test_site_contracts.py`:

```python
    def test_single_slide_url_removes_all_slides_query(self):
        self.assertIn("function slideUrl(index)", self.index_html)
        self.assertIn('params.delete("slides");', self.index_html)
        self.assertIn("const query = params.toString();", self.index_html)
        self.assertIn(
            'return `${window.location.pathname}${query ? `?${query}` : ""}${hash}`;',
            self.index_html,
        )
        self.assertIn("const url = slideUrl(index);", self.index_html)
        self.assertIn(
            "if (window.location.hash === hash && !hasSlidesQuery()) return;",
            self.index_html,
        )
        self.assertNotIn(
            "const url = `${window.location.pathname}${window.location.search}${hash}`;",
            self.index_html,
        )
```

- [ ] **Step 3: Vérifier le rouge**

Run:

```bash
python3 -m unittest discover -s miweb-objectifs-2030-v1/tests -p 'test_site_contracts.py'
python3 -m unittest discover -s matrice-slide-ai/tests -p 'test_site_contracts.py'
```

Expected: both commands fail on `test_single_slide_url_removes_all_slides_query`.

## Task 2: Corriger le helper d'URL dans les générateurs

**Files:**
- Modify: `matrice-slide-ai/build.py`
- Modify: `miweb-objectifs-2030-v1/build.py`
- Modify: `miweb-objectifs-2030-v2/build.py`
- Modify: `miweb-objectifs-2030-v3/build.py`
- Modify: `miweb-objectifs-2030-v4/build.py`
- Modify: `miweb-offre-mutualisee-listes-diffusion-2026-condensee/build.py`
- Modify: `miweb-offre-mutualisee-listes-diffusion-2026-longue/build.py`
- Modify: `span-pan/build.py`
- Modify: `mise-en-gouvernance-du-span/build.py`
- Modify: `checklist-span-operationnel/build.py`

- [ ] **Step 1: Ajouter les helpers après `slideHash(index)`**

Insert in every listed `build.py`:

```javascript
  function hasSlidesQuery() {
    const params = new URLSearchParams(window.location.search);
    return params.has("slides");
  }

  function slideUrl(index) {
    const hash = slideHash(index);
    const params = new URLSearchParams(window.location.search);
    params.delete("slides");
    const query = params.toString();
    return `${window.location.pathname}${query ? `?${query}` : ""}${hash}`;
  }
```

- [ ] **Step 2: Remplacer `setUrl(index, replace)`**

Replace the body of `setUrl()` in every listed `build.py` with:

```javascript
  function setUrl(index, replace) {
    const hash = slideHash(index);
    if (window.location.hash === hash && !hasSlidesQuery()) return;
    const method = replace ? "replaceState" : "pushState";
    const url = slideUrl(index);
    window.history[method](null, "", url);
  }
```

- [ ] **Step 3: Vérifier la propagation source**

Run:

```bash
rg -n "function slideUrl|function hasSlidesQuery|params.delete\\(\"slides\"\\)" --glob build.py .
rg -n 'window\\.location\\.search\\}\\$\\{hash\\}' --glob build.py . && exit 1 || true
```

Expected: 10 occurrences for each new helper pattern and no occurrence of the old URL template.

## Task 3: Rebuild réel des variantes

**Files:**
- Generated: 9 `*/index.html`

- [ ] **Step 1: Rebuild les vrais dossiers**

Run:

```bash
for slug in miweb-objectifs-2030-v1 miweb-objectifs-2030-v2 miweb-objectifs-2030-v3 miweb-objectifs-2030-v4 miweb-offre-mutualisee-listes-diffusion-2026-condensee miweb-offre-mutualisee-listes-diffusion-2026-longue span-pan mise-en-gouvernance-du-span checklist-span-operationnel; do
  (cd "$slug" && python3 build.py) || exit 1
done
```

Expected: exit code 0.

- [ ] **Step 2: Vérifier les fichiers générés**

Run:

```bash
git diff --name-only
```

Expected: `build.py`, tests, 9 `index.html`, docs if already updated. ZIPs must not appear unless they were intentionally committed or regenerated separately before this plan.

## Task 4: Valider

**Files:**
- Test: all variant tests
- Test: `matrice-slide-ai/tests`

- [ ] **Step 1: Lancer les tests unitaires**

Run:

```bash
python3 -m unittest discover -s matrice-slide-ai/tests
for slug in miweb-objectifs-2030-v1 miweb-objectifs-2030-v2 miweb-objectifs-2030-v3 miweb-objectifs-2030-v4 miweb-offre-mutualisee-listes-diffusion-2026-condensee miweb-offre-mutualisee-listes-diffusion-2026-longue span-pan mise-en-gouvernance-du-span checklist-span-operationnel; do
  python3 -m unittest discover -s "$slug/tests" || exit 1
done
```

Expected: all tests pass.

- [ ] **Step 2: Lancer les validations standard**

Run:

```bash
for slug in miweb-objectifs-2030-v1 miweb-objectifs-2030-v2 miweb-objectifs-2030-v3 miweb-objectifs-2030-v4 miweb-offre-mutualisee-listes-diffusion-2026-condensee miweb-offre-mutualisee-listes-diffusion-2026-longue span-pan mise-en-gouvernance-du-span checklist-span-operationnel; do
  scripts/validate_variant.sh "$slug" || exit 1
done
```

Expected: all validations pass.

- [ ] **Step 3: Vérifier en navigateur local**

Start or reuse the local server:

```bash
scripts/serve-local.sh 8000
```

In another shell, run:

```bash
cd visual-tests
npm ci
node --input-type=module <<'NODE'
import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.goto('http://127.0.0.1:8000/miweb-objectifs-2030-v1/?slides=all#diaporama', { waitUntil: 'domcontentloaded' });
await page.locator('[data-slide-all]').click();
const url = new URL(page.url());
if (url.searchParams.has('slides')) {
  throw new Error(`slides query still present: ${page.url()}`);
}
if (!url.hash.startsWith('#slide-')) {
  throw new Error(`single slide hash missing: ${page.url()}`);
}
await browser.close();
NODE
```

Expected: exit code 0. If Chromium is missing, run `npx playwright install chromium` from `visual-tests`, then repeat.

## Task 5: Mettre à jour les docs et commiter localement

**Files:**
- Modify: `CHANGELOG.MD`
- Modify: `prd-meta-workflow/PRD-007-nettoyage-parametre-slides-all.MD`

- [ ] **Step 1: Ajouter le changelog d'implémentation**

Add to `CHANGELOG.MD` under `2026-07-01`:

```markdown
- Implémentation locale du `PRD-007` : nettoyage de `slides=all` à la sortie du mode toutes slides.
```

Add to the PRD changelog:

```markdown
| 2026-07-01 | Alex + Codex | Implémentation locale du PRD |
```

- [ ] **Step 2: Contrôler les accents**

Run from `/Users/alex/Claude`:

```bash
bash scripts/check-accents.sh miweb-objectifs-2030/CHANGELOG.MD miweb-objectifs-2030/prd-meta-workflow/PRD-007-nettoyage-parametre-slides-all.MD
```

Expected: exit code 0.

- [ ] **Step 3: Contrôler le diff et commiter**

Run:

```bash
git diff --check
git status --short
git diff --name-only | rg 'assets/downloads|\\.zip$' && exit 1 || true
git add CHANGELOG.MD prd-meta-workflow/PRD-007-nettoyage-parametre-slides-all.MD matrice-slide-ai/tests/test_site_contracts.py miweb-objectifs-2030-v1/tests/test_site_contracts.py matrice-slide-ai/build.py miweb-objectifs-2030-v1/build.py miweb-objectifs-2030-v2/build.py miweb-objectifs-2030-v3/build.py miweb-objectifs-2030-v4/build.py miweb-offre-mutualisee-listes-diffusion-2026-condensee/build.py miweb-offre-mutualisee-listes-diffusion-2026-longue/build.py span-pan/build.py mise-en-gouvernance-du-span/build.py checklist-span-operationnel/build.py miweb-objectifs-2030-v1/index.html miweb-objectifs-2030-v2/index.html miweb-objectifs-2030-v3/index.html miweb-objectifs-2030-v4/index.html miweb-offre-mutualisee-listes-diffusion-2026-condensee/index.html miweb-offre-mutualisee-listes-diffusion-2026-longue/index.html span-pan/index.html mise-en-gouvernance-du-span/index.html checklist-span-operationnel/index.html
git diff --cached --check
git commit -m "fix: Nettoie le mode toutes slides dans les URLs"
```

Expected: commit local created, no push.
