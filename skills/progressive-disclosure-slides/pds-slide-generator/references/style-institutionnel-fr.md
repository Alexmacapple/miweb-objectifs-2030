# Style institutionnel français

Cette référence distille le style visuel portable du skill source. Elle sert de profil par défaut pour les slides PDS quand l'utilisateur ne fournit pas de charte propre.

Objectif : produire des slides institutionnelles sobres, françaises, lisibles en miniature et centrées sur une transformation visible. Ce profil n'est pas une charte officielle ; c'est une grammaire de génération dérivée d'images de référence.

## Capsule obligatoire

Tout prompt de rendu doit conserver cette capsule, sauf style utilisateur explicite :

```text
Style : slide institutionnelle française 16:9, fond blanc dominant, panneaux gris froids, bleu nuit #001070 pour structure, titres, flèches et icônes, rouge #E44850 uniquement pour alerte, risque ou décision critique, typographie sans-serif sobre, icônes filaires, cartes rectangulaires peu arrondies, aucune photographie, aucune 3D, aucun dégradé, aucun faux logo.
```

## Palette

- Fond principal : blanc.
- Panneaux : gris froid très clair, proche de `#F2F3F7`.
- Séparateurs : gris structure, proche de `#E6E8F0`.
- Couleur principale : bleu nuit `#001070`.
- Bleu secondaire : `#002080` pour étapes ou blocs actifs.
- Accent critique : rouge `#E44850`, réservé aux alertes, risques, blocages, sécurité ou décisions critiques.
- Texte secondaire : gris bleuté sombre, proche de `#20243A`.

Règles :

- le blanc reste dominant ;
- le bleu porte la structure et l'autorité ;
- le rouge ne sert jamais de décoration ;
- les gris servent de support, pas de thème principal.

## Typographie

- Utiliser une sans-serif sobre : Marianne, Inter, Arial, Helvetica Neue ou équivalent.
- Titre en casse de phrase, jamais tout en capitales.
- Titre haut gauche, gras, bleu nuit, environ 34 à 48 px sur une image 1600 x 900.
- Sous-titre optionnel, court, 18 à 22 px, seulement s'il précise la valeur ou le contrôle.
- Labels courts, semi-gras, 13 à 17 px, jamais des phrases longues.
- Footer absent par défaut ; s'il est demandé, il reste très discret en bas droit.

## Layouts autorisés

Choisir une seule famille dominante par slide :

- couverture avec métaphore concrète : titre fort à gauche, scène filaire à droite ;
- comparaison incarnée : deux situations comparables, flèches et résultat visible ;
- progression horizontale : étapes de gauche à droite avec flèches bleues ;
- architecture à deux périmètres : deux blocs de responsabilité et validation centrale ;
- décision en trois piliers : trois cartes égales et recommandation courte ;
- objet métier transformé : entrée à gauche, action au centre, livrable à droite ;
- boucle de validation : objet central, quatre actions maximum, retour visible.

## Composants

- Cartes : rectangles gris très clair, faible rayon, taille uniforme pour rôle équivalent.
- Bandeaux : bleu nuit avec texte blanc, réservés aux conteneurs majeurs.
- Connecteurs : flèches fines bleues, toujours porteuses d'un passage ou d'une transformation.
- Callout : un seul encadré bas, bleu ou gris ; rouge seulement si le message est critique.
- Repère de progression : discret, stable, utile seulement pour une série.
- Icônes : filaires, simples, bleu principal ; rouge seulement pour alerte ou validation critique.

## Style éditorial

- Le titre doit être un message-action, pas un thème abstrait.
- La scène doit déjà faire comprendre le message avant lecture fine.
- Utiliser 3 à 6 labels ou badges courts.
- Un callout maximum, pour bénéfice, risque évité ou décision.
- Aucun paragraphe dans une carte.
- Aucun chiffre inventé.
- Vocabulaire privilégié : générer, exploiter, maîtriser, contrôler, valider, produire, transformation, sécurité, capitalisation, traçabilité.

## Interdits

- Photographie ou rendu réaliste.
- Effets 3D, ombres lourdes, pictogrammes multicolores.
- Dégradés décoratifs, blobs, fonds atmosphériques.
- Faux logo, emblème officiel, fournisseur ou cloud non demandé.
- Rouge décoratif ou rouge dominant.
- Schéma abstrait sans personne, équipe, objet concret ou transformation visible.
- Plus de deux hiérarchies visuelles concurrentes.
- Texte dense, texte parasite, labels non accentués ou lettres déformées.

## Calibration

Si l'utilisateur fournit des images de référence, analyser :

- composition ;
- palette ;
- typographie approximative ;
- composants récurrents ;
- densité de texte ;
- rythme entre slides ;
- éléments observés, inférés et incertains.

Ne copier ni logo, ni surface décorative, ni détails accidentels. Extraire la mécanique visuelle : message-action, scène concrète, grille, composants et progression.
