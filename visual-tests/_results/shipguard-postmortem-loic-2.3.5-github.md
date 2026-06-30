# Postmortem ShipGuard 2.3.5 - points generiques a corriger

Date : 2026-06-30

Contexte : recette de ShipGuard `2.3.5` apres le commit
`50e71da test: harden ShipGuard smoke coverage`.

Objectif de ce document : isoler les points utiles pour le repo GitHub
ShipGuard, sans contexte machine, utilisateur ou depot client specifique.

## Verdict court

La version `2.3.5` corrige bien les frictions principales remontees en
`2.3.4` :

- smoke tests `review` et `monitor` avec `--port`, `--debug`, `--keep-tmp` ;
- diagnostics de type `listen EPERM` beaucoup plus exploitables ;
- smoke tests deterministes pour `sg-visual-fix --dry-run`,
  `sg-scout --offline --dry-run`, `sg-improve --dry-run` ;
- dashboard protege contre l'auto-traduction navigateur ;
- `GET /favicon.ico` silencieux ;
- fallback Agents legacy depuis IDs `SG-Z*` ;
- compteur route explicite a `0` quand aucun bug n'est associe ;
- documentation sandbox et migration Codex ajoutees.

Il reste quelques points generiques a corriger ou documenter.

## Points a ouvrir / corriger

### 1. Mise a jour Claude : diagnostic insuffisant quand le cache reste sur une ancienne version

Severite : haute, surtout DX / installation.

Symptome generique :

```text
claude plugin marketplace update shipguard
-> success

claude plugin update shipguard@shipguard
-> already at the latest version (<ancienne version>)

claude plugin list
-> shipguard@shipguard <ancienne version>
```

Alors que le manifest source du marketplace local contient une version plus
recente.

Impact :

- l'utilisateur croit etre a jour, mais la session ou le cache CLI expose
  encore l'ancienne version ;
- les tests peuvent etre executes sur un vieux skill sans que ce soit visible ;
- difficile de distinguer bug du plugin, cache stale, mauvais marketplace ou
  redemarrage manquant.

Proposition :

- documenter une procedure de purge/reinstall Claude quand `plugin update`
  reste bloque ;
- dans la documentation ShipGuard, demander explicitement de comparer :
  `claude plugin marketplace list`, version du manifest source, puis
  `claude plugin list` ;
- si possible cote tooling, afficher dans `plugin update` le chemin source lu,
  la version source detectee et la version installee ;
- ajouter une section "si Claude dit latest mais reste sur l'ancienne version".

Critere d'acceptation :

- un utilisateur peut prouver quelle version Claude charge reellement ;
- si la version installee ne suit pas le manifest source, la doc donne une
  commande claire de recuperation.

### 2. Migration depuis l'ancien adaptateur Codex local encore trop facile a rater

Severite : moyenne.

Symptome generique :

```text
codex plugin list
shipguard-codex@personal  installed, enabled  <ancienne version>
shipguard@shipguard       installed, enabled  <version officielle>
```

La suppression fonctionne avec :

```text
codex plugin remove shipguard-codex@personal --json
```

mais peut echouer en environnement sandboxe avec un `Operation not permitted`
lors de la suppression du cache. Le contournement est de relancer avec
permission d'ecriture sur le cache plugin.

Impact :

- confusion possible entre l'ancien adaptateur local et le plugin officiel ;
- risque de croire tester la version officielle alors que des skills anciens
  restent visibles ;
- les retours de recette peuvent melanger deux implementations.

Proposition :

- garder la doc migration, mais la rendre plus visible dans le README ;
- ajouter une checklist post-install :
  `codex plugin list` ne doit idealement montrer qu'un seul ShipGuard actif ;
- fournir une commande de nettoyage recommandee :
  `codex plugin remove shipguard-codex@personal` ;
- preciser que cette commande peut necessiter une permission hors sandbox
  puisqu'elle supprime un cache plugin ;
- eventuellement ajouter un avertissement dans la doc si les deux noms sont
  presents.

Critere d'acceptation :

- apres installation officielle, l'utilisateur sait quel plugin garder ;
- la presence de l'ancien adaptateur est traitee comme etape de migration, pas
  comme detail cache.
- si la suppression echoue sur `EPERM`, la doc indique clairement la permission
  necessaire.

### 3. `sg-record/lib/integration-test.mjs` n'est pas autonome depuis le cache plugin

Severite : moyenne.

Symptome generique :

Le test d'integration recorder passe quand il est installe dans un projet :

```text
node visual-tests/lib/integration-test.mjs
-> 11 pass, 0 fail
```

Mais il peut echouer s'il est lance directement depuis le cache ou le dossier
du skill :

```text
node <plugin-root>/skills/sg-record/lib/integration-test.mjs
-> echec sur Review page rebuilt
```

Cause probable :

- le test suppose que `build-review.mjs` existe au niveau du dossier parent de
  `lib/` ;
- ce fichier existe dans `visual-tests/` apres installation projet, mais pas
  dans `skills/sg-record/` dans le cache plugin.

Impact :

- la commande de verification est ambigue : elle passe dans le projet, echoue
  dans le cache ;
- un mainteneur peut croire a une regression recorder alors que c'est un
  probleme de fixture.

Proposition :

- rendre le smoke test autonome : creer un dossier temporaire de fixture,
  copier `sg-record` + `sg-visual-review/build-review.mjs` + template, puis
  executer le test dedans ;
- ou documenter explicitement que ce test doit etre lance seulement apres
  installation dans `visual-tests/lib/`.

Critere d'acceptation :

- `node <plugin-root>/skills/sg-record/lib/integration-test.mjs` passe depuis
  un checkout plugin propre, ou echoue avec un message indiquant le mode
  attendu ;
- le test ne tente pas d'ecrire dans un cache plugin potentiellement read-only.

### 4. Monitor API : `agent-update` accepte des payloads ambigus et peut creer `agents.undefined`

Severite : moyenne.

Symptome generique :

```http
POST /api/monitor/agent-update
Content-Type: application/json

{"id":"z1","status":"running"}
```

Peut repondre `200` mais creer une entree d'etat sous une cle `undefined`, car
le handler attend `agent_id` ou `zone_id`.

Impact :

- l'appelant a l'impression que l'update est acceptee ;
- le dashboard peut afficher un etat incoherent ou difficile a deboguer ;
- les integrateurs risquent naturellement d'envoyer `id`, champ tres courant.

Proposition :

- accepter `id` comme alias de `agent_id` ;
- ou rejeter le payload avec `400` et un message clair :
  `agent-update requires agent_id or zone_id` ;
- ajouter ce cas au smoke test monitor.

Critere d'acceptation :

- aucun payload valide ne produit `agents.undefined` ;
- un payload invalide echoue explicitement en `400`.

### 5. Monitor API : duplication possible entre cle initiale `r1:<zone>` et update `agent_id:<zone>`

Severite : basse a moyenne.

Symptome generique :

Un `audit-start` initialise les zones avec une cle de type :

```text
r1:z1
```

Puis un `agent-update` avec :

```json
{"agent_id":"z1","status":"completed"}
```

peut produire deux entrees :

```json
{
  "agents": {
    "r1:z1": {"status":"pending"},
    "z1": {"status":"completed"}
  }
}
```

Impact :

- la timeline peut afficher une entree pending parasite ;
- le statut humain devient ambigu : l'agent est-il termine ou encore pending ?

Proposition :

- normaliser les cles d'agents entre `audit-start` et `agent-update` ;
- accepter `agent_id: z1` comme mise a jour de `r1:z1` quand une seule entree
  correspond ;
- ou documenter explicitement que l'appelant doit reutiliser `agent_id:
  r1:z1`.

Critere d'acceptation :

- un cycle start/update/complete minimal ne laisse pas d'agent pending
  fantome ;
- le smoke test monitor couvre le format recommande.

### 6. `HEAD /favicon.ico` reste a `404`

Severite : basse.

Etat actuel :

```text
GET  /favicon.ico -> 204
HEAD /favicon.ico -> 404
```

Impact :

- le bruit navigateur standard est corrige ;
- certains outils de smoke HTTP peuvent utiliser `HEAD` et voir encore un
  faux negatif.

Proposition :

- repondre `204` aussi pour `HEAD /favicon.ico`.

Critere d'acceptation :

```text
GET  /favicon.ico -> 204
HEAD /favicon.ico -> 204
```

### 7. `sg-record` interactif depend de Playwright importable localement

Severite : moyenne.

Symptome generique :

Les tests Node du recorder peuvent passer une fois les fichiers installes dans
un projet :

```text
node visual-tests/lib/actions-to-yaml.test.mjs
node visual-tests/lib/integration-test.mjs
```

Mais le lancement interactif peut echouer avant ouverture du navigateur dans un
depot non Node ou sans Playwright importable :

```text
node visual-tests/sg-record.mjs <url> --name <name>

Playwright not found. Install with:
  npm init -y && npm install playwright && npx playwright install chromium
```

Impact :

- le recorder est presente comme fonctionnalite ShipGuard, mais il depend d'un
  runtime Playwright que les autres lanes peuvent ne pas exiger directement ;
- dans un site statique ou un depot non Node, les smoke tests de conversion
  passent, mais le recorder interactif ne demarre pas ;
- l'utilisateur peut confondre "agent-browser disponible" avec "Playwright
  importable par sg-record".

Proposition :

- ajouter un preflight explicite `sg-record --check` ou une section de doc
  "recorder interactif = Playwright requis" ;
- faire echouer avec un diagnostic plus actionnable : projet Node detecte ou
  non, commande minimale, alternative si Playwright est deja disponible ailleurs ;
- envisager une option de resolution via variable d'environnement ou runtime
  bundled, si le plugin peut reutiliser un Playwright deja installe ;
- documenter que `agent-browser --version` ne suffit pas a valider
  `sg-record`.

Critere d'acceptation :

- avant d'ouvrir Chromium, le recorder indique clairement la dependance
  manquante et le contexte detecte ;
- la checklist de verification distingue tests Node recorder et recorder
  interactif reel.

### 8. `sg-improve --rollback` manque d'un smoke test deterministe officiel

Severite : moyenne.

Constat generique :

Le principe de rollback est testable sur une fixture `.shipguard` isolee :

1. creer `.shipguard/learnings.yaml` et `.shipguard/mistakes.md` ;
2. creer `.shipguard/history/<timestamp>/` avec copies et metadata ;
3. simuler une modification des fichiers courants ;
4. restaurer depuis le snapshot ;
5. verifier que les fichiers reviennent a l'etat initial et que le snapshot est
   consomme.

Impact :

- `sg-improve --dry-run` a maintenant un smoke test deterministe, mais pas le
  chemin rollback ;
- le rollback est le garde-fou du mode reel, donc il merite une preuve
  automatique avant d'encourager les ecritures `.shipguard/` ;
- sans fixture officielle, chaque recette doit bricoler son propre test.

Proposition :

- ajouter `improve-rollback-smoke-test.mjs` ou equivalent ;
- utiliser uniquement un dossier temporaire, jamais le depot courant ;
- verifier :
  - snapshot cree avant modification ;
  - `learnings.yaml` restaure ;
  - `mistakes.md` restaure ;
  - snapshot consomme ou etat history conforme a la spec ;
  - aucune ecriture hors fixture.

Critere d'acceptation :

```text
node plugins/shipguard/skills/sg-improve/improve-rollback-smoke-test.mjs
-> improve rollback smoke test passed
```

## Points verifies comme corriges en 2.3.5

Ces points ne semblent pas necessiter de nouvelle issue, sauf regression :

- `review-smoke-test.mjs --port=<port>` passe ;
- `monitor-smoke-test.mjs --port=<port>` passe ;
- les smoke tests exposent `--debug` et `--keep-tmp` ;
- les erreurs sandbox `listen EPERM` sont documentees et diagnosables ;
- `sg-visual-fix` a un smoke test dry-run deterministe ;
- `sg-scout` a un smoke test offline/dry-run deterministe ;
- `sg-improve` a un smoke test dry-run deterministe ;
- le dashboard contient `translate="no"`, `notranslate` et meta Google ;
- `GET /favicon.ico` ne pollue plus la console ;
- l'onglet Agents n'est plus vide avec des IDs legacy `SG-Z*` ;
- les routes avec zero bug affichees dans le tableau montrent `0` au lieu
  d'une cellule vide ;
- `visual-results.json` reste le contrat machine canonique pour le dashboard.

## Commandes de verification recommandees

```bash
node --check $(find plugins/shipguard/skills -name '*.mjs')
claude plugin validate plugins/shipguard

node visual-tests/review-smoke-test.mjs --port=23101
node visual-tests/monitor-smoke-test.mjs --port=23102

node plugins/shipguard/skills/sg-visual-fix/visual-fix-dry-run-smoke-test.mjs
node plugins/shipguard/skills/sg-scout/offline-dry-run-smoke-test.mjs
node plugins/shipguard/skills/sg-improve/improve-dry-run-smoke-test.mjs

node visual-tests/lib/actions-to-yaml.test.mjs
node visual-tests/lib/integration-test.mjs
```

Si le test recorder doit etre supporte depuis le cache plugin, ajouter aussi :

```bash
node plugins/shipguard/skills/sg-record/lib/integration-test.mjs
```

avec la correction de fixture decrite plus haut.
