# Postmortem ShipGuard 2.3.7 - validation finale

Date : 2026-06-30

Destinataire : Loïc, pour action éventuelle dans le dépôt ShipGuard.

Périmètre : retest du plugin ShipGuard `2.3.7`, commit amont
`df57f67 fix: make recorder preflight less brittle`, sur le harnais
`visual-tests/` du dépôt MiWeb. Les constats ci-dessous ne retiennent que les
points génériques utiles pour ShipGuard.

## Verdict court

Les smoke tests principaux passent et le plugin est utilisable pour une recette
complète report-only. Les points recorder corrigés en `2.3.7` sont validés sur
le préflight et sur l'arrêt par bouton `Stop`.

Il reste des sujets produit à corriger ou à clarifier :

1. le monitor live accepte `id` mais écrit encore `agents.undefined` ;
2. les agents préremplis `r1:z1` / `r1:z2` ne sont pas réconciliés avec les
   updates `z1` / `z2` ;
3. les sous-runs visuels perdent leur scope après rebuild de la review ;
4. la route `/` peut sélectionner toute la suite par matching préfixe ;
5. les routes non HTML ne sont pas représentées comme `skipped` ou
   `uncovered` dans le résultat machine ;
6. `sg-record` valide `Stop` en E2E, mais `Check` reste validé seulement au
   niveau de la barre injectée, pas dans un test E2E complet ;
7. `sg-ship` est documenté comme orchestrateur, mais n'existe pas comme
   commande shell native.

## Socle validé

### Version testée

```text
ShipGuard marketplace HEAD : df57f67
Plugin cache Codex         : shipguard/2.3.7
Dépôt MiWeb                : 42b85d5
```

### Smokes et checks passants

```text
node --check visual-tests/build-review.mjs                         OK
node --check visual-tests/review-smoke-test.mjs                    OK
node --check visual-tests/monitor-smoke-test.mjs                   OK
node --check visual-tests/sg-record.mjs                            OK
node visual-tests/lib/actions-to-yaml.test.mjs                     13 pass, 0 fail
node visual-tests/lib/integration-test.mjs                         11 pass, 0 fail
node visual-tests/review-smoke-test.mjs --port=23124 --debug       review smoke test passed
node visual-tests/monitor-smoke-test.mjs --port=23125 --debug      monitor smoke test passed
node .../sg-visual-fix/visual-fix-dry-run-smoke-test.mjs           visual-fix dry-run smoke test passed
node .../sg-scout/offline-dry-run-smoke-test.mjs                   scout offline dry-run smoke test passed
node .../sg-improve/improve-dry-run-smoke-test.mjs                 improve dry-run smoke test passed
node .../sg-improve/improve-rollback-smoke-test.mjs                improve rollback smoke test passed
```

### Run visuel complet

Le runner statique local a exécuté les 28 routes :

```text
[sg-visual-run] Visual run complete: 28/28 passed
```

Après restauration du JSON canonique et rebuild :

```text
Status: 28 pass, 0 fail, 0 error, 0 stale, 0 skipped
Screenshots matched: 28/28
Found 3 recorded manifests
```

## Points confirmés

### B1 - Monitor : `id` devient `agents.undefined`

Sévérité proposée : haute.

Reproduction exécutée sur le serveur de review local :

```text
POST /api/monitor/audit-start
POST /api/monitor/agent-update {"id":"z2","status":"completed"}
GET  /api/monitor/status
```

Résultat observé :

```json
{
  "agentKeys": ["r1:z1", "r1:z2", "undefined"],
  "undefined": {
    "id": "z2",
    "status": "completed",
    "bugs_found": 0,
    "duration_s": 8
  },
  "r1z2": {
    "zone_id": "z2",
    "status": "pending"
  }
}
```

Verdict : confirmé. Le smoke officiel passe parce qu'il utilise `agent_id`, pas
`id`. Il ne couvre donc pas ce cas.

Correction attendue :

- normaliser `id`, `agent_id` et `zone_id` dans une fonction unique ;
- refuser explicitement un update sans identifiant normalisable ;
- ajouter une assertion de smoke test : aucune clé `undefined` dans
  `status.agents`.

### B2 - Monitor : `r1:z1` et `z1` ne pointent pas vers la même entité

Sévérité proposée : moyenne à haute.

Reproduction exécutée après préremplissage par `audit-start` :

```text
zones: r1:z1, r1:z2
agent-update: {"id":"z1","status":"completed"}
```

Résultat observé :

```json
{
  "agentKeys": ["r1:z1", "r1:z2", "undefined"],
  "undefined": {
    "id": "z1",
    "status": "completed"
  },
  "r1:z1": {
    "zone_id": "z1",
    "status": "pending"
  },
  "r1:z2": {
    "zone_id": "z2",
    "status": "pending"
  }
}
```

Verdict : confirmé. L'activité reçue ne met pas à jour l'agent prérempli.

Correction attendue :

- définir un format canonique d'identifiant monitor ;
- réconcilier `zone_id` avec l'identifiant prérempli quand le round est connu ;
- tester `r1:z1` plus `z1` dans les deux sens.

### B3 - Sous-runs visuels : scope perdu après rebuild

Sévérité proposée : moyenne.

Sous-run audit contrôlé :

```text
Avant rebuild : 13 total, 13 pass, 0 stale
Après rebuild : 28 total, 13 pass, 15 stale
Scope après rebuild : absent
```

Sous-run process contrôlé :

```text
Avant rebuild : 4 total, 4 pass, 0 stale
Après rebuild : 28 total, 4 pass, 24 stale
Scope après rebuild : absent
```

Verdict : confirmé. Le rapport ciblé peut être correct, mais la review
reconstruite retransforme le sous-run en vue globale. Les routes non exécutées
sont affichées comme `STALE` au lieu d'être hors scope ou explicitement non
sélectionnées.

Correction attendue :

- persister `run_id`, `scope`, `selected_routes`, `selected_manifests` et
  `uncovered_routes` dans `visual-results.json` ;
- distinguer `selected_total` de `full_suite_total` ;
- afficher le scope courant dans la review ;
- ne pas convertir les tests hors scope en `STALE` sans raison explicite.

### B4 - Matching de `/` trop large

Sévérité proposée : moyenne.

Source du contrat actuel : `sg-visual-run/references/invocation-modes.md`
indique qu'un manifest matche si son pathname commence par la route impactée
ou lui est égal.

Mesure exécutée :

```text
from-audit  : impacted route "/" -> matching naïf 28 manifests
from-audit  : matching contrôlé -> 13 manifests
from-process: impacted route "/" -> matching naïf 28 manifests
from-process: matching contrôlé -> 4 manifests
```

Verdict : confirmé par le contrat et par la mesure. La racine `/` doit être un
cas spécial, sinon elle sélectionne toute la suite.

Correction attendue :

```text
"/" matches only the root page manifest
```

ou une règle explicitement documentée si ShipGuard veut un autre comportement.

### B5 - Routes non HTML sans statut machine explicite

Sévérité proposée : moyenne.

Routes impactées non couvertes pendant le sous-run audit :

```text
/span-pan/assets/downloads/span-pan-slides.zip
/mise-en-gouvernance-du-span/assets/downloads/mise-en-gouvernance-du-span-slides.zip
/review.html
```

Route impactée non couverte pendant le sous-run process :

```text
/review.html
```

Verdict : confirmé. Ces routes sont détectables, mais ne sont pas conservées
comme objets `skipped` ou `uncovered` dans le JSON reconstruit par la review.

Correction attendue :

```json
{
  "route": "/assets/downloads/file.zip",
  "status": "skipped",
  "reason": "non_html_asset"
}
```

et :

```json
{
  "route": "/review.html",
  "status": "uncovered",
  "reason": "no_visual_manifest"
}
```

### B6 - `sg-record` : `Stop` validé, `Check` pas encore validé en E2E complet

Sévérité proposée : moyenne.

Préflight validé :

```text
ShipGuard Recorder Preflight
PLAYWRIGHT_OK
CHROMIUM_OK
GUI_LAUNCH_OK
```

Run E2E après autorisation du terminal :

```text
■ Stop — finalizing...
Saved 16 steps to visual-tests/manifests/recorded-retest-check-stop-authorized-20260630.yaml
```

Le manifest produit est détecté par la review :

```text
Found 3 recorded manifests
```

Limite confirmée :

```text
recorded-retest-check-stop-authorized-20260630.yaml
contient 16 actions + screenshot final
ne contient pas assert_text, llm-check ou action check
```

Test isolé de la barre injectée :

```json
{
  "eventCount": 2,
  "events": [
    { "type": "step", "stepType": "check", "text": "Objectifs 2030" },
    { "type": "stop", "steps": [{ "type": "check", "text": "Objectifs 2030" }] }
  ]
}
```

Verdict : `Stop` est validé en E2E réel. Le contrat interne du bouton `Check`
est valide dans un test Playwright isolé. En revanche, le flux complet
`sg-record.mjs` n'a pas encore de test E2E automatisé qui prouve `Check` puis
`Stop` dans la fenêtre réelle du recorder.

Correction attendue :

- ajouter un mode de test officiel du recorder qui expose un contrôle
  automatisable, par exemple un port DevTools optionnel en test, ou un mode
  headless dédié ;
- ajouter une assertion E2E : le manifest final contient au moins un
  `assert_text` après usage de `Check`.

### B7 - `sg-ship` : skill agentique, pas commande shell

Sévérité proposée : basse à moyenne, surtout documentation / DX.

Vérification exécutée :

```text
command -v sg-ship -> absent
sg-ship --help     -> command not found
```

Dans le cache plugin :

```text
skills/sg-ship/SKILL.md
skills/sg-ship/agents/openai.yaml
```

Aucun exécutable `sg-ship` n'est présent.

Verdict : confirmé. `sg-ship` fonctionne comme skill agentique, pas comme CLI
native. La documentation peut rester ainsi, mais le mot "one command" prête à
confusion si l'utilisateur cherche une commande shell.

Correction attendue :

- soit documenter explicitement que `/sg-ship` est une commande de skill, pas
  un binaire ;
- soit fournir un wrapper CLI `sg-ship` qui orchestre les lanes report-only.

## Points non bloquants observés pendant la recette

### Dépendances Node du recorder

Après resynchronisation du dépôt de recette, `visual-tests/package.json` et
`package-lock.json` étaient présents, mais `node_modules` ne l'était pas.

```text
node visual-tests/sg-record.mjs --check -> PLAYWRIGHT_MISSING
npm ci                                   -> added 3 packages, 0 vulnerabilities
node visual-tests/sg-record.mjs --check -> PLAYWRIGHT_OK / CHROMIUM_OK / GUI_LAUNCH_OK
```

Ce n'est pas un bug ShipGuard si le dépôt ne versionne pas `node_modules`.
Point utile : le message `PLAYWRIGHT_MISSING` est clair et actionnable.

### Rapport Markdown français et fallback review

Le runner statique local écrit un `report.md` français. Quand le JSON ciblé
reste présent, `build-review.mjs` utilise correctement le JSON comme source.
Sans JSON canonique complet, le fallback Markdown n'est pas une source fiable
pour reconstruire les statuts.

Ce point confirme l'intérêt du contrat `visual-results.json` comme source
canonique, déjà documenté côté ShipGuard.

## Priorités proposées

1. Corriger le monitor live : interdire `agents.undefined` et réconcilier
   `r1:z1` avec `z1`.
2. Ajouter un contrat de scope pour les sous-runs visuels ciblés.
3. Spécialiser le matching de la route `/`.
4. Représenter les routes non HTML ou non couvertes dans le JSON machine.
5. Ajouter un E2E officiel du recorder qui valide `Check` puis `Stop`.
6. Clarifier `sg-ship` : skill slash-command ou CLI native.

## Message court copiable pour GitHub

```text
ShipGuard 2.3.7 final retest: smoke suite OK and full visual suite OK
(28/28 pass). Recorder preflight and Stop flow are fixed enough for use.

Still reproducible:
1. monitor agent-update with {"id":"z2"} returns 200 but stores agents.undefined;
2. prefilled r1:z1 agents stay pending when updates arrive as z1;
3. targeted visual runs lose scope after review rebuild (13/13 becomes 28 total
   with 15 stale, 4/4 becomes 28 total with 24 stale);
4. impacted route "/" prefix-matches every manifest unless special-cased;
5. non-HTML or unmanifested routes should be persisted as skipped/uncovered;
6. sg-record Check is validated in toolbar isolation, but not yet by an official
   full E2E recorder test that proves Check then Stop writes assert_text;
7. sg-ship is a skill slash-command, not a shell command.
```
