# Rapport ShipGuard process-check - 2026-06-30

Mode : `hybrid`, depuis `audit-results.json` et les serveurs locaux actifs,
sans correction et sans baseline before.

## Synthèse

- Unités vérifiées : 4
- Observations raisonnées : 2
- Observations mesurées : 3
- Changements de comportement : 0, car aucun correctif n'a été appliqué
- Surprises : 0

## Observations mesurées

| Unité | Requête | Résultat | Observation |
|---|---|---|---|
| `visual-tests/build-review.mjs --serve` | `GET http://127.0.0.1:8888/` | HTTP 200, 156443 bytes, 0.008063 s | La review reconstruite est servie. |
| `visual-tests/build-review.mjs --serve` | `GET http://127.0.0.1:8888/visual-results.json` | HTTP 200, 13061 bytes, 0.006733 s | Le JSON canonique reste disponible après l'ajout du manifest enregistré. |
| `scripts/serve-local.sh 8001` | `GET http://127.0.0.1:8001/` | HTTP 200, 10800 bytes, 0.014038 s | Le serveur statique est disponible pour les ponts visuels. |

## Observations raisonnées

| Unité | Verdict | Preuve | Observation |
|---|---|---|---|
| `matrice-slide-ai/publish_variant.py` | unchanged | reasoned | Le comportement reste raisonné ; le mesurer impliquerait une publication locale contrôlée. |
| `matrice-slide-ai/build.py` | unchanged | reasoned | Le confinement des chemins d'image reste à mesurer avec un fixture contrôlé. |

## Limites

- Aucune baseline before réelle n'a été construite ; `--mode=execute` reste
  nécessaire pour un before/after entièrement mesuré.
- `scripts/validate_variant.sh` n'a pas été mesuré pour éviter une exécution
  `npx` réseau avec paquets non verrouillés.
- `visual-tests/_shipguard_static_run.py` n'a pas été relancé dans cet item,
  car le pont `sg-visual-run` est testé séparément.
- Les endpoints POST du monitor et de `save-manifest` ne sont pas couverts par
  cet item.
