# sg-improve dry-run - 2026-06-29

Mode : `--dry-run`

## Sources lues

- `visual-tests/_results/report.md`
- `visual-tests/_results/audit-results.json`
- `visual-tests/_results/process-report.md`
- `visual-tests/_results/shipguard-postmortem.md`
- captures et interface HTML sous `visual-tests/_results/`

## Apprentissages locaux proposés

À écrire dans `.shipguard/learnings.yaml` lors d'un run non dry-run :

```yaml
learnings:
  - id: miweb-root-publication
    scope: miweb-objectifs-2030
    pattern: "Les build.py de variantes ne doivent pas publier l'accueil racine."
    severity: high
    check: "Chercher render_root() et écritures vers REPO_ROOT/index.html hors publish_variant.py."
  - id: shipguard-sandbox-agent-browser
    scope: codex-harness
    pattern: "agent-browser nécessite un socket hors sandbox dans ~/.agent-browser."
    severity: medium
    check: "Relancer sg-visual-run avec autorisation ou configurer un socket dans /private/tmp."
  - id: shipguard-review-report-schema
    scope: shipguard-adapter
    pattern: "sg-visual-review dépend des identifiants techniques dans report.md."
    severity: medium
    check: "Conserver pages/<slug> dans la première colonne ou générer un results JSON canonique."
```

## Mistakes proposées

À écrire dans `.shipguard/mistakes.md` lors d'un run non dry-run :

- Ne pas présenter un audit accessibilité comme preuve ShipGuard.
- Ne pas franciser la colonne d'identifiant du rapport Markdown sans vérifier
  le parser `sg-visual-review`.
- Ne pas tester `POST /save-manifest` depuis le sandbox sans autorisation
  réseau explicite.

## Propositions amont ShipGuard

- `sg-visual-review` : consommer `impacted_ui_routes` en plus de
  `impacted_routes`.
- `sg-visual-review` : afficher un audit valide avec `bugs: []` comme "0 bug"
  plutôt que "No audit data found".
- `build-review.mjs --serve` : binder explicitement sur `127.0.0.1`.
- `build-review.mjs` : remplacer le test `startsWith(RESULTS_DIR)` par une
  vérification de chemin résolu et confiné.
- `sg-visual-run` : produire un JSON de résultats canonique, moins fragile que
  le parsing Markdown.

## Statut

Dry-run uniquement : aucun snapshot `.shipguard/history/`, aucune écriture
`.shipguard/`, aucune issue GitHub.
