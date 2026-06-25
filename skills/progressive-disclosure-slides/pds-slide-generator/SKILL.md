---
name: pds-slide-generator
description: Générer des storyboards et prompts de slides PDS à partir d'une source, indépendamment du moteur image. Utiliser pour créer une série de slides visuelles 16:9, préparer un rendu image via adaptateur, ou contrôler une sortie image-based. Ne pas utiliser pour produire directement un backend, un studio complet, un PPTX éditable ou une image sans fiche PDS.
---

# PDS slide generator

Ce skill transforme une source en slides PDS prêtes à rendre. Il ne dépend d'aucune technologie d'image : le rendu passe par un adaptateur séparé qui doit déclarer ce qu'il a réellement produit.

Mission : préserver la narration PDS tout en rendant le moteur de rendu interchangeable.

## Contrat bloquant

- Partir d'une scène, jamais d'un concept nu.
- Produire une fiche PDS avant tout rendu.
- Séparer moteur de raisonnement, prompt et moteur de rendu.
- Ne jamais déclarer une image produite sans fichier, URL ou statut de rendu vérifiable.
- Marquer `NOT VERIFIED` quand le rendu, le fichier, le ratio ou l'inspection manque.
- Garder le rouge pour alerte, risque ou décision critique.
- Ne pas créer de studio complet, backend, historique ou gestion multi-projets dans ce workflow.

## Ressources

- Lire `references/pds-method.md` pour la doctrine PDS complète, surtout si la série dépasse 3 slides.
- Lire `references/renderer-contract.md` avant d'appeler ou de définir un moteur de rendu.
- Lire `references/text-model-role.md` si Albert ou un autre modèle texte est envisagé.

## Workflow

1. **Cadrer la demande** : identifier source, public, objectif, nombre de slides et livrable attendu. Par défaut, produire 5 slides pour une source longue structurée.
2. **Construire la colonne vertébrale** : définir 3 à 6 étapes maximum. Chaque étape doit porter une transformation visible.
3. **Créer les fiches PDS** : pour chaque slide, renseigner rôle, idée, scène, objet, transformation, texte exact, masque commun, compréhension en 3 secondes, continuité et risque.
4. **Rédiger les prompts de rendu** : transformer chaque fiche PDS en prompt complet pour un adaptateur image, sans dépendre d'un fournisseur précis.
5. **Appeler ou simuler le rendu selon contexte** : si un moteur est disponible, utiliser son adaptateur ; sinon produire les prompts et statuts `ready` sans inventer d'image.
6. **Contrôler les sorties** : appliquer le contrat de rendu, inspecter lisibilité, ratio, progression, stabilité du masque et texte parasite.
7. **Livrer un reçu** : fournir storyboard, prompts, statut de rendu, chemins ou absence de chemins, défauts et contrôles effectués.

## Format de fiche PDS

```text
Rôle dans la colonne vertébrale :
Idée principale :
Scène :
Personnage ou objet-système :
Transformation visible :
Texte exact :
Masque commun :
Ce que l'image seule doit faire comprendre :
Ajout à la slide précédente et préparation de la suivante :
Risque à éviter :
```

## Format du reçu

```tsv
slide	status	renderer	prompt_ref	asset_ref	ratio	inspection	notes
slide-01	ready	none	prompts/slide-01.txt	NOT_RENDERED	unknown	NOT_VERIFIED	Prompt prêt, rendu non lancé.
slide-02	rendered	example	prompts/slide-02.txt	assets/slide-02.png	16:9	OK	Texte lisible.
```

États autorisés : `ready`, `rendered`, `failed`, `not_verified`.

## Exemple end-to-end

Entrée : article sur le choix entre HTML et PDF.

Sortie attendue :

1. Colonne vertébrale : décider, comparer HTML, qualifier les exceptions PDF, arbitrer les cas, publier sans exclure.
2. Cinq fiches PDS complètes.
3. Cinq prompts de rendu 16:9.
4. Reçu avec `ready` si aucun moteur image n'est branché, ou `rendered` seulement si chaque fichier existe.
5. Note `NOT VERIFIED` sur toute slide dont l'image n'a pas été inspectée.

## Pièges connus

- **Promesse fausse** : présenter un modèle texte comme moteur image. Correction : lire `references/text-model-role.md` et déclarer le rendu séparément.
- **Abstraction froide** : produire un schéma sans scène. Correction : revenir à la fiche PDS et nommer l'objet concret.
- **Succès simulé** : livrer un chemin absent ou une image non inspectée. Correction : statut `NOT VERIFIED`.
- **Studio prématuré** : ajouter projets, comptes, backend ou historique. Correction : garder seulement le flux Source -> PDS -> Prompts -> Rendu -> Contrôle.

## Checklist de livraison

- [ ] La colonne vertébrale contient 3 à 6 étapes.
- [ ] Chaque slide a une fiche PDS complète.
- [ ] Chaque prompt mentionne format 16:9, scène, texte exact et interdits.
- [ ] Le moteur de rendu est nommé ou déclaré absent.
- [ ] Le reçu utilise seulement les états autorisés.
- [ ] Toute absence de fichier ou d'inspection est marquée `NOT VERIFIED`.
- [ ] Le livrable ne dépend pas d'un fournisseur, d'un cache local ou d'un chemin propre à un harnais.
