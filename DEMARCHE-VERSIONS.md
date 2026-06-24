# Démarche de publication des variantes

Cette procédure sert à publier une nouvelle variante `miweb-objectifs-2030-vN` ou une variante thématique nommée, en conservant le fonctionnement des versions déjà publiées. Par défaut, seules les images de slides, les alternatives textuelles et les sources de la variante changent.

Les variantes déjà publiées `miweb-objectifs-2030-v1` à `miweb-objectifs-2030-v4` sont des références stables : ne pas les modifier pour publier une nouvelle variante.

## Sources

- Images validées : dossier `outputs/ia-slides/...` du projet actif.
- Site publié : `/Users/alex/Claude/projets-heberges/miweb-objectifs-2030`.
- Source éditoriale : note validée utilisée pour produire le storyboard de la variante.

## Étapes

1. Créer le dossier de variante à partir de la dernière version publiée, ou initialiser un dossier thématique nommé en réutilisant le même modèle de site.
2. Copier les images validées `slide-01.png` à `slide-NN.png` dans `assets/slides/`, selon le nombre réel de slides de la variante.
3. Copier le storyboard de génération dans `source/`, avec un nom explicite pour la variante.
4. Mettre à jour `slides.json` : titre, alternative courte, description, textes visibles et message.
5. Adapter `build.py` si la nouvelle variante n’est pas encore listée dans `PUBLISHED_VERSIONS` ou si son libellé public ne suit pas le format `Version N`.
6. Lancer `python3 <dossier-variante>/build.py`.
7. Vérifier :
   - `python3 -m unittest discover -s <dossier-variante>/tests` ;
   - `npx --yes html-validate <dossier-variante>/index.html <dossier-variante>/alternatives.html <dossier-variante>/accessibilite.html index.html` ;
   - `npx --yes vnu-jar --errors-only <dossier-variante>/index.html <dossier-variante>/alternatives.html <dossier-variante>/accessibilite.html index.html`.
8. Inspecter localement au navigateur :
   - `<dossier-variante>/#slide-01` ;
   - `<dossier-variante>/?projection=1#slide-01` ;
   - `<dossier-variante>/alternatives.html`.
9. Vérifier que la navigation par swipe horizontal est conservée dans le diaporama, dans les pages générées et dans les tests de contrat.
10. Mettre à jour le README racine et pousser sur GitHub Pages.

## Variantes thématiques nommées

Utiliser un dossier thématique nommé quand le jeu de slides ne remplace pas les variantes `Objectifs 2030` V1 à V4, mais ajoute un nouveau support dans le même modèle GitHub Pages.

Pour une variante thématique :

- garder le modèle de publication existant : `index.html`, `alternatives.html`, `accessibilite.html`, `alternatives.md`, `assets/slides/`, `assets/downloads/`, `source/` et `slides.json` ;
- conserver les images validées dans `assets/slides/` ;
- renseigner `slides.json` comme source canonique des transcriptions : `alt`, `description`, `textes_visibles` et `message` ;
- vérifier que les transcriptions apparaissent à la fois dans les accordéons de la présentation, dans `alternatives.html` et dans `alternatives.md` ;
- lister la variante dans l’accueil racine seulement après génération et vérification ;
- ne pas renommer, déplacer ni modifier `miweb-objectifs-2030-v1`, `miweb-objectifs-2030-v2`, `miweb-objectifs-2030-v3` ou `miweb-objectifs-2030-v4`.

## Variantes publiées

- V1 : variante initiale de 10 slides.
- V2 : variante de 10 slides centrée sur la chaîne qualité durable.
- V3 : variante de 8 slides centrée sur la dette visible, les portes qualité, le run, la mutualisation et les arbitrages.
- V4 : variante de 8 slides centrée sur la chaîne de preuve de l’accès réel, avec cadrage, contrôles croisés, run, mutualisation, arbitrages et indicateurs consolidables.
- Jeu 5 : support thématique « Offre mutualisée de listes de diffusion », version condensée.
- Jeu 6 : support thématique « Offre mutualisée de listes de diffusion », version longue.

## Comportement tactile commun

Les variantes 1 à 4 et les jeux 5 et 6 partagent une navigation par swipe horizontal dans le diaporama. Toute future variante ou tout futur jeu de slides doit conserver ce comportement dans son `build.py`, ses pages générées et ses tests de contrat :

- swipe vers la gauche : slide suivante ;
- swipe vers la droite : slide précédente ;
- seuil minimal : 48 pixels horizontaux ;
- protection du scroll vertical : le geste horizontal doit dominer le mouvement vertical ;
- exclusion des cibles interactives : liens, boutons, champs, accordéons et contrôles DSFR.

Validation réalisée avant publication des jeux 5 et 6 : test iPhone hors réseau local via serveur local `127.0.0.1:8010` exposé temporairement avec `localtunnel`, puis contrôle des deux jeux sur `#slide-06`.

## Points de vigilance

- Ne pas modifier une version déjà publiée pour créer une variante.
- Ne pas publier une image sans alternative textuelle correspondante.
- Ne pas publier un site GitHub Pages qui expose les images sans leurs transcriptions.
- Ne pas inventer de chiffre, de seuil ou d’engagement absent de la note source.
- Ne pas présenter la variante comme auditée RGAA sans audit dédié.
- Garder l’accueil racine cohérent avec la dernière version publiée.
