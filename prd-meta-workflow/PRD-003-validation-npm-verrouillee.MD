# PRD-003 : Validation npm verrouillée des variantes

**Statut** : Brouillon
**Date** : 2026-06-30
**Auteur** : Alex
**Source** : recette ShipGuard 2.3.7, bug `SG-Z1-001`, lecture de `scripts/validate_variant.sh`

---

## Vision

Le quoi : la validation canonique d'une variante doit exécuter des validateurs
npm installés localement et verrouillés par un lockfile.

Le pourquoi : `scripts/validate_variant.sh` est un garde avant publication. S'il
télécharge la dernière version de validateurs au moment du contrôle, la preuve
change sans changement du dépôt. Le mécanisme robuste est de faire entrer les
validateurs dans la chaîne de dépendances versionnée : mêmes versions, mêmes
résolutions, même commande.

Le comment : renvoyé au Plan d'implémentation.

## Exemple bout-en-bout (projeté)

Un agent prépare une nouvelle variante `nouveau-jeu/`, lance son build, puis
exécute :

```bash
scripts/validate_variant.sh nouveau-jeu
```

Le script lance d'abord les tests Python du jeu. Il lance ensuite
`html-validate` et `vnu-jar` depuis les dépendances npm locales du dépôt.

Si les dépendances ne sont pas installées, la commande échoue avec un message
actionnable qui demande `npm ci`, au lieu de télécharger silencieusement un
paquet depuis npm.

Si le dépôt est installé proprement avec `npm ci`, les validateurs exécutés sont
ceux du `package-lock.json`. Deux machines qui utilisent le même commit
exécutent donc les mêmes versions.

---

## Contexte

Le script [scripts/validate_variant.sh](../scripts/validate_variant.sh) contient
aujourd'hui :

```bash
npx --yes html-validate ...
npx --yes vnu-jar ...
```

À la racine du dépôt, il n'existe pas de `package.json` ni de lockfile qui
verrouille ces deux validateurs. Le seul `package.json` existant est sous
`visual-tests/` et concerne Playwright.

ShipGuard a remonté `SG-Z1-001` : la validation de publication exécute des
paquets npm non verrouillés.

## Problème

`npx --yes` peut télécharger et exécuter la version courante publiée sur npm.
Cette pratique pose deux problèmes :

- reproductibilité faible : le même commit peut être validé avec des versions
  différentes des outils ;
- surface supply-chain inutile : une commande de validation exécute du code
  récupéré au moment du contrôle.

Le risque est particulièrement gênant parce que `validate_variant.sh` est la
commande canonique documentée pour vérifier un jeu avant publication.

## Solution

Créer une chaîne npm racine dédiée aux validateurs HTML :

- ajouter un `package.json` racine minimal, limité aux métadonnées utiles et
  aux `devDependencies` nécessaires ;
- déclarer `html-validate` et `vnu-jar` en `devDependencies` avec versions
  verrouillées par `package-lock.json` ;
- remplacer les appels `npx --yes` par des appels directs aux exécutables
  locaux `node_modules/.bin/html-validate` et `node_modules/.bin/vnu-jar` ;
- vérifier explicitement la présence de ces exécutables avant la validation
  HTML, avec un message d'erreur qui demande `npm ci` si les dépendances sont
  absentes ;
- documenter `npm ci` comme prérequis quand les dépendances ne sont pas encore
  installées.

## Options évaluées

### Option A (retenue) : dépendances npm racine avec lockfile

**Avantages** :
- rend la validation reproductible entre machines ;
- évite le téléchargement implicite pendant la validation ;
- s'intègre aux pratiques standard npm (`npm ci`) ;
- permet de faire évoluer les validateurs par diff explicite du lockfile.

**Inconvénients** :
- ajoute `package.json` et `package-lock.json` à la racine ;
- impose une étape d'installation npm avant la validation complète ;
- le lockfile peut être volumineux et devra être maintenu.

### Option B : versions explicites dans `npx package@version`

**Avantages** :
- changement minimal du script ;
- pas de lockfile racine.

**Inconvénients** :
- continue à télécharger et exécuter du code au moment de la validation ;
- ne verrouille pas toute l'arborescence transitive comme un lockfile ;
- reste dépendant du registre npm à chaque exécution sans cache local.

### Option C : supprimer les validateurs npm du script canonique

**Avantages** :
- retire le risque supply-chain npm de la validation ;
- garde une commande Python simple.

**Inconvénients** :
- réduit la couverture HTML avant publication ;
- dégrade le rôle de `validate_variant.sh` comme garde de qualité ;
- déplace le problème vers des validations manuelles ou CI moins visibles.

## Décision

Retenir l'option A : le dépôt doit posséder une chaîne npm racine verrouillée
pour les validateurs HTML utilisés par `scripts/validate_variant.sh`.

Le script ne doit plus utiliser `npx --yes` pour les validateurs de publication.
Il doit échouer clairement si les dépendances locales ne sont pas installées.
Les documents actifs qui mentionnent encore un accès réseau `npx` doivent être
alignés sur ce nouveau contrat pour éviter qu'un agent réintroduise l'ancien
chemin.

## Plan d'implémentation

1. Ajouter un test ou contrôle scripté qui échoue si
   `scripts/validate_variant.sh` contient encore `npx --yes` pour
   `html-validate` ou `vnu-jar`.
2. Ajouter un `package.json` racine minimal avec dépendances de développement
   pour `html-validate` et `vnu-jar`, sans créer de second chemin de validation
   par scripts npm.
3. Générer et committer `package-lock.json` avec `npm install --package-lock-only`
   ou une commande équivalente contrôlée.
4. Modifier `scripts/validate_variant.sh` pour appeler les validateurs locaux
   via `node_modules/.bin/html-validate` et `node_modules/.bin/vnu-jar`, sans
   téléchargement implicite.
5. Vérifier le comportement quand `node_modules` est absent : message clair
   demandant `npm ci`.
6. Mettre à jour les documents actifs qui décrivent encore `npx` ou
   `npx --yes` comme chemin normal ou comme relance réseau attendue pour
   `html-validate` et `vnu-jar`. Les usages `npx` sans rapport avec la
   validation HTML, comme le tunnel local, restent hors périmètre.
7. Lancer `npm ci`, puis valider au moins une variante représentative avec
   `scripts/validate_variant.sh`.

## Métriques de succès

- `rg "npx --yes (html-validate|vnu-jar)" scripts/validate_variant.sh` ne
  trouve rien.
- `package.json` et `package-lock.json` existent à la racine.
- `npm ci` réussit depuis la racine.
- `scripts/validate_variant.sh` référence les binaires locaux
  `node_modules/.bin/html-validate` et `node_modules/.bin/vnu-jar`.
- `scripts/validate_variant.sh miweb-objectifs-2030-v1` réussit après
  installation des dépendances.
- Sans `node_modules`, le script échoue avant validation npm avec un message qui
  mentionne `npm ci`.
- Les documents actifs `AGENTS.md`, `README.md`,
  `GUIDE-REGENERATION-SITES-SLIDES.md` et `matrice-slide-ai/MODE-OPERATOIRE.md`
  ne présentent plus `npx` ou `npx --yes` comme chemin de validation standard
  pour `html-validate` et `vnu-jar`.
- La suite `python3 -m unittest discover -s matrice-slide-ai/tests` reste
  passante.

## Changelog

| Date | Auteur | Changement |
|------|--------|------------|
| 2026-06-30 | Alex + Codex | Précision du périmètre `npx` et suppression du chemin scripts npm |
| 2026-06-30 | Alex + Codex | Réduction des tensions d'implémentation |
| 2026-06-30 | Alex + Codex | Création du PRD |
