# sg-scout dry-run - 2026-06-29

Mode : `--topic=visual --dry-run`

## Préconditions

- `gh auth status` : connecté au compte GitHub `Alexmacapple`.
- Première tentative `gh api` dans le sandbox : échec réseau.
- Relance avec autorisation réseau : succès.

## Recherche exécutée

Query :

```text
"visual regression" AI screenshot testing
```

Résultats principaux :

| Repo | Signal |
|---|---|
| `marmutapp/superbased-codex-plugin` | plugin Codex orienté screenshot, OCR, visual testing |
| `marmutapp/superbased-claude-code-plugin` | variante Claude Code du même outillage |
| `ujjwaldahiya399/visual-regression-testing-with-AI-diff-analysis` | classification LLM des diffs screenshot |

## Lecture légère

README détecté pour `ujjwaldahiya399/visual-regression-testing-with-AI-diff-analysis` :

```text
https://raw.githubusercontent.com/ujjwaldahiya399/visual-regression-testing-with-AI-diff-analysis/master/README.md
```

## Proposition sèche

Technique à explorer : classification des diffs visuels par LLM pour distinguer
bug réel, changement intentionnel et bruit de rendu.

Adaptation ShipGuard possible :

- ajouter une étape optionnelle à `sg-visual-run` après capture ;
- comparer une capture courante à une baseline si disponible ;
- produire une classe `bug | intended-change | rendering-noise | inconclusive` ;
- afficher cette classe dans `sg-visual-review`.

Statut : dry-run uniquement, aucune issue GitHub créée, aucun fichier écrit dans
le dépôt ShipGuard amont.
