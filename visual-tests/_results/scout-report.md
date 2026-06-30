# Scout Report - dry-run offline ShipGuard 2.3.4

Mode : `--offline --dry-run`
Fixture : `visual-tests/fixtures/scout-repos.json`
Date : 2026-06-29

## Résumé

Repos scannés : 1
Techniques trouvées : 3
Propositions publiées : 0, dry-run sans GitHub

Ce rapport prouve le chemin offline/dry-run sans accès réseau, sans création
d'issue GitHub et sans écriture dans `docs/scout-reports/`.

## Top Findings

### 1. Smoke tests isolés du dashboard

Source : `bacoco/ShipGuard` - `review-smoke-test.mjs`
Score : 4.2/5.0
Catégorie : testability

Ce que fait la technique :

Le test construit un fixture temporaire, génère `review.html`, démarre un
serveur local, vérifie les fichiers servis, teste `POST /save-manifest` et le
rejet path traversal encodé.

Adaptation ShipGuard :

Conserver ce pattern et l'étendre aux chemins encore non couverts :

- `sg-visual-fix --dry-run` ;
- `sg-scout --offline --dry-run` ;
- `sg-improve --dry-run`.

### 2. Monitor API smoke test

Source : `bacoco/ShipGuard` - `monitor-smoke-test.mjs`
Score : 3.8/5.0
Catégorie : observability

Ce que fait la technique :

Elle vérifie les endpoints temps réel `audit-start`, `agent-update`, `status`
et `audit-complete` avec persistance dans `audit-monitor.json`.

Adaptation ShipGuard :

Ajouter un cas où plusieurs agents partagent un préfixe legacy ou un format
d'ID différent, pour éviter les panneaux vides avec badge non nul.

### 3. Documentation sandbox explicite

Source : `bacoco/ShipGuard` - `docs/sandbox.md`
Score : 3.6/5.0
Catégorie : developer-experience

Ce que fait la technique :

Elle documente les contraintes d'environnement pour les serveurs locaux, le
navigateur, GitHub et les écritures locales.

Adaptation ShipGuard :

Ajouter les retours de cette reprise :

- `listen EPERM` doit apparaître dans les erreurs smoke test ;
- les smoke tests ouvrent un port aléatoire ;
- Chrome auto-translate peut muter le dashboard et déclencher du réseau externe.

## All Techniques

| # | Technique | Source | Score | Catégorie | Statut |
|---|---|---:|---:|---|---|
| 1 | Smoke tests isolés du dashboard | review-smoke-test.mjs | 4.2 | testability | proposed |
| 2 | Monitor API smoke test | monitor-smoke-test.mjs | 3.8 | observability | proposed |
| 3 | Documentation sandbox explicite | docs/sandbox.md | 3.6 | developer-experience | proposed |

## Repos Analyzed

| Repo | Techniques | Top Score |
|---|---:|---:|
| bacoco/ShipGuard | 3 | 4.2 |

Run without `--dry-run` to publish these findings.
