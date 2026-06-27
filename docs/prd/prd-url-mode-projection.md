# PRD : URL de lancement du mode projection

**Statut** : Implémenté, conservé comme archive de cadrage
**Date** : 2026-06-20
**Auteur** : Alex + Codex
**Source** : échanges de cadrage du 20 juin 2026, projet `miweb-objectifs-2030`

---

## État actuel - 2026-06-25

Les URL `?projection=1#slide-XX` et `?slides=all#diaporama` sont intégrées au générateur de matrice et vérifiées par les tests de contrat. Le plein écran réel reste déclenché par une action utilisateur, conformément à la contrainte navigateur.

La procédure active pour les futurs jeux passe par `matrice-slide-ai/create_variant.py`, le `build.py` du jeu généré, puis `matrice-slide-ai/publish_variant.py` pour l’accueil racine.

## Vision

Le site doit permettre de partager une URL qui prépare directement le diaporama au mode projection, par exemple :

```text
miweb-objectifs-2030-v1/?projection=1#slide-05
```

Cette URL doit ouvrir la bonne slide, amener l’utilisateur au bon endroit et rendre l’entrée en plein écran immédiate au clavier ou au pointeur. Elle ne doit pas prétendre contourner la règle des navigateurs : le vrai `requestFullscreen()` nécessite une activation utilisateur transitoire. L’URL peut donc préparer le mode projection, mais le passage en plein écran système doit rester déclenché par un geste utilisateur.

Le mécanisme attendu est un compromis robuste : une URL partageable pour un usage de présentation, un seul geste pour lancer le plein écran réel, et aucune dégradation des garanties RGAA déjà cadrées pour le mode projection.

## Exemple bout-en-bout projeté

Un présentateur reçoit l’URL :

```text
https://example.github.io/miweb-objectifs-2030/miweb-objectifs-2030-v1/?projection=1#slide-05
```

La page charge la slide 5, comme le comportement d’ancre actuel. Le script détecte `projection=1`, force le mode une seule slide si nécessaire, fait défiler la page vers le diaporama et place le focus sur le bouton d’entrée en plein écran.

L’utilisateur appuie sur `Entrée` ou clique sur le bouton. Cette action utilisateur déclenche `requestFullscreen()` sur `#diaporama`. Le mode projection plein écran existant s’applique alors : navigation standard masquée, mini-barre de projection visible, bouton `Quitter le plein écran` focalisé, accordéon d’alternative textuelle visible sous la slide et aligné avec le cadre.

Si le navigateur refuse le plein écran ou si la Fullscreen API est indisponible, la page reste consultable en mode normal, le bouton plein écran est désactivé de manière native, et la slide ciblée reste visible.

---

## Contexte

Le PRD `docs/prd/prd-mode-projection-plein-ecran.md` cadre déjà le comportement du mode projection une fois le plein écran activé. La nouvelle demande porte sur l’entrée dans ce mode depuis une URL.

Le site dispose déjà d’une navigation par hash `#slide-01` à `#slide-10`. Cette base est saine : elle rend les slides partageables, fonctionne sans JavaScript et reste compatible avec le sommaire.

La difficulté spécifique est la Fullscreen API. D’après MDN et la spécification Fullscreen, `requestFullscreen()` exige une activation utilisateur. Une URL seule ne peut donc pas déclencher automatiquement le plein écran réel dans un navigateur conforme.

Références :

- MDN, `Element.requestFullscreen()` : `https://developer.mozilla.org/en-US/docs/Web/API/Element/requestFullscreen`
- WHATWG, Fullscreen API Standard : `https://fullscreen.spec.whatwg.org/`

## Problème

Sans variable URL, préparer une projection demande plusieurs actions manuelles :

- ouvrir la page ;
- rejoindre la bonne slide ;
- activer le plein écran ;
- vérifier que le mode projection est prêt.

Pour un usage de présentation, cette friction est inutile. Il faut pouvoir préparer la bonne slide et l’action de plein écran depuis un lien, sans casser la navigation existante ni introduire un faux plein écran trompeur.

## Solution

Ajouter une variable d’URL `projection=1` sur la page principale `miweb-objectifs-2030-v1/index.html`.

Comportement retenu :

- `?projection=1` active un état de préparation à la projection ;
- le hash `#slide-XX` reste la source de vérité pour la slide initiale ;
- si le hash est absent, la slide 1 est utilisée ;
- si le hash est invalide, le comportement actuel de repli vers la slide 1 est conservé ;
- au chargement, le script passe en mode une slide active ;
- la page défile vers `#diaporama` ;
- le focus est placé sur le bouton d’entrée en plein écran ;
- le vrai plein écran n’est déclenché qu’après activation explicite du bouton par l’utilisateur ;
- après entrée réelle en plein écran, le comportement du PRD plein écran existant s’applique sans variante.

La variable ne doit pas créer un second mode applicatif permanent. Elle sert uniquement à préparer l’état initial de la page.

## Options évaluées

### Option A retenue : URL de préparation + un geste utilisateur

**Avantages** :

- Compatible avec la Fullscreen API et les contraintes de sécurité navigateur.
- Partageable : `?projection=1#slide-05`.
- Accessible : le focus arrive sur un contrôle natif activable au clavier.
- Préserve le comportement existant des ancres.
- Limite le risque de confusion entre faux plein écran et plein écran réel.
- Ne crée pas de piège clavier.

**Inconvénients** :

- Nécessite encore une action utilisateur pour entrer réellement en plein écran.
- Le terme `projection=1` peut laisser penser que le plein écran est automatique ; il faudra que le comportement soit clair par le focus et le libellé du bouton.

### Option B : faux mode projection automatique

**Avantages** :

- Activation immédiate dès l’ouverture de l’URL.
- Peut masquer header, footer et zones documentaires sans interaction.
- Donne une impression de mode présentation dans la fenêtre courante.

**Inconvénients** :

- Ce n’est pas un vrai plein écran : la barre d’adresse et l’interface navigateur restent visibles.
- Risque de confusion utilisateur.
- Nécessite une seconde logique CSS hors `:fullscreen`.
- Peut dupliquer les règles du mode plein écran et créer des divergences.
- Plus risqué côté accessibilité si des zones sont masquées sans que l’utilisateur ait explicitement choisi ce mode.

### Option C : tentative automatique de `requestFullscreen()` au chargement

**Avantages** :

- Objectif fonctionnel apparent : une URL lancerait directement le plein écran.

**Inconvénients** :

- Non fiable : les navigateurs peuvent refuser l’appel faute d’activation utilisateur.
- Génère des promesses rejetées ou des comportements différents selon navigateur.
- Mauvaise base produit : elle promet un comportement que la plateforme Web ne garantit pas.
- Accessibilité fragile si l’interface dépend d’un état qui échoue silencieusement.

## Décision

Retenir l’option A : `?projection=1#slide-XX` prépare la projection et place le focus sur l’action de plein écran, mais ne déclenche pas automatiquement `requestFullscreen()`.

Cette décision respecte la plateforme Web, garde un parcours clavier explicite et s’appuie sur le mode projection plein écran déjà cadré.

## Plan d’implémentation

1. Ajouter une fonction de lecture de paramètres d’URL dans `MAIN_JS`, sans dépendance externe.
2. Détecter `projection=1` ou `projection=true` au chargement de la page.
3. Conserver `#slide-XX` comme source de vérité de la slide initiale.
4. Si le mode toutes les slides est actif, forcer le retour au mode une slide active avant la préparation.
5. Faire défiler `#diaporama` dans la zone visible sans casser les liens d’évitement.
6. Placer le focus sur le bouton plein écran si la Fullscreen API est disponible.
7. Si la Fullscreen API est indisponible, conserver le bouton désactivé et ne pas déplacer le focus vers un élément inactif.
8. Optionnellement adapter le libellé du bouton en contexte `projection=1`, par exemple `Lancer le plein écran`, sans modifier son rôle ni son activation.
9. Ne pas ajouter de stockage local.
10. Ne pas supprimer le paramètre `projection=1` lors des changements de slide ; les changements de hash doivent préserver la partie query de l’URL.
11. Mettre à jour les tests unitaires de contrat pour vérifier la présence de la logique URL.
12. Ajouter un test navigateur local qui ouvre `?projection=1#slide-05` et vérifie la slide active, le focus et l’absence de tentative automatique de plein écran.
13. Vérifier que le comportement sans JavaScript reste identique : l’ancre cible la bonne slide dans le flux long.

## Exigences fonctionnelles

- L’URL canonique est `?projection=1#slide-XX`.
- `?projection=true#slide-XX` peut être accepté comme alias, mais les liens documentés doivent utiliser `projection=1`.
- `#slide-XX` continue de fonctionner sans `projection=1`.
- `?projection=1` sans hash cible la slide 1.
- Un hash invalide cible la slide 1.
- Le mode projection préparé ne doit pas activer automatiquement `document.fullscreenElement`.
- Le bouton plein écran reste le seul déclencheur du vrai plein écran au chargement.
- Une activation clavier du bouton plein écran doit fonctionner comme un clic.
- Après entrée réelle en plein écran, le focus doit aller sur `Quitter le plein écran`, comme prévu dans le PRD plein écran.
- Après sortie du plein écran, le focus revient sur le bouton plein écran.
- Les changements de slide conservent la query string `?projection=1` dans l’URL.
- La logique ne doit pas s’appliquer sur `alternatives.html`, `accessibilite.html` ou la page racine.

## Exigences d’accessibilité

- Le focus initial ne doit être déplacé vers le bouton plein écran que si ce bouton est activable.
- Aucun élément masqué ne doit recevoir le focus.
- Aucun piège de focus ne doit être créé.
- La touche `Échap` reste gérée par le navigateur une fois le vrai plein écran activé.
- Le statut de slide existant reste mis à jour.
- Les technologies d’assistance doivent pouvoir comprendre le contexte grâce au bouton focalisé et au titre de slide actif hors plein écran.
- Si le libellé devient `Lancer le plein écran`, il doit rester explicite et cohérent avec l’action réelle.
- Le comportement sans JavaScript doit rester acceptable : la page affiche les slides et l’ancre cible la slide demandée.

## Spécifications d’implémentation

La source de vérité reste `miweb-objectifs-2030-v1/build.py`. Les HTML générés ne doivent pas être modifiés à la main.

La lecture d’URL doit utiliser `URLSearchParams` :

```js
const params = new URLSearchParams(window.location.search);
const projectionRequested = ["1", "true"].includes(params.get("projection"));
```

Le déclenchement automatique de `requestFullscreen()` au chargement est interdit. La fonction `toggleFullscreen()` existante reste appelée uniquement depuis une action utilisateur.

La fonction de mise à jour d’URL doit préserver `window.location.search` quand le hash est modifié. Un appel de type `window.history[method](null, "", hash)` peut être insuffisant si une future évolution reconstruit l’URL ; le contrat à préserver est `pathname + search + hash`.

Le test navigateur doit vérifier que `document.fullscreenElement` est `null` après chargement de `?projection=1#slide-05`, avant activation utilisateur.

## Métriques de succès

- `python3 miweb-objectifs-2030-v1/build.py` réussit.
- `python3 -m unittest discover -s miweb-objectifs-2030-v1/tests` réussit.
- `npx --yes html-validate miweb-objectifs-2030-v1/index.html miweb-objectifs-2030-v1/alternatives.html miweb-objectifs-2030-v1/accessibilite.html index.html` réussit.
- `npx --yes vnu-jar --errors-only miweb-objectifs-2030-v1/index.html miweb-objectifs-2030-v1/alternatives.html miweb-objectifs-2030-v1/accessibilite.html index.html` réussit.
- Un test navigateur ouvre `miweb-objectifs-2030-v1/?projection=1#slide-05` et confirme que la slide 5 est active.
- Le même test confirme que le focus est sur le bouton plein écran ou sur un contrôle équivalent activable.
- Le même test confirme que `document.fullscreenElement === null` avant activation utilisateur.
- Après activation du bouton plein écran, un test navigateur confirme que `#diaporama` devient l’élément plein écran quand l’environnement le permet.
- Le changement vers la slide suivante conserve `?projection=1` dans l’URL.
- Un test sans JavaScript ou une inspection HTML confirme que `#slide-05` reste une ancre réelle.

## Risques et parades

**Risque** : l’utilisateur pense que l’URL ouvre directement le plein écran.

**Parade** : documenter et implémenter le comportement comme une préparation projection, avec focus sur l’action utilisateur nécessaire.

**Risque** : un navigateur refuse le plein écran.

**Parade** : conserver le comportement actuel de désactivation du bouton si la Fullscreen API n’est pas disponible, et ne pas masquer le contenu.

**Risque** : la query string disparaît lors des changements de slide.

**Parade** : tester explicitement la conservation de `?projection=1` après navigation.

**Risque** : le focus est déplacé vers un bouton désactivé.

**Parade** : conditionner le focus à la disponibilité de `fullscreenButton.disabled === false`.

## Hors périmètre

- Lancement automatique du vrai plein écran sans action utilisateur.
- Faux mode projection plein écran dans la fenêtre normale.
- Mode présentateur.
- Notes privées.
- Télécommande externe.
- Paramètres avancés de navigation, par exemple `?autoplay=1` ou `?timer=30`.
- Modification du comportement des pages `alternatives.html` et `accessibilite.html`.

## Changelog

| Date | Auteur | Changement |
|------|--------|------------|
| 2026-06-20 | Alex + Codex | Création du PRD pour la variable URL du mode projection |
