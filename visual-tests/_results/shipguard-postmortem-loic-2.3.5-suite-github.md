# Postmortem ShipGuard 2.3.5 - passe complementaire

Date : 2026-06-30

Contexte : passe de tests complementaire effectuee apres l'envoi du premier
postmortem generique `2.3.5` a Loic.

Objectif : ne documenter ici que les nouveaux tests executes apres ce premier
envoi, avec les enseignements generiques utiles pour le repo GitHub ShipGuard.

## Resume

Trois points ont ete testes en plus :

1. migration / suppression de l'ancien adaptateur Codex local ;
2. lancement reel du recorder interactif `sg-record` ;
3. principe de rollback `sg-improve` sur fixture isolee.

Resultat :

- la suppression de l'ancien adaptateur Codex fonctionne, mais peut necessiter
  une permission hors sandbox ;
- le recorder interactif ne demarre pas dans un depot sans Playwright importable,
  meme si les tests Node du recorder passent ;
- le principe de rollback `.shipguard` fonctionne en fixture, mais il manque un
  smoke test officiel dedie.

## 1. Migration Codex : suppression de l'ancien adaptateur local

### Test effectue

Etat initial generique :

```text
codex plugin list
shipguard-codex@personal  installed, enabled  <ancienne version>
shipguard@shipguard       installed, enabled  2.3.5
```

Commande testee :

```bash
codex plugin remove shipguard-codex@personal --json
```

### Resultat

Premiere tentative en environnement sandboxe :

```text
Error: failed to remove existing plugin cache entry: Operation not permitted
```

Relance avec permission d'ecriture sur le cache plugin :

```json
{
  "pluginId": "shipguard-codex@personal",
  "name": "shipguard-codex",
  "marketplaceName": "personal"
}
```

Etat final :

```text
shipguard-codex@personal  not installed
shipguard@shipguard       installed, enabled  2.3.5
```

### Feedback generique pour ShipGuard

La doc migration devrait preciser que la suppression de l'ancien adaptateur :

- supprime aussi une entree de cache plugin ;
- peut echouer avec `EPERM` sous sandbox ;
- doit etre relancee avec une permission d'ecriture adaptee ;
- se verifie ensuite avec `codex plugin list`.

### Critere d'acceptation propose

La section migration Codex contient une sous-section :

```text
If removal fails with EPERM, rerun with permission to modify the plugin cache,
then verify that shipguard-codex@personal is listed as not installed.
```

## 2. `sg-record` interactif : dependance Playwright explicite

### Test effectue

Commande :

```bash
node visual-tests/sg-record.mjs <url> --name recette-235-interactive
```

### Resultat

Le recorder ne va pas jusqu'a l'ouverture du navigateur :

```text
ShipGuard Recorder
URL: <url>
Name: recette-235-interactive

Playwright not found. Install with:
  npm init -y && npm install playwright && npx playwright install chromium
```

Ce resultat est distinct des tests Node du recorder, qui peuvent passer :

```text
actions-to-yaml.test.mjs  -> 13/13
integration-test.mjs      -> 11/11
```

### Feedback generique pour ShipGuard

Le recorder interactif a une dependance runtime plus forte que les autres tests
du recorder :

- `actions-to-yaml` valide la conversion ;
- `integration-test` valide l'integration apres installation dans un projet ;
- mais `sg-record.mjs` exige `playwright` importable localement et Chromium
  installable/disponible.

Le message actuel est utile, mais la documentation devrait mieux distinguer :

- `agent-browser` disponible ;
- tests Node recorder OK ;
- Playwright importable par `sg-record` ;
- recorder interactif reel OK.

### Proposition

Ajouter un preflight ou une commande documentee :

```bash
node visual-tests/sg-record.mjs --check
```

ou, a defaut, une section :

```text
Recorder interactive prerequisites:
- Node project or local npm setup
- playwright importable from the project
- Chromium installed
- GUI/browser launch permission
```

### Critere d'acceptation propose

Avant la recette interactive, l'utilisateur peut executer un check qui dit :

```text
PLAYWRIGHT_OK
CHROMIUM_OK
GUI_LAUNCH_OK
```

ou un diagnostic precis indiquant quoi installer.

## 3. `sg-improve --rollback` : besoin d'un smoke test officiel

### Test effectue

Fixture isolee `.shipguard` :

1. creation de `learnings.yaml` et `mistakes.md` initiaux ;
2. creation d'un snapshot `history/<timestamp>/` ;
3. simulation d'une modification des deux fichiers courants ;
4. restauration depuis le snapshot ;
5. suppression du snapshot consomme.

### Resultat

Apres rollback :

```text
learnings.yaml -> contenu initial restaure
mistakes.md    -> contenu initial restaure
history/       -> snapshot consomme
```

Le principe fonctionne en fixture isolee.

### Feedback generique pour ShipGuard

`sg-improve --dry-run` dispose maintenant d'un smoke test deterministe. Le mode
rollback est le garde-fou du mode reel, mais il n'a pas encore de smoke test
officiel comparable.

### Proposition

Ajouter un test du type :

```bash
node plugins/shipguard/skills/sg-improve/improve-rollback-smoke-test.mjs
```

Ce test devrait :

- creer une fixture temporaire ;
- ecrire `.shipguard/learnings.yaml` et `.shipguard/mistakes.md` ;
- creer un snapshot ;
- modifier les fichiers ;
- lancer le rollback ;
- verifier que les contenus initiaux sont restaures ;
- verifier qu'aucune ecriture ne sort de la fixture.

### Critere d'acceptation propose

```text
improve rollback smoke test passed
```

avec une garantie que le depot courant n'a pas ete modifie.

## Synthese des nouveaux points a traiter

| Sujet | Priorite | Action recommandee |
|---|---:|---|
| Suppression ancien adaptateur Codex sous sandbox | Moyenne | Documenter `EPERM` et verification post-remove. |
| Recorder interactif sans Playwright | Moyenne | Ajouter preflight/doc de prerequis interactifs. |
| Rollback `sg-improve` | Moyenne | Ajouter smoke test officiel sur fixture temporaire. |

## Points non testes dans cette passe

- `sg-record` interactif complet avec barre flottante, car Playwright n'etait
  pas importable localement.
- `sg-visual-fix` reel avec modification before/after.
- `sg-process-check --mode=hybrid` et `--mode=execute`.
- `sg-scout` avec creation/commentaire d'issue GitHub.
- `sg-improve` reel dans un depot utilisateur.
- `sg-ship` complet de bout en bout.
