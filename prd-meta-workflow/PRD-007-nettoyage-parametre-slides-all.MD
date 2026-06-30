# PRD-007 : Nettoyage du paramètre `slides=all`

**Statut** : Brouillon
**Date** : 2026-07-01
**Auteur** : Alex
**Source** : ShipGuard `SG-Z3-002`, inspection de `miweb-objectifs-2030-v1/build.py`, recherche croisée dans les générateurs de variantes

---

## Vision

Le quoi : l'URL du diaporama doit refléter le mode d'affichage courant. Le mode
« toutes slides » est un état temporaire demandé par `?slides=all`; dès que
l'utilisateur revient à une slide unique, ce paramètre doit être retiré.

Le pourquoi : le diaporama utilise l'URL comme contrat de reprise, de partage et
d'historique navigateur. Si `?slides=all` reste dans l'URL après retour à une
slide unique, un rechargement ou un partage réactive un mode que l'interface ne
montre plus. Le correctif doit donc nettoyer seulement le paramètre de mode
obsolète, sans effacer les autres paramètres utiles comme `projection=1`.

Le comment : renvoyé au Plan d'implémentation Superpowers.

## Exemple bout-en-bout (projeté)

Un utilisateur ouvre :

```text
/miweb-objectifs-2030-v1/?slides=all#diaporama
```

La page affiche toutes les slides, le bouton annonce « Revenir au mode
diaporama » et le focus est placé sur le contrôle attendu.

L'utilisateur clique sur « Revenir au mode diaporama » ou sur une entrée du
sommaire pointant vers `#slide-03`.

Résultat attendu :

```text
/miweb-objectifs-2030-v1/#slide-03
```

Si l'URL contenait aussi `?projection=1`, le résultat attendu conserve ce
paramètre et retire seulement `slides=all` :

```text
/miweb-objectifs-2030-v1/?projection=1#slide-03
```

---

## Contexte

ShipGuard signale `SG-Z3-002` sur `miweb-objectifs-2030-v1/build.py:402` :
`setUrl()` reconstruit l'URL avec `window.location.search`. Ce comportement
conserve `?slides=all` quand `showSlide()` sort du mode toutes slides.

L'inspection locale montre que le même motif existe dans la matrice et dans les
variantes autonomes. La V1 est la version la plus critique côté usage, mais la
cause est commune.

## Problème

Le code mélange deux responsabilités :

- `isAllSlidesRequested()` lit `?slides=all` comme demande initiale ;
- `setUrl()` réutilise ensuite toute la query string courante, même quand
  l'interface vient de quitter ce mode.

Le résultat est une incohérence entre l'état visible et l'état partageable :
l'utilisateur voit une slide unique, mais l'URL promet encore toutes les
slides.

## Solution

Ajouter un helper d'URL pour le mode slide unique :

- calculer le hash cible avec `slideHash(index)` ;
- copier les paramètres courants avec `URLSearchParams` ;
- supprimer le paramètre `slides` ;
- reconstruire l'URL avec les autres paramètres conservés ;
- utiliser ce helper dans `setUrl()`.

La correction doit être portée dans `matrice-slide-ai/build.py` et propagée aux
9 variantes autonomes existantes. Les pages générées doivent ensuite être
rebuildées localement pour que les `index.html` publiés contiennent le nouveau
script et le nouveau hash CSP.

## Options évaluées

### Option A (retenue) : nettoyer `slides` dans le helper d'URL slide unique

**Avantages** :
- corrige toutes les sorties vers une slide unique : bouton, sommaire, clavier,
  projection et historique ;
- conserve les autres paramètres utiles ;
- centralise le comportement dans `setUrl()` ;
- reste compatible avec la structure actuelle des générateurs autonomes.

**Inconvénients** :
- impose de propager le même changement dans 10 `build.py` ;
- nécessite un rebuild des `index.html` générés.

### Option B : changer seulement le clic du bouton « toutes slides »

**Avantages** :
- modification plus petite dans le chemin utilisateur signalé ;
- moins de risque de toucher aux autres modes.

**Inconvénients** :
- ne corrige pas la sortie via sommaire, clavier, projection ou historique ;
- laisse `setUrl()` conserver un état obsolète ;
- ne protège pas les futures variantes générées depuis la matrice.

### Option C : supprimer toute la query string lors d'un retour à une slide

**Avantages** :
- corrige `slides=all` avec peu de code ;
- rend les URLs de slide très simples.

**Inconvénients** :
- supprime aussi `projection=1` et tout futur paramètre légitime ;
- transforme une correction ciblée en changement de contrat plus large ;
- risque une régression sur les liens de présentation plein écran.

## Décision

Retenir l'option A.

Le bug vient d'un paramètre de mode devenu périmé, pas d'une mauvaise query
string en général. La correction doit donc retirer seulement `slides` lors du
retour à une slide unique et préserver le reste de l'URL.

Plan associé :

`docs/superpowers/plans/2026-07-01-nettoyage-slides-all.md`

## Plan d'implémentation

1. Isoler ou commiter séparément les ZIPs déjà reconstruits par `PRD-006`.
2. Ajouter les tests TDD sur V1 et sur la matrice pour exiger la suppression de
   `slides` dans l'URL de slide unique.
3. Observer les tests rouges avant correction.
4. Ajouter un helper d'URL dans la matrice et les 9 variantes autonomes.
5. Rebuild les 9 variantes pour régénérer les `index.html`.
6. Lancer les suites `unittest`, les validations standard et un smoke navigateur
   sur V1.
7. Commit local sans push, en séparant les artefacts ZIP de tout changement de
   navigation.

## Métriques de succès

- `miweb-objectifs-2030-v1/tests/test_site_contracts.py` échoue avant correction
  puis passe après correction.
- `matrice-slide-ai/tests/test_site_contracts.py` échoue avant correction puis
  passe après correction.
- Les 10 `build.py` contiennent le helper de nettoyage de `slides`.
- `rg 'window\\.location\\.search\\}\\$\\{hash\\}' --glob build.py .` ne trouve plus
  l'ancien assemblage d'URL.
- Les 9 suites `unittest` de variantes passent.
- `python3 -m unittest discover -s matrice-slide-ai/tests` passe.
- `scripts/validate_variant.sh` passe sur les 9 variantes.
- Le smoke navigateur local sur V1 prouve que `?slides=all#diaporama` devient
  une URL de slide unique sans paramètre `slides`.
- Le commit de code ne mélange pas les ZIPs de `PRD-006` avec la correction de
  navigation.

## Changelog

| Date | Auteur | Changement |
|------|--------|------------|
| 2026-07-01 | Alex + Codex | Création du PRD |
