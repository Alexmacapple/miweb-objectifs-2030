# Postmortem Loïc - reprise ShipGuard 2.3.4

Date : 2026-06-29 19:01 CEST

Contexte : reprise de la recette ShipGuard après les commits annoncés par
Loïc :

- `8edb990 feat: harden visual review contracts`
- `583e6f3 test: add review dashboard smoke tests`
- `304f414 docs: formalize agent workflow contracts`

Objectif : tester le plugin ShipGuard lui-même, en version officielle
`shipguard@shipguard` `2.3.4`, sur un dépôt client réel, sans commit et sans
appliquer de correction au site testé.

## Résumé court

La version `2.3.4` corrige bien les points remontés dans le premier postmortem :

- manifests plugin Codex et Claude passés en `2.3.4` ;
- `visual-results.json` canonique présent dans le dashboard ;
- fallback Markdown conservé ;
- état audit zéro bug représentable dans le smoke fixture ;
- `impacted_ui_routes` utilisé comme contrat canonique ;
- champ `agents[]` disponible dans le fixture audit ;
- serveur par défaut sur `127.0.0.1` ;
- protection path traversal par `resolve` / `relative` ;
- smoke tests officiels `review-smoke-test.mjs` et `monitor-smoke-test.mjs` ;
- `sg-visual-fix --dry-run` documenté ;
- `sg-scout --offline` / `--dry-run` documentés ;
- `sg-improve --dry-run` documenté ;
- documentation sandbox ajoutée.

Les frictions restantes ne remettent pas en cause le coeur du plugin. Elles
concernent surtout l'installation multi-outils, la migration depuis l'ancien
adaptateur Codex local, et les diagnostics quand un test serveur échoue en
environnement sandboxé.

## Ce qui a été vérifié localement

### Source amont ShipGuard

Le marketplace local a été fast-forward de :

```text
556807d feat: add Codex plugin packaging
```

vers :

```text
304f414 docs: formalize agent workflow contracts
583e6f3 test: add review dashboard smoke tests
8edb990 feat: harden visual review contracts
```

Les manifests source indiquent bien :

```json
"version": "2.3.4"
```

pour :

- `plugins/shipguard/.codex-plugin/plugin.json`
- `plugins/shipguard/.claude-plugin/plugin.json`

### Installation Codex

Installation officielle réussie :

```bash
codex plugin add shipguard@shipguard --json
```

Résultat :

```json
{
  "pluginId": "shipguard@shipguard",
  "name": "shipguard",
  "marketplaceName": "shipguard",
  "version": "2.3.4",
  "installedPath": "/Users/alex/.codex/plugins/cache/shipguard/shipguard/2.3.4"
}
```

`codex plugin list` montre bien :

```text
shipguard@shipguard  installed, enabled  2.3.4
```

### Installation Claude

Après mise à jour du marketplace réellement utilisé par Claude :

```bash
claude plugin update shipguard@shipguard
```

Résultat :

```text
Plugin "shipguard" updated from 2.3.0 to 2.3.4 for scope user.
Restart to apply changes.
```

`claude plugin list --json` montre :

```json
{
  "id": "shipguard@shipguard",
  "version": "2.3.4",
  "scope": "user",
  "enabled": true,
  "installPath": "/Users/alex/.claude/plugins/cache/shipguard/shipguard/2.3.4"
}
```

### Scripts recopiés dans le harnais de recette

Pour tester exactement les scripts `2.3.4`, les fichiers suivants ont été
recopiés depuis le cache officiel Codex vers `visual-tests/` :

- `skills/sg-visual-review/build-review.mjs`
- `skills/sg-visual-review/_review-template.html`
- `skills/sg-visual-review/review-smoke-test.mjs`
- `skills/sg-visual-review/monitor-smoke-test.mjs`
- `skills/sg-record/sg-record.mjs`
- `skills/sg-record/lib/actions-to-yaml.mjs`
- `skills/sg-record/lib/actions-to-yaml.test.mjs`
- `skills/sg-record/lib/integration-test.mjs`
- `skills/sg-record/lib/recorder-toolbar.js`
- `skills/sg-record/lib/recorder-toolbar.css`

### Vérifications passées

Syntaxe :

```text
node --check visual-tests/build-review.mjs        OK
node --check visual-tests/sg-record.mjs           OK
node --check visual-tests/review-smoke-test.mjs   OK
node --check visual-tests/monitor-smoke-test.mjs  OK
```

Recorder :

```text
node visual-tests/lib/actions-to-yaml.test.mjs
tests 13, pass 13, fail 0
```

Intégration recorder :

```text
node visual-tests/lib/integration-test.mjs
11 pass, 0 fail
```

Smoke tests dashboard hors sandbox :

```text
node visual-tests/review-smoke-test.mjs
review smoke test passed

node visual-tests/monitor-smoke-test.mjs
monitor smoke test passed
```

Dashboard sur les résultats MiWeb réels :

```text
node visual-tests/build-review.mjs
Found 28 test manifests
Status: 28 pass, 0 fail, 0 error, 0 stale, 0 skipped
Visual results: visual-tests/_results/visual-results.json
Found 1 recorded manifests
Persona reports: 6 pages
```

Serveur local `2.3.4` :

```text
Server: http://127.0.0.1:8888 (PID 30141)
```

Endpoints vérifiés :

```text
GET /                              -> 200
GET /visual-results.json           -> 200
GET /audit-results.json            -> 200
GET /persona-reports/index.html    -> 200
GET /health                        -> {"status":"ok", ...}
GET /api/monitor/status            -> {"status":"idle"}
GET /..%2Fsecret.txt               -> 403
```

Inspection navigateur Chrome DevTools :

```text
Page ouverte : http://127.0.0.1:8888/
Capture : visual-tests/_results/shipguard-2.3.4-browser-dashboard.png
Console : 1 erreur 404 favicon.ico
Réseau local : /, /audit-results.json OK
Réseau externe observé : Google Translate, déclenché par l'auto-traduction Chrome
```

Interactions vérifiées dans le dashboard :

```text
Code Audit       -> tableau des 19 bugs visible
Visual Tests     -> 28 cartes PASS visibles avec miniatures
Recorded Tests   -> 1 manifest enregistré visible
Routes           -> 8 routes visibles
Agents           -> badge 5 visible, panneau vide avec audit legacy
Lightbox         -> ouverture d'une carte, image, navigation et panneau visibles
Annotation UI    -> note créée, test sélectionné, manifest généré
```

Annotation UI :

```text
Capture lightbox : visual-tests/_results/shipguard-2.3.4-lightbox.png
Capture saved    : visual-tests/_results/shipguard-2.3.4-annotation-saved.png
POST /save-manifest -> 200
fix-manifest.json   -> contient l'annotation avec coordonnées normalisées
```

Dry-run `sg-visual-fix` :

```text
visual-tests/_results/visual-fix-plan.md
```

Le dry-run a lu `fix-manifest.json`, la capture annotée et les fichiers
candidats. Il n'a modifié aucun fichier source et conclut sans correction, car
l'annotation créée était volontairement une note de recette non corrective.

Dry-run/offline `sg-scout` :

```text
Fixture : visual-tests/fixtures/scout-repos.json
Rapport : visual-tests/_results/scout-report.md
```

Dry-run `sg-improve` :

```text
Preview : visual-tests/_results/sg-improve-preview.md
```

Ces deux chemins n'ont créé aucune issue GitHub, aucune écriture `.shipguard/`
et aucune modification source.

## Frictions restantes utiles pour Loïc

### F1 - Codex garde l'ancien adaptateur local actif

Constat :

```text
shipguard-codex@personal  installed, enabled  2.3.0+codex.local-20260629125036
shipguard@shipguard       installed, enabled  2.3.4
```

Impact :

- un utilisateur peut croire tester `2.3.4` alors qu'il utilise encore
  l'adaptateur local `shipguard-codex@personal` ;
- la liste Codex affiche deux plugins ShipGuard actifs ;
- le risque de confusion augmente si les deux exposent des skills proches.

Cause :

L'adaptateur local a été utile avant que le dépôt amont ShipGuard contienne un
packaging Codex complet. Après `2.3.4`, il devient probablement obsolète, mais
il n'est pas automatiquement désactivé.

Proposition générique :

- documenter une étape de migration depuis l'adaptateur local vers le plugin
  officiel ;
- proposer une commande claire de nettoyage ou de désactivation ;
- idéalement, détecter la présence de `shipguard-codex@personal` et afficher
  un avertissement dans la documentation d'installation Codex.

Critère d'acceptation :

- après installation officielle, un utilisateur sait quel plugin doit être
  actif ;
- la recette ne peut pas mélanger sans le voir `shipguard-codex@personal` et
  `shipguard@shipguard`.

### F2 - Codex ne trouvait pas le marketplace `shipguard` au premier install

Constat :

```text
codex plugin add shipguard@shipguard --json
Error: plugin `shipguard` was not found in marketplace `shipguard`
```

Contournement :

```bash
codex plugin marketplace add /Users/alex/.claude/plugins/marketplaces/shipguard
codex plugin add shipguard@shipguard --json
```

Impact :

- le plugin était bien présent localement côté Claude, mais pas enregistré côté
  Codex ;
- l'utilisateur peut interpréter cela comme une version non publiée ou une
  régression du plugin.

Proposition :

- ajouter dans le README une section "Codex depuis un marketplace local Claude"
  avec les deux commandes ;
- afficher explicitement le chemin source utilisé par Codex après ajout du
  marketplace ;
- préciser la différence entre `plugin marketplace add` et `plugin add`.

### F3 - Claude utilisait un autre clone marketplace que celui mis à jour

Constat :

`claude plugin marketplace list` indiquait :

```text
shipguard
Source: Directory (/Users/alex/.codex/.tmp/marketplaces/shipguard)
```

alors qu'un autre clone mis à jour existait ici :

```text
/Users/alex/.claude/plugins/marketplaces/shipguard
```

Impact :

- le bon clone pouvait être en `2.3.4`, mais Claude continuait à voir
  `2.3.0` ;
- `claude plugin update shipguard@shipguard` disait à tort :
  `already at the latest version (2.3.0)` parce que sa source réelle était
  encore ancienne.

Contournement :

Mettre à jour le clone réellement référencé par Claude :

```bash
git -C /Users/alex/.codex/.tmp/marketplaces/shipguard fetch --all --tags
git -C /Users/alex/.codex/.tmp/marketplaces/shipguard merge --ff-only origin/main
claude plugin update shipguard@shipguard
```

Proposition :

- dans les docs, demander d'abord :
  `claude plugin marketplace list` ;
- recommander de mettre à jour le marketplace source exact, pas un clone
  adjacent ;
- si possible, faire afficher à `claude plugin update` le chemin marketplace
  inspecté quand il conclut "latest".

### F4 - Claude demande un restart après update, mais la suite de test ne le rend pas visible

Constat :

```text
Plugin "shipguard" updated from 2.3.0 to 2.3.4 for scope user.
Restart to apply changes.
```

Impact :

- l'installation disque est en `2.3.4`, mais une session Claude déjà ouverte
  peut continuer à exposer les anciens skills jusqu'au redémarrage ;
- la vérification par `claude plugin list --json` est rassurante mais ne prouve
  pas forcément que la session courante a rechargé les skills.

Proposition :

- documenter un check post-restart ;
- ajouter une commande ou un message "active session version" si Claude le
  permet ;
- dans les runbooks, écrire "redémarrer Claude avant de conclure que les skills
  `2.3.4` sont actifs".

### F5 - Les smoke tests échouent en sandbox avec un message trop générique

Constat en sandbox Codex :

```text
review smoke test failed: review server did not become ready
monitor smoke test failed: review server did not become ready
```

Diagnostic réel reproduit avec stderr visible :

```text
Error: listen EPERM: operation not permitted 127.0.0.1:23456
```

Cause :

Les smoke tests lancent un serveur local sur `127.0.0.1:<port aléatoire>`.
Dans un environnement sandboxé, l'écoute réseau locale peut être interdite sans
autorisation explicite.

Impact :

- l'erreur affichée fait penser à un problème applicatif ou à un timeout ;
- la vraie cause (`EPERM` sur `listen`) est cachée dans le stderr du processus
  enfant ;
- l'utilisateur ne sait pas qu'il doit relancer hors sandbox.

Contournement validé :

Relancer hors sandbox :

```text
node visual-tests/review-smoke-test.mjs    -> passed
node visual-tests/monitor-smoke-test.mjs   -> passed
```

Proposition :

- capturer `stderr` du serveur enfant dans les smoke tests ;
- si `waitForServer` échoue, afficher les dernières lignes stdout/stderr du
  serveur ;
- reconnaître `listen EPERM` et afficher un message dédié :
  "local server bind denied by sandbox; rerun with localhost/network
  permission" ;
- optionnel : ajouter `--debug` ou `SHIPGUARD_SMOKE_DEBUG=1`.

Critère d'acceptation :

- un échec sandbox doit dire `EPERM listen 127.0.0.1:<port>` ;
- le message doit orienter vers l'autorisation nécessaire, pas vers un faux
  problème de readiness.

### F6 - Les smoke tests nécessitent une autorisation hors sandbox malgré leur caractère "local"

Constat :

Les mêmes tests :

- échouent en sandbox ;
- passent hors sandbox.

Impact :

Pour Codex, les nouveaux smoke tests sont bons mais doivent être documentés
comme tests nécessitant l'ouverture d'un serveur local. Ce n'est pas un accès
internet, mais c'est quand même une permission réseau/process.

Proposition :

- ajouter dans `plugins/shipguard/docs/sandbox.md` une ligne dédiée :

```text
review-smoke-test.mjs / monitor-smoke-test.mjs : ouvrent un serveur
127.0.0.1 sur port aléatoire ; sous Codex sandbox, relancer avec autorisation.
```

### F7 - Le port aléatoire complique les règles d'autorisation persistantes

Constat :

`review-smoke-test.mjs` choisit :

```js
const port = 21000 + Math.floor(Math.random() * 10000);
```

`monitor-smoke-test.mjs` choisit :

```js
const port = 22000 + Math.floor(Math.random() * 10000);
```

Impact :

- pratique pour éviter les collisions ;
- moins pratique pour les environnements qui accordent des permissions par
  commande ou par port ;
- complique le diagnostic si plusieurs essais tournent.

Proposition :

- accepter `--port=<port>` ou `SHIPGUARD_SMOKE_PORT`;
- conserver le port aléatoire par défaut ;
- logger le port dès le lancement, même avant readiness.

### F8 - Les smoke tests cachent les fichiers temporaires utiles au diagnostic

Constat :

Les fixtures sont créés dans `/tmp` via `mkdtempSync`, mais le chemin n'est pas
affiché en cas d'échec.

Impact :

- quand le serveur ne démarre pas, on ne sait pas facilement quel fixture a été
  généré ;
- il faut reconstruire manuellement le cas pour inspecter `review.html`,
  `visual-results.json`, `audit-monitor.json`, etc.

Proposition :

- en cas d'échec, afficher :
  - chemin du fixture ;
  - commande exacte relançable ;
  - dernières lignes stdout/stderr ;
- option `--keep-tmp` pour conserver le fixture.

### F9 - `sg-visual-fix --dry-run` fonctionne comme flux non destructif, mais il manque un smoke test automatisé

Constat :

`sg-visual-fix/SKILL.md` documente maintenant `--dry-run`, ce qui répond au
besoin initial. Dans cette reprise, un dry-run non destructif a été exécuté sur
un `fix-manifest.json` annoté réel :

```text
visual-tests/_results/visual-fix-plan.md
```

Impact :

- la documentation est présente ;
- la preuve annotation -> manifest -> plan dry-run fonctionne ;
- la preuve d'un vrai correctif visuel reste à faire avec une annotation
  correspondant à un défaut réel.

Proposition :

- conserver ou fournir un fixture minimal `fix-manifest.json` dans le plugin ;
- ajouter un smoke test automatisé de dry-run qui vérifie :
  - aucune modification de fichier source ;
  - plan de correction produit ;
  - captures/annotations lues ;
  - fichiers candidats listés ou absence motivée.

### F10 - `sg-scout --offline --dry-run` et `sg-improve --dry-run` fonctionnent en preview, mais restent LLM-driven

Constat :

Les modes sont visibles dans les skills et ont été exercés en reprise `2.3.4`
sans réseau et sans écriture destructive :

```text
visual-tests/fixtures/scout-repos.json
visual-tests/_results/scout-report.md
visual-tests/_results/sg-improve-preview.md
```

Impact :

La preuve preview existe. En revanche, comme ces skills sont LLM-driven, il ne
s'agit pas encore d'un smoke test automatisé déterministe comparable à
`review-smoke-test.mjs`.

Proposition :

- ajouter des fixtures officielles pour :
  - `sg-scout --offline --dry-run` ;
  - `sg-improve --dry-run` ;
- fournir des commandes de smoke test déterministes qui ne nécessitent ni
  GitHub ni écriture `.shipguard/` ;
- vérifier automatiquement que les fichiers cibles réels ne sont pas créés en
  dry-run.

### F11 - Compatibilité legacy `agents: number` vs nouveau `agents[]`

Constat :

L'ancien `audit-results.json` de recette contient :

```json
{
  "agents": 5,
  "impacted_ui_routes": [...]
}
```

Le template `2.3.4` ne casse pas : il sait utiliser `agents` numérique pour le
compteur. En revanche, il ne peut pas construire les cartes Agents avec ce
fichier legacy, car :

- `agents` est un nombre, pas un tableau ;
- les IDs de bugs de cette recette sont au format `SG-Z2-001` ;
- le fallback actuel extrait les zones avec une regex de type `^r\d+-...`.

Résultat navigateur :

```text
Onglet Agents : badge "5"
Panneau Agents : vide
Capture : visual-tests/_results/shipguard-2.3.4-agents-empty-legacy.png
```

Ce fichier legacy ne contient pas encore le nouveau contrat riche :

```json
{
  "agent_count": 5,
  "agents": [
    {"id": "z1", "status": "completed", "paths": [], "bugs_found": 0}
  ]
}
```

Impact :

- la rétrocompatibilité fonctionne pour l'affichage minimal ;
- le badge Agents et le contenu du panneau peuvent se contredire ;
- l'utilisateur ne voit pas pourquoi les cartes Agents sont absentes ;
- après upgrade `2.3.4`, il faut probablement relancer `/sg-code-audit` pour
  obtenir le nouveau schéma complet.

Proposition :

- documenter explicitement "les anciens `audit-results.json` restent lisibles
  mais ne contiennent pas `agents[]`" ;
- afficher une note douce dans le dashboard si `typeof agents === "number"` :
  "legacy audit schema; rerun sg-code-audit for detailed agent cards" ;
- si `agents` est numérique et qu'aucune carte ne peut être reconstruite,
  afficher au moins une carte synthétique ou un état explicatif ;
- accepter les anciens IDs `SG-Z<zone>-<n>` dans le fallback, si ce format a
  déjà été produit par des recettes ShipGuard/Codex ;
- préférer `agent_count` pour le nombre, et réserver `agents[]` au tableau.

### F11 bis - Route `/` sans nombre de bugs explicite

Constat :

Dans l'onglet Routes, la ligne `/` apparaît avec sévérité et raison, mais la
colonne "bug count" est vide, alors que d'autres routes affichent `1` ou `2`.

Interprétation :

Le correctif évite bien l'ancien problème où `/` comptait trop largement tous
les bugs. En revanche, l'absence de valeur visible peut être ambiguë :

- `0 bug` ;
- champ absent ;
- compteur non calculable.

Proposition :

- afficher `0` quand le compteur calculé vaut zéro ;
- ou afficher `—` avec tooltip "not provided / not inferred" si le compteur est
  volontairement inconnu.

### F12 - Auto-traduction Chrome du dashboard local

Constat :

Lors de l'inspection navigateur, Chrome a auto-traduit le dashboard local :

```text
SHIPGUARD        -> GARDE-SHAMPOOING
Mission Control  -> Contrôle de mission
Bugs             -> Insectes
PASS             -> PASSER
Copy IDs         -> Copier les pièces d'identité
High             -> Haut
Medium           -> Moyen
Low              -> Faible
```

Le réseau DevTools montre aussi des appels externes Google Translate depuis la
page locale :

```text
translate.googleapis.com
translate-pa.googleapis.com
translate.google.com/gen204
```

Impact :

- le nom produit et les termes techniques peuvent devenir absurdes ;
- une page de revue locale peut déclencher du réseau externe via la traduction
  automatique du navigateur ;
- les snapshots agentiques peuvent capturer du texte traduit et devenir
  instables selon la langue utilisateur.

Cause probable :

Comportement de Chrome côté utilisateur, pas un bug direct de ShipGuard. Mais
le dashboard peut se protéger partiellement avec des attributs HTML.

Proposition :

- ajouter `lang="en"` sur le document si l'UI reste en anglais ;
- ajouter `translate="no"` ou `class="notranslate"` sur le nom `ShipGuard`,
  les commandes slash, statuts et libellés techniques ;
- envisager une vraie localisation pilotée par le plugin plutôt que de laisser
  Chrome traduire librement les termes métier.

Critère d'acceptation :

- `ShipGuard` ne doit jamais être traduit ;
- les commandes `/sg-*`, statuts `PASS/FAIL/STALE`, routes et noms de fichiers
  restent stables dans les snapshots ;
- aucune capture de validation ne dépend d'une auto-traduction navigateur.

### F13 - `favicon.ico` 404 dans le dashboard

Constat :

La console Chrome affiche :

```text
Failed to load resource: the server responded with a status of 404 (Not Found)
```

La requête réseau correspond à :

```text
GET http://127.0.0.1:8888/favicon.ico [404]
```

Impact :

Mineur. Cela ajoute une erreur console qui peut polluer les smoke tests
navigateur et masquer des erreurs plus importantes.

Proposition :

- servir un favicon minimal ;
- ou ajouter `<link rel="icon" href="data:,">` dans le template.

## Points positifs à conserver

- La séparation `visual-results.json` / `report.md` clarifie le contrat machine
  vs le rendu humain.
- Les smoke tests officiels sont très utiles : ils ont permis de distinguer un
  problème sandbox d'un problème plugin.
- Le serveur bind par défaut sur `127.0.0.1`, c'est le bon choix.
- La protection anti-traversal encodée est testée dans le smoke test :
  `GET /..%2Fsecret.txt` doit répondre `403`.
- Le monitor smoke test donne enfin une preuve automatique des endpoints live.
- Le recorder reste stable : 13 tests unitaires + 11 tests d'intégration OK
  après recopie depuis `2.3.4`.

## Recommandations courtes pour la suite

1. Ajouter une section migration "ancien adaptateur Codex -> plugin officiel".
2. Améliorer les messages d'erreur des smoke tests quand le serveur enfant
   échoue.
3. Ajouter options `--port`, `--keep-tmp` et `--debug` aux smoke tests.
4. Documenter explicitement que les smoke tests dashboard/monitor ouvrent un
   port local et peuvent nécessiter une autorisation hors sandbox.
5. Ajouter un fixture/smoke test pour `sg-visual-fix --dry-run`.
6. Ajouter des fixtures sans réseau pour `sg-scout --offline --dry-run` et
   `sg-improve --dry-run`.

## État à la fin de cette reprise

- `shipguard@shipguard` officiel : installé et activé en `2.3.4` côté Codex.
- `shipguard@shipguard` : mis à jour en `2.3.4` côté Claude, redémarrage requis
  pour appliquer en session.
- Ancien `shipguard-codex@personal` : toujours installé et activé en `2.3.0`
  côté Codex, non supprimé volontairement.
- Tests `2.3.4` passés :
  - `node --check` sur dashboard, recorder et smoke tests ;
  - `actions-to-yaml.test.mjs` : 13/13 ;
  - `integration-test.mjs` : 11/11 ;
  - `review-smoke-test.mjs` : OK hors sandbox ;
  - `monitor-smoke-test.mjs` : OK hors sandbox.
- Aucun commit effectué.
