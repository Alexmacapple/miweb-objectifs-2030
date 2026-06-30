# ShipGuard - note de reprise prochaine session

Date : 2026-06-29

## Statut

Le ZIP horodaté a été préparé pour Loïc :

`/Users/alex/Desktop/shipguard-resultats-loic-2.3.4-20260629-191950.zip`

Il contient notamment :

- `shipguard-postmortem-loic-2.3.4.md`
- `visual-fix-plan.md`
- `scout-report.md`
- `sg-improve-preview.md`
- `fix-manifest.json`
- `visual-tests/fixtures/scout-repos.json`

Le postmortem de référence pour Loïc est :

`visual-tests/_results/shipguard-postmortem-loic-2.3.4.md`

## Décision de pause

On attend le retour de Loïc avant de tester les workflows lourds ou destructifs.

Raison : les tests restants impliquent des modifications locales, du réseau
GitHub, des écritures `.shipguard/` ou un orchestration complète. Les frictions
déjà remontées peuvent être corrigées rapidement et évitent de produire du bruit
dans la suite de la recette.

## Frictions restantes prioritaires remontées à Loïc

- Migration depuis l'ancien adaptateur Codex `shipguard-codex@personal`.
- Diagnostic des smoke tests en sandbox : afficher la vraie erreur
  `listen EPERM`.
- Onglet Agents : badge `5` mais panneau vide avec audit legacy `agents: 5`.
- Auto-traduction Chrome du dashboard : protéger `ShipGuard`, commandes,
  statuts et libellés techniques.
- `favicon.ico` 404.
- Besoin de fixtures/smoke tests déterministes pour :
  - `sg-visual-fix --dry-run`
  - `sg-scout --offline --dry-run`
  - `sg-improve --dry-run`

## Déjà validé en 2.3.4

- Installation officielle `shipguard@shipguard` en 2.3.4 côté Codex.
- Mise à jour Claude en 2.3.4, avec redémarrage requis.
- Dashboard 2.3.4 sur les résultats MiWeb.
- `visual-results.json` canonique : 28 tests, 28 pass, 0 stale.
- `review-smoke-test.mjs` : OK hors sandbox.
- `monitor-smoke-test.mjs` : OK hors sandbox.
- `sg-record` : 13 tests unitaires OK, 11 tests intégration OK.
- Lightbox et annotation UI.
- `POST /save-manifest` et `fix-manifest.json` annoté.
- `sg-visual-fix --dry-run` : plan non destructif généré.
- `sg-scout --offline --dry-run` : rapport preview généré.
- `sg-improve --dry-run` : preview générée.

## À ne pas lancer avant retour de Loïc

- `sg-visual-fix` en mode réel.
- `sg-improve` en mode réel avec écriture `.shipguard/`.
- `sg-scout` complet avec GitHub ou création/commentaire d'issue.
- `sg-ship` complet.
- `sg-process-check --mode=execute`.

## Tests à reprendre après retour de Loïc

1. Réinstaller ou mettre à jour `shipguard@shipguard`.
2. Vérifier si l'ancien `shipguard-codex@personal` doit être désactivé.
3. Relancer les smoke tests officiels.
4. Relancer un `sg-code-audit` post-correctifs pour obtenir le nouveau schéma
   `agent_count` / `agents[]`.
5. Tester `sg-visual-run --from-audit`.
6. Tester `sg-visual-run --from-process`.
7. Tester `sg-record` interactif réel.
8. Tester `sg-visual-fix` réel uniquement sur une zone isolée ou une copie.
9. Tester `sg-improve` réel avec rollback.
10. Tester `sg-ship` comme orchestrateur de bout en bout.

## État Git

Ne rien commit.

État attendu :

```text
?? visual-tests/
```

