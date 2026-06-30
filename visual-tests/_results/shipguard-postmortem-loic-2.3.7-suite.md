# Postmortem ShipGuard 2.3.7 - recette fonctionnelle

Date : 2026-06-30

Destinataire : Loïc, pour action éventuelle dans le dépôt ShipGuard.

Objectif : transformer la nouvelle recette en constats génériques
reproductibles côté ShipGuard. Ce postmortem évite volontairement les détails
propres à l'environnement de test local.

## Verdict court

ShipGuard 2.3.7 tient correctement les scénarios principaux de recette :

- review visuelle complète reconstruite avec 28 tests, 28 réussites ;
- `sg-visual-fix` valide en dry-run contrôlé ;
- `sg-record` produit bien un manifest interactif ;
- `sg-process-check --mode=hybrid` produit des résultats structurés ;
- sous-runs `sg-visual-run --from-audit` et `--from-process` exécutés avec
  succès ;
- smoke monitor, scout, improve, rollback et arrêt serveur de review passants ;
- orchestration `sg-ship` report-only reconstituée sans modification source.

Les points vraiment actionnables côté dépôt ShipGuard concernent surtout :

1. la normalisation des identifiants du monitor live ;
2. la traçabilité des sous-runs visuels ciblés ;
3. le matching de la route racine `/` ;
4. le contrat de comptage et de validation E2E de `sg-record` ;
5. l'ambiguïté entre un skill agentique `sg-ship` et une commande shell.

## Ce qui est validé

### Review visuelle

Résultat consolidé :

```text
28 tests exécutés
28 réussites
0 échec
0 erreur
```

La review reconstruit les captures, les manifests enregistrés et les rapports
personas. Aucun correctif source n'a été appliqué pendant cette recette.

### `sg-visual-fix`

Le dry-run lit correctement un manifest annoté et produit un plan sans
modifier le site.

Statut : contrat dry-run OK.

### `sg-record`

Le recorder passe son préflight, capture des actions réelles et écrit un
manifest YAML exploitable.

Statut : capture et écriture OK, mais contrat E2E incomplet sur la barre de
contrôle.

### `sg-process-check`

Le mode `hybrid` produit un JSON valide et distingue les observations
mesurées des observations raisonnées.

Statut : sortie structurée OK, avec limite normale du mode hybride.

### `sg-scout` et `sg-improve`

Les smoke tests déterministes passent :

```text
scout offline dry-run smoke test passed
improve dry-run smoke test passed
improve rollback smoke test passed
```

Statut : pas de régression observée sur les dry-runs et rollback.

## Blocages et points actionnables

### B1 - Monitor : payload `id` persisté sous `agents.undefined`

Sévérité proposée : haute.

Constat générique :

`POST /api/monitor/agent-update` accepte un payload contenant `id`, répond en
succès, mais persiste l'entrée sous la clé `undefined`.

Reproduction minimale côté ShipGuard :

```text
POST /api/monitor/audit-start
POST /api/monitor/agent-update {"id":"z2","status":"completed"}
GET  /api/monitor/status
```

Résultat actuel :

```text
agents.undefined.id = "z2"
```

Résultat attendu :

```text
agents.z2.status = "completed"
```

ou bien une erreur explicite si `id` n'est pas un champ accepté.

Correction attendue :

- normaliser `id`, `agent_id` et `zone_id` dans une fonction unique ;
- refuser un update sans identifiant normalisable ;
- ajouter un test qui échoue si une clé `undefined` apparaît dans `agents`.

### B2 - Monitor : incohérence de namespace `r1:z1` versus `z1`

Sévérité proposée : moyenne à haute.

Constat générique :

Quand le monitor préremplit des agents de type `r1:z1` / `r1:z2`, des updates
arrivant sous `z1` ou `z2` peuvent créer ou modifier une autre entrée. Les
agents préremplis restent alors `pending`, alors que l'activité a bien été
reçue.

Résultat attendu :

Un update doit cibler la même entité logique que l'agent prérempli, ou le
serveur doit documenter et imposer un format unique d'identifiant.

Tests à ajouter :

```text
start agents: r1:z1, r1:z2
update id: z1
expected: r1:z1 completed, no duplicate z1
```

et :

```text
start agents: z1, z2
update id: r1:z1
expected: comportement explicitement défini
```

### B3 - Sous-runs visuels : le scope se perd dans le dashboard

Sévérité proposée : moyenne.

Constat générique :

Après un sous-run visuel ciblé, le rapport humain reflète bien la sous-suite
exécutée, mais les résultats reconstruits pour le dashboard peuvent revenir à
un résumé global de toute la suite.

Exemple observé :

```text
from-audit  : 13/13 pass dans le rapport ciblé
from-process: 4/4 pass dans le rapport ciblé
dashboard   : résumé global 28/28 après rebuild
```

Résultat attendu :

Le dashboard doit indiquer clairement si la vue courante correspond à un run
complet ou à un sous-run ciblé.

Correction attendue :

- ajouter un `run_id` ;
- persister `scope`, `selected_routes`, `selected_manifests` et
  `total_selected` ;
- distinguer `full_suite_total` et `selected_total` ;
- afficher les routes non couvertes avec une raison.

### B4 - Matching de la route `/` trop large

Sévérité proposée : moyenne.

Constat générique :

Dans un mode `--from-audit` ou `--from-process`, une route impactée `/` ne
doit pas matcher tous les manifests par simple préfixe.

Résultat actuel à risque :

```text
impacted_routes includes "/"
naive prefix matching selects every route
```

Résultat attendu :

La racine `/` doit être traitée comme cas spécial :

```text
"/" matches only the root page manifest
```

ou selon une règle explicitement documentée.

Test à ajouter :

```text
routes: "/", "/about/", "/docs/"
input : impacted_routes = ["/"]
expected selected manifests: only root
```

### B5 - Routes non HTML : statut `uncovered` ou `skipped` explicite

Sévérité proposée : moyenne.

Constat générique :

Les routes non rendables comme une archive ZIP, ou les routes internes comme
une page de review, ne sont pas couvertes par les manifests visuels HTML.

Résultat attendu :

Le run ciblé doit l'écrire explicitement :

```text
route: /assets/downloads/file.zip
status: skipped
reason: non_html_asset
```

et :

```text
route: /review.html
status: uncovered
reason: no_visual_manifest
```

Cela éviterait de confondre une réussite visuelle avec une couverture totale
des routes impactées.

### B6 - `sg-record` : écart entre compteur console et actions YAML

Sévérité proposée : basse à moyenne.

Constat générique :

Le recorder annonce un nombre d'étapes sauvegardées, mais le YAML contient une
action supplémentaire liée à la capture finale.

Exemple de contrat à clarifier :

```text
console: Saved 15 steps
yaml   : 16 actions including final screenshot
```

Résultat attendu :

Le message console doit compter exactement ce que le YAML contient, ou
expliciter la capture finale hors compteur.

Tests à ajouter :

- compter les actions YAML après finalisation ;
- vérifier le message console ;
- tester la finalisation par fermeture du navigateur ;
- tester la finalisation par le bouton `Stop`.

### B7 - `sg-record` : validation E2E de la barre `Check` / `Stop`

Sévérité proposée : moyenne.

Constat générique :

La capture interactive fonctionne, mais la recette n'a pas validé de bout en
bout les boutons `Check` et `Stop` de la barre flottante dans un test autonome.

Point important : ce n'est pas formulé comme un bug utilisateur. C'est un
manque de test robuste côté ShipGuard.

Test recommandé côté dépôt :

```text
launch recorder in a controlled Playwright test
click page content
click toolbar Check
assert validation state is visible or exported
click toolbar Stop
assert manifest is written
assert process exits cleanly
```

Le test doit piloter la page et la barre dans le même contexte navigateur, sans
dépendre d'une automatisation système externe.

### B8 - `sg-ship` : skill agentique versus commande exécutable

Sévérité proposée : basse à moyenne.

Constat générique :

La recette attendait une commande `sg-ship` native. Dans cette session,
`sg-ship` était un skill agentique : l'orchestration a donc été vérifiée en
reconstituant les lanes, pas via un binaire unique.

Résultat attendu :

Choisir et documenter un contrat unique :

- soit `sg-ship` est une orchestration agentique, et la documentation ne doit
  pas la présenter comme une commande shell ;
- soit ShipGuard fournit un vrai entrypoint CLI `sg-ship` ;
- soit les deux existent, avec des garanties différentes.

Test d'acceptation possible :

```text
sg-ship --quick --all --report-only --mode=reason
expected: no source modification, report summary, explicit lane statuses
```

## Non-bugs à ne pas surinterpréter

- Les échecs de pilotage d'une interface graphique externe ne doivent pas être
  traités comme un bug ShipGuard tant qu'un test E2E interne ne les reproduit
  pas.
- Le mode `sg-process-check --mode=hybrid` n'a pas de baseline before complète
  par définition ; il doit seulement dire clairement ce qui est mesuré et ce
  qui est raisonné.
- Les scans GitHub réels, écritures `.shipguard/` et issues GitHub n'ont pas
  été déclenchés pendant cette recette. Les constats sur `sg-scout` et
  `sg-improve` couvrent donc les smokes, pas les effets réels distants.
- Aucun correctif visuel n'a été appliqué au site de test ; les résultats ne
  prouvent pas le comportement d'un mode auto-fix complet.

## Priorités proposées

### P0

Corriger la normalisation monitor pour empêcher toute entrée
`agents.undefined`.

Critère d'acceptation :

```text
all accepted update payloads produce a defined agent key
no monitor status contains agents.undefined
```

### P1

Préserver le scope des sous-runs visuels dans les résultats consommés par le
dashboard.

Critère d'acceptation :

```text
targeted run report and dashboard agree on selected_total
full suite total remains visible but separate
```

### P1

Spécialiser le matching de `/` et tracer les routes non couvertes.

Critère d'acceptation :

```text
"/" does not select every manifest
non HTML routes are reported as skipped or uncovered with a reason
```

### P2

Durcir le contrat E2E de `sg-record`.

Critère d'acceptation :

```text
toolbar Check and Stop are covered by an automated test
console step count matches the YAML contract
```

### P2

Clarifier le statut de `sg-ship`.

Critère d'acceptation :

```text
documentation and implementation agree: agentic workflow, CLI, or both
```

## Résumé actionnable pour issue GitHub

```text
ShipGuard 2.3.7 retest: main flows OK, but monitor and targeted visual run
traceability need fixes.

Confirmed:
- visual full suite: 28/28 pass
- visual-fix dry-run: pass
- recorder preflight and manifest write: pass
- process hybrid JSON/report: pass
- scout/improve dry-run and rollback smokes: pass

Actionable issues:
1. monitor agent-update accepts {"id": "..."} but stores agents.undefined.
2. monitor updates may not reconcile z1 with prefilled r1:z1 agents.
3. targeted visual runs lose their selected scope in dashboard/rebuilt JSON.
4. impacted route "/" must not prefix-match every manifest.
5. non HTML or internal routes should be explicit skipped/uncovered entries.
6. recorder console step count differs from YAML actions when final screenshot is added.
7. recorder toolbar Check/Stop needs a self-contained E2E test.
8. sg-ship should be documented as agentic workflow or exposed as a real CLI.
```
