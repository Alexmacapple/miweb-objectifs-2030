# Progressive Disclosure Slides

Ce dossier partage un skill agnostique pour transformer une source en slides PDS, sans dépendre d'un générateur d'image, d'un modèle texte, d'un cache local ou d'un harnais agentique.

PDS signifie **Progressive Disclosure Slides** : une série de slides qui révèle une idée étape par étape. Chaque slide part d'une scène concrète, montre une transformation visible, limite le texte et conserve un masque commun.

## Pourquoi ce skill existe

En mode Software 3.0, le prompt devient un programme exécutable par LLM. Le bon livrable n'est donc pas seulement une image ou un fichier de slides : c'est un contrat qui dit comment transformer une source, vérifier la sortie et refuser une réussite non prouvée.

Ce package conserve le noyau utile du workflow d'origine :

- colonne vertébrale narrative ;
- fiche PDS avant tout rendu ;
- prompt de rendu indépendant du fournisseur ;
- reçu de statut ;
- refus des slides faibles ;
- inspection groupée des séries.

## Structure

```text
skills/progressive-disclosure-slides/
  README.md
  pds-slide-generator/
    SKILL.md
    standalone-system.md
    references/
      pds-method.md
      renderer-contract.md
      text-model-role.md
    examples/
      aria-role-button/
      pm-ai-agent-loops/
        storyboard.md
        assets/
          contact-sheet.png
          slide-01.png
          slide-02.png
          slide-03.png
          slide-04.png
          slide-05.png
          rejected/
    docs/
      prd-product-framing.md
      prd-reverse-engineering.md
```

## Utilisation

Pour un agent compatible skills, utiliser :

```text
pds-slide-generator/SKILL.md
```

Pour un outil qui accepte un seul fichier Markdown comme prompt système, utiliser :

```text
pds-slide-generator/standalone-system.md
```

Dans les deux cas, le flux attendu est :

```text
Source -> Colonne vertébrale -> Fiches PDS -> Prompts -> Rendu optionnel -> Contrôle
```

## Contrat de rendu

Le moteur image est optionnel et interchangeable. Un rendu peut seulement être déclaré `rendered` si un fichier, une URL ou un artefact exploitable existe.

États autorisés :

- `ready` : prompt prêt, rendu non lancé ;
- `rendered` : artefact exploitable produit ;
- `failed` : moteur appelé mais échec explicite ;
- `not_verified` : sortie absente, incomplète ou non inspectée.

## Garde-fous

- Ne pas partir d'un concept nu : partir d'une scène.
- Ne pas déclarer une image produite sans artefact.
- Marquer `not_verified` si le ratio, le texte, le chemin ou l'inspection manque.
- Refuser ou régénérer une slide illisible, trop dense ou incohérente.
- Pour une série rendue, exiger une contact sheet, une grille d'aperçu ou une inspection groupée équivalente.
- Ne pas lier le skill à un fournisseur, une marque ou un moteur précis.

## Exemples

- `examples/aria-role-button/storyboard.md` : slide pédagogique unique sur ARIA et HTML natif.
- `examples/pm-ai-agent-loops/storyboard.md` : série de 5 slides avec images rendues, reçu et contact sheet.

## Limites

Ce package ne fournit pas de backend, de studio complet, de gestion de projet, de PPTX éditable ni de connecteur image. Il fournit la méthode, les contrats et des exemples reproductibles.
