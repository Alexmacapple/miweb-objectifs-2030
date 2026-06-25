# Objectifs 2030 - accessibilité numérique

Site public : <https://alexmacapple.github.io/miweb-objectifs-2030/>

Ce dépôt publie des variantes web DSFR, statiques et accessibles des slides MiWeb « Objectifs 2030 - accessibilité numérique », ainsi que des supports thématiques produits avec le même modèle de publication.

## Pourquoi

Le site sert à comparer plusieurs variantes visuelles d’un même support sans perdre la traçabilité : chaque version garde ses images, ses alternatives textuelles, son storyboard source et son ZIP.

Le principe Saint-Exupéry s’applique ici : ne garder que ce qui sert la lecture, l’accessibilité, la comparaison des variantes et la publication. Une version ne doit pas accumuler de fonctionnalités ou de fichiers décoratifs.

## Versions

- Version 1 : <https://alexmacapple.github.io/miweb-objectifs-2030/miweb-objectifs-2030-v1/>
- Version 2 : <https://alexmacapple.github.io/miweb-objectifs-2030/miweb-objectifs-2030-v2/>
- Version 3 : <https://alexmacapple.github.io/miweb-objectifs-2030/miweb-objectifs-2030-v3/>
- Version 4 : <https://alexmacapple.github.io/miweb-objectifs-2030/miweb-objectifs-2030-v4/>

## Supports thématiques

- Jeu 5 - Offre mutualisée de listes de diffusion, version condensée : <https://alexmacapple.github.io/miweb-objectifs-2030/miweb-offre-mutualisee-listes-diffusion-2026-condensee/>
- Jeu 6 - Offre mutualisée de listes de diffusion, version longue : <https://alexmacapple.github.io/miweb-objectifs-2030/miweb-offre-mutualisee-listes-diffusion-2026-longue/>

## Accès directs dernière version publiée

- Présentation plein écran : <https://alexmacapple.github.io/miweb-objectifs-2030/miweb-offre-mutualisee-listes-diffusion-2026-longue/?projection=1#slide-01>
- Toutes les slides : <https://alexmacapple.github.io/miweb-objectifs-2030/miweb-offre-mutualisee-listes-diffusion-2026-longue/?slides=all#diaporama>
- Alternatives textuelles : <https://alexmacapple.github.io/miweb-objectifs-2030/miweb-offre-mutualisee-listes-diffusion-2026-longue/alternatives.html>
- Page accessibilité : <https://alexmacapple.github.io/miweb-objectifs-2030/miweb-offre-mutualisee-listes-diffusion-2026-longue/accessibilite.html>

## Organisation

- `index.html` : accueil des versions.
- `miweb-objectifs-2030-v1/` : diaporama V1, alternatives, page accessibilité et sources.
- `miweb-objectifs-2030-v2/` : diaporama V2, alternatives, page accessibilité et sources.
- `miweb-objectifs-2030-v3/` : diaporama V3, alternatives, page accessibilité et sources.
- `miweb-objectifs-2030-v4/` : diaporama V4, alternatives, page accessibilité et sources.
- `miweb-offre-mutualisee-listes-diffusion-2026-condensee/` : support thématique condensé, alternatives, page accessibilité et sources.
- `miweb-offre-mutualisee-listes-diffusion-2026-longue/` : support thématique long, alternatives, page accessibilité et sources.
- `matrice-slide-ai/` : matrice de création des futurs jeux autonomes.
- `skills/progressive-disclosure-slides/` : skill agnostique pour générer des slides PDS indépendamment d'un moteur image.
- `miweb-objectifs-2030-v1/source/storyboard-slides-accessibilite-2030.md` : storyboard source V1.
- `miweb-objectifs-2030-v2/source/storyboard-v2.md` : storyboard source V2.
- `miweb-objectifs-2030-v3/source/storyboard-v3.md` : storyboard source V3.
- `miweb-objectifs-2030-v4/source/storyboard-v4.md` : storyboard source V4.
- `slides.json` dans chaque version : titres, alternatives textuelles, descriptions et messages.
- `build.py` dans chaque version : génération HTML, Markdown et ZIP.
- `DEMARCHE-VERSIONS.md` : procédure pour publier les futurs jeux.

## Créer un nouveau jeu

La voie recommandée passe par la matrice :

```bash
python3 matrice-slide-ai/create_variant.py \
  --slug nouveau-jeu \
  --title "Titre public" \
  --storyboard chemin/storyboard.md \
  --slides-dir chemin/assets/slides
```

Ensuite :

```bash
python3 nouveau-jeu/build.py
python3 -m unittest discover -s nouveau-jeu/tests
```

`build.py` génère seulement le dossier du jeu. La publication sur l’accueil racine est séparée :

```bash
python3 matrice-slide-ai/publish_variant.py --slug nouveau-jeu
```

Seul `publish_variant.py` est autorisé à modifier `published-versions.json` et `index.html` racine.

## État courant

- Dernière version publiée : `miweb-offre-mutualisee-listes-diffusion-2026-longue/`.
- Matrice active : `matrice-slide-ai/`.
- Publication racine : `publish_variant.py` écrit `published-versions.json` puis `index.html`.
- `build.py` d’un jeu ne doit générer que le dossier du jeu.

## Régénérer la dernière version publiée

```bash
python3 miweb-offre-mutualisee-listes-diffusion-2026-longue/build.py
```

## Tester localement

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

URL locale de la dernière variante publiée :

```text
http://127.0.0.1:8000/miweb-offre-mutualisee-listes-diffusion-2026-longue/
```

## Navigation tactile commune

Depuis le 25 juin 2026, les variantes 1 à 4 et les jeux 5 et 6 prennent en charge le swipe horizontal dans le diaporama sur iPhone et écrans tactiles :

- glisser vers la gauche affiche la slide suivante ;
- glisser vers la droite affiche la slide précédente ;
- les liens, boutons, accordéons et contrôles DSFR restent prioritaires et ne déclenchent pas de changement de slide ;
- le défilement vertical reste possible grâce à `touch-action: pan-y`.

Tout futur jeu de slides doit conserver ce comportement dans son `build.py`, ses pages générées et ses tests de contrat. Le comportement a été validé sur iPhone hors réseau local avec un serveur local lié à `127.0.0.1:8010`, exposé temporairement par `localtunnel`, puis testé sur `#slide-06` pour les jeux 5 et 6. Les URL `loca.lt` ne sont pas conservées comme liens durables : elles expirent avec le tunnel.

## Vérifier avant publication

```bash
python3 -m unittest discover -s matrice-slide-ai/tests
python3 -m unittest discover -s miweb-offre-mutualisee-listes-diffusion-2026-condensee/tests
python3 -m unittest discover -s miweb-offre-mutualisee-listes-diffusion-2026-longue/tests
npx --yes html-validate miweb-offre-mutualisee-listes-diffusion-2026-condensee/index.html miweb-offre-mutualisee-listes-diffusion-2026-condensee/alternatives.html miweb-offre-mutualisee-listes-diffusion-2026-condensee/accessibilite.html miweb-offre-mutualisee-listes-diffusion-2026-longue/index.html miweb-offre-mutualisee-listes-diffusion-2026-longue/alternatives.html miweb-offre-mutualisee-listes-diffusion-2026-longue/accessibilite.html index.html
npx --yes vnu-jar --errors-only miweb-offre-mutualisee-listes-diffusion-2026-condensee/index.html miweb-offre-mutualisee-listes-diffusion-2026-condensee/alternatives.html miweb-offre-mutualisee-listes-diffusion-2026-condensee/accessibilite.html miweb-offre-mutualisee-listes-diffusion-2026-longue/index.html miweb-offre-mutualisee-listes-diffusion-2026-longue/alternatives.html miweb-offre-mutualisee-listes-diffusion-2026-longue/accessibilite.html index.html
```

Pour une vérification complète après modification commune V1/V2/V3/V4 :

```bash
python3 -m unittest discover -s matrice-slide-ai/tests
python3 -m unittest discover -s miweb-objectifs-2030-v1/tests
python3 -m unittest discover -s miweb-objectifs-2030-v2/tests
python3 -m unittest discover -s miweb-objectifs-2030-v3/tests
python3 -m unittest discover -s miweb-objectifs-2030-v4/tests
npx --yes html-validate miweb-objectifs-2030-v1/index.html miweb-objectifs-2030-v1/alternatives.html miweb-objectifs-2030-v1/accessibilite.html miweb-objectifs-2030-v2/index.html miweb-objectifs-2030-v2/alternatives.html miweb-objectifs-2030-v2/accessibilite.html miweb-objectifs-2030-v3/index.html miweb-objectifs-2030-v3/alternatives.html miweb-objectifs-2030-v3/accessibilite.html miweb-objectifs-2030-v4/index.html miweb-objectifs-2030-v4/alternatives.html miweb-objectifs-2030-v4/accessibilite.html index.html
npx --yes vnu-jar --errors-only miweb-objectifs-2030-v1/index.html miweb-objectifs-2030-v1/alternatives.html miweb-objectifs-2030-v1/accessibilite.html miweb-objectifs-2030-v2/index.html miweb-objectifs-2030-v2/alternatives.html miweb-objectifs-2030-v2/accessibilite.html miweb-objectifs-2030-v3/index.html miweb-objectifs-2030-v3/alternatives.html miweb-objectifs-2030-v3/accessibilite.html miweb-objectifs-2030-v4/index.html miweb-objectifs-2030-v4/alternatives.html miweb-objectifs-2030-v4/accessibilite.html index.html
```

## Limite

Le site vise une publication accessible et a fait l’objet de vérifications techniques automatisées. Il ne vaut pas déclaration de conformité RGAA sans audit humain complet.
