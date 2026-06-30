# PRD-002 : Publication centralisée de l'accueil racine

**Statut** : Implémenté localement
**Date** : 2026-06-30
**Auteur** : Alex
**Source** : recette ShipGuard 2.3.7, bug `SG-Z3-001`, lecture des `build.py` Objectifs 2030 et de `matrice-slide-ai/publish_variant.py`

---

## Vision

Le quoi : un seul chemin doit être autorisé à publier l'accueil racine du site.
Les `build.py` de variantes génèrent leur propre dossier ; `publish_variant.py`
publie le catalogue global et écrit `index.html` racine.

Le pourquoi : l'accueil racine est une vue de catalogue, pas une sortie locale
d'une variante. Si chaque variante peut le régénérer avec son propre catalogue
figé, le dernier build exécuté gagne et peut effacer des versions déjà publiées.
Le bon mécanisme est de séparer génération locale et publication globale.

Le comment : renvoyé au Plan d'implémentation.

## Exemple bout-en-bout (projeté)

Le dépôt publie neuf jeux dans `published-versions.json` : les versions
Objectifs 2030 V1 à V4, deux offres mutualisées, `span-pan`,
`mise-en-gouvernance-du-span` et `checklist-span-operationnel`.

Un agent corrige ensuite une alternative textuelle dans
`miweb-objectifs-2030-v1/slides.json` et relance :

```bash
python3 miweb-objectifs-2030-v1/build.py
```

Le résultat attendu est limité au dossier V1 : `index.html`,
`alternatives.html`, `accessibilite.html`, `alternatives.md`, `README.md` et le
ZIP de la variante.

Avec le comportement actuel, le script V1 écrit aussi `../index.html` via son
`render_root()` local. Cet accueil ne liste que V1 et le texte indique que
d'autres versions pourront être ajoutées ultérieurement. Les huit autres entrées
publiées peuvent disparaître de l'accueil racine.

Avec le comportement attendu, le build V1 ne touche jamais `../index.html`.
Pour modifier l'accueil racine, l'opérateur lance explicitement :

```bash
python3 matrice-slide-ai/publish_variant.py --slug miweb-objectifs-2030-v1
```

Cette commande lit `published-versions.json`, met à jour l'entrée cible si
nécessaire, puis rend l'accueil racine depuis le catalogue global.

---

## Contexte

Les fichiers `miweb-objectifs-2030-v1/build.py` à
`miweb-objectifs-2030-v4/build.py` contiennent chacun :

```python
(REPO_ROOT / "index.html").write_text(render_root(), encoding="utf-8")
```

Chaque `render_root()` est local à la variante. Dans V1, il ne liste que
`miweb-objectifs-2030-v1/`, alors que `published-versions.json` contient le
catalogue réel publié.

En parallèle, `matrice-slide-ai/publish_variant.py` possède déjà le mécanisme de
publication centralisée : il charge `published-versions.json`, applique
l'entrée de variante, rend l'accueil racine avec ce catalogue, puis écrit
`index.html` racine.

## Problème

Les générateurs de variantes Objectifs 2030 mélangent deux responsabilités :

- générer les pages propres à une variante ;
- publier l'accueil racine global.

Cette confusion crée un risque de régression silencieuse : relancer un build de
variante peut remplacer l'accueil racine courant par un catalogue local obsolète.

## Solution

Retirer l'écriture de `REPO_ROOT / "index.html"` des `build.py` de variantes
Objectifs 2030 et faire de `publish_variant.py` la seule commande autorisée à
publier l'accueil racine.

Le changement doit préserver la génération locale des variantes : les scripts
continuent d'écrire leurs pages, alternatives, README et ZIP dans leur propre
dossier. Ils ne modifient plus le catalogue global ni l'accueil racine.

## Options évaluées

### Option A (retenue) : retirer l'écriture racine des builds de variantes

**Avantages** :
- établit une séparation nette entre build local et publication globale ;
- élimine le risque d'écrasement accidentel de l'accueil racine ;
- s'appuie sur le mécanisme déjà présent dans `publish_variant.py` ;
- rend le workflow plus prévisible pour les agents et les humains.

**Inconvénients** :
- change une habitude possible : relancer `build.py` ne rafraîchit plus
  l'accueil racine ;
- impose de documenter que la publication passe par `publish_variant.py` ;
- peut nécessiter d'ajuster des tests qui attendaient l'écriture racine.

### Option B : conserver l'écriture racine mais lire `published-versions.json`

**Avantages** :
- maintient le comportement où un build de variante rafraîchit aussi l'accueil ;
- réduit le risque de catalogue obsolète si tous les scripts lisent la même
  source.

**Inconvénients** :
- garde deux chemins concurrents pour publier l'accueil racine ;
- oblige à dupliquer ou importer la logique de rendu globale dans chaque
  variante ;
- augmente la surface de régression quand le format du catalogue évolue.

### Option C : garder le comportement actuel et ajouter une consigne

**Avantages** :
- aucun changement de code immédiat ;
- aucune adaptation de tests.

**Inconvénients** :
- ne réduit pas le risque détecté ;
- dépend de la discipline humaine ou agentique ;
- laisse un build local capable de modifier une surface globale sans intention
  explicite.

## Décision

Retenir l'option A : les builds de variantes ne doivent plus écrire l'accueil
racine. La publication de `index.html` racine devient la responsabilité
exclusive de `matrice-slide-ai/publish_variant.py`.

Cette décision est cohérente avec `PRD-001` : une variante est d'abord générée
et vérifiée localement, puis publiée explicitement par une commande qui protège
les écritures globales.

## Plan d'implémentation

1. Ajouter un test de non-régression qui sauvegarde `index.html` racine, lance
   `python3 miweb-objectifs-2030-v1/build.py`, puis vérifie que l'accueil racine
   n'a pas changé.
2. Retirer l'écriture `(REPO_ROOT / "index.html").write_text(...)` dans les
   `build.py` Objectifs 2030 V1 à V4.
3. Vérifier que chaque build continue de générer ses sorties locales attendues.
4. Vérifier que `publish_variant.py --slug <variante>` reste le seul chemin
   d'écriture pour `published-versions.json` et `index.html` racine.
5. Mettre à jour la documentation opérationnelle si elle laisse entendre qu'un
   build de variante publie aussi l'accueil racine.

## Métriques de succès

- Après `python3 miweb-objectifs-2030-v1/build.py`, `git diff -- index.html` ne
  montre aucune modification.
- Les quatre scripts Objectifs 2030 V1 à V4 ne contiennent plus d'écriture vers
  `REPO_ROOT / "index.html"`.
- Chaque script V1 à V4 continue de produire son `index.html`,
  `alternatives.html`, `accessibilite.html`, `alternatives.md`, `README.md` et
  son ZIP local.
- `python3 matrice-slide-ai/publish_variant.py --slug miweb-objectifs-2030-v1`
  reste capable de publier l'accueil racine depuis `published-versions.json`.
- La suite `python3 -m unittest discover -s matrice-slide-ai/tests` passe.

## Changelog

| Date | Auteur | Changement |
|------|--------|------------|
| 2026-07-01 | Alex + Codex | Alignement documentaire avec l'implémentation locale |
| 2026-06-30 | Alex + Codex | Création du PRD |
