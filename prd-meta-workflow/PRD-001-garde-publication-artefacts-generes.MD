# PRD-001 : Garde de publication des artefacts générés

**Statut** : Implémenté localement
**Date** : 2026-06-30
**Auteur** : Alex
**Source** : recette ShipGuard 2.3.7, bug `SG-Z2-001`, lecture de `matrice-slide-ai/publish_variant.py` et des tests de contrat

---

## Vision

Le quoi : la publication d'un jeu de slides doit refuser tout artefact généré
qui ne correspond plus aux sources courantes du jeu.

Le pourquoi : dans ce dépôt, `slides.json` et `build.py` sont les sources de
vérité. Les fichiers HTML, Markdown et ZIP sont des sorties générées. Si la
publication ne compare que la présence des sorties, elle peut publier une
version ancienne tout en donnant une preuve de validation rassurante. Le bon
mécanisme est de vérifier la cohérence source -> rendu -> fichier publié avant
de modifier l'accueil racine.

Le comment : renvoyé au Plan d'implémentation.

## Exemple bout-en-bout (projeté)

Un agent crée `nouveau-jeu/` avec `matrice-slide-ai/create_variant.py`, complète
`slides.json`, puis lance `python3 nouveau-jeu/build.py`. Les pages générées
sont correctes. Plus tard, une alternative textuelle est corrigée dans
`nouveau-jeu/slides.json`, mais le build n'est pas relancé. L'agent lance
ensuite `python3 matrice-slide-ai/publish_variant.py --slug nouveau-jeu`.

Avec le comportement actuel, `publish_variant.py` vérifie que les fichiers
existent, lance les tests qui rendent les pages en mémoire depuis les sources,
puis peut mettre à jour `published-versions.json` et `index.html` racine alors
que `nouveau-jeu/index.html` sur disque est encore l'ancienne version.

Avec le garde attendu, la publication échoue avant toute écriture racine. Le
message indique que les pages générées sont périmées et demande de relancer
`python3 nouveau-jeu/build.py`. Après rebuild, la même commande de publication
passe et l'accueil racine pointe vers un jeu cohérent.

---

## Contexte

La procédure active du dépôt impose un flux explicite :

1. modifier les sources du jeu ;
2. lancer le `build.py` du jeu ;
3. vérifier le jeu ;
4. publier avec `matrice-slide-ai/publish_variant.py`.

`publish_variant.py` est la seule commande autorisée à modifier
`published-versions.json` et `index.html` racine. Son rôle est donc de refuser
un jeu non vérifiable avant d'écrire la publication.

La recette ShipGuard a remonté `SG-Z2-001` : `publish_variant.py` peut publier
une variante dont les pages générées sont périmées. La lecture du code confirme
le risque pour les pages HTML et Markdown : les tests de contrat rendent le
contenu attendu en mémoire depuis `slides.json` et `build.py`, sans comparer ce
rendu aux fichiers générés sur disque.

## Problème

`verify_variant()` vérifie l'existence de `index.html`, `alternatives.html`,
`accessibilite.html`, `slides.json` et du ZIP, puis lance les tests du jeu.
Cette validation ne garantit pas que les fichiers générés sur disque
correspondent aux sources courantes.

Le risque concret est une publication racine correcte en apparence, mais qui
pointe vers des pages de variante anciennes.

## Solution

Ajouter dans `publish_variant.py` un garde de fraîcheur des artefacts générés.
La publication doit échouer si les sorties générées ne correspondent pas au
rendu actuel produit par le `build.py` du jeu et son `slides.json`.

Le garde doit couvrir au minimum :

- `index.html` ;
- `alternatives.html` ;
- `accessibilite.html` ;
- `alternatives.md`, quand le jeu le génère.

Le ZIP reste couvert par les tests actuels qui comparent les images courantes
avec l'archive. Si cette couverture varie selon les jeux, le plan
d'implémentation devra le signaler.

## Contrat d'implémentation

### Fonction cible

Ajouter une fonction dédiée dans `matrice-slide-ai/publish_variant.py` :

```python
def assert_generated_outputs_fresh(target: Path) -> None:
    ...
```

Cette fonction est appelée par `verify_variant()` après la vérification de
présence des fichiers et avant le retour du `target`. Elle ne doit écrire aucun
fichier.

### Sorties à comparer

Comparer strictement les sorties textuelles suivantes quand elles existent ou
quand le générateur sait les produire :

| Fichier sur disque | Rendu attendu |
|--------------------|---------------|
| `index.html` | `build.render_v1_index(slides)` |
| `alternatives.html` | `build.render_alternatives(slides)` |
| `accessibilite.html` | `build.render_accessibility()` |
| `alternatives.md` | `build.render_markdown(slides)` |

`alternatives.md` reste optionnel pour compatibilité avec les jeux qui ne le
génèrent pas encore. S'il existe sur disque et que `render_markdown` existe, il
doit être comparé.

### Méthode de comparaison

La comparaison est stricte, en texte UTF-8 :

- pas de normalisation HTML ;
- pas de correction automatique ;
- pas de tolérance sur les différences de contenu ;
- pas de rebuild implicite.

Une différence signifie que le fichier généré sur disque n'est plus la sortie
exacte des sources courantes.

### Compatibilité historique

Le garde cible d'abord les jeux issus de la matrice récente, c'est-à-dire les
jeux dont le `build.py` expose les fonctions listées ci-dessus. Pour un jeu
historique qui ne respecte pas ce contrat, la publication doit échouer avec un
message explicite plutôt que supposer que le jeu est frais.

Si cette règle révèle une divergence sur un jeu existant, la correction attendue
est de relancer le `build.py` du jeu ou d'aligner son générateur, pas de
contourner le garde dans `publish_variant.py`.

### Message d'erreur

Le message d'erreur doit nommer les fichiers périmés et la commande attendue :

```text
jeu non vérifiable : artefacts générés périmés pour <slug> :
- index.html
- alternatives.html
Relancer python3 <slug>/build.py avant publication.
```

### Cas explicitement hors périmètre

- Ne pas relancer automatiquement `build.py`.
- Ne pas réécrire le dossier de jeu depuis `publish_variant.py`.
- Ne pas corriger les HTML générés à la main.
- Ne pas comparer les PNG octet par octet dans ce nouveau garde : le ZIP reste
  couvert par les tests existants du jeu.

## Options évaluées

### Option A (retenue) : refuser les artefacts périmés dans `publish_variant.py`

**Avantages** :
- conserve le rôle de `publish_variant.py` comme garde de publication ;
- évite les modifications silencieuses du dossier de jeu ;
- produit une erreur claire avant toute écriture racine ;
- s'applique aux futurs jeux créés depuis la matrice.

**Inconvénients** :
- demande d'importer ou d'exécuter le `build.py` du jeu pour obtenir le rendu
  attendu ;
- peut révéler des divergences historiques dans des jeux existants ;
- impose de maintenir une comparaison stable des sorties textuelles.

### Option B : relancer automatiquement le build avant publication

**Avantages** :
- corrige automatiquement les artefacts périmés ;
- réduit le nombre d'étapes manuelles pour l'opérateur.

**Inconvénients** :
- change le dossier de jeu pendant une commande de publication ;
- masque l'oubli de rebuild au lieu de le rendre observable ;
- peut changer des fichiers non relus juste avant publication ;
- augmente le périmètre de `publish_variant.py`, qui ne devrait publier qu'un
  jeu déjà généré et vérifié.

### Option C : garder la procédure documentaire sans garde technique

**Avantages** :
- aucun changement de code ;
- aucune friction supplémentaire dans le flux actuel.

**Inconvénients** :
- ne corrige pas le défaut détecté ;
- dépend entièrement de la discipline humaine ou agentique ;
- laisse possible une publication racine incohérente.

## Décision

Retenir l'option A : `publish_variant.py` doit refuser les artefacts générés
périmés.

Le choix est cohérent avec la règle du dépôt : les sources sont modifiées, le
jeu est généré, puis la publication vérifie et écrit uniquement l'accueil
racine. La commande de publication ne doit pas reconstruire silencieusement le
jeu.

## Plan d'implémentation

1. Ajouter un test de non-régression dans
   `matrice-slide-ai/tests/test_matrix_workflow.py` :
   `create_variant`, `build.py`, modification contrôlée de `slides.json`,
   puis `publish_variant.py --slug jeu-test` doit échouer sans modifier
   `published-versions.json` ni `index.html` racine.
2. Ajouter dans `publish_variant.py` la fonction
   `assert_generated_outputs_fresh(target: Path)`.
3. Charger le `build.py` du jeu cible, lire `slides.json`, rendre les pages
   attendues et comparer strictement avec les fichiers sur disque.
4. Produire un message d'erreur actionnable, par exemple :
   `jeu non vérifiable : artefacts générés périmés pour <slug>`.
5. Vérifier que le cas heureux existant `create -> build -> publish` reste
   passant.
6. Lancer les tests de la matrice et, si nécessaire, les tests du jeu concerné.

## Métriques de succès

- Un test reproduisant `build -> modification de slides.json -> publish sans
  rebuild` échoue avant correction et passe après correction.
- `publish_variant.py` ne change pas `published-versions.json` ni
  `index.html` racine quand les artefacts générés sont périmés.
- Le test existant `test_publish_variant_updates_catalog_and_root_after_build`
  reste passant.
- La commande `python3 -m unittest discover -s matrice-slide-ai/tests` passe.
- Le message d'erreur contient le slug du jeu ou la commande de rebuild à
  exécuter.
- Un jeu dont le générateur ne fournit pas les fonctions attendues échoue avec
  un message explicite au lieu d'être publié sans preuve de fraîcheur.
- `publish_variant.py` n'écrit aucun fichier dans le dossier de jeu.

## Changelog

| Date | Auteur | Changement |
|------|--------|------------|
| 2026-07-01 | Alex + Codex | Alignement documentaire avec l'implémentation locale |
| 2026-06-30 | Alex + Codex | Ajout du contrat d'implémentation détaillé |
| 2026-06-30 | Alex + Codex | Création du PRD |
