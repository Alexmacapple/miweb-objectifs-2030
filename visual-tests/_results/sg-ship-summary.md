# Synthèse sg-ship - MiWeb Objectifs 2030

Date : 2026-06-30

Mode visé : `quick --all --report-only --mode=reason`

Mode réellement vérifié dans cette session : orchestration manuelle des lanes
ShipGuard 2.3.7 disponibles dans Codex, sans correction et sans commit. Le
slash `sg-ship` est un skill agentique, pas un binaire callable directement
depuis le shell.

## Lanes exécutées ou reprises

| Lane | Statut | Artefact |
|---|---|---|
| `sg-code-audit` | artefact existant repris en report-only | `visual-tests/_results/audit-results.json` |
| `sg-process-check` | vérifié en mode `hybrid` pendant l'item 4 | `visual-tests/_results/process-results.json` |
| `sg-visual-run --all` | relancé sur 28 routes | `visual-tests/_results/report.md` |
| `sg-visual-review` | rebuild OK et serveur 8888 actif | `http://127.0.0.1:8888/` |

## Résultats consolidés

- Code audit : 19 constats, dont 4 high, 11 medium, 4 low.
- Process check : 4 unités, 3 observations mesurées, 2 observations
  raisonnées, 0 surprise.
- Visual run complet : 28 tests exécutés, 28 réussis, 0 échec, 0 erreur.
- Review : 28 manifests, 28 captures appariées, 2 manifests enregistrés,
  persona reports générés.

## Décisions de sûreté

- Aucune correction `sg-visual-fix` appliquée.
- Aucun mode `sg-process-check --mode=execute` lancé.
- Aucun scan GitHub réel, aucune issue GitHub, aucune écriture `.shipguard/`.
- Aucun commit.

## Points à regarder pour Loïc

1. `sg-record` écrit un manifest si le navigateur est fermé, mais le clic
   `Check` / `Stop` dans la barre n'a pas été automatisable dans cette session.
2. Monitor : `agent-update` avec `id` seul crée encore `agents.undefined`.
3. Visual bridges : la route `/` doit être traitée comme cas spécial, sinon un
   matching par préfixe relance toute la suite.
4. Après un sous-run visuel ciblé, `report.md` reflète la sous-suite, mais
   `visual-results.json` et la review peuvent rester ou revenir sur un résumé
   global 28/28.

## Premier point à regarder

Le blocage monitor `agents.undefined` est le plus reproductible et le plus
direct à corriger côté API. Le deuxième sujet est la traçabilité des sous-runs
visuels ciblés dans `visual-results.json`.
