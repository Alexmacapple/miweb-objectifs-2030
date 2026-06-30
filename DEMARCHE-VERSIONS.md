# Démarche de publication des variantes

Cette procédure est le chemin court pour publier une nouvelle variante `miweb-objectifs-2030-vN` ou une variante thématique nommée. Elle complète le README racine et renvoie au guide long quand il faut détailler les contrôles, l’inspection locale ou la publication GitHub Pages.

Par défaut, seules les images de slides, les alternatives textuelles et les sources de la variante changent. La génération du dossier de jeu et la publication sur l’accueil racine restent deux actions séparées.

Les variantes déjà publiées `miweb-objectifs-2030-v1` à `miweb-objectifs-2030-v4` sont des références stables : ne pas les modifier pour publier une nouvelle variante.

## Positionnement documentaire

- `README.md` : entrée courte et commandes principales.
- `DEMARCHE-VERSIONS.md` : procédure opérationnelle de publication.
- `GUIDE-REGENERATION-SITES-SLIDES.md` : mode opératoire complet pour les cas longs, l’inspection locale et les preuves.
- `matrice-slide-ai/README.md` : fonctionnement de la matrice.
- `docs/prd/`, `docs/prompts/`, `docs/goals/` : cadrages et objectifs historiques, conservés hors racine.

## Sources

- Images validées : dossier `outputs/ia-slides/...` du projet actif.
- Dépôt de publication : `/Users/alex/Claude/miweb-objectifs-2030`.
- Site public : <https://alexmacapple.github.io/miweb-objectifs-2030/>.
- Source éditoriale : note validée utilisée pour produire le storyboard de la variante.

## Chemin heureux

```bash
python3 matrice-slide-ai/create_variant.py \
  --slug <dossier-variante> \
  --title "Titre public" \
  --storyboard chemin/storyboard.md \
  --slides-dir chemin/assets/slides
python3 <dossier-variante>/build.py
scripts/validate_variant.sh <dossier-variante>
python3 matrice-slide-ai/publish_variant.py --slug <dossier-variante>
scripts/validate_variant.sh <dossier-variante>
git status --short
git diff -- README.md DEMARCHE-VERSIONS.md GUIDE-REGENERATION-SITES-SLIDES.md index.html published-versions.json <dossier-variante>
scripts/push-pages.sh
```

Si les images source sont préfixées, ajouter `--slide-prefix <prefixe>` à la commande de création. Si le jeu devient un support public durable, mettre à jour le README racine avant le diff et le push.

## Étapes

1. Préparer les images validées `slide-01.png` à `slide-NN.png`, ou noter leur préfixe si elles sont nommées autrement, et le storyboard source.
2. Créer le dossier de variante avec `matrice-slide-ai/create_variant.py`.
3. Vérifier que les images et le storyboard ont bien été copiés dans le dossier généré.
4. Mettre à jour `slides.json` : titre, alternative courte, description, textes visibles et message.
5. Lancer `python3 <dossier-variante>/build.py` pour générer seulement le dossier de variante.
6. Vérifier :
   - `scripts/validate_variant.sh <dossier-variante>`.
7. Inspecter localement au navigateur :
   - `<dossier-variante>/#slide-01` ;
   - `<dossier-variante>/?projection=1#slide-01` ;
   - `<dossier-variante>/alternatives.html`.
8. Vérifier que la navigation par swipe horizontal est conservée dans le diaporama, dans les pages générées et dans les tests de contrat.
9. Publier explicitement avec `python3 matrice-slide-ai/publish_variant.py --slug <dossier-variante>`.
10. Vérifier que `published-versions.json` et `index.html` racine ont changé uniquement après cette publication.
11. Mettre à jour le README racine si le nouveau jeu doit être documenté comme support public.
12. Pousser sur GitHub Pages avec `scripts/push-pages.sh`.

## Création avec la matrice

La matrice est le chemin recommandé pour tout nouveau jeu :

```bash
python3 matrice-slide-ai/create_variant.py \
  --slug <dossier-variante> \
  --title "Titre public" \
  --storyboard chemin/storyboard.md \
  --slides-dir chemin/assets/slides
```

Cette commande crée un dossier autonome et ne publie jamais. Elle ne change ni `index.html` racine ni `published-versions.json`.

Si le lot source utilise des noms préfixés, par exemple `checklist-span-slide-01.png`, ajouter :

```bash
--slide-prefix checklist-span-
```

La matrice copie alors les images en `assets/slides/slide-*.png`.

Optimiser les images avant le build. Si des PNG sont optimisés ou remplacés après génération, relancer `python3 <dossier-variante>/build.py` pour reconstruire le ZIP.

Dans un environnement sandboxé, les validateurs `npx` peuvent demander un accès réseau, et le serveur local peut demander une autorisation d’ouverture de port. Ces frictions sont attendues : utiliser les scripts projet pour obtenir une commande unique et une erreur explicite.

## Publication séparée

Publier seulement après génération et vérifications :

```bash
python3 matrice-slide-ai/publish_variant.py --slug <dossier-variante>
scripts/validate_variant.sh <dossier-variante>
```

`publish_variant.py` est la seule commande autorisée à modifier `published-versions.json` et `index.html` racine. Elle refuse un jeu dont les pages générées, le ZIP ou les tests sont absents ou en échec.

Après publication racine, inspecter le diff avant tout push :

```bash
git status --short
git diff -- README.md DEMARCHE-VERSIONS.md GUIDE-REGENERATION-SITES-SLIDES.md index.html published-versions.json <dossier-variante>
```

## Variantes thématiques nommées

Utiliser un dossier thématique nommé quand le jeu de slides ne remplace pas les variantes `Objectifs 2030` V1 à V4, mais ajoute un nouveau support dans le même modèle GitHub Pages.

Pour une variante thématique :

- garder le modèle de publication existant : `index.html`, `alternatives.html`, `accessibilite.html`, `alternatives.md`, `assets/slides/`, `assets/downloads/`, `source/` et `slides.json` ;
- conserver les images validées dans `assets/slides/` ;
- renseigner `slides.json` comme source canonique des transcriptions : `alt`, `description`, `textes_visibles` et `message` ;
- vérifier que les transcriptions apparaissent à la fois dans les accordéons de la présentation, dans `alternatives.html` et dans `alternatives.md` ;
- lister la variante dans l’accueil racine seulement avec `publish_variant.py`, après génération et vérification ;
- ne pas renommer, déplacer ni modifier `miweb-objectifs-2030-v1`, `miweb-objectifs-2030-v2`, `miweb-objectifs-2030-v3` ou `miweb-objectifs-2030-v4`.

## Variantes publiées

- V1 : variante initiale de 10 slides.
- V2 : variante de 10 slides centrée sur la chaîne qualité durable.
- V3 : variante de 8 slides centrée sur la dette visible, les portes qualité, le run, la mutualisation et les arbitrages.
- V4 : variante de 8 slides centrée sur la chaîne de preuve de l’accès réel, avec cadrage, contrôles croisés, run, mutualisation, arbitrages et indicateurs consolidables.
- Jeu 5 : support thématique « Offre mutualisée de listes de diffusion », version condensée.
- Jeu 6 : support thématique « Offre mutualisée de listes de diffusion », version longue.
- Jeu 7 : support thématique « SPAN / PAN - accessibilité numérique ».
- Jeu 8 : support thématique « Mise en gouvernance du SPAN ».
- Jeu 9 : support thématique « Checklist SPAN opérationnel ».
- Jeu 10 : support thématique « Émojis accessibles - réseaux sociaux », dernière version publiée.

## Comportement tactile commun

Les variantes 1 à 4 et les jeux 5 à 10 partagent une navigation par swipe horizontal dans le diaporama. Toute future variante ou tout futur jeu de slides doit conserver ce comportement dans son `build.py`, ses pages générées et ses tests de contrat :

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
- Ne pas pousser avant d’avoir vérifié le diff et l’URL publique attendue après publication.
