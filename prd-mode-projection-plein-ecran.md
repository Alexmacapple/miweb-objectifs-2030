# PRD : Mode projection plein écran du diaporama

**Statut** : Implémenté, conservé comme archive de cadrage
**Date** : 2026-06-20
**Auteur** : Alex + Codex
**Source** : échange de cadrage du 20 juin 2026, projet `miweb-objectifs-2030`

---

## État actuel - 2026-06-25

Le mode projection plein écran est intégré au générateur de matrice et couvert par les tests de contrat : contrôles de projection, `requestFullscreen`, `exitFullscreen`, statut de projection, maintien des alternatives et absence de `href="#"`.

Pour un nouveau jeu, ne modifier ni les HTML générés ni une ancienne variante publiée : créer le dossier avec `matrice-slide-ai/create_variant.py`, générer avec son `build.py`, puis publier avec `matrice-slide-ai/publish_variant.py`.

## Vision

Le mode plein écran du diaporama doit se comporter comme un mode projection de slides : l’image de la slide active devient l’objet principal, les éléments documentaires de la page disparaissent visuellement, et les commandes restantes sont réduites au strict nécessaire.

Le mécanisme recherché est simple : séparer le mode de consultation web, riche en structure et en alternatives, du mode de projection, orienté présentation. Cette séparation améliore la lisibilité en projection sans supprimer les garanties d’accessibilité du site, car les alternatives et la structure complète restent disponibles hors plein écran. Le mode projection ne doit pas devenir une version appauvrie et piégeante du site : il doit rester quittable, navigable et compréhensible.

## Exemple bout-en-bout projeté

Un utilisateur ouvre la page du diaporama et active le bouton `Plein écran`.

Le navigateur affiche le conteneur `#diaporama` en plein écran. Si l’utilisateur était en mode `Afficher toutes les slides`, le diaporama repasse en mode une slide active avant d’entrer en projection. Le titre `#diaporama-title`, les titres `.miweb-slide-title` et la navigation standard `.miweb-slide-controls` ne sont plus visibles. L’image de la slide active occupe la zone principale. L’accordéon d’alternative textuelle de la slide active reste visible immédiatement sous la slide, aligné sur la même grille que le cadre de slide.

Une mini-barre dédiée au mode projection reste visible. Elle contient trois contrôles natifs visibles : `Précédente`, `Suivante` et `Quitter le plein écran`. Elle expose aussi un statut non visuel de type `Slide 3 sur 10 - Titre de la slide` pour annoncer les changements de slide aux technologies d’assistance.

À l’entrée en plein écran, le focus est déplacé vers le bouton `Quitter le plein écran`, car le bouton `Plein écran` standard devient masqué avec la navigation standard. L’utilisateur peut changer de slide avec les boutons de la mini-barre. Il peut aussi sortir du plein écran avec le bouton dédié ou avec la touche `Échap`, selon le comportement natif du navigateur. À la sortie, le focus revient sur le bouton `Plein écran` de la navigation standard.

Hors plein écran, l’expérience actuelle reste inchangée : les titres, les alternatives textuelles, l’accordéon, le sommaire et les liens de téléchargement restent disponibles.

---

## Contexte

Le site publie un diaporama HTML accessible des slides MiWeb « Objectifs 2030 - accessibilité numérique ». Le plein écran existe déjà, mais il conserve actuellement la navigation standard, les titres et l’accordéon d’alternative textuelle. Ce comportement est robuste côté accessibilité, mais donne moins l’impression d’un vrai mode projection.

La demande produit est de rendre le plein écran plus proche d’un mode présentation : ne pas afficher `h2#diaporama-title`, les `h3.miweb-slide-title` ni le menu standard `.miweb-slide-controls`, tout en conservant l’accordéon d’alternative textuelle directement sous la slide, aligné sur son cadre, et en prévoyant une sortie accessible du plein écran.

## Consultation RGAA locale AY11

La consultation du dépôt `/Users/alex/Claude/git-hors-workflow/ay11-pre-audit` confirme que le référentiel local RGAA 4.1.2 est valide : 106 critères, 258 tests, profils stricts exécutables.

Les critères sensibles pour ce changement sont :

- `7.1` : composants contrôlés par script, nom, rôle, état et alternative accessible.
- `7.3` : activation clavier et dispositif de pointage des contrôles JavaScript.
- `7.5` : message de statut correctement annoncé lors du changement de slide.
- `9.1` : hiérarchie des titres, à préserver dans le mode page.
- `10.2` et `10.3` : information présente et compréhensible sans CSS.
- `10.7` : focus visible sur chaque élément interactif.
- `10.11` et `10.12` : disponibilité des informations et lisibilité à petit viewport, zoom et espacement du texte.
- `12.6` : identification, évitement ou atteinte des zones de regroupement.
- `12.8` : ordre de tabulation cohérent.
- `12.9` : absence de piège clavier et mécanisme de sortie.
- `1.1` et `1.3` : présence et pertinence d’une alternative textuelle pour les images de slides porteuses d’information.

Conclusion : le mode projection peut rester accessible si les éléments sont masqués uniquement dans l’état plein écran, si le DOM complet reste disponible hors plein écran, si les contrôles de projection sont des boutons natifs, si le focus visible est préservé, et si la sortie du plein écran est possible au clavier comme au pointeur.

Le masquage ne doit pas être uniforme :

- les contrôles standard doivent être retirés du rendu en plein écran afin de ne pas rester focusables ;
- l’accordéon d’alternative textuelle doit rester visible, aligné sur le cadre de slide et utilisable au clavier ;
- les titres doivent conserver un contexte programmatique fiable, soit via une classe de masquage visuel, soit via un nom accessible stable sur les régions concernées ;
- le focus ne doit jamais rester sur un élément devenu invisible après le passage en plein écran.

## Problème

Le plein écran actuel est trop proche du mode page. Il affiche des éléments utiles à la consultation web, mais encombrants en projection :

- le titre de section du diaporama ;
- le titre structuré de la slide active ;
- la navigation standard complète avec téléchargement et mode toutes les slides.

À l’inverse, supprimer tous les contrôles visibles en plein écran rendrait la navigation peu découvrable et fragiliserait l’accessibilité clavier.

## Solution

Ajouter un mode projection dédié à l’état `#diaporama:fullscreen`.

Dans cet état :

- ne pas afficher visuellement `#diaporama-title` ;
- ne pas afficher visuellement `.miweb-slide-title` ;
- retirer du rendu `.miweb-slide-controls` ;
- maximiser la figure de la slide active ;
- conserver `.fr-accordions-group` visible juste sous la slide, aligné sur la même largeur que `.miweb-slide-frame` ;
- afficher une mini-barre de projection indépendante ;
- proposer trois contrôles natifs : `Précédente`, `Suivante`, `Quitter le plein écran`.
- annoncer les changements de slide via un statut non visuel dédié au mode projection.

La mini-barre ne remplace pas la navigation standard hors plein écran. Elle n’existe que pour l’expérience de projection.

## Options évaluées

### Option A retenue : mode projection épuré avec mini-barre dédiée

**Avantages** :

- Rendu proche d’une projection de slides.
- Navigation explicite sans dépendre uniquement des raccourcis clavier.
- Boutons natifs compatibles clavier, pointeur et technologies d’assistance.
- Sortie du plein écran visible et nommée.
- Risque RGAA maîtrisable par tests clavier et focus.
- Possibilité d’annoncer les changements de slide sans réafficher toute la navigation standard.
- Alternative textuelle directement disponible dans le mode projection.

**Inconvénients** :

- Ajoute une seconde couche de contrôles à maintenir.
- Demande une synchronisation d’état entre boutons standard et boutons projection.
- Nécessite des tests navigateur réels du plein écran.

### Option B : mode projection minimal avec seulement `Quitter le plein écran`

**Avantages** :

- Interface la plus proche d’une slide seule.
- Moins de surface visuelle.
- Moins de boutons à afficher en projection.

**Inconvénients** :

- Navigation entre slides moins découvrable.
- Dépendance forte aux touches clavier non visibles.
- Accessibilité plus fragile pour les utilisateurs qui ne connaissent pas les raccourcis.
- Risque accru sur `12.8` et `12.9` si le parcours clavier devient ambigu.

### Option C : conserver la navigation standard en plein écran

**Avantages** :

- Comportement actuel déjà testé.
- Toutes les commandes restent disponibles.
- Peu de changement technique.

**Inconvénients** :

- Ne répond pas au besoin de projection.
- Interface trop chargée en plein écran.
- L’accordéon et les titres concurrencent visuellement la slide.

## Décision

Retenir l’option A : un mode projection épuré avec mini-barre dédiée.

La navigation standard reste visible hors plein écran et masquée en plein écran. La mini-barre de projection devient le seul groupe de contrôles visible en plein écran. L’alternative textuelle de la slide active reste disponible en projection via son accordéon placé juste sous la slide et aligné sur son cadre ; elle reste aussi disponible hors plein écran et via la page dédiée.

## Plan d’implémentation

1. Ajouter dans le rendu HTML une mini-barre de projection dédiée, distincte de `.miweb-slide-controls`.
2. Créer trois boutons natifs : précédent, suivant, quitter le plein écran.
3. Ajouter dans la mini-barre un statut non visuel `aria-live="polite"` synchronisé avec la slide active.
4. Masquer la mini-barre hors plein écran sans la laisser dans l’ordre de tabulation.
5. En plein écran, retirer du rendu la navigation standard afin que ses boutons ne soient plus focusables.
6. En plein écran, masquer les titres sans casser le nom accessible du diaporama ni l’identification de la slide active.
7. En plein écran, conserver l’accordéon d’alternative textuelle de la slide active, l’aligner sous le cadre de slide et le rendre utilisable au clavier.
8. Avant d’entrer en plein écran, repasser en mode une slide active si le mode `Afficher toutes les slides` est actif.
9. Réutiliser la logique existante de changement de slide pour les boutons projection.
10. Adapter la gestion du focus : hors plein écran, le changement de slide peut continuer à focaliser le titre ; en plein écran, il ne doit jamais focaliser un titre masqué.
11. Synchroniser les états désactivés des boutons précédent et suivant, côté navigation standard et côté projection.
12. Si une action désactive le bouton qui avait le focus, déplacer le focus vers un contrôle de projection encore actif.
13. À l’entrée en plein écran, déplacer le focus vers `Quitter le plein écran`.
14. À la sortie du plein écran, restaurer le focus sur le bouton `Plein écran`.
15. Vérifier que la touche `Échap` reste gérée par le navigateur et ne pas intercepter ce comportement.
16. Ajouter ou mettre à jour les tests unitaires de contrat HTML.
17. Vérifier au navigateur le focus visible, l’ordre de tabulation, la sortie du plein écran et l’absence de régression sans JavaScript.

## Exigences fonctionnelles

- Le bouton `Plein écran` standard reste présent hors plein écran avec `aria-pressed`.
- En plein écran, `.miweb-slide-controls` n’est pas affiché.
- En plein écran, `#diaporama-title` n’est pas affiché.
- En plein écran, `.miweb-slide-title` n’est pas affiché.
- En plein écran, `.fr-accordions-group` reste affiché immédiatement sous la slide active, avec les mêmes bords gauche et droit que `.miweb-slide-frame`.
- En plein écran, une mini-barre de projection est affichée.
- La mini-barre contient `Précédente`, `Suivante` et `Quitter le plein écran`.
- Les boutons projection sont des éléments `<button type="button">`.
- Le bouton `Quitter le plein écran` appelle `document.exitFullscreen()`.
- La sortie native par `Échap` reste possible.
- L’entrée en plein écran force le mode une slide active si le mode toutes les slides était actif.
- L’entrée en plein écran déplace le focus vers `Quitter le plein écran`.
- Le focus revient sur le bouton `Plein écran` après sortie du plein écran.
- En plein écran, les boutons projection et les raccourcis clavier existants ne déplacent jamais le focus vers un titre de slide masqué.
- Les boutons `Précédente` et `Suivante` de projection utilisent les mêmes règles de désactivation que les boutons standard.
- Un statut non visuel de projection annonce le numéro et le titre de la slide active.
- Si `Précédente` ou `Suivante` devient désactivé après activation, le focus est déplacé vers un bouton encore actif de la mini-barre.

## Exigences d’accessibilité

- Aucun contrôle focusable masqué ne doit rester atteignable dans l’ordre de tabulation du plein écran.
- La mini-barre doit avoir un nom accessible, par exemple `aria-label="Contrôles de projection"`.
- Chaque bouton doit avoir un intitulé visible explicite.
- Les noms accessibles de `Précédente` et `Suivante` doivent préciser l’action, par exemple `Slide précédente` et `Slide suivante`, tout en conservant l’intitulé visible dans le nom accessible.
- Le focus visible doit être conservé sur les boutons de projection.
- Les états `disabled` des boutons précédent et suivant doivent refléter la première ou la dernière slide.
- Le changement de slide doit mettre à jour un statut annoncé aux technologies d’assistance avec `role="status"` ou avec `aria-live="polite"` et `aria-atomic="true"`.
- Le diaporama doit conserver un nom accessible fiable même si `#diaporama-title` n’est pas affiché visuellement en plein écran.
- La slide active doit conserver son alternative textuelle pertinente en projection via l’accordéon visible et utilisable au clavier.
- Les alternatives textuelles ne doivent pas être supprimées du site ; elles restent disponibles hors plein écran et dans `alternatives.html`.
- La mini-barre doit rester utilisable sans défilement horizontal à 320 px de large et à zoom élevé.
- Le texte de la mini-barre doit conserver un contraste minimal de 4,5:1 et l’indicateur de focus un contraste minimal de 3:1, y compris si la barre est superposée à l’image.
- Le mode sans JavaScript doit conserver le contenu consultable hors plein écran.

## Spécifications d’implémentation

La source de vérité de l’implémentation est `miweb-objectifs-2030-v1/build.py`. Les fichiers HTML générés ne doivent pas être modifiés à la main : toute évolution du HTML, du CSS ou du JavaScript doit passer par `build.py`, puis par la régénération du site. Cette contrainte évite les divergences entre source, pages générées et politique CSP.

La politique CSP est recalculée par le build à partir de `CUSTOM_CSS` et `MAIN_JS`. Modifier ces blocs dans `build.py` est compatible avec la CSP existante, à condition de relancer la génération avant les validations HTML.

Les attributs de ciblage JavaScript doivent rester explicites et testables. Les noms exacts peuvent évoluer, mais le contrat recommandé est :

- `data-projection-controls` pour la mini-barre ;
- `data-projection-previous` pour le bouton précédent ;
- `data-projection-next` pour le bouton suivant ;
- `data-projection-exit` pour le bouton de sortie ;
- `data-projection-status` pour le statut non visuel.

La mini-barre ne doit pas utiliser l’attribut HTML `hidden` si son affichage dépend uniquement de `#diaporama:fullscreen`, sauf si le script retire explicitement cet attribut à l’entrée en plein écran. Un masquage CSS contrôlé par `display: none` hors plein écran et `display: flex` dans `#diaporama:fullscreen` est plus simple à vérifier.

La navigation standard peut être retirée du rendu en plein écran avec `display: none`, car ses contrôles ne doivent pas rester atteignables au clavier pendant la projection.

L’accordéon d’alternative textuelle ne doit pas être retiré du rendu. Il doit rester dans la slide active, immédiatement sous la figure, avec la même largeur maximale et les mêmes bords gauche et droit que `.miweb-slide-frame`, un focus visible sur son bouton et un comportement DSFR standard `aria-expanded` / `aria-controls`.

Les titres ne doivent pas être supprimés du HTML généré. La préférence d’implémentation est de les masquer en plein écran avec une classe de masquage visuel compatible technologies d’assistance, par exemple `fr-sr-only`, plutôt qu’avec `display: none`. Si leur rendu plein écran utilise `display: none`, le conteneur `#diaporama` et la slide active doivent recevoir un autre nom accessible stable.

Le statut live annonce seulement le numéro et le titre de la slide. Le contenu détaillé de l’alternative textuelle reste porté par l’accordéon et ne doit pas être annoncé automatiquement en entier à chaque navigation.

Il ne faut pas créer de piège de focus artificiel. Le parcours clavier doit rester court et cohérent, mais la sortie doit reposer sur le bouton dédié et sur le comportement natif `Échap`.

Le code actuel déplace le focus vers `[data-slide-title]` lors de certains changements de slide. Cette stratégie reste adaptée hors plein écran. En mode projection, elle doit être neutralisée ou redirigée vers un contrôle visible de la mini-barre, sinon le focus peut se retrouver sur un titre non affiché.

## Métriques de succès

- `python3 miweb-objectifs-2030-v1/build.py` réussit.
- `python3 -m unittest discover -s miweb-objectifs-2030-v1/tests` réussit.
- `npx --yes html-validate miweb-objectifs-2030-v1/index.html miweb-objectifs-2030-v1/alternatives.html miweb-objectifs-2030-v1/accessibilite.html index.html` réussit.
- `npx --yes vnu-jar --errors-only miweb-objectifs-2030-v1/index.html miweb-objectifs-2030-v1/alternatives.html miweb-objectifs-2030-v1/accessibilite.html index.html` réussit.
- Un test navigateur confirme que la mini-barre est visible en plein écran.
- Un test navigateur confirme que `.miweb-slide-controls`, `.miweb-slide-title` et `#diaporama-title` ne sont pas visibles en plein écran.
- Un test navigateur confirme que `.fr-accordions-group` reste visible, aligné sous `.miweb-slide-frame` et utilisable au clavier en plein écran.
- Un test clavier confirme que `Tab` atteint les boutons projection dans un ordre cohérent.
- Un test clavier confirme que `Quitter le plein écran` fonctionne.
- Un test confirme que le focus arrive sur `Quitter le plein écran` après l’entrée en plein écran.
- Un test confirme que le focus revient sur `Plein écran` après la sortie.
- Un test confirme que les boutons projection, `ArrowLeft`, `ArrowRight`, `Home` et `End` ne focalisent pas un titre masqué en plein écran.
- Un test confirme qu’aucun bouton de navigation standard n’est focusable pendant le plein écran.
- Un test confirme que l’accordéon d’alternative textuelle de la slide active reste consultable en projection.
- Un test confirme qu’une action qui désactive `Précédente` ou `Suivante` ne laisse pas le focus sur un bouton désactivé.
- Un test à 320 px de large ou équivalent confirme l’absence de défilement horizontal de la mini-barre.
- Un test vérifie les noms accessibles des trois boutons de projection.
- Un contrôle visuel ou instrumenté vérifie le contraste du texte et du focus de la mini-barre.
- Un contrôle visuel confirme que la slide active est cadrée sans chevauchement incohérent.

Si l’environnement Playwright ne permet pas de déclencher réellement la Fullscreen API, les tests navigateur doivent au minimum vérifier la présence du code `fullscreenchange`, les sélecteurs CSS `#diaporama:fullscreen`, la structure HTML de la mini-barre et le comportement des fonctions JavaScript isolables.

## Hors périmètre

- Refonte complète du diaporama.
- Ajout d’un mode présentateur avec notes.
- Ajout d’une télécommande ou d’un second écran.
- Suppression des alternatives textuelles.
- Déclaration de conformité RGAA.
- Raccourcis clavier documentés dans l’interface.
- Boucle de focus forcée dans le conteneur plein écran.

## Risques et parades

**Risque** : masquer la navigation standard rend des boutons encore focusables.

**Parade** : utiliser une règle CSS qui masque réellement les contrôles standard en plein écran et vérifier le parcours Tab.

**Risque** : la sortie du plein écran devient dépendante de `Échap`.

**Parade** : ajouter un bouton visible `Quitter le plein écran` dans la mini-barre.

**Risque** : les titres masqués dégradent la structure perçue par technologies d’assistance.

**Parade** : limiter le masquage à l’état plein écran et conserver la structure complète hors plein écran.

**Risque** : l’accordéon d’alternative textuelle gêne la projection ou devient difficile à atteindre.

**Parade** : placer l’accordéon juste sous la slide avec les mêmes bords que le cadre de slide, préserver son comportement DSFR standard, et vérifier le parcours clavier en plein écran.

**Risque** : le bouton qui a déclenché le plein écran devient masqué alors qu’il conserve le focus.

**Parade** : déplacer le focus vers le bouton `Quitter le plein écran` dès que `fullscreenchange` confirme l’entrée en plein écran.

**Risque** : le mode `Afficher toutes les slides` produit une projection confuse avec plusieurs slides visibles.

**Parade** : forcer le retour au mode une slide active avant ou pendant l’entrée en plein écran.

**Risque** : la logique existante de changement de slide place le focus sur un titre masqué en projection.

**Parade** : conditionner `focusCurrentTitle()` à l’absence de plein écran, ou rediriger le focus vers un bouton visible de la mini-barre quand `document.fullscreenElement === fullscreenTarget`.

**Risque** : `Précédente` ou `Suivante` devient désactivé alors qu’il porte le focus.

**Parade** : après chaque changement de slide, si `document.activeElement` est un bouton de projection désormais désactivé, déplacer le focus vers `Quitter le plein écran` ou vers l’autre bouton de navigation encore actif.

## Points à ne pas faire

- Ne pas supprimer les titres, accordéons ou alternatives du HTML généré.
- Ne pas compter uniquement sur les flèches clavier pour naviguer.
- Ne pas ajouter de `tabindex` positif.
- Ne pas masquer un bouton encore focusé sans déplacer le focus.
- Ne pas focaliser un titre de slide non visible en mode projection.
- Ne pas masquer l’accordéon d’alternative textuelle en mode projection.
- Ne pas mettre le contenu détaillé de l’accordéon dans une région live qui le relirait entièrement à chaque navigation.
- Ne pas faire de la mini-barre une copie de la navigation standard complète.

## Changelog

| Date | Auteur | Changement |
|------|--------|------------|
| 2026-06-20 | Alex + Codex | Création du PRD pour le mode projection plein écran |
| 2026-06-20 | Alex + Codex | Durcissement du focus, du statut de projection et des exigences de masquage |
| 2026-06-20 | Alex + Codex | Ajout du garde-fou sur le focus des titres masqués pendant la projection |
| 2026-06-20 | Alex + Codex | Ajout de la contrainte source de vérité `build.py` et CSP |
| 2026-06-20 | Alex + Codex | Ajout des garde-fous sur l’équivalent textuel, le statut atomique, le focus désactivé et le reflow |
| 2026-06-20 | Alex + Codex | Ajout des exigences de nom accessible et de contraste des contrôles |
| 2026-06-20 | Alex + Codex | Conservation de l’accordéon d’alternative textuelle aligné sous la slide |
