# Plan de test ShipGuard - reprise

Date de création : 2026-06-29

Contexte : recette du plugin ShipGuard sur le dépôt
`miweb-objectifs-2030`, sans commit. Le but de la reprise est de continuer la
validation fonctionnelle de ShipGuard lui-même, pas de corriger le site MiWeb.

## État au moment de la pause

### Pause après reprise 2.3.4

Le retour de Loïc est attendu avant de lancer les workflows destructifs ou
coûteux. Voir le mémo de reprise :

`visual-tests/_results/shipguard-reprise-prochaine-session.md`

- Serveur site : `http://127.0.0.1:8001/`
- Interface ShipGuard : `http://localhost:8888/`
- Interface HTML générée : `visual-tests/_results/review.html`
- Postmortem local : `visual-tests/_results/shipguard-postmortem.md`
- Audit code : `visual-tests/_results/audit-results.json`
- Rapport visuel : `visual-tests/_results/report.md`
- Process check : `visual-tests/_results/process-results.json`
- Change report persona : `visual-tests/_results/persona-reports/shipguard-recette-miweb/client.html`
- État Git attendu : uniquement `?? visual-tests/`
- Aucun commit effectué.

## Déjà validé

### `sg-visual-discover`

- Découverte statique HTML : 28 routes.
- Manifests générés dans `visual-tests/pages/*.yaml`.
- Config générée : `visual-tests/_config.yaml`.

### `sg-visual-run`

- Run complet sur 28 routes.
- Résultat : 28 exécutés, 28 réussis, 0 échec, 0 erreur.
- Captures : `visual-tests/_results/screenshots/`.
- Planche-contact : `visual-tests/_results/contact-sheet.png`.

### `sg-visual-review`

- `build-review.mjs` et `_review-template.html` installés.
- Interface servie sur `http://localhost:8888/`.
- Onglets vérifiés : Code Audit, Visual Tests, Recorded Tests, Routes.
- Rapports persona générés.

### `sg-code-audit`

- Audit quick report-only en 5 zones.
- Résultat agrégé : 19 constats, 4 high, 11 medium, 4 low.
- Aucune correction appliquée.

### `sg-process-check`

- Mode `reason` uniquement.
- 5 unités simulées depuis `audit-results.json`.
- Aucune mesure réelle before/after.

### `sg-record`

- Runtime installé dans `visual-tests/`.
- Tests unitaires `actions-to-yaml` : 13/13.
- Test d'intégration : 11/11.
- Manifest enregistré de recette visible dans Recorded Tests.

### `sg-change-report`

- Rapport source créé dans `change-reports/shipguard-recette-miweb/`.
- Pages persona générées : client, product, design, engineering.
- URL client vérifiée en `200 OK`.

### `sg-scout`

- Dry-run uniquement.
- `gh auth status` OK.
- Recherche GitHub OK avec autorisation réseau.
- Pas d'issue GitHub créée.

### `sg-improve`

- Dry-run uniquement.
- Propositions d'apprentissages écrites dans `sg-improve-dry-run.md`.
- Pas d'écriture `.shipguard/`.

## À tester à la reprise

### 1. Interface de revue visuelle complète

Objectif : valider les interactions humaines de `sg-visual-review`.

- Ouvrir `http://localhost:8888/`.
- Aller dans `Visual Tests`.
- Ouvrir une carte en lightbox.
- Vérifier affichage plein écran de la capture.
- Tester le crayon d'annotation.
- Créer une annotation avec sévérité et note.
- Sélectionner un ou plusieurs tests.
- Tester `Copy IDs`.
- Tester `Re-run selected`.
- Tester `Validate & Generate Report` depuis l'UI, pas seulement via POST direct.
- Vérifier que `visual-tests/_results/fix-manifest.json` est écrit et contient les annotations.

Critère OK : le manifest exporté contient les tests sélectionnés, les notes et
les coordonnées d'annotation.

### 2. `sg-visual-fix` en mode contrôlé

Objectif : tester la chaîne de correction sans risquer de modifier le site
principal sans décision.

Précondition : travailler sur une copie ou accepter des changements locaux non
commités.

- Partir d'un `fix-manifest.json` volontairement simple.
- Lire la capture annotée.
- Vérifier que ShipGuard identifie les fichiers sources plausibles.
- Arrêter avant application si aucun mode dry-run n'existe.
- Si on accepte le test complet : laisser appliquer une correction minime, puis
  vérifier before/after et diff.

Critère OK minimal : le skill sait lire le manifest et expliquer ce qu'il
modifierait. Critère OK complet : il produit une capture `*-after.png` et une
comparaison before/after.

### 3. `sg-record` interactif réel

Objectif : valider le recorder navigateur, pas seulement ses tests Node.

- Lancer le recorder sur `http://127.0.0.1:8001/`.
- Vérifier l'apparition de la barre flottante.
- Naviguer sur l'accueil.
- Cliquer un lien de variante.
- Utiliser le mode `Check`.
- Cliquer `Stop`.
- Vérifier le manifest dans `visual-tests/manifests/`.
- Rebuilder `review.html`.
- Vérifier que le manifest apparaît dans `Recorded Tests`.

Critère OK : un parcours humain complet devient un manifest rejouable.

### 4. `sg-process-check --mode=hybrid`

Objectif : distinguer ce qui reste raisonné de ce qui peut être mesuré.

- Choisir une unité simple et non destructive.
- Lancer un mode hybride.
- Vérifier que chaque observation est taguée `reasoned` ou `measured`.
- Vérifier que les limites sont explicites.

Critère OK : aucune observation prédite n'est présentée comme mesure.

### 5. `sg-process-check --mode=execute`

Objectif : tester le mode before/after réel seulement si le coût est acceptable.

- Créer ou utiliser un diff très petit.
- Vérifier création éventuelle de worktree baseline.
- Vérifier nettoyage du worktree.
- Vérifier que les résultats mesurés remplacent les prédictions.

Critère OK : baseline propre, résultat mesuré, aucun artefact parasite.

### 6. `sg-visual-run --from-audit`

Objectif : vérifier le pont audit code vers tests visuels.

- Utiliser `audit-results.json`.
- Lancer seulement les routes impactées.
- Vérifier que les routes invalides ou non HTML sont ignorées ou signalées.
- Vérifier le rapport final.

Critère OK : les routes issues de `impacted_ui_routes` sont testées sans lancer
inutilement toute la suite.

### 7. `sg-visual-run --from-process`

Objectif : vérifier le pont process-check vers confirmation visuelle.

- Utiliser `process-results.json`.
- Tester les routes impactées par le process.
- Vérifier le résumé dans `report.md`.

Critère OK : les routes process sont bien reprises ou explicitement ignorées.

### 8. Monitoring temps réel

Objectif : tester les endpoints de suivi de l'interface.

- POST `/api/monitor/audit-start`.
- POST `/api/monitor/agent-update`.
- GET `/api/monitor/status`.
- POST `/api/monitor/audit-complete`.
- Vérifier l'onglet Monitor si disponible.

Critère OK : la timeline ou l'état live apparaît sans casser l'audit final.

### 9. `sg-scout` complet

Objectif : tester au-delà du dry-run, seulement si on accepte l'écriture.

- Créer un vrai rapport scout dans `docs/scout-reports/` ou dans un dossier de
  test.
- Ne pas créer d'issue GitHub sans validation explicite.
- Vérifier la déduplication des propositions.

Critère OK : rapport scout exploitable, sans issue non voulue.

### 10. `sg-improve` complet

Objectif : capitaliser les apprentissages dans `.shipguard/`.

- Créer un snapshot `.shipguard/history/<timestamp>/`.
- Écrire `.shipguard/learnings.yaml`.
- Écrire `.shipguard/mistakes.md`.
- Tester `--rollback` sur un artefact de test.

Critère OK : apprentissages locaux présents et rollback démontré.

### 11. `sg-visual-review-stop`

Objectif : valider l'arrêt propre du serveur.

- Vérifier que `http://localhost:8888/` répond.
- Lancer `node visual-tests/build-review.mjs --stop`.
- Vérifier que l'URL ne répond plus.
- Relancer `--serve`.

Critère OK : arrêt et relance propres.

### 12. `sg-ship` natif

Objectif : tester l'orchestrateur comme commande unique, pas seulement les lanes.

- Lancer en `quick --all --report-only --mode=reason`.
- Vérifier qu'il enchaîne audit, process, visual et review.
- Vérifier que les skips sont explicitement motivés.
- Vérifier qu'il ne corrige rien en `--report-only`.

Critère OK : un seul workflow produit les mêmes familles d'artefacts que la
recette manuelle.

## Points génériques utiles pour Loïc / ShipGuard

Ces points sont utiles pour améliorer le plugin ShipGuard lui-même. Ils ne sont
pas spécifiques au dépôt MiWeb.

### 1. `sg-visual-review` devrait consommer un JSON canonique de résultats

Constat : l'interface dépend du parsing de `report.md` pour retrouver les
statuts. Dès que le rapport Markdown est adapté ou traduit, l'UI peut classer
les tests en `STALE`.

Amélioration générique :

- produire `visual-tests/_results/visual-results.json` ;
- faire consommer ce JSON par `build-review.mjs` ;
- garder `report.md` comme rendu humain uniquement.

### 2. `sg-visual-review` doit accepter `impacted_ui_routes`

Constat : le schéma d'audit expose `impacted_ui_routes`, mais le template lit
aussi ou surtout `impacted_routes`.

Amélioration générique :

- accepter les deux champs ;
- normaliser au build ;
- documenter le champ canonique.

### 3. Un audit valide avec zéro bug ne doit pas s'afficher comme absent

Constat : `bugs: []` peut déclencher l'état vide `No audit data found`.

Amélioration générique :

- distinguer `no audit file`, `audit failed`, `audit completed with zero bug` ;
- afficher une carte "0 bug found" quand `summary.total_bugs = 0`.

### 4. Le serveur de revue doit binder explicitement sur `127.0.0.1`

Constat : `server.listen(PORT)` peut écouter plus large que prévu, alors que
l'interface expose des endpoints POST locaux.

Amélioration générique :

- utiliser `server.listen(PORT, "127.0.0.1")` par défaut ;
- ajouter une option explicite `--host=0.0.0.0` si nécessaire ;
- afficher l'host réel dans les logs.

### 5. Le garde anti-path traversal doit utiliser des chemins résolus

Constat : `startsWith(RESULTS_DIR)` sur chaîne est fragile.

Amélioration générique :

- calculer `resolved = resolve(filePath)` ;
- vérifier `relative(RESULTS_DIR, resolved)` ;
- refuser les chemins qui commencent par `..` ou sont absolus hors racine.

### 6. Ajouter un mode `--dry-run` officiel à `sg-visual-fix`

Constat : le flux de correction est utile à tester, mais il est destructif par
conception.

Amélioration générique :

- lire le manifest ;
- analyser les captures ;
- proposer les fichiers et corrections envisagés ;
- ne rien écrire ;
- produire un rapport de plan de correction.

### 7. `sg-record` doit éviter les préchecks `npx` non bornés

Constat : `npx playwright --version` peut suspendre ou tenter le réseau.

Amélioration générique :

- détecter d'abord un binaire local ;
- borner tout précheck avec timeout ;
- afficher une commande d'installation au lieu de bloquer.

### 8. Le bootstrap doit être strictement séquentiel pour les dossiers

Constat : copier des fichiers en parallèle avant `mkdir -p` peut échouer.

Amélioration générique :

- créer tous les dossiers avant les copies ;
- éviter la parallélisation dans les étapes de bootstrap ;
- rendre les copies idempotentes.

### 9. L'onglet Agents devrait accepter un champ `agents[]`

Constat : l'UI déduit les agents depuis le format des IDs de bugs. Si les IDs
diffèrent, le compteur peut exister sans détails utiles.

Amélioration générique :

- ajouter `agents[]` dans `audit-results.json` ;
- ne pas dépendre uniquement du pattern d'ID ;
- afficher zones, fichiers audités, durée et bugs par agent.

### 10. Le compteur de bugs par route doit être calculé proprement

Constat : la route `/` peut matcher trop largement et compter tous les bugs.

Amélioration générique :

- accepter un `bug_count` optionnel par route ;
- sinon calculer par mapping explicite bug -> route ;
- traiter `/` comme cas spécial.

### 11. Les endpoints de monitor devraient avoir un smoke test

Constat : les endpoints existent, mais ils n'ont pas été validés par un script
de recette officiel.

Amélioration générique :

- fournir `node visual-tests/monitor-smoke-test.mjs` ;
- tester audit-start, agent-update, status, audit-complete ;
- vérifier rendu dans l'interface.

### 12. Documenter les contraintes sandbox des agents

Constat : `agent-browser`, serveurs locaux, `curl POST`, `gh api` et `npx`
peuvent nécessiter des autorisations différentes selon l'environnement.

Amélioration générique :

- ajouter une section "Codex / sandbox" dans les runbooks ;
- lister les actions qui demandent autorisation ;
- proposer des variables de chemin vers `/tmp` pour les sockets et caches.

## Commandes utiles à la reprise

```bash
cd /Users/alex/Claude/miweb-objectifs-2030

# Relancer le serveur du site si besoin
scripts/serve-local.sh 8001

# Relancer l'interface ShipGuard
node visual-tests/build-review.mjs --serve

# Refaire le run visuel complet
PYTHONPYCACHEPREFIX=/private/tmp/pycache-miweb python3 visual-tests/_shipguard_static_run.py --run

# Rebuilder l'interface sans relancer le serveur
node visual-tests/build-review.mjs

# Vérifications rapides
python3 -m json.tool visual-tests/_results/audit-results.json >/tmp/audit.json
python3 -m json.tool visual-tests/_results/process-results.json >/tmp/process.json
node visual-tests/lib/actions-to-yaml.test.mjs
curl -I http://localhost:8888/
git status --short
```
