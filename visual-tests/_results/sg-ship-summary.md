# Synthèse sg-ship - MiWeb Objectifs 2030

Date : 2026-06-29

Mode : `quick --all --report-only --mode=reason`

## Lanes exécutées

| Lane | Statut | Artefact |
|---|---|---|
| `sg-code-audit` | exécuté en 5 zones report-only | `visual-tests/_results/audit-results.json` |
| `sg-process-check` | exécuté en simulation raisonnée depuis audit | `visual-tests/_results/process-results.json` |
| `sg-visual-run` | exécuté sur 28 routes | `visual-tests/_results/report.md` |
| `sg-visual-review` | interface HTML servie | `http://localhost:8888/` |

## Résultats consolidés

- Code audit : 19 constats, dont 4 high, 11 medium, 4 low.
- Process check : 5 unités raisonnées, 0 mesure, 0 correction.
- Visual run : 28 tests exécutés, 28 réussis, 0 échec, 0 erreur.
- Review : Code Audit, Visual Tests, Recorded Tests et persona reports visibles.

## Décisions de sûreté

- Aucune correction `sg-visual-fix` appliquée.
- Aucun commit.
- Les rapports et manifests produits restent des artefacts locaux non suivis.

## Premier point à regarder

Le sujet le plus structurant est la publication racine : plusieurs générateurs
de variantes peuvent encore réécrire l'accueil avec un catalogue local obsolète,
alors que le dépôt documente que la publication racine doit passer par
`publish_variant.py`.
