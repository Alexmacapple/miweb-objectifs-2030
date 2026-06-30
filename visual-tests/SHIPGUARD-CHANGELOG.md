# Changelog recette ShipGuard

Ce fichier suit la recette locale ShipGuard dans `visual-tests/`. Il documente
les retours Loic, les commits amont testés, les vérifications passées et le
plan de reprise.

Ne pas confondre avec le changelog produit du repo ShipGuard. Ici, on suit la
recette et les RETEX.

## 2026-06-30 - Validation ShipGuard 2.3.7 recorder preflight

### État validé

Dernière version testée :

```text
ShipGuard 2.3.7
commit: df57f67 fix: make recorder preflight less brittle
```

Installations locales :

```text
Codex  -> shipguard@shipguard 2.3.7 installé et activé
Claude -> shipguard@shipguard 2.3.7 installé et activé, restart requis pour une session déjà ouverte
```

Scripts de recette synchronisés depuis :

```text
/Users/alex/.codex/plugins/cache/shipguard/shipguard/2.3.7
```

### Points recorder validés

- Doc `sg-record` clarifiée : le prérequis est le package Node `playwright`
  importable depuis le projet, pas Playwright Python/global.
- Message `PLAYWRIGHT_MISSING` explicite sur ce prérequis.
- Timeout GUI par défaut passé à `15000ms`.
- Retry automatique une fois présent dans le code.
- Option et variable d'environnement ajoutées et vérifiées :
  `--check-timeout=30000` et `SHIPGUARD_RECORD_CHECK_TIMEOUT=30000`.

### Preuves exécutées

```text
node --check visual-tests/build-review.mjs                         OK
node --check visual-tests/review-smoke-test.mjs                    OK
node --check visual-tests/monitor-smoke-test.mjs                   OK
node --check visual-tests/sg-record.mjs                            OK
node visual-tests/lib/actions-to-yaml.test.mjs                     13 pass, 0 fail
node visual-tests/lib/integration-test.mjs                         11 pass, 0 fail
claude plugin validate .../plugins/shipguard                       Validation passed
node <cache-2.3.7>/skills/sg-record/sg-record.mjs --check          PLAYWRIGHT_MISSING explicite
node visual-tests/sg-record.mjs --check                            PLAYWRIGHT_OK / CHROMIUM_OK / GUI_LAUNCH_OK
node visual-tests/sg-record.mjs --check --check-timeout=30000      PLAYWRIGHT_OK / CHROMIUM_OK / GUI_LAUNCH_OK
SHIPGUARD_RECORD_CHECK_TIMEOUT=30000 node visual-tests/sg-record.mjs --check
                                                                  PLAYWRIGHT_OK / CHROMIUM_OK / GUI_LAUNCH_OK
```

### Verdict pour Loic

Pas de blocage à remonter sur les points recorder corrigés par `df57f67`.

Non vérifiés dans cette passe :

- recorder interactif complet jusqu'au clic humain Stop et génération d'un
  nouveau manifest réel ;
- blocages monitor, favicon, bootstrap MacBook Pro et workflows `sg-visual-run`,
  `sg-visual-fix`, `sg-improve`.

## 2026-06-30 - Reprise prête après addendum Playwright

### État courant

Dernière version testée :

```text
ShipGuard 2.3.6
commit: aa17030 test: add recorder preflight and improve rollback smoke
```

Documents de référence :

```text
visual-tests/AGENTS.md
visual-tests/_results/shipguard-postmortem-loic-2.3.6-retest-github.md
visual-tests/_results/shipguard-plan-test-reprise.md
/Users/alex/Desktop/tests-reprises-alex.md
```

### Addendum Playwright transmis a Loic

Constat :

- une commande `playwright` existait deja localement ;
- elle venait de Playwright Python :

```text
~/Library/Python/3.9/bin/playwright
```

- `sg-record.mjs` importe Playwright cote Node avec `await import('playwright')`.

Conclusion :

Le prerequis du recorder est Playwright Node importable depuis le projet ou le
harness `visual-tests`, pas seulement une commande Playwright globale/Python.

Action locale :

```bash
cd visual-tests
npm init -y
npm install --save-dev playwright
npx playwright install chromium
```

Verification finale :

```text
node visual-tests/sg-record.mjs --check
ShipGuard Recorder Preflight
PLAYWRIGHT_OK
CHROMIUM_OK
GUI_LAUNCH_OK
```

Nuance :

- première tentative après installation : `GUI_LAUNCH_FAILED` sur timeout
  `5000ms` ;
- deuxieme tentative : OK.

Feedback utile pour Loic :

- documenter explicitement Playwright Node local/importable ;
- distinguer Playwright Python/global du package Node ;
- envisager timeout plus long, retry, ou option/env de timeout pour le check
  GUI.

### Plan actif apres addendum

Priorité 1 :

1. `sg-record` interactif reel.
2. `sg-process-check --mode=hybrid`.
3. `sg-visual-run --from-audit`.
4. `sg-visual-run --from-process`.

Priorité 2 :

5. `sg-visual-fix` reel sur copie isolee.
6. `sg-improve` reel sur fixture/copie avec rollback.

Priorité 3 :

7. Monitor live complet apres correction ou validation explicite.
8. `sg-ship` orchestrateur complet.
9. `sg-scout` GitHub reel avec accord explicite.
10. `sg-process-check --mode=execute` avec diff très contrôlé.

## 2026-06-30 - Retour bootstrap MacBook Pro

### Source

Installation ShipGuard sur un MacBook Pro distinct. RETEX dedie :

```text
visual-tests/_results/shipguard-postmortem-loic-2.3.6-macbook-bootstrap.md
```

### Ce qui etait deja couvert

- migration depuis l'ancien adaptateur Codex local ;
- confusion possible entre `shipguard-codex@personal` et `shipguard@shipguard` ;
- besoin d'une doc d'installation Codex claire ;
- distinction entre `agent-browser` disponible et dependances runtime reelles.

### Nouveaux points isoles

1. `SessionStart hook exited with code 127`
   - trace locale : hook Codex du harnais execute `uv run --directory
     /Users/alex/Claude/wiki python hooks/session-start.py` ;
   - interpretation : probablement `uv` ou chemin de harnais absent sur
     machine neuve ;
   - action proposee : WARN non bloquant si le hook de harnais ne peut pas
     tourner.

2. Check ShipGuard non runtime-aware
   - le check peut FAIL sur Claude absent meme si l'usage cible est Codex ;
   - action proposee : `--runtime=codex|claude|all`, WARN pour runtimes non
     demandes.

3. Chemins trop stricts / historiques
   - contrat local pointe encore vers caches `2.3.0` et adaptateur
     `shipguard-codex@personal` ;
   - action proposee : detecter la version installee et preferer
     `shipguard@shipguard`.

4. Bootstrap Codex clean
   - le chemin via `sync-shipguard-codex-adapter.sh` reste manuel et legacy ;
   - action proposee : une doc/commande unique pour
     `codex plugin marketplace add bacoco/shipguard` +
     `codex plugin add shipguard@shipguard`.

5. Validation Claude non bloquante
   - `claude plugin validate --strict` doit etre "non vérifié" si Claude CLI
     absent et runtime cible Codex.

6. Dependances du check
   - le script local echoue si `PyYAML` est absent :
     `[FAIL] PyYAML indisponible: No module named 'yaml'`.

### Phrase courte pour Loic

```text
Le bootstrap devrait etre runtime-aware : si l'utilisateur installe pour Codex,
Claude absent doit etre WARN/non verifie, pas FAIL. Le check doit valider le
runtime demande et detecter la version/plugin installee plutot que des chemins
cache historiques. Cote Codex, privilegier le chemin officiel
shipguard@shipguard et documenter l'ancien adaptateur comme legacy. Le
SessionStart hook code 127 semble relever du harnais local (uv/chemin manquant)
et devrait etre non bloquant pour ShipGuard.
```

## 2026-06-30 - ShipGuard 2.3.6

### Retour Loic

Loic a pousse :

```text
aa17030 test: add recorder preflight and improve rollback smoke
```

Annonce :

- doc migration Codex enrichie pour le cas `EPERM` lors du remove cache ;
- `sg-record.mjs --check` ajoute ;
- diagnostic `PLAYWRIGHT_OK`, `CHROMIUM_OK`, `GUI_LAUNCH_OK` ou erreur precise ;
- doc `sg-record` mise a jour avec prerequis interactifs ;
- smoke test officiel ajoute pour `sg-improve --rollback` ;
- version bump `2.3.6`.

Verifications annoncees par Loic :

- `node --check` sur `sg-record.mjs` et
  `improve-rollback-smoke-test.mjs` ;
- `improve rollback smoke test passed` ;
- `improve dry-run smoke test passed` ;
- `actions-to-yaml.test.mjs` : 13/13 ;
- `claude plugin validate plugins/shipguard` : OK ;
- `sg-record --check` sort bien `PLAYWRIGHT_MISSING` dans un repo sans
  Playwright, avec commande d'installation claire.

### Verification locale

Version / packaging :

```text
Codex  -> shipguard@shipguard 2.3.6
Claude -> shipguard@shipguard 2.3.6, restart requis
Ancien adaptateur shipguard-codex@personal -> not installed
claude plugin validate -> OK
```

Smoke tests et checks :

```text
node --check visual-tests/build-review.mjs                       OK
node --check visual-tests/review-smoke-test.mjs                  OK
node --check visual-tests/monitor-smoke-test.mjs                 OK
node --check visual-tests/sg-record.mjs                          OK
node --check skills/sg-improve/improve-rollback-smoke-test.mjs   OK

review-smoke-test.mjs --port --debug --keep-tmp                 OK
monitor-smoke-test.mjs --port --debug --keep-tmp                OK
visual-fix-dry-run-smoke-test.mjs                               OK
offline-dry-run-smoke-test.mjs                                  OK
improve-dry-run-smoke-test.mjs                                  OK
improve-rollback-smoke-test.mjs                                 OK
actions-to-yaml.test.mjs                                        13/13
visual-tests/lib/integration-test.mjs                           11/11
```

Dashboard :

```text
28 routes
28 PASS
GET /visual-results.json -> 200
GET /favicon.ico         -> 204
HEAD /favicon.ico        -> 404
```

### Points corriges en 2.3.6

- migration Codex : doc du cas `EPERM` ;
- recorder : `--check` et doc prerequis ;
- `sg-improve --rollback` : smoke test officiel ;
- pas de regression sur les smoke tests dry-run/offline ;
- diagnostic recorder beaucoup plus clair.

### Blocages encore ouverts

- Monitor API : `agent-update` avec `id` peut creer `agents.undefined`.
- Monitor API : duplication `r1:z1` pending et `z1` completed.
- `HEAD /favicon.ico` retourne encore `404`.
- `sg-record/lib/integration-test.mjs` n'est pas autonome depuis le cache
  plugin.

RETEX :

```text
visual-tests/_results/shipguard-postmortem-loic-2.3.6-retest-github.md
```

## 2026-06-30 - ShipGuard 2.3.5

### Retour Loic

Loic a pousse :

```text
50e71da test: harden ShipGuard smoke coverage
```

Annonce :

- bump Claude/Codex en `2.3.5` ;
- smoke tests dry-run/offline pour `sg-visual-fix`, `sg-scout`, `sg-improve` ;
- durcissement smoke tests review/monitor : `--port`, `--debug`,
  `--keep-tmp`, diagnostics `listen EPERM` ;
- dashboard : `notranslate`, favicon silencieux, agents legacy, IDs `SG-Z*` ;
- doc sandbox mise a jour ;
- doc migration Codex ajoutee ;
- Codex local reinstall en `shipguard@shipguard 2.3.5` ;
- Claude local mis a jour de `2.3.0` vers `2.3.5`.

### Verification locale

Points confirmes en recette :

- smoke review/monitor avec port fixe : OK ;
- diagnostics `--debug` et `--keep-tmp` : OK ;
- dry-run/offline `sg-visual-fix`, `sg-scout`, `sg-improve` : OK ;
- dashboard protege contre l'auto-traduction : OK ;
- `GET /favicon.ico` silencieux : OK ;
- fallback Agents legacy depuis `SG-Z*` : OK ;
- route `/` affiche `0` plutot qu'une cellule vide : OK.

RETEX :

```text
visual-tests/_results/shipguard-postmortem-loic-2.3.5-github.md
visual-tests/_results/shipguard-postmortem-loic-2.3.5-suite-github.md
```

Points remontes apres 2.3.5 :

- migration remove cache peut demander permission si `EPERM` ;
- besoin de `sg-record --check` ;
- besoin de doc prerequis recorder interactif ;
- besoin de smoke test `sg-improve --rollback`.

## 2026-06-29 - ShipGuard 2.3.4

### Commits amont testes

```text
8edb990 feat: harden visual review contracts
583e6f3 test: add review dashboard smoke tests
304f414 docs: formalize agent workflow contracts
```

### Points validates

- manifests Claude/Codex en `2.3.4` ;
- installation officielle Codex `shipguard@shipguard 2.3.4` ;
- Claude mis a jour en `2.3.4`, restart requis ;
- `visual-results.json` canonique ;
- fallback Markdown conserve ;
- dashboard bind par défaut sur `127.0.0.1` ;
- protection path traversal ;
- `review-smoke-test.mjs` et `monitor-smoke-test.mjs` hors sandbox : OK ;
- `sg-record` tests Node : 13/13 ;
- `sg-record` integration : 11/11 ;
- dashboard sur 28 routes : 28 PASS ;
- lightbox et annotation UI ;
- `POST /save-manifest` et `fix-manifest.json` ;
- `sg-visual-fix --dry-run` plan non destructif ;
- `sg-scout --offline --dry-run` preview ;
- `sg-improve --dry-run` preview.

### Frictions remontees a Loic

- ancien adaptateur Codex local encore actif en parallele ;
- Codex marketplace local pas toujours enregistre ;
- Claude pouvait pointer vers un autre clone marketplace ;
- restart Claude pas assez visible ;
- smoke tests opaques en sandbox sur `listen EPERM` ;
- port aleatoire difficile pour permissions persistantes ;
- fixtures temporaires non visibles ;
- besoin de smoke tests dry-run/offline officiels ;
- agents legacy : badge sans cartes ;
- route `/` sans bug count explicite ;
- auto-traduction Chrome ;
- `favicon.ico` 404.

RETEX :

```text
visual-tests/_results/shipguard-postmortem-loic-2.3.4.md
```

## Avant 2.3.4 - Socle de recette

Fonctionnalites deja exercees avant les retours Loic successifs :

- `sg-visual-discover` : 28 routes detectees.
- `sg-visual-run` : 28/28 PASS.
- `sg-visual-review` : dashboard, onglets, lightbox, annotations.
- `sg-code-audit` quick report-only : 19 constats.
- `sg-process-check --mode=reason` : simulation sans mesure reelle.
- `sg-change-report` : rapports persona generes.
- `sg-visual-review-stop` : arret/relance serveur via `build-review.mjs`.

## Procedure quand Loic envoie un nouveau commit

1. Lire le message de Loic et noter commit + version dans ce changelog.
2. Mettre a jour les marketplaces locaux reellement utilises :

```bash
git -C /Users/alex/.claude/plugins/marketplaces/shipguard fetch origin main
git -C /Users/alex/.claude/plugins/marketplaces/shipguard merge --ff-only origin/main

git -C /Users/alex/.codex/.tmp/marketplaces/shipguard fetch origin main
git -C /Users/alex/.codex/.tmp/marketplaces/shipguard merge --ff-only origin/main
```

3. Installer / mettre a jour :

```bash
codex plugin add shipguard@shipguard
claude plugin marketplace update shipguard
claude plugin update shipguard@shipguard
```

4. Vérifier :

```bash
codex plugin list
claude plugin list
claude plugin validate /Users/alex/.claude/plugins/marketplaces/shipguard/plugins/shipguard
```

5. Copier les scripts actualises dans `visual-tests/` et relancer la smoke
   suite de `visual-tests/AGENTS.md`.
6. Retester d'abord les points que Loic annonce corriges.
7. Mettre a jour ce changelog, le plan de reprise et un nouveau RETEX si des
   frictions restent actionnables.

## Etat Git / hygiene

- `visual-tests/` est un harnais non suivi.
- `visual-tests/node_modules/` est ignore via `visual-tests/.gitignore`.
- Ne pas commit les artefacts de recette sans demande explicite.
- Ne pas modifier le site client pour tester ShipGuard, sauf copie isolee ou
  accord explicite.
