# Postmortem ShipGuard 2.3.6 - retest correctifs Loic

Date : 2026-06-30

Contexte : retest de ShipGuard apres le commit :

```text
aa17030 test: add recorder preflight and improve rollback smoke
```

Objectif : verifier si les points remontes dans les postmortems `2.3.5` ont
ete corriges, et isoler les nouveaux blocages utiles pour le repo GitHub
ShipGuard, sans contexte machine ou depot client specifique.

## Verdict court

La version `2.3.6` corrige bien les points annonces par Loic :

- bump des manifests Claude/Codex en `2.3.6` ;
- installation Codex officielle en `shipguard@shipguard 2.3.6` ;
- installation Claude en `shipguard@shipguard 2.3.6`, avec restart requis ;
- doc migration Codex enrichie pour le cas `EPERM` lors du retrait de l'ancien
  cache/adaptateur ;
- `sg-record.mjs --check` ajoute et actionnable ;
- documentation `sg-record` enrichie sur les prerequis interactifs ;
- smoke test officiel `sg-improve --rollback` ajoute et passant ;
- smoke test officiel `sg-improve --dry-run` toujours passant ;
- smoke tests `sg-visual-fix --dry-run` et `sg-scout --offline --dry-run`
  toujours passants ;
- smoke tests `review` / `monitor` avec `--port`, `--debug`, `--keep-tmp`
  toujours passants ;
- dashboard toujours protege contre l'auto-traduction navigateur ;
- `GET /favicon.ico` silencieux ;
- fallback Agents legacy et compteur route `0` toujours presents.

Il reste quelques points generiques utiles a corriger, principalement autour
du monitor live et de l'autonomie du test d'integration recorder depuis le
cache plugin.

## Verifications passees

### Version et packaging

```text
ShipGuard upstream main -> aa17030
manifest Codex          -> 2.3.6
manifest Claude         -> 2.3.6
codex plugin list       -> shipguard@shipguard installed, enabled, 2.3.6
claude plugin list      -> shipguard@shipguard enabled, 2.3.6
claude plugin validate  -> OK
```

Etat migration Codex :

```text
shipguard-codex@personal -> not installed
shipguard@shipguard      -> installed, enabled, 2.3.6
```

### Checks syntaxe

```text
node --check visual-tests/build-review.mjs                         OK
node --check visual-tests/review-smoke-test.mjs                    OK
node --check visual-tests/monitor-smoke-test.mjs                   OK
node --check visual-tests/sg-record.mjs                            OK
node --check skills/sg-improve/improve-rollback-smoke-test.mjs     OK
```

### Smoke tests dashboard / monitor

```text
node visual-tests/review-smoke-test.mjs --port=23114 --debug --keep-tmp
-> review smoke test passed
-> fixture path logged
-> port logged
-> child stdout logged
-> fixture kept

node visual-tests/monitor-smoke-test.mjs --port=23115 --debug --keep-tmp
-> monitor smoke test passed
-> fixture path logged
-> port logged
-> child stdout logged
-> fixture kept
```

Dans le profil de test courant, `listen EPERM` n'a pas ete reproduit : les
smoke tests passent meme sans relance explicite hors sandbox. En revanche, les
options de diagnostic demandees sont bien presentes et exploitables.

### Smoke tests deterministes des skills

```text
node skills/sg-visual-fix/visual-fix-dry-run-smoke-test.mjs
-> visual-fix dry-run smoke test passed

node skills/sg-scout/offline-dry-run-smoke-test.mjs
-> scout offline dry-run smoke test passed

node skills/sg-improve/improve-dry-run-smoke-test.mjs
-> improve dry-run smoke test passed

node skills/sg-improve/improve-rollback-smoke-test.mjs
-> improve rollback smoke test passed
```

### Recorder

Tests unitaires et integration dans un harnais projet :

```text
node visual-tests/lib/actions-to-yaml.test.mjs
-> tests 13, pass 13, fail 0

node visual-tests/lib/integration-test.mjs
-> 11 pass, 0 fail
```

Nouveau preflight interactif :

```text
node visual-tests/sg-record.mjs --check
-> ShipGuard Recorder Preflight
-> PLAYWRIGHT_MISSING
-> Install with: npm init -y && npm install --save-dev playwright && npx playwright install chromium
-> Detail: Cannot find package 'playwright' ...
```

Interpretation : le depot de test ne fournit pas Playwright, mais le diagnostic
est maintenant clair et actionnable. C'est une amelioration valide de `2.3.6`.

### Dashboard sur resultats existants

```text
node visual-tests/build-review.mjs --serve --port=23113
-> Found 28 test manifests
-> Status: 28 pass, 0 fail, 0 error, 0 stale, 0 skipped
-> Visual results: visual-tests/_results/visual-results.json
-> Found 1 recorded manifests
-> Persona reports: 6 pages
```

Verifications HTTP :

```text
GET  /visual-results.json -> 200
GET  /favicon.ico         -> 204
HEAD /favicon.ico         -> 404
```

Le bruit console navigateur standard est donc corrige pour `GET
/favicon.ico`. L'asymetrie `HEAD` reste un polish serveur.

## Points corriges depuis le dernier RETEX

### 1. Migration Codex : cas `EPERM` documente

La documentation mentionne maintenant explicitement le cas ou le retrait de
l'ancien adaptateur/cache echoue avec `EPERM`.

Critere initial :

```text
If removal fails with EPERM, rerun with permission to modify the plugin cache.
```

Statut : corrige.

### 2. `sg-record --check`

Le preflight existe et distingue correctement au moins le cas
`PLAYWRIGHT_MISSING`, avec une commande d'installation claire.

Statut : corrige pour le diagnostic preflight.

Point non couvert par cette passe : le lancement interactif complet du recorder
n'a pas ete execute, car Playwright n'est pas installe dans le depot de test.

### 3. Documentation prerequis recorder

La documentation `sg-record` contient maintenant une entree `--check` et des
prerequis explicites autour de Playwright, Chromium et lancement GUI.

Statut : corrige.

### 4. `sg-improve --rollback`

Le smoke test officiel existe et passe :

```text
improve rollback smoke test passed
```

Statut : corrige.

### 5. Smoke tests dry-run/offline existants

Les smoke tests suivants restent OK en `2.3.6` :

- `sg-visual-fix --dry-run` ;
- `sg-scout --offline --dry-run` ;
- `sg-improve --dry-run`.

Statut : pas de regression observee.

## Blocages / points encore actionnables

### B1 - Marketplace local multiple : risque de mise a jour du mauvais clone

Severite : moyenne, surtout installation / DX.

Constat generique :

La mise a jour a necessite de verifier quel marketplace local etait reellement
utilise par Claude. Un clone local pouvait etre a jour en `2.3.6`, pendant que
Claude pointait encore vers un autre clone plus ancien. Une fois le clone
effectivement reference par `claude plugin marketplace list` mis a jour, Claude
a correctement installe `2.3.6`.

Impact :

- un utilisateur peut mettre a jour le bon repo amont mais pas le clone lu par
  l'outil ;
- `plugin update` peut sembler incoherent si la source inspectee n'est pas
  visible dans le message ;
- les recettes peuvent etre lancees contre une ancienne version sans le voir.

Proposition :

- ajouter une checklist d'installation demandant de verifier d'abord :
  `claude plugin marketplace list` et `codex plugin list` ;
- documenter que le clone a mettre a jour est le chemin affiche par la commande
  marketplace de l'outil ;
- si possible cote CLI, afficher le chemin source et la version detectee lors
  de `plugin update`.

Critere d'acceptation :

- un utilisateur peut prouver en trois commandes :
  source marketplace, version source, version installee.

### B2 - Monitor API : `agent-update` accepte `id` et cree `agents.undefined`

Severite : moyenne.

Reproduction generique :

```http
POST /api/monitor/agent-update
Content-Type: application/json

{"id":"z1","status":"running"}
```

Resultat observe :

```json
{
  "agents": {
    "undefined": {
      "id": "z1",
      "status": "running"
    }
  },
  "status": "running"
}
```

Impact :

- l'API repond OK alors que le payload ne respecte pas le contrat attendu ;
- le dashboard peut se retrouver avec un agent fantome ;
- `id` est un champ naturel pour un integrateur, donc l'erreur est probable.

Proposition :

- accepter `id` comme alias de `agent_id` ;
- ou rejeter explicitement avec `400` :
  `agent-update requires agent_id or zone_id` ;
- ajouter ce cas au smoke test `monitor`.

Critere d'acceptation :

```text
Aucun POST valide ne produit agents.undefined.
Un POST invalide retourne 400 avec message clair.
```

### B3 - Monitor API : duplication `r1:z1` pending et `z1` completed

Severite : moyenne.

Reproduction generique :

1. Demarrer un audit avec une zone :

```json
{
  "zones": [
    {"zone_id": "z1", "paths": ["src"], "file_count": 1}
  ]
}
```

2. Envoyer une update :

```json
{"agent_id":"z1","status":"completed","bugs_found":0,"tokens":10}
```

3. Terminer l'audit.

Etat final observe :

```json
{
  "agents": {
    "r1:z1": {
      "zone_id": "z1",
      "status": "pending"
    },
    "z1": {
      "agent_id": "z1",
      "status": "completed",
      "bugs_found": 0
    }
  },
  "status": "completed"
}
```

Impact :

- un agent peut apparaitre a la fois pending et completed ;
- les compteurs live peuvent devenir incoherents ;
- le contrat exact de cle agent n'est pas evident pour l'appelant.

Proposition :

- normaliser les cles entre `audit-start` et `agent-update` ;
- si `audit-start` cree `r1:z1`, faire correspondre `agent_id: z1` a cette
  entree lorsqu'il n'y a qu'une zone `z1` ;
- ou documenter et tester que l'appelant doit envoyer `agent_id: r1:z1`.

Critere d'acceptation :

```text
Un cycle start/update/complete minimal ne laisse aucun agent pending fantome.
```

### B4 - `HEAD /favicon.ico` retourne encore `404`

Severite : basse.

Etat observe :

```text
GET  /favicon.ico -> 204
HEAD /favicon.ico -> 404
```

Impact :

- le cas navigateur standard est corrige ;
- certains smoke tests HTTP ou probes utilisent `HEAD` et peuvent encore voir
  un faux negatif.

Proposition :

- repondre `204` aussi pour `HEAD /favicon.ico`.

Critere d'acceptation :

```text
GET  /favicon.ico -> 204
HEAD /favicon.ico -> 204
```

### B5 - `sg-record/lib/integration-test.mjs` n'est pas autonome depuis le cache plugin

Severite : moyenne.

Constat :

Le test passe lorsqu'il est copie dans un harnais projet contenant
`build-review.mjs` :

```text
node visual-tests/lib/integration-test.mjs
-> 11 pass, 0 fail
```

Mais il echoue s'il est lance directement depuis le cache ou le dossier du
plugin :

```text
node <plugin-root>/skills/sg-record/lib/integration-test.mjs
```

En sandbox :

```text
Error: EPERM: operation not permitted, open
<plugin-root>/skills/sg-record/manifests/recorded-integration-test.yaml
```

Hors sandbox :

```text
Manifest created                         OK
Has source: recorded                     OK
Has assert_text                          OK
Has expected field                       OK
Uses {base_url}                          OK
Has recorded_at quoted                   OK
Review page rebuilt                      FAIL
6 pass, 1 fail
```

Cause probable :

- le test calcule `ROOT` comme `skills/sg-record` ;
- il suppose ensuite que `build-review.mjs` existe dans ce meme root ;
- dans le packaging plugin, `build-review.mjs` appartient a
  `skills/sg-visual-review`, pas a `skills/sg-record` ;
- le test ecrit aussi dans le cache plugin, qui peut etre read-only sous
  sandbox.

Proposition :

- rendre le test autonome via un dossier temporaire :
  copier `sg-record`, `sg-visual-review/build-review.mjs` et le template dans
  une fixture ;
- ou faire accepter un `--root=<visual-tests-root>` documente ;
- ou documenter que ce test ne doit pas etre lance depuis le cache plugin.

Critere d'acceptation :

```text
node <plugin-root>/skills/sg-record/lib/integration-test.mjs
```

doit soit passer dans une fixture isolee, soit echouer avec un message
indiquant clairement le mode d'execution attendu. Il ne doit pas essayer
d'ecrire dans un cache plugin installe.

### B6 - Recorder interactif complet toujours non valide dans un depot sans Playwright

Severite : basse a moyenne, maintenant surtout prerequis environnement.

Statut :

`sg-record --check` corrige le diagnostic. En revanche, le flux interactif
complet n'a pas ete execute dans cette passe, car Playwright n'est pas
disponible dans le depot de test.

Proposition optionnelle :

- fournir un mini smoke test recorder interactif optionnel, saute proprement si
  `PLAYWRIGHT_MISSING` ;
- ou documenter une commande de preflight + install + lancement de verification
  sur une page statique de fixture.

Critere d'acceptation :

```text
sg-record --check
```

dit explicitement si le recorder reel peut etre lance, et la recette ne
confond plus tests YAML avec interaction navigateur.

## Non testes volontairement dans cette passe

Ces flux restent hors scope du retest `2.3.6`, car ils peuvent modifier des
fichiers, creer des issues ou orchestrer plusieurs actions :

- `sg-visual-fix` en mode reel avec modification de code ;
- `sg-scout` avec GitHub reel et creation/commentaire d'issue ;
- `sg-improve` en mode reel avec ecriture `.shipguard/` ;
- `sg-process-check --mode=execute` ;
- `sg-ship` comme orchestrateur complet de bout en bout ;
- `sg-record` interactif complet. Il etait initialement bloque par Playwright
  Node local manquant ; voir addendum ci-dessous, le preflight est maintenant
  OK mais le parcours interactif reel reste a tester.

## Recommandations courtes

1. Ajouter les deux cas monitor (`id` et duplication `r1:z1` / `z1`) au smoke
   test officiel.
2. Rendre `sg-record/lib/integration-test.mjs` autonome depuis le plugin
   installe, ou documenter son contexte d'execution exact.
3. Aligner `HEAD /favicon.ico` sur `GET /favicon.ico`.
4. Ajouter dans la doc installation une mini-checklist "marketplace source
   reellement utilisee" pour Claude et Codex.
5. Garder `sg-record --check` comme preflight obligatoire avant toute recette
   interactive.

## Etat final de cette passe

```text
ShipGuard 2.3.6 installe cote Codex  -> OK
ShipGuard 2.3.6 installe cote Claude -> OK, restart requis pour appliquer en session
Ancien adaptateur Codex local        -> not installed
Smoke tests non destructifs          -> OK
Recorder YAML/integration harnais    -> OK
Recorder preflight                   -> initialement PLAYWRIGHT_MISSING ; voir addendum, OK apres installation Playwright Node
Recorder integration depuis cache    -> KO, non autonome
Monitor live minimal                 -> KO, agents.undefined et duplication agent
```

## Addendum apres envoi - precision Playwright recorder

Ce point a ete transmis a Loic apres l'envoi initial du RETEX `2.3.6`.

Le blocage initial `PLAYWRIGHT_MISSING` n'etait pas du a l'absence totale de
Playwright sur la machine. Une commande Playwright existait, mais elle venait
de l'installation Python :

```text
~/Library/Python/3.9/bin/playwright
```

Or `sg-record.mjs` fait un import Node :

```js
await import('playwright')
```

Le prerequis reel est donc : package Node `playwright` resolvable depuis le
projet ou le harnais `visual-tests`.

Installation locale effectuee :

```bash
cd visual-tests
npm init -y
npm install --save-dev playwright
npx playwright install chromium
```

Preflight final :

```text
node visual-tests/sg-record.mjs --check
ShipGuard Recorder Preflight
PLAYWRIGHT_OK
CHROMIUM_OK
GUI_LAUNCH_OK
```

Nuance observee :

- premiere tentative apres installation : `GUI_LAUNCH_FAILED` sur timeout
  `5000ms` ;
- deuxieme tentative : OK.

Action utile cote ShipGuard :

- clarifier dans la doc que `sg-record` exige Playwright Node local/importable,
  pas Playwright Python ni seulement une commande globale ;
- envisager un timeout plus long, un retry, ou une option/env de timeout pour
  le check GUI.

Statut actualise pour la reprise :

```text
Recorder preflight -> OK
Recorder interactif reel -> reste a tester
```

## Addendum separe - bootstrap MacBook Pro

Un retour d'installation ShipGuard sur MacBook Pro a ete isole dans un RETEX
dedie, car il concerne le bootstrap multi-runtime et le harnais local plus que
les smoke tests `2.3.6` :

```text
visual-tests/_results/shipguard-postmortem-loic-2.3.6-macbook-bootstrap.md
```

Points nouveaux traces :

- `SessionStart hook exited with code 127` probablement lie au harnais local
  (`uv` ou chemin de hook absent) ;
- check trop multi-runtime : Claude absent peut bloquer alors que Codex est le
  runtime cible ;
- chemins stricts et caches historiques `2.3.0` dans le contrat local ;
- confusion entre bootstrap Codex officiel `shipguard@shipguard` et ancien
  adaptateur `shipguard-codex@personal` ;
- besoin d'un verdict runtime-aware : `Codex OK`, `Claude WARN non verifie`,
  global OK pour runtime cible Codex ;
- dependance `PyYAML` du script local de check.
