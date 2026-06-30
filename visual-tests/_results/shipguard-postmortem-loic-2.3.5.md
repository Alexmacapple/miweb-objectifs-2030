# Postmortem Loic - reprise ShipGuard 2.3.5

Date : 2026-06-30 08:57 CEST

Contexte : reprise de la recette ShipGuard apres le commit annonce par Loic :

- `50e71da399eb9792e9220582b11c504274818671 test: harden ShipGuard smoke coverage`

Objectif : retester ShipGuard `2.3.5` sur le depot MiWeb, verifier que les
frictions du postmortem `2.3.4` sont corrigees, et noter les points restants
sans commit ni correction du site teste.

## Resume court

La version `2.3.5` corrige bien la majorite des frictions techniques remontees
en `2.3.4` :

- smoke tests `review` et `monitor` avec `--port`, `--debug`, `--keep-tmp` ;
- diagnostics `listen EPERM` presents dans les scripts ;
- smoke tests deterministes ajoutes pour `sg-visual-fix --dry-run`,
  `sg-scout --offline --dry-run`, `sg-improve --dry-run` ;
- dashboard protege contre l'auto-traduction (`translate="no"`,
  `notranslate`, meta Google) ;
- favicon silencieux en `GET /favicon.ico` ;
- panneau Agents legacy reconstruit depuis les IDs `SG-Z*` ;
- compteur Routes explicite a `0` au lieu d'une cellule vide ;
- documentation sandbox et migration Codex ajoutees.

Point bloquant restant cote installation : Codex voit bien `shipguard@shipguard`
`2.3.5`, mais Claude reste annonce en `2.3.4` localement, meme apres
`claude plugin marketplace update shipguard` puis
`claude plugin update shipguard@shipguard`.

## Etat source et installation

### Source amont

Verification :

```text
git ls-remote https://github.com/bacoco/ShipGuard.git refs/heads/main
50e71da399eb9792e9220582b11c504274818671 refs/heads/main
```

Le marketplace local a ete fast-forward de `304f414` vers `50e71da`.
Les manifests source indiquent bien `2.3.5` pour :

- `plugins/shipguard/.codex-plugin/plugin.json`
- `plugins/shipguard/.claude-plugin/plugin.json`

### Codex

OK.

```text
codex plugin add shipguard@shipguard
Installed plugin root: /Users/alex/.codex/plugins/cache/shipguard/shipguard/2.3.5
```

`codex plugin list` montre :

```text
shipguard@shipguard  installed, enabled  2.3.5
```

Friction encore visible : l'ancien adaptateur reste actif :

```text
shipguard-codex@personal  installed, enabled  2.3.0+codex.local-20260629125036
```

La doc `docs/codex-migration.md` explique maintenant de le retirer, mais il
n'est pas automatiquement desactive.

### Claude

KO / a investiguer.

Le marketplace local contient bien `2.3.5`, et `claude plugin validate` passe
sur le plugin source. Mais l'installation Claude reste bloquee en `2.3.4` :

```text
claude plugin list
shipguard@shipguard  Version: 2.3.4
```

La commande :

```text
claude plugin update shipguard@shipguard
```

repond encore :

```text
shipguard is already at the latest version (2.3.4)
```

alors que le marketplace source local contient `2.3.5`. Ce point contredit
l'etat attendu annonce et merite un correctif ou une procedure de purge cache.

## Verifications passees

### Syntaxe et manifests

OK :

```text
claude plugin validate plugins/shipguard
node --check sur tous les scripts .mjs du cache Codex 2.3.5
node --check sur tous les scripts .mjs de visual-tests/
parse des scripts inline de visual-tests/_review-template.html : 1 script OK
agent-browser --version : 0.31.1
```

### Smoke tests officiels 2.3.5

OK :

```text
node visual-tests/review-smoke-test.mjs --port=23101
review smoke test passed

node visual-tests/monitor-smoke-test.mjs --port=23102
monitor smoke test passed

node .../sg-visual-fix/visual-fix-dry-run-smoke-test.mjs
visual-fix dry-run smoke test passed

node .../sg-scout/offline-dry-run-smoke-test.mjs
scout offline dry-run smoke test passed

node .../sg-improve/improve-dry-run-smoke-test.mjs
improve dry-run smoke test passed
```

`sg-scout` a aussi ete teste avec le fixture officiel explicite :

```text
node .../sg-scout/offline-dry-run-smoke-test.mjs --from .../fixtures/scout-repos.json
scout offline dry-run smoke test passed
```

### Recorder

OK dans le harnais projet :

```text
node visual-tests/lib/actions-to-yaml.test.mjs
tests 13, pass 13, fail 0

node visual-tests/lib/integration-test.mjs
11 pass, 0 fail
```

Friction nouvelle : le test `sg-record/lib/integration-test.mjs` n'est pas
autonome s'il est lance directement depuis le cache plugin.

- en sandbox : `EPERM` sur creation de `skills/sg-record/manifests` ;
- hors sandbox : le test echoue sur `Review page rebuilt`, car il cherche
  `build-review.mjs` dans `skills/sg-record/`, ou il n'existe pas.

Conclusion : le test est bon une fois installe dans un projet, mais son chemin
cache plugin est fragile.

### Visual run MiWeb

OK :

```text
python3 visual-tests/_shipguard_static_run.py --run
[sg-visual-run] Visual run complete: 28/28 passed
Report: visual-tests/_results/report.md
Contact sheet: visual-tests/_results/contact-sheet.png
```

`visual-tests/_results/visual-results.json` a ete regenere avec 28 tests
`PASS`.

### Dashboard 2.3.5

Serveur lance sur `127.0.0.1:23103`, puis arrete et relance sur `23104` pour
tester `--stop`.

Endpoints verifies :

```text
GET /                              -> 200
GET /visual-results.json           -> 200
GET /audit-results.json            -> 200
GET /persona-reports/index.html    -> 200
GET /health                        -> 200 {"status":"ok", ...}
GET /api/monitor/status            -> 200
GET /..%2Fsecret.txt               -> 403
GET /favicon.ico                   -> 204
HEAD /favicon.ico                  -> 404
```

Le bruit navigateur `favicon.ico` est corrige pour `GET`, qui est le cas
standard. `HEAD /favicon.ico` reste a 404, point mineur.

### UI dashboard

Captures produites :

- `shipguard-2.3.5-browser-dashboard.png`
- `shipguard-2.3.5-agents-legacy.png`
- `shipguard-2.3.5-routes.png`
- `shipguard-2.3.5-visual-tests.png`
- `shipguard-2.3.5-recorded-tests.png`
- `shipguard-2.3.5-lightbox.png`

Verifications navigateur :

- `SHIPGUARD` visible, non traduit ;
- `Code Audit 19 bugs` visible ;
- `Visual Tests` : 28 cartes `PASS`, filtre `UPDATED (28)`, miniatures ;
- `Recorded Tests` : 1 manifest, `miweb-home-smoke`, 2 steps, 1 check ;
- `Routes` : 8 routes, la ligne `/` affiche `BUG COUNT = 0` ;
- `Agents` : panneau non vide, reconstruit en `z1` a `z5` depuis les IDs
  legacy `SG-Z*` ;
- lightbox : image, navigation, details, steps, bouton `+ Add Note` ;
- clic `+ Add Note` : le mode affiche `Click image to place a pin`.

### save-manifest et visual-fix dry-run projet

OK :

```text
POST /save-manifest -> 200
fix-manifest.json   -> ecrit avec annotation normalisee
```

Un plan dry-run projet a ete regenere :

```text
visual-tests/_results/visual-fix-plan.md
```

Il lit le manifest, la capture `root-index.png`, les coordonnees et les
fichiers candidats. Aucune correction n'est proposee car l'annotation est une
note de recette non corrective. Aucun fichier source n'a ete modifie.

### Monitor

OK pour le contrat principal :

```text
POST /api/monitor/audit-start     -> 200
POST /api/monitor/agent-update    -> 200
POST /api/monitor/audit-complete  -> 200
GET  /api/monitor/status          -> 200, status completed
```

Friction mineure observee : si `audit-start` cree une entree depuis `zones`
avec cle `r1:z1` et que `agent-update` utilise `agent_id: z1`, l'etat final
contient deux entrees :

```json
"agents": {
  "r1:z1": {"status":"pending", ...},
  "z1": {"status":"completed", ...}
}
```

Ce n'est pas bloquant pour le smoke test, mais le dashboard peut afficher une
entree pending parasite selon le payload de l'appelant. Il faudrait normaliser
la cle agent entre `audit-start` et `agent-update`, ou documenter que
`agent_id` doit reutiliser exactement la cle initiale.

### Scout GitHub

OK en lecture seule :

```text
gh auth status                         -> OK
gh api search/repositories ...         -> OK
gh issue list --repo bacoco/ShipGuard  -> OK avec autorisation reseau
```

Aucune issue n'a ete creee ou commentee.

### Review stop

OK :

```text
node visual-tests/build-review.mjs --stop
Server stopped
curl http://127.0.0.1:23103/ -> 000
node visual-tests/build-review.mjs --serve --port=23104 -> 200
node visual-tests/build-review.mjs --stop -> Server stopped
```

## Matrice des frictions 2.3.4

| ID | Statut 2.3.5 | Preuve / commentaire |
|---|---|---|
| F1 ancien adaptateur Codex actif | Partiel | `docs/codex-migration.md` ajoute la procedure, mais `shipguard-codex@personal` reste installe et enabled. |
| F2 marketplace Codex introuvable | Partiel / OK local | Apres marketplace local a jour, `codex plugin add shipguard@shipguard` installe `2.3.5`. Pas reteste depuis une machine vierge. |
| F3 Claude sur mauvais clone/cache | Non regle localement | Marketplace source en `2.3.5`, mais `claude plugin list` et `update` restent en `2.3.4`. |
| F4 restart Claude peu visible | Non verifie | Toujours impossible de prouver une session Claude active en `2.3.5` puisque le cache CLI reste `2.3.4`. |
| F5 diagnostics smoke sandbox opaques | Regle | Scripts `2.3.5` capturent stderr, fixture, commande de rerun et hint `listen EPERM`; smoke tests passes avec `--port`. |
| F6 doc sandbox ports locaux | Regle | `docs/sandbox.md` documente `review-smoke-test`, `monitor-smoke-test`, loopback et `listen EPERM`. |
| F7 port aleatoire | Regle | `--port=<port>` et variables `SHIPGUARD_*_PORT` disponibles ; testes sur `23101` et `23102`. |
| F8 fixtures temporaires cachees | Regle | Les smoke tests loggent fixture et supportent `--keep-tmp` / `--debug`. |
| F9 smoke `sg-visual-fix --dry-run` | Regle | Smoke officiel passe ; plan dry-run projet regenere sans modification source. |
| F10 smoke `sg-scout` / `sg-improve` dry-run | Regle | Smoke tests officiels passent ; `sg-scout` offline teste avec fixture explicite. |
| F11 Agents legacy vide | Regle | Panneau Agents affiche `z1` a `z5` avec compteurs de bugs depuis `SG-Z*`. |
| F11 bis route `/` sans bug count | Regle | Ligne `/` affiche `0`. |
| F12 auto-traduction Chrome | Regle fonctionnellement | HTML contient `translate="no"`, `class="notranslate"`, meta Google ; snapshot navigateur non traduit. Pas de trace DevTools reseau Google verifiee dans cette reprise. |
| F13 favicon 404 | Regle pour navigateur | `GET /favicon.ico` -> `204`. `HEAD /favicon.ico` reste `404`, mineur. |

## Matrice du plan de reprise

| Test prevu | Statut | Commentaire |
|---|---|---|
| Installation / update 2.3.5 | Partiel | Codex OK, Claude KO localement. |
| Smoke tests officiels | OK | Review, monitor, visual-fix dry-run, scout offline dry-run, improve dry-run. |
| `sg-visual-discover` / manifests | OK | Runner statique : 28 routes et manifests. |
| `sg-visual-run` complet | OK | 28/28 PASS. |
| `sg-visual-review` dashboard | OK | Build, serveur, endpoints, tabs, captures. |
| Lightbox / annotation UI | Partiel OK | Lightbox et `+ Add Note` verifies ; dessin precis non automatise. `POST /save-manifest` verifie. |
| `sg-visual-fix --dry-run` projet | OK | Plan ecrit, aucun source modifie. |
| `sg-visual-fix` reel | Non lance | Destructif, necessite zone isolee ou accord explicite. |
| `sg-record` Node | OK | 13/13 + 11/11 dans le projet. |
| `sg-record` interactif reel | Non lance | Necessite interaction navigateur humaine complete. |
| `sg-process-check reason` | Deja couvert 2.3.4 | `process-results.json` existant. |
| `sg-process-check hybrid` | Non lance | Pas de harness mecanique non destructif disponible ici. |
| `sg-process-check execute` | Non lance | Before/after reel, potentiellement couteux/destructif. |
| `sg-visual-run --from-audit` | Non lance | Le runner local ne supporte pas ce flag ; couverture indirecte par suite complete. |
| `sg-visual-run --from-process` | Non lance | Meme limite. |
| Monitor live | OK | Endpoints testes sur serveur reel + smoke test. |
| `sg-scout` GitHub lecture | OK | Recherche et issue list en lecture seule. |
| `sg-scout` avec creation/commentaire issue | Non lance | Effet externe, pas d'autorisation explicite de publication. |
| `sg-improve --dry-run` | OK | Smoke officiel passe. |
| `sg-improve` reel + rollback | Non lance | Ecrit `.shipguard/`, a faire sur fixture isolee ou accord explicite. |
| `sg-visual-review-stop` | OK | Stop, port ferme, relance, stop. |
| `sg-ship` complet | Non lance | Orchestrateur lourd ; depend de lanes non destructives/destructives. |

## Nouvelles frictions utiles pour Loic

### N1 - Claude reste bloque en 2.3.4 alors que le marketplace local est en 2.3.5

Impact : l'utilisateur peut croire avoir mis a jour Claude alors que la session
et le cache CLI exposent encore `2.3.4`.

Suggestion :

- ajouter une procedure de purge/reinstall Claude pour un marketplace local ;
- faire afficher par `claude plugin update` le chemin source, la version lue du
  manifest source et la version installee ;
- documenter quoi faire si `marketplace update` voit `2.3.5` mais
  `plugin update` conclut `latest 2.3.4`.

### N2 - `sg-record/lib/integration-test.mjs` n'est pas autonome depuis le cache plugin

Impact : Loic liste ce test comme verification passee. Dans un cache plugin, il
peut echouer meme si le recorder projet fonctionne.

Suggestion :

- soit faire copier `build-review.mjs` dans une fixture temporaire avant de
  rebuilder ;
- soit documenter que ce test doit etre lance depuis `visual-tests/lib/` apres
  installation dans un projet.

### N3 - Monitor : cles agent potentiellement dupliquees

Impact : avec `zones[].zone_id = z1` puis `agent-update.agent_id = z1`, l'etat
contient `r1:z1` pending et `z1` completed. Cela peut produire une timeline
ambigue.

Suggestion :

- normaliser la cle agent ;
- accepter `agent_id: z1` comme mise a jour de `r1:z1` si une seule entree
  correspond ;
- ou documenter explicitement que `agent_id` doit reutiliser `r1:<zone_id>`.

## Etat final

- Aucun commit effectue.
- `visual-tests/` reste non suivi dans Git.
- Serveur dashboard ShipGuard arrete.
- Serveur site MiWeb `scripts/serve-local.sh 8001` encore actif pendant la
  redaction ; a arreter en fin de session.
- Tests non destructifs `2.3.5` : OK cote Codex.
- Installation Claude `2.3.5` : non confirmee, reste le point principal a
  renvoyer a Loic.
