# Prompt site DSFR GitHub Pages pour les slides accessibles

## Statut actuel - 2026-06-25

Ce prompt est l’archive de création de la V1. Il ne décrit plus l’architecture complète du dépôt.

État courant :

- dépôt actif : `/Users/alex/Claude/projets-heberges/miweb-objectifs-2030` ;
- accueil racine : `index.html` ;
- variantes publiées : `miweb-objectifs-2030-v1/` à `miweb-objectifs-2030-v4/` ;
- supports thématiques publiés : versions condensée et longue de l’offre mutualisée de listes de diffusion ;
- matrice active : `matrice-slide-ai/` ;
- création d’un nouveau jeu : `python3 matrice-slide-ai/create_variant.py ...` ;
- publication racine : `python3 matrice-slide-ai/publish_variant.py --slug <dossier-jeu>`.

Conserver le reste du document comme prompt historique V1, pas comme procédure actuelle.

Tu dois créer un site statique GitHub Pages DSFR accessible pour héberger les slides « Objectifs 2030 - Accessibilité numérique ».

## Pourquoi / finalité

Le site sert à publier une version web accessible, partageable et versionnée des slides visuelles.

Objectifs :

- permettre la consultation des slides dans un navigateur, sans outil bureautique ;
- permettre une consultation confortable en mode page et en mode plein écran ;
- rendre les visuels accessibles grâce à des alternatives courtes et longues ;
- permettre une navigation simple au clavier, au lecteur d’écran et sans JavaScript ;
- offrir une URL stable GitHub Pages pour partager la version 1 ;
- conserver une structure compatible avec de futures versions du support.

Ce site ne remplace pas la note source et ne doit pas reformuler librement son contenu. Il sert à rendre consultables les slides finales relues, avec leur équivalent textuel.

## Dépôt cible

`/Users/alex/miweb-objectifs-2030`

## Architecture attendue

```text
miweb-objectifs-2030/
├── index.html
└── miweb-objectifs-2030-v1/
    ├── index.html
    ├── alternatives.html
    ├── accessibilite.html
    ├── slides.json
    ├── build.py
    ├── README.md
    └── assets/
        ├── slides/
        │   ├── slide-01.png
        │   ├── slide-02.png
        │   ├── slide-03.png
        │   ├── slide-04.png
        │   ├── slide-05.png
        │   ├── slide-06.png
        │   ├── slide-07.png
        │   ├── slide-08.png
        │   ├── slide-09.png
        │   └── slide-10.png
        └── downloads/
            └── miweb-objectifs-2030-v1-slides.zip
```

- `index.html` à la racine : sélecteur de versions DSFR léger.
- `miweb-objectifs-2030-v1/index.html` : diaporama accessible.
- `miweb-objectifs-2030-v1/alternatives.html` : alternatives textuelles en lecture continue.
- `miweb-objectifs-2030-v1/accessibilite.html` : page minimale, statut « Accessibilité : non auditée ».
- `miweb-objectifs-2030-v1/slides.json` : source unique des contenus.
- `miweb-objectifs-2030-v1/build.py` : génération statique.
- `miweb-objectifs-2030-v1/README.md` : synthèse courte de la v1, commandes de génération et vérifications.

## Source des images

Copier uniquement `slide-01.png` à `slide-10.png` depuis :

`/Users/alex/Claude/projets-actifs/ay11-snum-schema/projet-note-accessibilite-2030/outputs/ia-slides/2026-06-19-objectifs-2030-miweb-accessibilite-relu-sm/`

Destination :

`/Users/alex/miweb-objectifs-2030/miweb-objectifs-2030-v1/assets/slides/`

Ne pas copier la contact sheet. Ne pas copier les versions d’essai.

## Identité éditoriale

Titre du site :

`Objectifs 2030 - Accessibilité numérique`

Baseline :

`MiWeb - Juin 2026`

Version affichée discrètement :

`Version 1 - Juin 2026`

## Contraintes DSFR

- Utiliser le DSFR officiel `GouvernementFR/dsfr`, version `1.14.4`, via CDN jsdelivr.
- Importer explicitement le CSS principal DSFR, le CSS utilitaire, puis les deux scripts DSFR requis avec ces URLs :
  - `https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.14.4/dist/dsfr/dsfr.min.css`
  - `https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.14.4/dist/utility/utility.min.css`
  - `https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.14.4/dist/dsfr/dsfr.module.min.js` avec `type="module"`
  - `https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@1.14.4/dist/dsfr/dsfr.nomodule.min.js` avec `nomodule`
- Respecter les composants DSFR : en-tête, pied de page, sommaire, liens d’évitement, accordéon.
- Ne pas personnaliser la structure des composants DSFR.
- Ne pas écraser les classes `fr-*` avec du CSS custom.
- Aucun `href="#"`.
- Tous les liens du pied de page doivent pointer vers des pages ou fichiers réels.
- Utiliser un en-tête DSFR avec bloc marque République Française.
- Utiliser un pied de page inspiré du composant DSFR, volontairement restreint aux liens réels de cette v1.
- Ne pas revendiquer une conformité institutionnelle complète du pied de page si les liens obligatoires habituels ne sont pas tous présents.
- Le pied de page doit rester sémantique, accessible et cohérent visuellement avec le DSFR.
- Utiliser les liens réels uniquement :
  - `Présentation`
  - `Alternatives textuelles`
  - `Télécharger les slides`

Références DSFR à respecter :

- dépôt officiel DSFR : `https://github.com/GouvernementFR/dsfr`
- accordéon : `https://www.systeme-de-design.gouv.fr/version-courante/fr/composants/accordeon`
- accessibilité de l’accordéon : `https://www.systeme-de-design.gouv.fr/version-courante/fr/composants/accordeon/accessibilite-de-l-accordeon`
- code de l’accordéon : `https://www.systeme-de-design.gouv.fr/version-courante/fr/composants/accordeon/code-de-l-accordeon`
- en-tête : `https://www.systeme-de-design.gouv.fr/version-courante/fr/composants/en-tete`
- code de l’en-tête : `https://www.systeme-de-design.gouv.fr/version-courante/fr/composants/en-tete/code-de-l-en-tete`
- accessibilité de l’en-tête : `https://www.systeme-de-design.gouv.fr/version-courante/fr/composants/en-tete/accessibilite-de-l-en-tete`
- pied de page : `https://www.systeme-de-design.gouv.fr/version-courante/fr/composants/pied-de-page`
- code du pied de page : `https://www.systeme-de-design.gouv.fr/version-courante/fr/composants/pied-de-page/code-du-pied-de-page`
- accessibilité du pied de page : `https://www.systeme-de-design.gouv.fr/version-courante/fr/composants/pied-de-page/accessibilite-du-pied-de-page`
- sommaire : `https://www.systeme-de-design.gouv.fr/version-courante/fr/composants/sommaire`
- liens d’évitement : `https://www.systeme-de-design.gouv.fr/version-courante/fr/composants/liens-d-evitement`

Après génération, vérifier explicitement la structure HTML des composants DSFR utilisés contre ces références, en priorité :

- en-tête ;
- pied de page inspiré DSFR ;
- sommaire ;
- liens d’évitement ;
- accordéons.

## Page racine

Créer `/Users/alex/miweb-objectifs-2030/index.html`.

Exigences :

- page DSFR légère ;
- titre `Objectifs 2030 - Accessibilité numérique` ;
- section `Versions disponibles` ;
- lien ou tuile DSFR vers `miweb-objectifs-2030-v1/` ;
- phrase sobre : `D’autres versions pourront être ajoutées ultérieurement.` ;
- en-tête DSFR simple et pied de page inspiré DSFR limité aux liens réels ;
- aucun contenu lourd à la racine.

## Page principale v1

Créer `/Users/alex/miweb-objectifs-2030/miweb-objectifs-2030-v1/index.html`.

Exigences de mise en page :

- mise en page de type présentation centrée ;
- première slide visible rapidement ;
- image centrée ;
- `max-width: 1120px` ;
- `width: 100%` ;
- `height: auto` ;
- ratio 16:9 respecté ;
- boutons natifs `Précédente` et `Suivante` ;
- compteur `Slide X sur 10` ;
- sommaire DSFR permettant d’aller directement à chaque slide ;
- pas de pagination numérotée supplémentaire ;
- bouton natif `Afficher toutes les slides` / `Revenir au mode diaporama` ;
- ce bouton est un vrai bouton de bascule et doit exposer son état avec `aria-pressed="false"` puis `aria-pressed="true"` quand toutes les slides sont affichées ;
- bouton natif `Plein écran` / `Quitter le plein écran` ;
- le bouton plein écran cible le conteneur du diaporama complet, pas seulement l’image PNG ;
- en plein écran, conserver les contrôles `Précédente`, `Suivante`, `Afficher toutes les slides`, `Télécharger les slides au format ZIP` et l’accordéon d’alternative de la slide active ;
- le bouton plein écran expose son état avec `aria-pressed="false"` puis `aria-pressed="true"` quand le conteneur du diaporama est effectivement en plein écran ;
- la sortie du plein écran doit rester possible via le bouton et via le comportement natif du navigateur, notamment `Échap` ;
- si la Fullscreen API n’est pas disponible, le bouton doit être rendu inactif de manière native, sans casser la navigation du diaporama ;
- accordéon DSFR fermé par défaut sous chaque slide ;
- libellé d’accordéon : `Lire l’alternative textuelle de la slide X` ;
- pas d’aide visible sur les raccourcis clavier.

## Accessibilité de la page principale

Appliquer ces règles :

- HTML natif d’abord, ARIA seulement quand nécessaire.
- Chaque slide est une vraie `<section>` avec titre.
- Chaque image de slide est dans une `<figure>` avec `<figcaption>`.
- Pour satisfaire le contrôle RGAA 1.9 du pré-audit, chaque `<figure>` de slide doit porter `role="group"` ou `role="figure"` et un `aria-label` strictement identique au texte du `<figcaption>`.
- Le HTML initial ne doit poser aucun `hidden` sur les slides : sans JavaScript, toutes les slides doivent rester visibles.
- Après initialisation du JavaScript, seules les slides non actives sont masquées avec l’attribut `hidden`.
- Au changement de slide, déplacer le focus vers le titre de la slide active.
- Le titre de la slide active peut recevoir `tabindex="-1"` pour permettre ce focus programmatique.
- Ajouter une zone `aria-live="polite"` courte pour annoncer `Slide X sur 10`.
- Les boutons début et fin doivent être réellement `disabled`.
- Sans JavaScript, toutes les slides restent visibles en page longue.
- L’URL suit la slide active avec `#slide-01`, `#slide-02`, etc.
- Au chargement de `index.html#slide-04`, afficher directement la slide 4.
- Les liens du sommaire restent de vrais liens d’ancre vers `#slide-01` à `#slide-10`.
- Avec JavaScript activé, intercepter les liens du sommaire pour activer la slide cible avant de déplacer le focus, afin de ne jamais envoyer le focus vers une section encore masquée par `hidden`.
- Sans JavaScript, les mêmes liens du sommaire doivent fonctionner naturellement car toutes les slides restent visibles dans le flux.
- Avec JavaScript désactivé, ne pas dépendre de l’ouverture des accordéons pour accéder aux alternatives : prévoir un lien visible vers `alternatives.html` dans le contenu principal. Ce lien est le fallback obligatoire d’accès aux alternatives textuelles.
- Pas de stockage local : pas de `localStorage`.
- Focus visible et logique.
- Aucun piège clavier.
- Le mode plein écran ne doit pas créer de piège clavier : les contrôles restent atteignables, le focus visible reste conservé et la sortie native du navigateur reste disponible.
- L’état du bouton plein écran doit être synchronisé avec l’événement `fullscreenchange`, pas seulement avec le clic utilisateur.

## Navigation clavier

Comportement attendu :

- `Tab` suit l’ordre naturel.
- `Entrée` et `Espace` activent les boutons et les accordéons.
- Flèche gauche : slide précédente.
- Flèche droite : slide suivante.
- `Home` : première slide.
- `End` : dernière slide.
- `Échap` : sortie du plein écran par comportement natif du navigateur quand le mode plein écran est actif.

Ne pas afficher d’aide visible sur ces raccourcis dans l’interface. Les boutons visibles doivent suffire.

## Liens d’évitement DSFR

Placer les liens d’évitement tout en haut de la page, avant l’en-tête.

Adapter les liens d’évitement page par page : chaque lien doit pointer vers une ancre réellement présente dans la page courante.

Liens attendus sur la page principale v1 :

- `Accéder au contenu`
- `Accéder au sommaire`
- `Accéder au diaporama`
- `Accéder aux alternatives`
- `Accéder au pied de page`

Sur la page racine, `alternatives.html` et `accessibilite.html`, ne conserver que les liens pertinents et existants, par exemple `Accéder au contenu` et `Accéder au pied de page`.

Sur la page principale, le lien `Accéder aux alternatives` ne doit jamais pointer vers une zone `hidden` ni vers un panneau d’accordéon fermé. Créer une ancre stable visible, par exemple `id="alternative-active"`, placée sur le bouton ou le titre visible de l’accordéon d’alternative de la slide active, et la maintenir à jour lors des changements de slide.

## Alternatives textuelles

`slides.json` est la source unique des contenus.

Pour chaque slide, renseigner :

- numéro ;
- titre ;
- chemin image ;
- texte alternatif court ;
- description longue ;
- textes visibles ;
- message à retenir.

Format de description longue :

- un paragraphe décrivant la scène visible ;
- une liste des textes visibles ;
- une phrase `Message à retenir`.

Le texte alternatif court doit être utilisé dans l’attribut `alt` de l’image. Il doit identifier brièvement le rôle du visuel, sans reprendre la description longue. Viser 60 caractères maximum par `alt`. La description longue doit rester dans l’accordéon associé et dans `alternatives.html`.

Rédiger les descriptions longues après inspection des PNG réels, pas seulement à partir du storyboard.

Lire obligatoirement le storyboard existant avant de rédiger les alternatives :

`/Users/alex/Claude/projets-actifs/ay11-snum-schema/projet-note-accessibilite-2030/storyboard-slides-accessibilite-2030.md`

Utiliser ce storyboard comme base de sens, puis ajuster chaque alternative après inspection visuelle du PNG correspondant.

La qualité des alternatives textuelles est le point critique du projet. Après génération de `slides.json`, faire une passe de relecture humaine ou équivalente, slide par slide, pour vérifier :

- que le `alt` court identifie correctement le rôle du visuel sans décrire excessivement ;
- qu’aucun `alt` de slide ne dépasse 60 caractères ;
- que la description longue décrit bien ce qui est visible dans le PNG réel ;
- que les textes visibles listés correspondent aux textes réellement présents dans l’image ;
- que le `message à retenir` reste fidèle au storyboard et à la note source ;
- qu’aucune alternative ne transforme la slide en commentaire libre ou en résumé inventé de la note.

## Page alternatives

Créer `/Users/alex/miweb-objectifs-2030/miweb-objectifs-2030-v1/alternatives.html`.

Exigences :

- page purement textuelle ;
- aucune image ;
- HTML sémantique ;
- un seul `h1` ;
- une section par slide ;
- `h2` pour chaque slide ;
- `h3` si nécessaire ;
- paragraphes pour les descriptions ;
- listes pour les textes visibles et les messages à retenir ;
- liens explicites vers la slide correspondante dans le diaporama ;
- fil d’Ariane DSFR ;
- pied de page inspiré DSFR simplifié.

## Page accessibilité

Créer `/Users/alex/miweb-objectifs-2030/miweb-objectifs-2030-v1/accessibilite.html`.

Exigences :

- page minimale ;
- statut : `Accessibilité : non auditée` ;
- date : `Juin 2026` ;
- périmètre : `miweb-objectifs-2030-v1` ;
- mention claire : le site vise une conception accessible, mais aucun audit RGAA complet n’a encore été réalisé ;
- lien de retour vers la présentation ;
- fil d’Ariane DSFR ;
- pied de page inspiré DSFR simplifié.

Ne pas afficher la mention « non auditée » dans la page principale en dehors du lien de pied de page.

## Fil d’Ariane

- Pas de fil d’Ariane sur le diaporama principal, pour garder la première slide visible rapidement.
- Fil d’Ariane DSFR sur `alternatives.html`.
- Fil d’Ariane DSFR sur `accessibilite.html`.

## Téléchargement

Générer :

`/Users/alex/miweb-objectifs-2030/miweb-objectifs-2030-v1/assets/downloads/miweb-objectifs-2030-v1-slides.zip`

Le ZIP doit contenir uniquement :

- `slide-01.png` à `slide-10.png` ;
- `alternatives.md`.

Pas de licence ou mention d’usage spécifique dans le ZIP.

Lien visible dans l’interface :

`Télécharger les slides au format ZIP`

Le fichier `alternatives.md` du ZIP doit être généré depuis `slides.json`, avec les mêmes contenus que `alternatives.html`, dans un format Markdown lisible hors ligne.

## Génération statique

Créer :

`/Users/alex/miweb-objectifs-2030/miweb-objectifs-2030-v1/build.py`

Exigences :

- Python standard autant que possible, éviter les dépendances inutiles.
- `build.py` lit `slides.json`.
- `build.py` génère :
  - son propre `index.html` de v1, c’est-à-dire `/Users/alex/miweb-objectifs-2030/miweb-objectifs-2030-v1/index.html`
  - `alternatives.html`
  - `accessibilite.html`
  - `alternatives.md`
  - `README.md`
  - le ZIP de téléchargement
- Le `index.html` racine du dépôt est un sélecteur de versions distinct : il peut être généré par `build.py` ou maintenu séparément, mais il ne doit pas être confondu avec le diaporama v1.
- Le site publié reste 100 % statique.
- Aucun backend.
- Aucun build côté GitHub Pages.
- Tous les chemins doivent être relatifs.

## CSS

CSS custom minimal.

Contraintes :

- ne pas écraser les classes DSFR ;
- ne pas modifier la structure DSFR ;
- conserver une largeur de lecture confortable pour les alternatives ;
- rendre les slides responsives ;
- ne pas fixer une hauteur qui coupe les images.
- prévoir un style dédié pour `#diaporama:fullscreen` :
  - fond lisible ;
  - défilement possible si le contenu dépasse la hauteur disponible ;
  - contrôles visibles en haut du diaporama ;
  - image agrandie sans recadrage ni déformation ;
  - alternatives toujours accessibles sous la slide.

Ajouter un CSS print minimal :

- masquer les contrôles du diaporama à l’impression ;
- afficher toutes les slides si la page principale est imprimée ;
- optimiser `alternatives.html` pour impression ;
- conserver les titres, paragraphes, listes et liens lisibles ;
- éviter les coupures maladroites dans les sections.

## Sécurité navigateur

Le site est statique et publié sur GitHub Pages, sans possibilité fiable d’ajouter des en-têtes HTTP personnalisés.

Exigences :

- ajouter une Content Security Policy en mode enforcement via une balise `<meta http-equiv="Content-Security-Policy">` ;
- ne pas utiliser `unsafe-inline` ;
- autoriser les ressources DSFR servies par `https://cdn.jsdelivr.net` quand elles sont nécessaires ;
- autoriser les scripts avec nonce et `strict-dynamic` ;
- autoriser les styles inline uniquement par hash CSP ;
- autoriser le favicon embarqué en `data:` ;
- ne pas définir `frame-ancestors` dans la meta CSP, car cette directive est ignorée dans une balise meta et remonte une issue Chrome ;
- éviter toute erreur console liée à la CSP dans Lighthouse.

## Tests obligatoires

Vérifications statiques :

- vérifier que les 10 images existent ;
- vérifier que les pages HTML générées existent et ne sont pas vides ;
- vérifier que `alternatives.md` existe ;
- vérifier que `README.md` existe ;
- vérifier que le ZIP existe ;
- vérifier qu’aucun `href="#"` ne reste ;
- vérifier que les liens internes pointent vers des fichiers ou ancres existants ;
- vérifier que tous les liens du pied de page pointent vers des pages ou fichiers réels ;
- vérifier que la page principale reste lisible sans JavaScript : aucun `hidden` initial ne doit masquer les sections de slides avant initialisation JS ;
- vérifier que le contrôle plein écran est un bouton natif, qu’il cible le conteneur `#diaporama`, qu’il utilise `requestFullscreen`, `exitFullscreen`, `fullscreenchange` et `document.fullscreenElement`, et qu’il expose `aria-pressed` ;
- vérifier que les 10 figures de slides associent correctement l’image et la légende : `figure`, `figcaption`, `role="group"` ou `role="figure"`, et `aria-label` strictement identique au `figcaption` ;
- vérifier qu’une CSP est présente en mode enforcement, sans `unsafe-inline`, avec hash des styles inline, nonce des scripts et autorisation des ressources DSFR nécessaires ;
- vérifier que `slides.json` contient les 10 slides et que chaque slide possède `titre`, `image`, `alt`, `description`, `textes_visibles` et `message`.

Tests navigateur avec Playwright :

- lancer d’abord un serveur statique local depuis `/Users/alex/miweb-objectifs-2030`, par exemple `python3 -m http.server 8000`, et tester via `http://127.0.0.1:8000/` plutôt qu’en `file://` ;
- tester en desktop ;
- tester en mobile ;
- tester `Tab` ;
- tester les boutons `Précédente` et `Suivante` ;
- tester les flèches gauche et droite ;
- tester `Home` et `End` ;
- tester `index.html#slide-04` au chargement ;
- tester le bouton `Afficher toutes les slides` ;
- tester le retour au mode diaporama ;
- tester le bouton `Plein écran` si l’environnement Playwright autorise la Fullscreen API ; sinon vérifier au minimum la présence du bouton, son état initial, le code de synchronisation `fullscreenchange` et les styles `#diaporama:fullscreen` ;
- tester les accordéons DSFR ;
- vérifier que le focus est visible et logique ;
- vérifier que les images s’affichent et ne sont pas coupées.

Assertions minimales Playwright obligatoires :

- au chargement de `http://127.0.0.1:8000/miweb-objectifs-2030-v1/#slide-04`, le titre et l’image de la slide 4 sont visibles, et les autres slides sont masquées après initialisation JS ;
- après action sur `Suivante`, l’URL passe à l’ancre de la slide suivante et le focus arrive sur le titre de cette slide ;
- avec `Tab`, les contrôles principaux sont atteignables dans un ordre logique : liens d’évitement, en-tête, sommaire, diaporama, boutons, accordéon, pied de page ;
- le bouton `Afficher toutes les slides` rend les 10 sections visibles ;
- le bouton `Afficher toutes les slides` expose `aria-pressed="true"` en mode toutes les slides, puis revient à `aria-pressed="false"` en mode diaporama ;
- le bouton `Plein écran` est visible dans les contrôles du diaporama, expose `aria-pressed="false"` au chargement et prévoit le libellé `Quitter le plein écran` quand le plein écran est actif ;
- le mode plein écran conserve les boutons de pagination et l’accès aux alternatives textuelles dans le conteneur du diaporama ;
- les liens du sommaire activent correctement une slide même si elle était masquée par `hidden` avant le clic ;
- les accordéons s’ouvrent et se ferment avec `Entrée` et `Espace`.

Ajouter aussi une vérification sans JavaScript, par Playwright avec JavaScript désactivé ou par inspection du HTML initial :

- les 10 slides doivent être visibles dans le flux de page ;
- les ancres `#slide-01` à `#slide-10` doivent fonctionner ;
- le contenu principal doit rester consultable sans interaction JavaScript.

## Contraintes GitHub Pages

- Le dépôt cible est `git@github.com:Alexmacapple/miweb-objectifs-2030.git`.
- Le dépôt local est `/Users/alex/miweb-objectifs-2030`.
- GitHub Pages devra publier depuis la branche `main`, dossier racine.
- La racine affiche le sélecteur de versions.
- La v1 vit dans `miweb-objectifs-2030-v1/`.
- Après push, vérifier explicitement que GitHub Pages est activé sur la branche `main`, dossier racine, et que l’URL publique charge bien le sélecteur de versions puis la v1.
