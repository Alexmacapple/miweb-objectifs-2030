# Doctrine PDS

PDS signifie Progressive Disclosure Slides. Le but est de raconter une scène compréhensible avant de demander au public de lire les labels.

## Invariants

- Ne jamais partir d'un concept. Toujours partir d'une scène.
- Une slide montre une seule tension, action ou transformation.
- Une série contient 3 à 6 étapes principales.
- Un masque commun stabilise titre, progression, grille, callout, zones de texte et codes couleur.
- Seuls les éléments qui portent la transformation narrative peuvent bouger.
- Les concepts abstraits doivent devenir personne, équipe, objet concret, tension, action et résultat.
- Le test des trois secondes doit permettre de dire qui agit, sur quoi, ce qui change et pourquoi c'est utile.

## Structure d'une série

Choisir une colonne vertébrale courte :

- douleur -> réponse -> bénéfice ;
- choix -> décision -> preuve ;
- avant -> pendant -> après ;
- niveau 1 -> niveau 2 -> niveau 3 ;
- problème -> contrôle -> livraison.

Chaque slide doit ajouter quelque chose à la précédente et préparer la suivante.

## Masque commun

Stabiliser :

- titre en haut à gauche ;
- progression en haut à droite ;
- scène principale au centre ;
- badges courts en bas ;
- callout unique ;
- fond clair ;
- bleu pour structure ;
- rouge seulement pour alerte, risque ou décision critique.

## Style par défaut

Le profil visuel canonique est `references/style-institutionnel-fr.md`. Le résumé ci-dessous doit rester dans chaque prompt si l'utilisateur ne fournit pas de style concurrent :

- slide institutionnelle française 16:9 ;
- fond blanc dominant et panneaux gris froids ;
- bleu nuit `#001070` pour titres, structure, flèches et icônes ;
- rouge `#E44850` uniquement pour alerte, risque, sécurité ou décision critique ;
- typographie sans-serif sobre, titre-action haut gauche, labels courts ;
- cartes rectangulaires peu arrondies, icônes filaires, flèches fines ;
- aucune photographie, aucune 3D, aucun dégradé, aucun blob, aucun faux logo.

## Règles éditoriales

- Titre-action court.
- 3 à 6 labels ou badges.
- Un callout maximum.
- Aucun paragraphe dans une carte.
- Aucun chiffre inventé.
- Aucun faux logo, emblème officiel, fournisseur ou cloud non demandé.
- Footer absent par défaut.

## Fiche avant rendu

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

Si une ligne est floue, ne pas générer encore.

## Prompt de rendu générique

```text
Cas d'usage : visuel de productivité publique.
Type d'actif : image finale de slide 16:9 paysage.
Demande : créer une slide institutionnelle française sobre, sans faux logo, emblème ni filigrane.
Style : slide institutionnelle française, fond blanc dominant, panneaux gris froids, bleu nuit #001070 pour structure, titres, flèches et icônes, rouge #E44850 seulement critique, typographie sans-serif sobre, icônes filaires, cartes rectangulaires peu arrondies, aucune photographie, aucune 3D, aucun dégradé.
Composition : [scène concrète et structure dominante].
Masque commun : [zones stables et éléments autorisés à évoluer].
Storyboard : [personnage ou objet, tension, action, résultat].
Texte exact : [titre, labels, callout].
À éviter : fournisseurs, faux symboles officiels, texte excessif, code, texte illisible, paragraphe, blob, rouge décoratif.
```
