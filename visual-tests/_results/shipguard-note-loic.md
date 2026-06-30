# Note pour Loïc - améliorations génériques ShipGuard

Date : 2026-06-29

Contexte : recette ShipGuard menée dans un dépôt de test statique, depuis Codex,
avec installation du plugin côté Codex et Claude. Cette note ne vise pas à
corriger le dépôt de test ; elle isole les points utiles pour améliorer
ShipGuard de façon générique.

Mise à jour reprise 2.3.4 : les correctifs de Loïc ont été récupérés et testés
dans un document séparé, centré sur les frictions restantes après correction :
`visual-tests/_results/shipguard-postmortem-loic-2.3.4.md`.

## Résumé exécutif

ShipGuard fonctionne sur la chaîne principale :

- découverte visuelle ;
- génération de manifests ;
- run avec captures ;
- dashboard HTML ;
- audit code report-only ;
- rapports persona ;
- recorder côté manifests ;
- scout et improve en dry-run.

Les points bloquants ne sont pas sur l'idée produit, mais sur la robustesse de
l'orchestration : formats d'échange trop implicites, dépendances au Markdown,
serveur local trop permissif, difficultés en environnement sandbox, et manque
de modes dry-run pour tester les chemins destructifs.

Les améliorations les plus rentables sont :

1. introduire des fichiers JSON canoniques entre les skills ;
2. durcir `build-review.mjs --serve` ;
3. rendre les états UI plus explicites ;
4. ajouter des smoke tests officiels pour review, monitor, recorder et fix ;
5. documenter les contraintes Codex/Claude sandbox.

## Priorité P0 - Contrats de données stables

### 1. Ajouter un `visual-results.json` canonique

#### Constat

`sg-visual-review` reconstruit l'état des tests visuels en parsant
`visual-tests/_results/report.md`. Le Markdown est un format humain, pas un
contrat machine. Dès que le rapport est traduit, reformatté ou enrichi, le
dashboard peut perdre les statuts et classer les tests en `STALE`.

#### Impact

- faux état dans l'interface ;
- perte de confiance dans le dashboard ;
- coupling fort entre le wording du rapport et le rendu HTML ;
- fragilité pour les plugins/adaptateurs localisés.

#### Proposition

Écrire un fichier canonique après chaque `sg-visual-run` :

```json
{
  "schema_version": "1.0",
  "timestamp": "2026-06-29T13:30:00Z",
  "base_url": "http://127.0.0.1:8001",
  "summary": {
    "total": 28,
    "pass": 28,
    "fail": 0,
    "error": 0,
    "stale": 0,
    "skipped": 0,
    "duration_ms": 36800
  },
  "tests": [
    {
      "id": "pages/root-index",
      "manifest": "visual-tests/pages/root-index.yaml",
      "name": "Accueil",
      "url": "/",
      "status": "PASS",
      "duration_ms": 1200,
      "screenshot": "screenshots/root-index.png",
      "failure_reason": null
    }
  ]
}
```

`report.md` devient uniquement un rendu lisible. `build-review.mjs` lit le JSON
en priorité, puis garde le parsing Markdown comme fallback legacy.

#### Critères d'acceptation

- Modifier le texte ou la langue de `report.md` ne change pas les statuts dans
  `review.html`.
- Un test `PASS` reste `PASS` dans le dashboard même si le rapport Markdown est
  absent.
- Le dashboard affiche un message clair si `visual-results.json` est invalide.

### 2. Normaliser `impacted_ui_routes` et `impacted_routes`

#### Constat

Le schéma ShipGuard côté audit expose `impacted_ui_routes`, mais certaines
parties du dashboard lisent `impacted_routes`. Un alias manuel a été nécessaire
pour que l'onglet Routes affiche les résultats.

#### Impact

- les routes impactées peuvent être invisibles ;
- le pont `sg-code-audit -> sg-visual-run --from-audit` devient fragile ;
- les utilisateurs doivent connaître deux noms de champs.

#### Proposition

Choisir un champ canonique :

```json
"impacted_ui_routes": [
  {"route": "/dashboard", "reason": "Bug visible", "severity": "high"}
]
```

Puis normaliser au chargement :

```js
const impactedRoutes = data.impacted_ui_routes || data.impacted_routes || [];
```

Le builder peut aussi réécrire `data.impacted_routes` uniquement pour compat.

#### Critères d'acceptation

- Un audit avec seulement `impacted_ui_routes` alimente l'onglet Routes.
- Un audit legacy avec seulement `impacted_routes` continue de fonctionner.
- Les docs et exemples utilisent un seul nom canonique.

## Priorité P0 - Sécurité du serveur local

### 3. Binder le serveur de revue sur `127.0.0.1`

#### Constat

`build-review.mjs --serve` utilise `server.listen(PORT)` sans host explicite.
Selon Node et l'environnement, cela peut écouter sur l'adresse non spécifiée.
Le commentaire parle d'un serveur localhost-only, mais le code ne l'impose pas.

#### Impact

Le serveur expose :

- fichiers sous `_results/` ;
- `POST /save-manifest` ;
- endpoints monitor ;
- CORS wildcard.

Sur un poste connecté à un réseau non fiable, une exposition involontaire du
port augmente la surface d'attaque.

#### Proposition

Par défaut :

```js
const HOST = "127.0.0.1";
server.listen(PORT, HOST, () => {
  console.log(`Server: http://${HOST}:${PORT}`);
});
```

Ajouter une option explicite :

```bash
node visual-tests/build-review.mjs --serve --host=0.0.0.0
```

et afficher un avertissement si `--host=0.0.0.0`.

#### Critères d'acceptation

- Par défaut, le serveur écoute sur `127.0.0.1`.
- Le log affiche l'host réel.
- L'exposition LAN demande une option explicite.

### 4. Remplacer le garde anti-path traversal basé sur `startsWith`

#### Constat

Le serveur de fichiers utilise une logique du type :

```js
if (!filePath.startsWith(RESULTS_DIR)) forbidden
```

Ce test chaîne est fragile. Un chemin résolu vers un dossier frère dont le nom
partage le même préfixe peut contourner l'intention.

#### Proposition

Utiliser `resolve` et `relative` :

```js
import { resolve, relative, isAbsolute } from "path";

const root = resolve(RESULTS_DIR);
const target = resolve(root, requestedPath);
const rel = relative(root, target);

if (rel.startsWith("..") || isAbsolute(rel)) {
  res.writeHead(403);
  res.end("Forbidden");
  return;
}
```

#### Critères d'acceptation

- `../` est refusé.
- Les chemins encodés sont refusés après décodage et résolution.
- Un dossier frère `_results-old` n'est pas servi.

## Priorité P1 - États UI et expérience dashboard

### 5. Distinguer "pas d'audit" et "audit avec zéro bug"

#### Constat

Un `audit-results.json` valide avec `bugs: []` peut être rendu comme
`No audit data found`.

#### Impact

Un bon résultat est présenté comme une absence de données. Cela crée une
ambiguïté importante :

- l'audit n'a pas tourné ;
- l'audit a échoué ;
- l'audit a tourné et n'a rien trouvé.

#### Proposition

États séparés :

| État | Condition | UI |
|---|---|---|
| No audit file | 404 sur `audit-results.json` | "Run /sg-code-audit" |
| Invalid audit | JSON invalide ou schéma incomplet | erreur lisible |
| Zero bug | `summary.total_bugs === 0` ou `bugs.length === 0` | "Audit complete, 0 bug found" |
| Bugs found | `bugs.length > 0` | dashboard actuel |

#### Critères d'acceptation

- `bugs: []` affiche un audit complet à 0 bug.
- L'onglet Code Audit ne montre pas "No audit data found" si un fichier valide
  existe.

### 6. Ajouter un champ `agents[]` explicite

#### Constat

L'onglet Agents déduit les agents depuis le format des IDs de bugs. Si les IDs
ne suivent pas le pattern attendu, le compteur peut être présent mais les cartes
agent restent peu informatives.

#### Proposition

Ajouter au schéma :

```json
"agents": [
  {
    "id": "z1",
    "label": "Zone 1",
    "status": "completed",
    "files_audited": 9,
    "bugs_found": 1,
    "duration_ms": 120000,
    "paths": ["scripts/*.sh", "README.md"]
  }
]
```

#### Critères d'acceptation

- L'onglet Agents fonctionne sans dépendre du format des IDs de bugs.
- Un audit à 0 bug peut quand même afficher les agents et fichiers audités.

### 7. Corriger le compteur de bugs par route

#### Constat

La route `/` peut matcher trop largement et compter tous les bugs.

#### Proposition

Option A : accepter `bug_count` directement dans `impacted_ui_routes`.

```json
{"route": "/", "reason": "...", "severity": "high", "bug_count": 3}
```

Option B : ajouter un mapping explicite dans chaque bug :

```json
"impacted_routes": ["/", "/settings"]
```

Éviter le matching implicite par chaîne sur le nom de fichier, surtout pour
`/`.

#### Critères d'acceptation

- `/` ne compte pas tous les bugs par défaut.
- Le compteur de route reste cohérent avec le tableau Bugs filtré.

## Priorité P1 - Modes dry-run et recette des chemins destructifs

### 8. Ajouter `--dry-run` à `sg-visual-fix`

#### Constat

`sg-visual-fix` est précieux mais destructif : il lit les annotations, infère le
bug, modifie le code, reconstruit et capture un état après correction. Il est
difficile de le recetter sans accepter des modifications.

#### Proposition

Ajouter un mode :

```bash
/sg-visual-fix --dry-run visual-tests/_results/fix-manifest.json
```

Comportement :

- lire le manifest ;
- charger les captures ;
- décrire les régions annotées ;
- proposer fichiers suspects ;
- proposer correction envisagée ;
- ne rien modifier ;
- écrire `visual-tests/_results/visual-fix-plan.md`.

#### Critères d'acceptation

- Le dry-run ne modifie aucun fichier source.
- Le plan liste les tests, captures, annotations, fichiers candidats et limites.
- Le mode normal reste inchangé.

### 9. Ajouter des smoke tests officiels de l'interface

#### Constat

La validation actuelle repose sur des tests manuels ou des commandes ad hoc.

#### Proposition

Fournir un script :

```bash
node visual-tests/review-smoke-test.mjs
```

Il devrait vérifier :

- `review.html` se génère ;
- `audit-results.json` est chargé ;
- `visual-results.json` ou fallback est chargé ;
- `Recorded Tests` détecte un manifest ;
- `POST /save-manifest` écrit un fichier ;
- les rapports persona sont générés si `change-reports/*/report.json` existe.

#### Critères d'acceptation

- Le script sort avec code 0 si l'interface minimale fonctionne.
- Le script produit une sortie courte et exploitable.

## Priorité P1 - Recorder

### 10. Éviter les préchecks `npx` non bornés dans `sg-record`

#### Constat

Un précheck du type `npx playwright --version` peut suspendre ou tenter un accès
réseau, surtout hors projet Node.

#### Proposition

Ordre plus sûr :

1. tester `node -e "import('playwright')"` depuis le projet ;
2. tester un binaire local `node_modules/.bin/playwright` ;
3. tester un binaire global si disponible ;
4. sinon afficher une instruction d'installation, sans bloquer ;
5. borner chaque commande avec un timeout.

#### Critères d'acceptation

- Pas de commande `npx` non bornée.
- Un environnement sans Playwright échoue vite avec un message clair.

### 11. Rendre le bootstrap strictement séquentiel

#### Constat

Les copies de fichiers recorder échouent si elles sont lancées avant
`mkdir -p visual-tests/lib visual-tests/manifests`.

#### Proposition

Le runbook doit imposer :

```bash
mkdir -p visual-tests/lib visual-tests/manifests
cp ...
cp ...
```

Éviter explicitement la parallélisation sur ces étapes.

#### Critères d'acceptation

- Un bootstrap depuis zéro ne dépend pas de l'ordre d'exécution du shell agent.
- Relancer le bootstrap est idempotent.

## Priorité P1 - Environnements sandbox Codex / Claude

### 12. Documenter les autorisations nécessaires

#### Constat

Plusieurs actions ShipGuard sont légitimes mais bloquées en sandbox par défaut :

- `agent-browser` écrit son socket dans le home ;
- `node --serve` écoute sur un port local ;
- `curl POST` vers localhost peut être bloqué ;
- `gh api` demande le réseau ;
- `npx` peut demander le réseau ;
- Python peut écrire du cache hors workspace sans `PYTHONPYCACHEPREFIX`.

#### Proposition

Ajouter une section "Sandbox / Codex / Claude" dans les skills :

| Action | Pourquoi | Contournement |
|---|---|---|
| `agent-browser` | socket local | autorisation ou socket configurable dans `/tmp` |
| `build-review --serve` | port local | autorisation, bind 127.0.0.1 |
| `curl POST localhost` | test endpoint | autorisation réseau locale |
| `gh api` | scout | autorisation réseau explicite |
| Python compile | pycache | `PYTHONPYCACHEPREFIX=/tmp/...` |

#### Critères d'acceptation

- Un utilisateur sait quelles autorisations accepter.
- Les erreurs sandbox sont reconnues comme telles dans les runbooks.

## Priorité P2 - Monitoring

### 13. Ajouter un smoke test des endpoints monitor

#### Constat

Les endpoints monitor existent :

- `/api/monitor/audit-start`
- `/api/monitor/agent-update`
- `/api/monitor/status`
- `/api/monitor/audit-complete`

Mais il manque un test de bout en bout simple.

#### Proposition

Ajouter :

```bash
node visual-tests/monitor-smoke-test.mjs
```

Le script :

- démarre ou détecte le serveur ;
- poste un audit factice ;
- poste deux agents factices ;
- vérifie `/status` ;
- poste completion ;
- vérifie que le dashboard peut charger l'état.

#### Critères d'acceptation

- Test sans dépendance externe.
- Aucune écriture hors `_results/audit-monitor.json`.
- Sortie claire en cas d'échec.

## Priorité P2 - Scout et Improve

### 14. Encadrer `sg-scout` en mode offline/dry-run

#### Constat

`sg-scout` dépend de GitHub et du réseau. En sandbox, c'est souvent bloqué au
premier run.

#### Proposition

Modes explicites :

```bash
/sg-scout --dry-run --topic=visual
/sg-scout --offline --from fixtures/scout-repos.json
```

Et production d'un rapport local même si GitHub n'est pas accessible :

```text
visual-tests/_results/scout-report.md
```

#### Critères d'acceptation

- Un dry-run ne crée jamais d'issue.
- Un échec réseau donne une sortie exploitable et non un arrêt opaque.

### 15. Encadrer `sg-improve` avec un vrai mode preview

#### Constat

`sg-improve --dry-run` doit montrer exactement ce qui serait écrit.

#### Proposition

Produire :

```text
.shipguard/preview/learnings.yaml
.shipguard/preview/mistakes.md
.shipguard/preview/upstream-proposals.md
```

ou, si on ne veut aucune écriture :

```text
visual-tests/_results/sg-improve-preview.md
```

#### Critères d'acceptation

- Le dry-run détaille les fichiers cibles.
- Le mode réel crée un snapshot avant écriture.
- Le rollback peut être testé sur un fixture.

## Proposition de roadmap courte

### Sprint 1 - Robustesse dashboard

1. `visual-results.json`
2. `impacted_ui_routes` normalisé
3. état audit zéro bug
4. bind `127.0.0.1`
5. path traversal avec `resolve` / `relative`

### Sprint 2 - Testabilité

1. `sg-visual-fix --dry-run`
2. `review-smoke-test.mjs`
3. `monitor-smoke-test.mjs`
4. bootstrap recorder séquentiel
5. préchecks sans `npx` non borné

### Sprint 3 - Agentic workflow

1. `agents[]` explicite
2. bug count par route fiable
3. modes scout offline/dry-run mieux formalisés
4. improve preview / rollback fixture
5. documentation sandbox Codex / Claude

## Tests de non-régression suggérés

### Dashboard sans Markdown

- Supprimer ou renommer `report.md`.
- Garder `visual-results.json`.
- Vérifier que Visual Tests affiche les statuts.

### Audit zéro bug

```json
{
  "summary": {"total_bugs": 0},
  "bugs": []
}
```

Vérifier que l'UI affiche "0 bug" et pas "No audit data found".

### Routes impactées

Tester les trois cas :

- seulement `impacted_ui_routes` ;
- seulement `impacted_routes` ;
- les deux champs.

### Sécurité serveur

Tester :

- `GET /../secret.txt` -> 403 ;
- dossier frère au préfixe similaire -> 403 ;
- host par défaut -> `127.0.0.1`.

### Recorder sans Playwright

Dans un projet sans `node_modules` :

- le précheck doit échouer vite ;
- le message doit indiquer quoi installer ;
- aucune commande ne doit rester suspendue.

## Note finale

La recette montre que ShipGuard est déjà utile comme cockpit de validation. Les
améliorations ci-dessus visent surtout à rendre le plugin plus robuste quand il
est utilisé hors du dépôt d'origine, avec des agents différents, des rapports
localisés, et des environnements sandboxés.
