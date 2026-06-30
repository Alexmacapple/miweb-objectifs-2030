# PRD-005 : Typage strict de `slides.json`

**Statut** : Brouillon
**Date** : 2026-06-30
**Auteur** : Alex
**Source** : recette ShipGuard 2.3.7, bug `SG-Z2-003`, plan Superpowers `docs/superpowers/plans/2026-06-30-typage-strict-slides-json.md`, lecture de `matrice-slide-ai/build.py`

---

## Vision

Le quoi : `slides.json` doit être validé comme un contrat de données typé avant
tout rendu HTML, Markdown ou ZIP.

Le pourquoi : `slides.json` est la source canonique des slides. Vérifier
seulement la présence des clés laisse passer des valeurs de mauvais type :
chaîne à la place d'un entier, objet à la place d'une chaîne, chaîne à la place
d'une liste. Le rendu peut alors casser tardivement ou produire un résultat
incohérent. Le mécanisme robuste est de refuser les types invalides dans
`load_slides()`, avec une erreur explicite qui nomme `slides.json` et le champ
fautif.

Le comment : renvoyé au Plan d'implémentation.

## Exemple bout-en-bout (projeté)

Un agent met à jour `slides.json` et écrit :

```json
{
  "numero": "1",
  "titre": ["Titre"],
  "image": "assets/slides/slide-01.png",
  "alt": null,
  "description": 42,
  "textes_visibles": "texte au lieu de liste",
  "message": {}
}
```

Le build ne doit pas attendre le rendu HTML pour échouer. Il doit refuser la
slide dès `load_slides()` avec une erreur qui mentionne `slides.json` et le champ
fautif.

Cas valide :

```json
{
  "numero": 1,
  "titre": "Titre valide",
  "image": "assets/slides/slide-01.png",
  "alt": "Alternative valide.",
  "description": "Description valide.",
  "textes_visibles": ["Texte visible valide"],
  "message": "Message valide."
}
```

Ce cas continue à générer le HTML, le Markdown et le ZIP.

---

## Contexte

Dans [matrice-slide-ai/build.py](../matrice-slide-ai/build.py), `load_slides()`
vérifie actuellement que les clés obligatoires sont présentes :

```python
required = {"numero", "titre", "image", "alt", "description", "textes_visibles", "message"}
missing = required - set(slide)
```

Le code utilise ensuite les champs comme s'ils avaient le bon type :

- `int(slide["numero"])` pour calculer l'ordre ;
- `esc(slide["titre"])`, `esc(slide["alt"])`, `esc(slide["description"])` ;
- boucle sur `slide["textes_visibles"]` ;
- insertion de `slide["message"]` dans le HTML et le Markdown.

ShipGuard a remonté `SG-Z2-003` : le contrat `slides.json` ne valide pas les
types des champs.

Comme pour `PRD-004`, les variantes sont autonomes. Le problème concerne donc la
matrice source et les `build.py` déjà copiés dans les variantes actuelles.

## Problème

Le build accepte des données qui respectent la forme minimale des clés, mais pas
le contrat métier attendu.

Risques :

- `numero` en chaîne accepté par conversion implicite ;
- `textes_visibles` en chaîne rendu caractère par caractère ;
- `titre`, `alt`, `description` ou `message` non textuels provoquant une erreur
  tardive ou un rendu incohérent ;
- erreur peu actionnable, car elle apparaît dans le rendu plutôt qu'au chargement
  de `slides.json` ;
- divergence entre futures variantes et variantes autonomes existantes si la
  correction reste seulement dans la matrice.

## Solution

Ajouter un garde de contrat typé dans `load_slides()` :

- `slides` doit être une liste non vide de dictionnaires ;
- `numero` doit être un entier strict et correspondre à l'ordre attendu ;
- `titre`, `image`, `alt`, `description` et `message` doivent être des chaînes
  non vides ;
- `textes_visibles` doit être une liste non vide de chaînes non vides ;
- les erreurs doivent être des `ValueError` contenant `slides.json` et le champ
  fautif ;
- le garde de chemin image `assets/slides/` ajouté par `PRD-004` reste séparé et
  réutilisé ;
- la correction doit être copiée dans les `build.py` autonomes, sans import
  runtime vers `matrice-slide-ai/`.

## Options évaluées

### Option A (retenue) : validation stricte dans `load_slides()`

**Avantages** :
- refuse les données invalides avant tout rendu ;
- produit des erreurs actionnables ;
- protège HTML, Markdown et ZIP avec une seule barrière ;
- reste compatible avec les variantes autonomes.

**Inconvénients** :
- ajoute quelques helpers dans chaque `build.py` autonome ;
- impose de maintenir le même contrat dans les copies existantes.

### Option B : validation seulement dans les tests

**Avantages** :
- peu de code runtime ajouté ;
- détecte les erreurs quand la validation standard est lancée.

**Inconvénients** :
- ne protège pas un build lancé directement ;
- laisse les erreurs apparaître tardivement ;
- ne corrige pas le point signalé dans le code de production.

### Option C : tolérance avec coercition des types

**Avantages** :
- accepte des fichiers `slides.json` plus permissifs ;
- peut réduire les erreurs sur des données générées approximatives.

**Inconvénients** :
- masque les erreurs de source ;
- entretient l'ambiguïté du contrat ;
- peut produire un rendu différent de l'intention réelle.

## Décision

Retenir l'option A : `slides.json` est une source canonique, donc le contrat doit
être strict et vérifié dans `load_slides()`.

Le changement doit préserver l'autonomie des variantes : pas d'import commun vers
`matrice-slide-ai/`.

## Plan d'implémentation

1. Ajouter dans `matrice-slide-ai/tests/test_matrix_workflow.py` un helper qui
   crée une variante temporaire, altère son `slides.json` et lance `build.py`.
2. Ajouter des tests invalides pour :
   - racine `slides.json` non liste ;
   - slide non objet ;
   - `numero` non entier ;
   - `titre`, `image`, `alt`, `description`, `message` non chaînes ;
   - `textes_visibles` non liste ;
   - `textes_visibles` liste vide ou contenant une chaîne vide.
3. Ajouter un test positif avec tous les champs au bon type.
4. Vérifier que les tests invalides échouent avant correction ou échouent avec
   une erreur qui ne respecte pas encore le contrat attendu.
5. Ajouter dans `matrice-slide-ai/build.py` les helpers
   `require_non_empty_string`, `require_visible_texts`,
   `validate_slide_contract` et `validate_slides_root`.
6. Modifier `load_slides()` pour appeler ces helpers avant le garde de chemin
   image.
7. Propager le même garde aux `build.py` autonomes actuels, sans dépendance
   d'exécution vers `matrice-slide-ai/`.
8. Renforcer `matrice-slide-ai/tests/test_site_contracts.py` pour vérifier les
   types sur les slides valides.
9. Lancer la suite matrice.
10. Après validation humaine, rebuild réel des variantes puis validation des
    neuf variantes principales.

## Métriques de succès

- Les tests couvrent les mauvais types listés dans le plan d'implémentation.
- Chaque build invalide échoue avec une erreur contenant `slides.json` et le
  champ fautif.
- Le cas positif avec types valides réussit et produit un HTML contenant
  `src="assets/slides/slide-01.png"`.
- `rg "int\\(slide\\[['\\\"]numero['\\\"]\\]\\)" --glob build.py .` ne trouve
  aucun usage restant : `numero` est déjà un entier validé.
- `rg "matrice[-_]slide[-_]ai|matrice-slide-ai" --glob build.py .` ne trouve
  aucun import ou couplage runtime.
- `python3 -m unittest discover -s matrice-slide-ai/tests` réussit.
- `scripts/validate_variant.sh miweb-objectifs-2030-v1` réussit.
- Les neuf variantes principales passent avec `scripts/validate_variant.sh`
  après rebuild réel validé par Alex.

## Changelog

| Date | Auteur | Changement |
|------|--------|------------|
| 2026-06-30 | Alex + Codex | Création du PRD |
