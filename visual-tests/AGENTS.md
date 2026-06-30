# AGENTS.md - reprise tests ShipGuard

## Règle de conduite

Toujours répondre et documenter en français.

Ce dossier `visual-tests/` est un harnais de recette pour tester le plugin
ShipGuard sur le dépôt courant. Le but est de tester ShipGuard, pas de corriger
le site client sauf demande explicite.

Ne pas faire de commit pendant cette recette. L'état Git attendu du dépôt parent
reste :

```text
?? visual-tests/
```

## État courant connu

Dernière version testée :

```text
ShipGuard 2.3.7
commit amont: df57f67 fix: make recorder preflight less brittle
date de reprise: 2026-06-30
```

Installations locales connues :

```text
Codex  -> shipguard@shipguard 2.3.7 installé et activé
Claude -> shipguard@shipguard 2.3.7 installé et activé, restart requis pour une session déjà ouverte
Ancien adaptateur Codex shipguard-codex@personal -> not installed
```

RETEX de référence :

```text
visual-tests/_results/shipguard-postmortem-loic-2.3.6-retest-github.md
visual-tests/_results/shipguard-postmortem-loic-2.3.6-macbook-bootstrap.md
```

Plan de reprise de référence :

```text
visual-tests/_results/shipguard-plan-test-reprise.md
/Users/alex/Desktop/tests-reprises-alex.md
```

Changelog de recette :

```text
visual-tests/SHIPGUARD-CHANGELOG.md
```

## Point Playwright à ne pas oublier

`sg-record.mjs` importe Playwright côté Node :

```js
await import('playwright')
```

Une commande Playwright Python ou globale ne suffit pas. Le package Node
`playwright` doit être résolvable depuis le projet ou depuis ce harnais.

État courant :

```text
visual-tests/package.json
visual-tests/package-lock.json
visual-tests/node_modules/playwright
```

Installation déjà faite :

```bash
cd visual-tests
npm init -y
npm install --save-dev playwright
npx playwright install chromium
```

Vérification passée :

```bash
node visual-tests/sg-record.mjs --check
```

Sortie attendue :

```text
ShipGuard Recorder Preflight
PLAYWRIGHT_OK
CHROMIUM_OK
GUI_LAUNCH_OK
```

Correctif `df57f67` validé : le check GUI utilise un timeout par défaut de
`15000ms`, retente une fois et accepte `--check-timeout=30000` ou
`SHIPGUARD_RECORD_CHECK_TIMEOUT=30000`.

## Si Loic revient avec un nouveau commit

1. Noter le commit et le message dans `visual-tests/SHIPGUARD-CHANGELOG.md`.
2. Mettre à jour les deux marketplaces locaux si les deux existent :

```bash
git -C /Users/alex/.claude/plugins/marketplaces/shipguard fetch origin main
git -C /Users/alex/.claude/plugins/marketplaces/shipguard merge --ff-only origin/main

git -C /Users/alex/.codex/.tmp/marketplaces/shipguard fetch origin main
git -C /Users/alex/.codex/.tmp/marketplaces/shipguard merge --ff-only origin/main
```

3. Vérifier le commit :

```bash
git -C /Users/alex/.claude/plugins/marketplaces/shipguard rev-parse --short HEAD
git -C /Users/alex/.codex/.tmp/marketplaces/shipguard rev-parse --short HEAD
```

4. Réinstaller / mettre à jour les plugins :

```bash
codex plugin add shipguard@shipguard
claude plugin marketplace update shipguard
claude plugin update shipguard@shipguard
claude plugin list
codex plugin list
```

5. Valider le plugin Claude :

```bash
claude plugin validate /Users/alex/.claude/plugins/marketplaces/shipguard/plugins/shipguard
```

6. Copier dans ce harnais les scripts ShipGuard à retester depuis le cache
   Codex de la nouvelle version :

```text
skills/sg-visual-review/build-review.mjs        -> visual-tests/build-review.mjs
skills/sg-visual-review/_review-template.html   -> visual-tests/_review-template.html
skills/sg-visual-review/review-smoke-test.mjs   -> visual-tests/review-smoke-test.mjs
skills/sg-visual-review/monitor-smoke-test.mjs  -> visual-tests/monitor-smoke-test.mjs
skills/sg-record/sg-record.mjs                  -> visual-tests/sg-record.mjs
skills/sg-record/lib/*                          -> visual-tests/lib/
```

Ne pas copier `node_modules/` depuis ou vers le plugin.

## Smoke suite à relancer après nouveau commit

Adapter le chemin `2.3.x` à la nouvelle version installée.

```bash
node --check visual-tests/build-review.mjs
node --check visual-tests/review-smoke-test.mjs
node --check visual-tests/monitor-smoke-test.mjs
node --check visual-tests/sg-record.mjs

node visual-tests/review-smoke-test.mjs --port=23114 --debug --keep-tmp
node visual-tests/monitor-smoke-test.mjs --port=23115 --debug --keep-tmp

node visual-tests/lib/actions-to-yaml.test.mjs
node visual-tests/lib/integration-test.mjs
node visual-tests/sg-record.mjs --check

node /Users/alex/.codex/plugins/cache/shipguard/shipguard/2.3.x/skills/sg-visual-fix/visual-fix-dry-run-smoke-test.mjs
node /Users/alex/.codex/plugins/cache/shipguard/shipguard/2.3.x/skills/sg-scout/offline-dry-run-smoke-test.mjs
node /Users/alex/.codex/plugins/cache/shipguard/shipguard/2.3.x/skills/sg-improve/improve-dry-run-smoke-test.mjs
node /Users/alex/.codex/plugins/cache/shipguard/shipguard/2.3.x/skills/sg-improve/improve-rollback-smoke-test.mjs
```

Les smoke tests `review` et `monitor` ouvrent un serveur local. En sandbox,
relancer avec autorisation locale si `listen EPERM` ou `curl` échoue.

## Blocages encore ouverts côté ShipGuard hors recorder 2.3.7

À vérifier si Loic annonce une correction :

1. Monitor API : `POST /api/monitor/agent-update` avec `{"id":"z1"}` crée
   encore `agents.undefined`.
2. Monitor API : un cycle `audit-start` puis `agent-update` peut laisser
   `r1:z1` en `pending` et crée `z1` en `completed`.
3. `HEAD /favicon.ico` répond encore `404` alors que `GET /favicon.ico`
   répond `204`.
4. `skills/sg-record/lib/integration-test.mjs` n'est pas autonome depuis le
   cache plugin : il tente d'écrire dans le cache et suppose `build-review.mjs`
   dans `skills/sg-record`.

## Retour MacBook Pro à reprendre si Loic corrige le bootstrap

RETEX :

```text
visual-tests/_results/shipguard-postmortem-loic-2.3.6-macbook-bootstrap.md
```

Points nouveaux :

1. `SessionStart hook exited with code 127` : probablement hook de harnais local
   (`uv` ou chemin `/Users/alex/Claude/wiki` absent), à traiter comme WARN non
   bloquant pour ShipGuard.
2. Check de harnais trop multi-runtime : Claude absent ne doit pas faire FAIL
   si le runtime cible est Codex.
3. Contrat local trop strict : chemins `~/.claude/...`, caches `2.3.0`, ancien
   `shipguard-codex@personal` encore encodé.
4. Bootstrap Codex clean : préférer `shipguard@shipguard` officiel ; garder
   `sync-shipguard-codex-adapter.sh` comme legacy.
5. `claude plugin validate --strict` doit être "non vérifié" si Claude CLI est
   absent et que le runtime cible est Codex.
6. Le script local `check-shipguard-harness-fit.sh` dépend de `PyYAML` et
   échoue avant les checks si `yaml` est absent.

Critère attendu d'un futur patch :

```text
check --runtime=codex
Codex: OK
Claude: WARN non installé / non vérifié
Verdict global: OK pour runtime cible codex
```

## Plan de test actif

Priorité 1, faisable maintenant :

1. `sg-record` interactif réel.
2. `sg-process-check --mode=hybrid`.
3. `sg-visual-run --from-audit`.
4. `sg-visual-run --from-process`.

Priorité 2, seulement sur copie isolée ou zone de test :

5. `sg-visual-fix` réel.
6. `sg-improve` réel avec rollback.

Priorité 3, attendre correction ou validation explicite :

7. Monitor live complet.
8. `sg-ship` orchestrateur complet.
9. `sg-scout` GitHub réel.
10. `sg-process-check --mode=execute`.

## Commandes utiles

Construire ou servir le dashboard :

```bash
node visual-tests/build-review.mjs
node visual-tests/build-review.mjs --serve --port=23113
node visual-tests/build-review.mjs --stop
```

Vérifier l'état HTTP local du dashboard :

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:23113/visual-results.json
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:23113/favicon.ico
curl -s -I -o /dev/null -w '%{http_code}\n' http://127.0.0.1:23113/favicon.ico
```

Tester le monitor live minimal :

```bash
curl -s -i -X POST http://127.0.0.1:23113/api/monitor/audit-start \
  -H 'Content-Type: application/json' \
  -d '{"timestamp":"2026-06-30T10:40:00.000Z","mode":"retest","zones":[{"zone_id":"z1","paths":["src"],"file_count":1}]}'

curl -s -i -X POST http://127.0.0.1:23113/api/monitor/agent-update \
  -H 'Content-Type: application/json' \
  -d '{"agent_id":"z1","status":"completed","bugs_found":0,"tokens":10}'

curl -s http://127.0.0.1:23113/api/monitor/status
```

## Interdits sans accord explicite

- Ne pas créer/commenter d'issue GitHub via `sg-scout` sans validation.
- Ne pas lancer `sg-visual-fix` réel sur le dépôt principal sans copie isolée.
- Ne pas lancer `sg-improve` réel sans accepter les écritures `.shipguard/`.
- Ne pas lancer `sg-process-check --mode=execute` sans diff très contrôlé.
- Ne pas commit les artefacts de recette.
