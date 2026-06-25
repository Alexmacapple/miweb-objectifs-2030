# Test PDS - ARIA annonce, HTML agit

Source : texte fourni par l'utilisateur sur ARIA, `role="button"` et le comportement clavier.

## Colonne vertébrale

1. Un faux bouton est annoncé comme bouton.
2. La touche Entrée ne déclenche rien, car le comportement manque.
3. Un bouton HTML natif reçoit le focus et s'active correctement.

## Fiche PDS - slide 01

Rôle dans la colonne vertébrale : comparaison problème -> réponse.

Idée principale : ARIA peut nommer un composant, mais ne crée pas son comportement.

Scène : une personne teste deux composants côte à côte avec un clavier. À gauche, un `div role="button"` est annoncé comme bouton mais reste inactif quand la touche Entrée est pressée. À droite, un bouton HTML natif s'active au clavier.

Personnage ou objet-système : poste de test accessibilité avec clavier, lecteur d'écran stylisé et deux composants.

Transformation visible : annoncé -> bloqué à gauche ; natif -> activé à droite.

Texte exact : titre « ARIA annonce, HTML agit » ; labels « Annonce », « Entrée », « HTML natif », « Action » ; callout « Le rôle ne crée pas le comportement ».

Masque commun : format 16:9, titre haut gauche, scène centrale en deux panneaux, badges courts en bas, callout bas droit, fond clair, bleu pour le chemin correct, rouge pour le blocage.

Ce que l'image seule doit faire comprendre : un rôle ARIA peut tromper si le comportement clavier n'est pas implémenté ; le HTML natif fournit déjà ce comportement.

Ajout à la slide précédente et préparation de la suivante : slide isolée de sensibilisation, suffisante pour ouvrir une discussion sur « no ARIA is better than bad ARIA ».

Risque à éviter : trop de code, texte illisible, promesse que ARIA est inutile partout, opposition trop simpliste.
