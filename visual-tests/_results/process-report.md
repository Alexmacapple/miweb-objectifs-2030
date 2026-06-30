# Rapport ShipGuard process-check - 2026-06-29

Mode : `reason`, depuis `audit-results.json`, sans correction et sans mesure
before/after.

## Synthèse

- Unités vérifiées : 5
- Observations raisonnées : 5
- Observations mesurées : 0
- Changements de comportement : 0, car aucun correctif n'a été appliqué
- Surprises : 0

## Observations

| Unité | Verdict | Preuve | Observation |
|---|---|---|---|
| `scripts/validate_variant.sh` | unchanged | reasoned | validation dépendante de paquets npm non verrouillés |
| `matrice-slide-ai/publish_variant.py` | unchanged | reasoned | publication possible d'artefacts HTML périmés |
| `matrice-slide-ai/build.py` | unchanged | reasoned | chemin image non confiné à confirmer par fixture |
| `visual-tests/build-review.mjs --serve` | unchanged | reasoned | serveur de revue et POST `/save-manifest` à durcir |
| `visual-tests/_shipguard_static_run.py` | unchanged | reasoned | faux positif possible sur page d'erreur non blanche |

## Limites

Ce passage ne remplace pas une mesure. Il documente le comportement attendu à
partir de l'audit statique et sert de pont vers `sg-visual-run` et
`sg-visual-review`.
