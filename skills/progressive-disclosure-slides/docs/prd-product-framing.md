# PRD : Skill PDS générique et proto d'interface

**Statut** : Brouillon de cadrage
**Date** : 2026-06-25
**Source** : conversation, tests réels du skill source, revue critique de l'option B/C
**Décision proposée** : package PDS autonome avec profil de style portable

---

## Vision

Créer un skill standalone minimal qui transforme une source en storyboard PDS, prompts de rendu et contrôles qualité, sans dépendre d'une technologie précise de création d'image.

Le mécanisme à préserver est le substrat PDS : partir d'une scène, montrer une transformation visible, limiter le texte, stabiliser un masque commun, conserver un style institutionnel par défaut et exiger une preuve de sortie. Le moteur image devient un adaptateur interchangeable ; le skill reste responsable de la narration, du contrat de rendu, du style par défaut et de la validation.

## Exemple bout-en-bout projeté

1. Un utilisateur colle un article ou une note longue.
2. L'interface extrait une colonne vertébrale de 3 à 6 étapes.
3. Le skill produit une fiche PDS par slide : scène, objet, tension, transformation, texte exact, risques.
4. Le profil de style institutionnel français est injecté dans chaque prompt, sauf style utilisateur explicite.
5. Un modèle texte peut aider à rédiger le storyboard et les prompts.
6. Un adaptateur de rendu reçoit les prompts et produit des images, ou marque le rendu non disponible.
7. Le système collecte chemin image, ratio, prompt, statut et défauts.
8. Une planche contact ou un équivalent permet de contrôler la cohérence de série.
9. L'utilisateur récupère un dossier projet complet : storyboard, prompts, reçus, images ou statuts `NOT VERIFIED`.

## Contexte

Le skill source fonctionne bien sur des tests réels, mais il était fortement lié à un moteur image et à un flux de fichiers local. La demande est de le rendre plus générique, utilisable par d'autres personnes, et compatible avec un moteur texte comme Albert OSS-120 pour la partie raisonnement.

Point critique : Albert OSS-120 doit être traité comme moteur de conception et d'orchestration, pas comme moteur image, sauf preuve contraire dans la documentation officielle disponible au moment de l'implémentation.

## Problème

Un nettoyage naïf peut supprimer ce qui fait la valeur du skill : le style institutionnel, la preuve de génération, l'inspection, le reçu, la contact sheet et les contraintes PDS. À l'inverse, transformer tout de suite l'idée en studio complet créerait trop de surfaces non vérifiées.

## Solution

Retenir une architecture en trois couches :

- **Noyau PDS** : skill générique, compact, indépendant du rendu, avec invariants bloquants.
- **Profil de style** : référence portable et capsule embarquée dans le standalone.
- **Contrat de rendu** : adaptateur optionnel qui déclare seulement ce qu'il produit réellement.

Le package publié dans `skills/progressive-disclosure-slides/` doit contenir :

- `SKILL.md` : skill standalone minimal.
- `references/pds-method.md` : substrat PDS complet.
- `references/style-institutionnel-fr.md` : profil visuel portable, utilisable par défaut sans créer un skill de style séparé.
- `references/renderer-contract.md` : contrat entre skill et moteur de rendu.
- `references/text-model-role.md` : rôle réaliste d'un modèle texte.
- `standalone-system.md` : prompt système autonome avec capsule de style embarquée.

## Options évaluées

### Option A : Atelier guidé pur

**Avantages** :
- Surface minimale et rapide à tester.
- Très bon alignement avec la logique PDS.
- Faible risque de promesse produit excessive.

**Inconvénients** :
- Moins lisible pour une adoption large.
- Donne peu de place aux notions de projets, styles et moteurs.

### Option B retenue : Package PDS autonome avec profil de style

**Avantages** :
- Conserve le coeur PDS.
- Donne un package compréhensible pour des agents et des humains.
- Prépare l'évolution vers plusieurs moteurs sans les implémenter trop tôt.
- Évite de présenter Albert comme moteur image.

**Inconvénients** :
- Moins démonstratif qu'une interface.
- Demande de maintenir la cohérence entre le skill, le standalone, les références et les exemples.

### Option C : Studio complet

**Avantages** :
- Vision produit plus ambitieuse.
- Peut couvrir projets, styles, historique, variantes, exports et droits.

**Inconvénients** :
- Trop large pour ce package.
- Masque le vrai test : le noyau PDS survit-il à la généricité ?
- Implique backend, persistance, comptes et connecteurs réels.

## Décision

Retenir **Option B** : package PDS autonome, avec skill agentique, prompt standalone, références, exemples et profil de style portable.

## Exigences fonctionnelles

- Le skill MUST générer une colonne vertébrale PDS de 3 à 6 étapes.
- Le skill MUST produire une fiche PDS par slide avant tout rendu.
- Le skill MUST appliquer un profil de style institutionnel français par défaut, sauf style utilisateur explicite.
- Le skill MUST séparer moteur de raisonnement et moteur de rendu.
- Le skill MUST accepter qu'un rendu soit indisponible et produire un statut `NOT VERIFIED`.
- Le contrat de rendu MUST exiger : prompt, fichier ou absence de fichier, ratio, statut, défauts observés.
- Le standalone MUST rester utilisable sans lire de référence externe.

## Non-objectifs

- Pas de backend réel.
- Pas de compte utilisateur.
- Pas de stockage multi-projets.
- Pas d'intégration de modèle texte fonctionnelle dans ce package.
- Pas de génération d'image réelle dans ce package.
- Pas de packaging PPTX dans le MVP.
- Pas de prototype applicatif dans le package publié.

## Plan d'implémentation

1. Créer `skills/progressive-disclosure-slides/pds-slide-generator/`.
2. Rédiger `SKILL.md` en gardant les invariants PDS et les sorties attendues.
3. Externaliser la doctrine complète dans `references/pds-method.md`.
4. Externaliser le profil visuel par défaut dans `references/style-institutionnel-fr.md`.
5. Rédiger `references/renderer-contract.md`.
6. Rédiger `references/text-model-role.md`.
7. Rédiger `standalone-system.md` avec une capsule de style embarquée.
8. Contrôler les accents sur les Markdown.
9. Vérifier que les fichiers existent et que les références internes sont cohérentes.

## Métriques de succès

- `SKILL.md` <= 200 lignes, sauf justification explicite.
- 100 % des invariants PDS du skill source sont présents dans `SKILL.md` ou `references/pds-method.md`.
- La capsule de style institutionnel est présente dans le skill agentique, le prompt standalone et les exemples.
- Le skill ne contient aucune référence obligatoire à un moteur image, un harnais agentique ou un cache local.
- Le contrat de rendu couvre au moins 4 états : `ready`, `rendered`, `failed`, `not_verified`.
- Les Markdown passent `bash scripts/check-accents.sh <fichier>`.
- Le dossier final est entièrement sous `skills/progressive-disclosure-slides/`.

## Limites inhérentes au LLM

- Le LLM peut produire un storyboard convaincant mais visuellement non générable.
- Le LLM peut inventer des capacités de rendu si le contrat ne force pas `NOT VERIFIED`.
- Le LLM peut ajouter du texte parasite dans les prompts.
- Le LLM ne peut pas prouver seul qu'un moteur image a rendu correctement une slide.
- Le coût réel inclut analyse source, prompts, rendu image éventuel, inspection et itérations.

## Spécifications d'implémentation pour le prochain agent

En tant que LLM implémenteur, il manque surtout :

- un nom final stable du skill : proposition `pds-slide-generator` ;
- une décision sur la langue de l'interface : français par défaut ;
- une règle stricte : si aucun fichier image n'existe, ne jamais simuler une réussite ;
- une preuve minimale : liste des fichiers, contrôle accents, références internes et absence de fragments de style obsolètes.

## Passage PDG

**Déclenchement** : oui, car ce PRD est une spécification qui sera exécutée par un agent.

**Skill invocation pass** : `prd` utilisé pour le format de cadrage ; `progressive-disclosure-guard` utilisé pour éviter un handoff ambigu. Le workflow PRD canonique du workspace n'est pas complété volontairement : ce document est un cadrage du package publié.

**Artefacts inspectés** : skill source `generer-images-slides-ia/SKILL.md`, références `prompting-pds.md` et `packaging.md`, skills `prd` et `progressive-disclosure-guard`, arbre local `workflow-decision-tree.md`, état Git.

**Matrice de claims** :

| Affirmation | Source | Verdict | Impact |
|---|---|---|---|
| Le skill source dépendait d'un moteur image précis | Skill source historique | Confirmé | À découpler |
| Le substrat PDS impose scène, transformation et masque commun | `references/prompting-pds.md` | Confirmé | À conserver |
| Le guide source contenait une grammaire de style riche | Guide de style source historique | Confirmé | À distiller en profil portable |
| La preuve actuelle inclut reçus, prompts et contact sheet | `SKILL.md`, `references/packaging.md` | Confirmé | À généraliser |
| Albert OSS-120 doit être traité comme moteur texte, pas image | Source web officielle à revérifier avant intégration | Partiel | Ne pas promettre le rendu image |

**Connus connus** : le package doit rester statique, générique, centré PDS, sous `skills/progressive-disclosure-slides/`.

**Connus inconnus** : API Albert exacte, disponibilité, quotas, authentification, modèle image éventuel, politique de déploiement.

**Inconnus connus** : le mot "studio" peut pousser un agent à créer backend, historique et multi-projets ; ces surfaces sont hors MVP.

**Inconnus inconnus** : incompatibilités futures entre prompts PDS et moteurs de rendu.

**Mauvais chemin d'implémentation** : créer un produit complet ou un backend avant de stabiliser le noyau PDS.

**Garde-fou ajouté** : le moteur de rendu est un contrat, pas une dépendance.

**Comportement existant à préserver** : storyboard concret, style institutionnel sobre, preuve de sortie, inspection, refus de réussite simulée.

**Raccourcis interdits** : supprimer le reçu, supprimer la capsule de style, simuler des images, présenter un modèle texte comme moteur image sans preuve, transformer le package en app complète.

**Preuve de régression requise** : fichiers sous `skills/progressive-disclosure-slides/`, contrôle accents des Markdown, vérification que `SKILL.md` ne dépend pas d'un moteur image précis.
