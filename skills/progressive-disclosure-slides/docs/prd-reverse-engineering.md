# PRD : Reverse engineering du prompt système PDS

**Statut** : Brouillon de reverse engineering
**Date** : 2026-06-25
**Source** : `pds-slide-generator/standalone-system.md`, tests PDS, wiki Karpathy
**Décision proposée** : documenter le prompt système comme artefact Software 3.0 autonome

---

## Vision

Le prompt système PDS doit être traité comme un programme exécutable par LLM, pas comme une simple consigne de style. Son rôle est de transformer une source en storyboard, fiches PDS, prompts de rendu et reçu de statut, tout en empêchant les réussites simulées.

Le mécanisme fonctionne parce qu'il combine cinq couches :

1. **Distillation** : extraire le noyau invariant du skill image IA sans garder la dépendance à un moteur.
2. **Programmation par prompt** : encoder les règles sous forme de contrat système stable.
3. **Progressive disclosure** : révéler successivement hypothèses, colonne vertébrale, fiches, prompts, reçu et limites.
4. **Style portable** : conserver une capsule visuelle institutionnelle sans dépendre d'un guide local.
5. **Vérification** : forcer les statuts `ready`, `rendered`, `failed` ou `not_verified` selon les preuves disponibles.

Le pourquoi Karpathy : en Software 3.0, le prompt est le programme, le LLM est l'interpréteur, le concept peut être le livrable principal, et les critères vérifiables remplacent les instructions vagues.

## Exemple bout-en-bout réel

Entrée : un texte sur des PM IA qui font tourner des boucles d'agents auto-correctives.

Exécution :

1. Le prompt système choisit 5 slides, car la source décrit un cycle complet.
2. Il réduit l'emphase initiale en modèle opérable : dérive, boucle, score, mémoire Git, maturité des artefacts.
3. Il produit une fiche PDS par slide avant tout prompt de rendu.
4. Il rédige des prompts 16:9 indépendants d'un fournisseur.
5. Il marque toutes les sorties `ready`, moteur `none`, artefact `NOT_RENDERED`, inspection `NOT_VERIFIED`.
6. Il ajoute une évaluation robuste locale : preuves, risques, score conservateur et limites.

Sortie : `pds-slide-generator/examples/pm-ai-agent-loops/storyboard.md`.

---

## Contexte

Le skill d'origine produisait des images de slides IA avec un harnais local, des artefacts, des reçus et des contrôles. La version générique conserve la valeur PDS tout en devenant indépendante de la technologie d'image.

La version mono-fichier répond à une contrainte forte : certains générateurs ne permettent d'uploader qu'un seul fichier Markdown. Le prompt système doit donc être autonome, cloisonné et utilisable sans références externes.

## Problème

Une distillation trop agressive risque de supprimer ce qui faisait la qualité du skill source : scène concrète, transformation visible, masque commun, style institutionnel, preuve de rendu, inspection, refus des images faibles et contrôle de série.

Une distillation trop faible garde au contraire trop de dépendances locales : chemins, outil image, cache, harnais agentique ou fournisseur implicite.

## Solution

Créer un prompt système autonome qui encode le noyau PDS et le contrat de preuve.

Le prompt doit imposer :

- une sortie en six sections : hypothèses, colonne vertébrale, fiches PDS, prompts de rendu, reçu, contrôles ;
- une fiche PDS avant tout prompt de rendu ;
- une capsule de style institutionnel française, sauf style utilisateur explicite ;
- des prompts 16:9 avec scène, texte exact et interdits ;
- un contrat de rendu où l'image n'existe que si un artefact exploitable existe ;
- `not_verified` si ratio, texte, chemin, inspection ou qualité sont insuffisants ;
- une inspection groupée pour toute série rendue ;
- aucune dépendance à un fournisseur, cache, chemin local ou outil précis.

## Prompt système distillé

Le prompt système complet reste dans `pds-slide-generator/standalone-system.md`. Sa structure utile est :

```text
Mission : générer des briefs de slides PDS en circuit fermé.
Entrées : source, nombre de slides, public, style, moteur, image rendue.
Règles : scène avant concept, une transformation par slide, masque commun, texte limité.
Fiche : rôle, idée, scène, objet, transformation, texte exact, masque, compréhension, continuité, risque.
Style : fond blanc, gris froids, bleu nuit, rouge critique, typographie sobre, composants filaires.
Rendu : adaptateur optionnel, statut strict, artefact requis pour `rendered`.
Contrôle : refus ou `not_verified` si slide faible ; contact sheet ou inspection groupée pour une série.
Sortie : hypothèses, colonne vertébrale, fiches, prompts, reçu, limites.
```

Ce bloc est la distillation opératoire. Le fichier complet ajoute les formats, exemples et règles bloquantes.

## Méthode de reverse engineering

1. Lire le skill source et lister les comportements réellement créateurs de qualité.
2. Séparer les invariants PDS des dépendances d'exécution.
3. Convertir les invariants en règles bloquantes.
4. Remplacer les appels d'outil par un contrat d'adaptateur.
5. Remplacer les preuves locales par un reçu de statut portable.
6. Ajouter des garde-fous contre les réussites simulées.
7. Tester sur deux types de sources : article structuré et post conceptuel.
8. Évaluer la sortie avec une matrice affirmation, source, verdict, impact.

## Options évaluées

### Option A : mettre à jour le PRD produit existant

**Avantages** :
- Un seul document de cadrage.
- Moins de fichiers à maintenir.

**Inconvénients** :
- Mélange produit, package publié et reverse engineering.
- Rend moins visible le raisonnement Software 3.0.
- Risque de noyer la méthode de distillation.

### Option B retenue : PRD dédié de reverse engineering

**Avantages** :
- Sépare clairement le produit du prompt système.
- Documente la méthode réutilisable pour d'autres skills.
- Ancre le pourquoi Karpathy sans alourdir le PRD initial.

**Inconvénients** :
- Ajoute un document supplémentaire.
- Demande de garder la cohérence avec le prompt source.

### Option C : PRD canonique dans `prd-meta-workflow`

**Avantages** :
- Suit le workflow PRD complet du workspace.
- Traçabilité plus forte via backlog, changelog et commit.

**Inconvénients** :
- Plus lourd que le besoin actuel.
- Moins adapté à un package publié sous `skills/progressive-disclosure-slides/`.

## Décision

Retenir l'option B : créer un PRD dédié de reverse engineering sous `skills/progressive-disclosure-slides/docs/`. Le PRD initial reste le cadrage produit ; ce document devient la mémoire du prompt système, de sa distillation et de son ancrage conceptuel.

## Métriques de succès

- Le prompt standalone tient dans un seul fichier Markdown.
- Le prompt ne contient aucune dépendance obligatoire à un fournisseur, outil local ou chemin absolu.
- Le prompt standalone contient une capsule de style suffisante pour éviter un rendu générique.
- Les deux garde-fous sont présents : refus des slides faibles et inspection groupée des séries.
- Une source longue produit 3 à 6 slides avec fiches PDS complètes.
- Une source courte peut produire une slide unique sans changer de format de sortie.
- Aucun rendu n'est déclaré `rendered` sans artefact exploitable.
- Les Markdown passent `bash scripts/check-accents.sh <fichier>`.

## Limites inhérentes au LLM

- Le LLM peut produire une scène plausible mais visuellement difficile à rendre.
- Le LLM peut confondre statut narratif et preuve d'artefact si le reçu n'est pas strict.
- Le LLM peut surcharger les slides en texte quand la source est dense.
- Le LLM ne peut pas vérifier lisibilité, ratio réel ou cohérence de série sans artefact rendu.
- Le LLM peut transformer le vocabulaire Karpathy en slogan ; le PRD doit garder le mécanisme : prompt-programme, concept-livrable, tests-critères.

## Spécifications d'implémentation

- Le prompt système MUST rester autonome.
- Le prompt système MUST conserver la sortie en six sections.
- Le prompt système MUST conserver la capsule de style par défaut.
- Le prompt système MUST conserver les statuts stricts.
- Le prompt système MUST refuser ou marquer `not_verified` toute slide faible.
- Le prompt système MUST exiger une inspection groupée pour les séries rendues.
- Le prompt système MUST NOT promettre une image, une inspection ou une automatisation non observée.
- Le prompt système MUST NOT introduire backend, studio, historique ou fournisseur par défaut.

## Sources et preuves

| Affirmation | Source | Verdict | Impact |
|---|---|---|---|
| Le prompt standalone encode les six sections | `pds-slide-generator/standalone-system.md` | Confirmé | Contrat de sortie stable |
| Le prompt standalone doit rester utilisable sans guide local | `pds-slide-generator/standalone-system.md` | Confirmé | La capsule de style doit être embarquée |
| Le prompt comme programme est cohérent avec Karpathy | `wiki/knowledge/karpathy/trois-eres-logiciel.md` | Confirmé | Justifie le traitement du prompt comme artefact |
| Le concept peut être le livrable principal | `wiki/knowledge/karpathy/livrable-concept.md` | Confirmé | Justifie le PRD reverse engineering |
| Les tests critériés guident mieux l'agent | `wiki/knowledge/karpathy/execution-guidee-objectif-criteres-reussite.md` | Confirmé | Justifie le reçu et les statuts |
| Le modèle compilateur relie source, LLM, sortie et tests | `wiki/knowledge/karpathy/analogie-compilateur.md` | Confirmé | Justifie source -> prompt -> sortie -> contrôle |

## Passage PDG

Décision : PDG déclenché, car ce PRD est un handoff pour maintenir ou répliquer un prompt système.

Sources inspectées : prompt standalone, PRD produit existant, skill `prd`, wiki Karpathy, PDG.

Connus connus : PRD initial déjà orienté produit ; prompt standalone validé comme mono-fichier ; package publié avec chemins relatifs.

Connus inconnus : comportement dans un générateur image externe, rendu réel, robustesse multi-modèle.

Inconnus connus : le terme « auto-réparation » peut créer une promesse excessive ; il doit rester traduit en score, rollback et preuve.

Inconnus inconnus : tolérance des moteurs image au français accentué, aux labels courts et aux contraintes négatives.

Mauvais chemin d'implémentation : copier le prompt complet dans chaque PRD ou mélanger produit, prompt et package dans un seul document.

Garde-fou ajouté : PRD dédié, source canonique du prompt conservée séparément.

Comportement à préserver : autonomie mono-fichier, statut honnête, distillation PDS, capsule de style, indépendance fournisseur.

Raccourcis interdits : déclarer `rendered` sans artefact, supprimer le reçu, supprimer l'inspection groupée, supprimer la capsule de style, transformer le PRD en documentation marketing.

Preuve de régression requise : refaire un test source courte et source longue, puis vérifier accents, statuts et présence des deux garde-fous.
