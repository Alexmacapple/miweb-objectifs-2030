# Postmortem recette ShipGuard - MiWeb Objectifs 2030

Date : 2026-06-29

## Contexte

Objectif : tester explicitement le plugin ShipGuard sur le site statique
`miweb-objectifs-2030`, sans commit, avec serveur local et interface HTML de
revue.

## Blocages et constats

### Reprise 2.3.4 après corrections de Loïc

Un postmortem dédié à la reprise après les commits ShipGuard `2.3.4` a été
ajouté ici :

`visual-tests/_results/shipguard-postmortem-loic-2.3.4.md`

Synthèse : les corrections principales sont présentes et les smoke tests
officiels passent hors sandbox. Les frictions restantes concernent surtout la
migration depuis l'ancien adaptateur Codex local, les clones marketplace
multiples entre Claude/Codex, le redémarrage Claude après update, et les smoke
tests qui masquent l'erreur réelle `listen EPERM` quand le sandbox refuse
l'ouverture d'un serveur local.

### 1. Confusion initiale entre accessibilité et ShipGuard

- Symptôme : premier passage orienté validations accessibilité classiques, pas
  preuve d'un workflow ShipGuard complet.
- Cause : le dépôt contient déjà des conventions fortes d'audit accessibilité,
  et le besoin ShipGuard n'était pas encore isolé dans les artefacts.
- Contournement : exécution explicite des runbooks `sg-visual-discover`,
  `sg-visual-run` et `sg-visual-review`.
- Action proposée : ajouter une commande unique de recette ShipGuard dans le
  dépôt de test ou dans l'adaptateur Codex.

### 2. `agent-browser` bloqué par le sandbox

- Symptôme : 28 erreurs `Socket directory '/Users/alex/.agent-browser' is not
  writable: Operation not permitted`.
- Cause : `agent-browser` écrit son socket dans le home utilisateur, hors racine
  autorisée par le sandbox.
- Contournement : relance du run ShipGuard avec autorisation hors sandbox.
- Action proposée : documenter ce besoin dans `sg-visual-run` pour Codex, ou
  permettre de configurer un répertoire de socket dans `/private/tmp`.

### 3. Rapport Markdown incompatible avec `sg-visual-review`

- Symptôme : l'interface HTML indiquait `0 pass, 0 fail, 28 stale` malgré un
  run visuel `28/28 PASS`.
- Cause : le rapport avait été francisé en remplaçant les identifiants
  techniques `pages/<slug>` par des libellés humains ; le builder HTML parse ces
  identifiants pour retrouver les statuts.
- Contournement : rapport final avec première colonne `pages/<slug>` et libellé
  français dans une colonne séparée.
- Action proposée : rendre le parser de `sg-visual-review` moins dépendant du
  format Markdown, ou écrire un JSON de résultats canonique consommé par l'UI.

### 4. Serveur `sg-visual-review` bloqué par le sandbox

- Symptôme : `listen EPERM: operation not permitted 0.0.0.0:8888`.
- Cause : écoute réseau locale refusée en sandbox.
- Contournement : lancement de `node visual-tests/build-review.mjs --serve`
  avec autorisation hors sandbox.
- Action proposée : documenter ce besoin pour Codex, et envisager un bind
  explicite sur `127.0.0.1`.

### 5. Onglet Code Audit vide tant que `audit-results.json` n'existe pas

- Symptôme : message UI `No audit data found. Run /sg-code-audit to start a new
  audit.`
- Cause : aucun `visual-tests/_results/audit-results.json` produit avant le
  passage `/sg-code-audit`.
- Contournement : lancement d'un audit `quick --report-only` en 5 zones, sans
  correction automatique.
- Action proposée : dans le dashboard, distinguer "pas encore lancé" de "audit
  lancé avec 0 bug".

### 6. Appels locaux `curl` bloqués sans autorisation explicite

- Symptôme : `curl -X POST http://localhost:8888/save-manifest` échouait avec
  `Immediate connect fail ... Operation not permitted`, alors que `curl -I`
  fonctionnait.
- Cause : seuls certains préfixes `curl` étaient déjà autorisés hors sandbox ;
  les autres connexions localhost restent bloquées.
- Contournement : exécuter le `POST /save-manifest` avec autorisation hors
  sandbox.
- Action proposée : documenter les préfixes réseau nécessaires pour tester
  entièrement l'interface ShipGuard dans Codex.

### 7. Lightbox non validée automatiquement par clic `agent-browser`

- Symptôme : le clic automatisé sur une carte Visual Tests ne faisait pas
  apparaître de lightbox visible dans le snapshot.
- Cause probable : différence entre le clic de l'arbre d'accessibilité et la
  zone de clic attendue par l'interface, ou état UI non capturé par le snapshot.
- Contournement : capture de la grille, test des filtres, test direct du serveur
  `/save-manifest` et conservation de la vérification manuelle de la lightbox.
- Action proposée : ajouter des attributs stables ou des boutons explicites sur
  les cartes pour les tests agentiques.

### 8. Compteur de bugs trop large sur la route `/`

- Symptôme : l'onglet Routes affiche 19 bugs pour `/`.
- Cause : le calcul du template compare le chemin de fichier à la route
  normalisée ; pour `/`, le préfixe devient trop générique.
- Contournement : conserver les routes impactées, mais ne pas considérer ce
  compteur comme fiable pour la route racine.
- Action proposée : traiter `/` comme cas spécial, ou fournir directement un
  `bug_count` calculé côté `audit-results.json`.

### 9. Onglet Agents peu détaillé avec IDs non standard

- Symptôme : compteur `Agents 5` visible, mais pas de cartes agents détaillées
  dans le snapshot.
- Cause probable : le template déduit les agents depuis des IDs au format
  `r1-z01-001`, alors que la recette a produit des IDs `SG-Zn-...`.
- Contournement : conserver les résultats par zone dans `audit-results.json` et
  le postmortem.
- Action proposée : accepter un champ `agents[]` explicite dans
  `audit-results.json`.

### 10. `npx playwright --version` suspendu

- Symptôme : la commande de précheck Playwright n'a pas rendu la main.
- Cause probable : usage de `npx` sans dépendance locale ou tentative réseau.
- Contournement : arrêt manuel de la commande, puis validation de `sg-record`
  via tests Node locaux fournis par le plugin.
- Action proposée : éviter `npx` pour le précheck si Playwright n'est pas dans
  `node_modules`, ou borner la commande avec timeout.

### 11. Bootstrap `sg-record` lancé trop parallèlement

- Symptôme : plusieurs `cp` vers `visual-tests/lib/` ont échoué car le dossier
  n'existait pas encore.
- Cause : orchestration parallèle de la création du dossier et des copies.
- Contournement : relance des copies après création du dossier.
- Action proposée : dans le runbook, exécuter `mkdir -p` séquentiellement avant
  toute copie.

### 12. `sg-scout` dépend d'un accès réseau explicite

- Symptôme : `gh api search/repositories` échoue dans le sandbox avec
  `error connecting to api.github.com`.
- Cause : réseau bloqué par défaut.
- Contournement : relance avec autorisation réseau, puis dry-run sans création
  d'issue.
- Action proposée : documenter le mode offline/dry-run et les autorisations
  réseau nécessaires.

### 13. `sg-visual-fix` non exécuté jusqu'à correction

- Symptôme : le flux a produit `fix-manifest.json`, mais aucun fix n'a été
  appliqué.
- Cause : `sg-visual-fix` modifie le code par conception, incompatible avec une
  recette sans correction automatique.
- Contournement : validation du manifeste et arrêt avant application.
- Action proposée : ajouter un mode officiel `--dry-run` à `sg-visual-fix`.

### 14. `sg-visual-review-stop` non exécuté

- Symptôme : le skill d'arrêt n'a pas été lancé.
- Cause : l'interface HTML doit rester accessible pour la revue utilisateur.
- Contournement : conserver le serveur actif sur `http://localhost:8888/`.
- Action proposée : tester `--stop` en fin de session seulement, quand
  l'interface n'est plus nécessaire.

## Artefacts de preuve

- Interface HTML : `visual-tests/_results/review.html`
- Rapport visuel : `visual-tests/_results/report.md`
- Planche-contact : `visual-tests/_results/contact-sheet.png`
- Captures : `visual-tests/_results/screenshots/`
- Captures de l'interface : `visual-tests/_results/shipguard-review-ui.png`,
  `visual-tests/_results/shipguard-review-visual-tests.png`
