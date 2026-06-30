# PRD-006 : ZIP déterministes et liens de téléchargement

**Statut** : Brouillon
**Date** : 2026-06-30
**Auteur** : Alex
**Source** : recette ShipGuard 2.3.7, alertes `G-Z4-002`, `SG-Z4-003`, `SG-Z4-004`, `SG-Z2-004`, plan Superpowers `docs/superpowers/plans/2026-06-30-zip-links-deterministes.md`

---

## Vision

Le quoi : les ZIPs de slides deviennent des artefacts de publication vérifiables
et reproductibles, et chaque lien de téléchargement généré doit pointer vers un
fichier existant.

Le pourquoi : un ZIP est une preuve de publication autant qu'un confort de
téléchargement. Si son contenu ne correspond pas aux images courantes, il ment
sur l'état publié. S'il change à chaque build sans changement de contenu, il
crée du bruit Git et masque les vraies différences. Si un footer pointe vers un
ZIP inexistant, la navigation publiée est cassée. Le mécanisme robuste est donc
de traiter le ZIP comme un contrat généré : contenu fidèle, métadonnées stables,
liens testés.

Le comment : renvoyé au Plan d'implémentation Superpowers.

## Exemple bout-en-bout (projeté)

Un agent corrige une variante et lance deux fois :

```bash
python3 build.py
python3 build.py
```

Sans changement de `slides.json`, `assets/slides/` ni `alternatives.md`, le ZIP
obtenu doit conserver le même SHA-256. Le fichier contient les entrées
`slide-*.png` dans l'ordre attendu, avec des octets identiques aux images
publiées, puis `alternatives.md`.

Sur la page racine générée par une variante, le lien « Télécharger les slides »
doit pointer vers le ZIP de la dernière version publiée, pas vers un mélange
entre slug d'une version et nom de ZIP d'une autre version.

---

## Contexte

ShipGuard remonte quatre points liés par le même contrat de publication :

- `G-Z4-002` : le footer racine généré par la variante condensée pointe vers un
  ZIP inexistant ;
- `SG-Z4-003` : le ZIP publié de `span-pan` ne correspondait pas aux images
  courantes ;
- `SG-Z4-004` : le ZIP publié de `mise-en-gouvernance-du-span` ne correspondait
  pas aux images courantes ;
- `SG-Z2-004` : les ZIPs générés ne sont pas déterministes entre deux builds
  sans changement fonctionnel.

La vérification locale a montré que `SG-Z4-003` et `SG-Z4-004` sont déjà
corrigés par le rebuild réel local, mais les ZIPs régénérés sont encore des
modifications non commitées. Le défaut structurel reste présent dans
`write_zip()`, qui utilise `zipfile.ZipFile.write()` et reprend des métadonnées
de fichiers.

## Problème

Le dépôt ne possède pas encore un contrat unifié pour les ZIPs de slides :

- le contenu du ZIP peut diverger des images courantes si le build n'est pas
  relancé après changement d'images ;
- deux builds sans changement peuvent produire deux binaires différents ;
- les liens HTML racine peuvent pointer vers un chemin inexistant si le slug et
  le nom du ZIP ne viennent pas de la même source ;
- les tests actuels ne couvrent pas systématiquement les ZIPs signalés par
  ShipGuard.

## Solution

Mettre en place un contrat de génération ZIP :

- écrire les entrées ZIP avec `ZipInfo`, date stable et permissions stables ;
- conserver l'ordre déterministe des entrées : `slide-*.png`, puis
  `alternatives.md` ;
- tester que les ZIPs de `span-pan` et `mise-en-gouvernance-du-span`
  correspondent aux images courantes ;
- tester que les liens ZIP racine des variantes longues et condensées pointent
  vers des fichiers existants ;
- séparer les commits : code et tests d'un côté, ZIPs régénérés de l'autre ;
- garder l'autonomie des variantes sans import runtime vers `matrice-slide-ai/`.

## Options évaluées

### Option A (retenue) : ZIP déterministes dans chaque générateur autonome

**Avantages** :
- corrige la cause de `SG-Z2-004` ;
- réduit le bruit Git entre deux builds sans changement ;
- protège la matrice et les variantes existantes ;
- respecte l'autonomie des variantes publiées.

**Inconvénients** :
- ajoute un helper identique dans chaque `build.py` autonome ;
- impose un rebuild réel pour stabiliser les ZIPs publiés.

### Option B : régénérer seulement les ZIPs signalés

**Avantages** :
- très rapide ;
- fait disparaître les divergences binaires de `span-pan` et
  `mise-en-gouvernance-du-span` à court terme.

**Inconvénients** :
- ne corrige pas le non-déterminisme ;
- laisse le lien racine condensé cassé dans `render_root()` ;
- ne crée pas de test de non-régression.

### Option C : ignorer les ZIPs et retirer les liens de téléchargement

**Avantages** :
- retire la surface de bug liée aux archives ;
- simplifie les pages.

**Inconvénients** :
- retire une fonctionnalité utile déjà publiée ;
- contredit les READMEs et les contrôles existants ;
- ne répond pas au besoin de livrer les slides hors ligne.

## Décision

Retenir l'option A.

Les ZIPs font partie du contrat de publication. Ils doivent être produits par le
générateur, pas corrigés à la main. Le plan d'implémentation associé est :

`docs/superpowers/plans/2026-06-30-zip-links-deterministes.md`

## Plan d'implémentation

1. Isoler l'état actuel : les 9 ZIPs déjà régénérés localement ne doivent pas
   être mélangés au commit de code.
2. Ajouter les tests TDD qui reproduisent le lien ZIP racine cassé dans la
   variante condensée.
3. Ajouter un test TDD de ZIP déterministe sur une variante temporaire générée
   depuis la matrice.
4. Ajouter les tests de fidélité ZIP pour `span-pan` et
   `mise-en-gouvernance-du-span`.
5. Corriger le lien ZIP racine avec un nom de ZIP dérivé de la dernière version
   publiée.
6. Remplacer `archive.write()` par un helper `write_zip_entry()` utilisant
   `ZipInfo` avec date et permissions stables.
7. Lancer les suites `unittest`, les validations standard et un double build en
   copie temporaire pour prouver le déterminisme.
8. Après validation Alex, rebuild réel des 9 variantes et commit séparé des
   ZIPs générés.

## Métriques de succès

- Le test du footer racine condensé échoue avant correction, puis passe avec un
  lien ZIP existant.
- Deux builds successifs sans changement produisent le même SHA-256 de ZIP.
- `rg "archive\\.write\\(" --glob build.py .` ne trouve aucun usage restant.
- Les tests de fidélité ZIP passent pour `span-pan` et
  `mise-en-gouvernance-du-span`.
- `python3 -m unittest discover -s matrice-slide-ai/tests` réussit.
- Les 9 suites `unittest` de variantes réussissent.
- Les 9 variantes passent avec `scripts/validate_variant.sh`.
- Les routes ZIP testées localement avec `/usr/bin/curl` répondent `200`.
- Le commit code/tests ne contient aucun ZIP.
- Le commit de ZIPs régénérés, s'il est validé par Alex, est séparé du commit
  code/tests.

## Contraintes d'exécution agentique

- L'agent doit utiliser le plan Superpowers et respecter le TDD : tests rouges
  avant correction du lien et du déterminisme.
- L'agent doit annoncer avant toute écriture si les ZIPs déjà modifiés sont
  commités, laissés en attente ou exclus du commit.
- L'agent ne doit pas push sans validation explicite.
- L'agent ne doit pas modifier l'accueil racine à la main ; la publication
  racine reste réservée à `publish_variant.py`.
- L'agent doit distinguer une alerte déjà résolue par rebuild local d'une
  correction structurelle du générateur.

## Changelog

| Date | Auteur | Changement |
|------|--------|------------|
| 2026-06-30 | Alex + Codex | Création du PRD |
