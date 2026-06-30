# Recette ShipGuard 2.3.7 - suite du plan

Date : 2026-06-30

Source du plan :

```text
visual-tests/_results/shipguard-plan-test-reprise.md
```

Périmètre : validation fonctionnelle de ShipGuard dans le harnais
`visual-tests/`, sans commit.

État attendu du dépôt parent :

```text
?? visual-tests/
```

## Règle de journalisation

Pour chaque item repris, noter le contexte utile à Loïc en cas de blocage :
commande ou geste UI, résultat observable, fichier produit, limite rencontrée,
hypothèse retenue et suite proposée. Ne pas résumer un échec sans conserver la
ligne décisive ou l'état exact qui permet de le reproduire.

## Journal

| Item | Sujet | Verdict | Preuve | Blocage / limite |
|---|---|---|---|---|
| 1 | Interface de revue visuelle complète | OK | Lightbox inspectée, annotation `high`, `Copy IDs` capture `pages/checklist-span-operationnel-accessibilite-html`, `fix-manifest.json` écrit avec 1 test et 1 annotation. | Lecture presse-papiers native refusée par Chromium (`NotAllowedError`) ; contenu vérifié par interception locale de `writeText`. |
| 2 | `sg-visual-fix` en mode contrôlé | OK minimal | `visual-tests/_results/visual-fix-plan.md` écrit pour le manifest 2.3.7 ; smoke officiel `visual-fix dry-run smoke test passed`. | Test exécuté en dry-run seulement : pas de correction source, pas de rebuild, pas de capture before/after. L'annotation était une note de recette non corrective. |
| 3 | `sg-record` interactif réel | OK partiel | `node visual-tests/sg-record.mjs --check` passe ; recorder lancé sur `http://127.0.0.1:8001/` ; sortie `Saved 15 steps` ; manifest `visual-tests/manifests/recorded-recette-237-interactive.yaml` écrit ; `build-review.mjs` trouve `2 recorded manifests`. | Le clic `Check` et le clic `Stop` dans la barre n'ont pas été validés : le Chromium Playwright n'était pas attachable par DevTools, Quartz ne listait aucune fenêtre pour son PID, et les clics globaux ciblaient une autre fenêtre Chrome. Fermeture du processus Chromium enfant utilisée pour finaliser l'enregistrement. |
| 4 | `sg-process-check --mode=hybrid` | OK | `process-results.json` valide en mode `hybrid` ; mix `3 measured / 2 reasoned` ; `process-report.md` écrit. | Pas de baseline before réelle : les mesures ancrent l'état courant seulement. `--mode=execute` reste nécessaire pour un before/after entièrement mesuré. |
| 5 | `sg-process-check --mode=execute` | Différé | Non lancé. | Mode before/after avec baseline worktree ; le plan le conditionne à un diff très petit et à une acceptation explicite du coût. |
| 6 | `sg-visual-run --from-audit` | OK | Sélection contrôlée : 13 manifests ; run visuel `13/13 passed` ; planche-contact inspectée. | Matching naïf de la route `/` donnerait 28 manifests ; les routes ZIP et `/review.html` restent non couvertes par les manifests HTML. Après rebuild, `visual-results.json` affiche encore 28/28 alors que `report.md` décrit la sous-suite 13/13. |
| 7 | `sg-visual-run --from-process` | OK | Sélection contrôlée : 4 manifests ; run visuel `4/4 passed` ; planche-contact inspectée. | Route `/review.html` non couverte par les manifests MiWeb. Après rebuild, `visual-results.json` affiche encore 28/28 alors que `report.md` décrit la sous-suite 4/4. |
| 8 | Monitoring temps réel | Blocage confirmé | Smoke isolé `monitor smoke test passed` ; live API 8888 : `audit-start`, `agent-update`, `status`, `audit-complete` répondent HTTP 200 ; `audit-monitor.json` persisté. | `POST /api/monitor/agent-update` avec `{"id":"z2"}` crée encore `agents.undefined`. Les agents prépeuplés `r1:z1` / `r1:z2` restent `pending` quand les updates arrivent sous `z1` / `undefined`. |
| 9 | `sg-scout` complet | OK smoke / réel différé | Smoke officiel offline dry-run passé deux fois, dont une avec fixture explicite `fixtures/scout-repos.json`. | Scan GitHub réel et création/commentaire d'issue non lancés sans validation explicite. |
| 10 | `sg-improve` complet | OK smoke / réel différé | Smoke officiel dry-run passé ; smoke officiel rollback passé ; aucun `.shipguard/` créé dans le dépôt principal. | Écriture réelle `.shipguard/learnings.yaml` / `mistakes.md` et issue GitHub non lancées sans validation explicite. |
| 11 | `sg-visual-review-stop` | OK | Avant stop : HTTP 200 ; `node visual-tests/build-review.mjs --stop` -> `Server stopped (PID 6089)` ; après stop : connexion refusée ; relance sur 8888 -> HTTP 200, PID 14954. | La relance garde le comportement déjà observé : la review reconstruite affiche 28/28 dans `visual-results.json` malgré le dernier sous-run visuel 4/4. |
| 12 | `sg-ship` natif | OK partiel | Full visual run relancé : `28/28 passed` ; review rebuild OK ; résumé `visual-tests/_results/sg-ship-summary.md` mis à jour. | Le slash `sg-ship` est un skill agentique et pas un binaire callable depuis le shell ; orchestration vérifiée manuellement. Lane process courante en `hybrid`, pas en `reason` exact. |

## Blocages

- Aucun blocage produit sur l'item 1. Limite d'observation : lecture native du
  presse-papiers refusée par Chromium, contournée par interception de
  `navigator.clipboard.writeText`.
- Aucun blocage produit sur l'item 2. Limite volontaire : le mode complet
  `sg-visual-fix` peut modifier le site ; le plan courant valide seulement le
  contrat dry-run et la lecture du manifest annoté.
- Blocage partiel sur l'item 3 : le recorder capture bien des actions et écrit
  un manifest, mais la barre flottante n'a pas pu être pilotée jusqu'à `Check`
  et `Stop` dans cette session.
- Aucun blocage produit sur l'item 4. Limite volontaire : pas de worktree
  baseline, pas d'exécution `npx`, pas de POST monitor.
- Item 5 différé volontairement : pas de mode `execute` sans accord explicite
  sur le coût et le périmètre du worktree baseline.
- Aucun blocage d'exécution sur les items 6 et 7. Blocage de cohérence observé
  côté review : le rapport humain reflète la sous-suite, mais
  `visual-results.json` et la review reconstruite restent sur 28 tests.
- Blocage confirmé sur l'item 8 : l'endpoint monitor accepte un payload avec
  `id`, mais l'enregistre sous la clé `undefined`.
- Items 9 et 10 limités volontairement aux smoke tests déterministes : pas de
  GitHub write et pas de mémoire `.shipguard/` dans le dépôt principal.
- Aucun blocage produit sur l'item 11 : arrêt et relance propres du serveur de
  revue.
- Item 12 validé partiellement : l'orchestration report-only est reconstituée,
  mais pas via une commande native unique.

## Commandes et preuves brutes

Les sorties longues sont résumées dans le journal. Les lignes décisives sont
citées dans la colonne Preuve.

### Item 2 - `sg-visual-fix` dry-run

Manifest testé :

```text
visual-tests/_results/fix-manifest.json
```

Fichier produit :

```text
visual-tests/_results/visual-fix-plan.md
```

Ligne décisive du smoke officiel :

```text
visual-fix dry-run smoke test passed
```

Observation : la zone annotée couvre le badge « Accessibilité : non auditée »
sur `checklist-span-operationnel/accessibilite.html`. La note humaine
`Recette 2.3.7 - annotation UI test` ne demande pas de correction ; le plan
conclut donc à aucune correction source pour éviter une modification
spéculative.

### Item 3 - `sg-record` interactif réel

Préflight :

```text
ShipGuard Recorder Preflight
PLAYWRIGHT_OK
CHROMIUM_OK
GUI_LAUNCH_OK
```

Cible :

```text
http://127.0.0.1:8001/
```

Ligne décisive recorder :

```text
Saved 15 steps to /Users/alex/Claude/miweb-objectifs-2030/visual-tests/manifests/recorded-recette-237-interactive.yaml
```

Manifest produit :

```text
visual-tests/manifests/recorded-recette-237-interactive.yaml
```

Observation utile pour Loïc :

- `sg-record` a bien capturé des clics réels de navigation et produit un YAML.
- Le YAML contient 16 entrées `action`, car une capture finale `final.png` est
  ajoutée alors que la console annonce `Saved 15 steps`.
- Le rebuild de la review indique `Found 2 recorded manifests`.
- La fenêtre Chromium lancée par Playwright utilise `--remote-debugging-pipe` ;
  elle n'est pas attachable via le DevTools MCP.
- Quartz ne listait aucune fenêtre visible pour le PID Chromium enfant du
  recorder, ce qui a empêché de cibler la barre flottante par automatisation.
- Des clics globaux macOS ont ciblé une autre fenêtre Chrome au lieu de la barre
  `SG Record`; ils ont ajouté des étapes de navigation, mais pas de `check`.
- Pour finaliser sans perdre les étapes, le processus Chromium enfant du
  recorder a été fermé ; `sg-record.mjs` a alors écrit le manifest via son
  chemin `context.on('close')`.

### Item 4 - `sg-process-check --mode=hybrid`

Fichiers produits :

```text
visual-tests/_results/process-results.json
visual-tests/_results/process-report.md
```

Contrôle JSON :

```text
mode: hybrid
evidence_mix: 3 measured / 2 reasoned
```

Mesures effectuées :

```text
GET http://127.0.0.1:8888/ -> HTTP 200, 156443 bytes
GET http://127.0.0.1:8888/visual-results.json -> HTTP 200, 13061 bytes
GET http://127.0.0.1:8001/ -> HTTP 200, 10800 bytes
```

Limite : aucune baseline before n'a été construite. Les mesures valident
l'état courant et l'étiquetage `measured`, tandis que les unités de publication
restent `reasoned`.

### Item 6 - `sg-visual-run --from-audit`

Sélection :

```text
impacted_routes = /, /miweb-objectifs-2030-v1/, /miweb-objectifs-2030-v2/, /miweb-objectifs-2030-v3/, /miweb-objectifs-2030-v4/, /span-pan/assets/downloads/span-pan-slides.zip, /mise-en-gouvernance-du-span/assets/downloads/mise-en-gouvernance-du-span-slides.zip, /review.html
matching naïf = 28 manifests
matching contrôlé = 13 manifests
```

Résultat :

```text
[sg-visual-run --from-audit] Visual run complete: 13/13 passed
```

Routes non couvertes :

```text
/span-pan/assets/downloads/span-pan-slides.zip
/mise-en-gouvernance-du-span/assets/downloads/mise-en-gouvernance-du-span-slides.zip
/review.html
```

Observation utile pour Loïc : la route `/` doit être traitée comme cas spécial.
Sinon, le matching par préfixe relance toute la suite au lieu de la racine.

### Item 7 - `sg-visual-run --from-process`

Sélection :

```text
process_routes = /, /miweb-objectifs-2030-v1/, /review.html
matching contrôlé = 4 manifests
```

Résultat :

```text
[sg-visual-run --from-process] Visual run complete: 4/4 passed
```

Route non couverte :

```text
/review.html
```

Observation utile pour Loïc : après les sous-runs 13 puis 4, `report.md` et la
planche-contact reflètent bien la sous-suite courante, mais `build-review.mjs`
reconstruit `visual-results.json` et la review avec un résumé 28/28. Le
dashboard ne distingue donc pas clairement une sous-suite ciblée d'un run
complet.

### Item 8 - Monitoring temps réel

Smoke isolé :

```text
monitor smoke test passed
```

Endpoints live testés sur `http://127.0.0.1:8888` :

```text
POST /api/monitor/audit-start -> HTTP 200
POST /api/monitor/agent-update avec agent_id=z1 -> HTTP 200
POST /api/monitor/agent-update avec id=z2 -> HTTP 200
GET /api/monitor/status -> HTTP 200
POST /api/monitor/audit-complete -> HTTP 200
GET /api/monitor/status -> HTTP 200
```

Fichier persisté :

```text
visual-tests/_results/audit-monitor.json
```

Blocage utile pour Loïc :

```text
"undefined": {
  "id": "z2",
  "status": "completed",
  "bugs_found": 0,
  "duration_s": 4
}
```

Interprétation : `agent-update` calcule l'identifiant depuis `agent_id` ou
`zone_id`, mais pas depuis `id`. Le payload avec `id` est accepté en 200 et
persiste sous `agents.undefined`, au lieu de refuser la requête ou de normaliser
`id` vers `agent_id` / `zone_id`.

### Item 9 - `sg-scout`

Smoke tests :

```text
scout offline dry-run smoke test passed
scout offline dry-run smoke test passed
```

Commandes couvertes :

```text
node .../skills/sg-scout/offline-dry-run-smoke-test.mjs
node .../skills/sg-scout/offline-dry-run-smoke-test.mjs --from .../fixtures/scout-repos.json
```

Limite : pas de scan GitHub réel, pas d'écriture dans
`docs/scout-reports/techniques-library.md`, pas d'issue GitHub.

### Item 10 - `sg-improve`

Smoke tests :

```text
improve dry-run smoke test passed
improve rollback smoke test passed
```

Contrôle :

```text
NO_DOT_SHIPGUARD
```

Limite : pas d'écriture réelle dans `.shipguard/learnings.yaml`,
`.shipguard/mistakes.md` ou `.shipguard/history/` du dépôt principal, et pas
d'issue GitHub.

### Item 11 - `sg-visual-review-stop`

Avant arrêt :

```text
GET http://127.0.0.1:8888/ -> HTTP 200
PID 6089
```

Arrêt :

```text
node visual-tests/build-review.mjs --stop
Server stopped (PID 6089).
```

Après arrêt :

```text
curl: (7) Failed to connect to 127.0.0.1 port 8888
```

Relance :

```text
node visual-tests/build-review.mjs --serve --port=8888
Server: http://127.0.0.1:8888 (PID 14954)
GET http://127.0.0.1:8888/ -> HTTP 200
```

### Item 12 - `sg-ship` natif

Mode visé :

```text
quick --all --report-only --mode=reason
```

Preuve visuelle complète :

```text
[sg-visual-run] Visual run complete: 28/28 passed
```

Review :

```text
Found 28 test manifests
Status: 28 pass, 0 fail, 0 error, 0 stale, 0 skipped
Screenshots matched: 28/28
Found 2 recorded manifests
GET http://127.0.0.1:8888/ -> HTTP 200
```

Résumé consolidé :

```text
visual-tests/_results/sg-ship-summary.md
```

Limite : le skill `sg-ship` n'est pas exposé comme commande shell unique dans
cette session. Les lanes ont donc été orchestrées manuellement à partir des
artefacts et scripts disponibles.

## État de fin de session

Après les preuves HTTP, les serveurs locaux ont été arrêtés pour ne pas laisser
de session d'outil pendante :

```text
http://127.0.0.1:8888/ -> connexion refusée
http://127.0.0.1:8001/ -> connexion refusée
```

Pour reprendre l'inspection manuelle :

```bash
python3 -m http.server 8001 --bind 127.0.0.1
node visual-tests/build-review.mjs --serve --port=8888
```
