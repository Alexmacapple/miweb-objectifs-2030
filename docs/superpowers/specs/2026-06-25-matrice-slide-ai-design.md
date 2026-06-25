# Design - matrice slide IA

## État actuel - 2026-06-25

La matrice décrite dans ce document existe dans `matrice-slide-ai/`.

État opérationnel :

- `create_variant.py` crée un dossier de jeu autonome sans publier ;
- `build.py` génère les pages et le ZIP du jeu sans écrire l’accueil racine ;
- `publish_variant.py` vérifie le jeu, met à jour `published-versions.json`, puis régénère `index.html` racine ;
- `tests/test_matrix_workflow.py` couvre création, build et publication séparée dans un dépôt temporaire ;
- `tests/test_site_contracts.py` couvre les contrats de rendu, projection, swipe, CSP et assets ;
- la documentation active est dans `matrice-slide-ai/README.md`, `matrice-slide-ai/MODE-OPERATOIRE.md`, `DEMARCHE-VERSIONS.md` et `GUIDE-REGENERATION-SITES-SLIDES.md`.

Le reste du document garde la décision de conception et les critères d’acceptation initiaux.

## Décision

Créer à la racine du dépôt un répertoire `matrice-slide-ai/` servant de matrice canonique pour les prochains jeux de slides générés avec IA.

La matrice doit être à la fois :

- une base complète et maintenue du modèle de diaporama ;
- un point de départ duplicable pour créer un nouveau jeu autonome ;
- la source de référence pour les comportements communs, notamment le swipe horizontal.

Les variantes existantes 1 à 4 et les jeux 5 et 6 restent publiés comme dossiers autonomes. La matrice ne doit pas les remplacer silencieusement.

## Objectif

Réduire la duplication de maintenance entre les `build.py` existants sans casser le modèle GitHub Pages actuel.

Le problème à éviter est celui observé avec le swipe : une amélioration commune ne doit plus obliger à corriger manuellement chaque nouveau générateur.

## Passe PRD intégrée

Vision : faire de `matrice-slide-ai/` une fabrique maintenue de jeux de slides statiques, pas une septième variante publiée.

Problème : le modèle actuel marche, mais chaque nouveau `build.py` recopie une grande partie du comportement. Cela rend les évolutions communes coûteuses et favorise les oublis.

Options évaluées :

- Option A retenue : matrice canonique, duplication autonome, catalogue racine et publication séparée. Elle protège GitHub Pages et la phase brouillon, au prix d’un suivi de dérive entre matrice et jeux générés.
- Option B rejetée : moteur central importé par toutes les variantes. Elle réduit la duplication, mais casse l’autonomie des dossiers publiés.
- Option C rejetée : simple template copié à la main. Elle est rapide, mais ne résout ni la dérive ni la preuve de build.

Métriques de succès :

- création et build d’un jeu temporaire sans modification de `index.html` racine ;
- zéro import relatif vers `matrice-slide-ai` dans le jeu généré ;
- tests unitaires, `html-validate` et `vnu-jar` réussis sur le jeu généré ;
- publication racine impossible sans `publish_variant.py`.

Limites LLM à verrouiller : ne pas confondre générer et publier, template et preuve, factorisation et dépendance centrale, exemple JSON et variante publiable.

## Constats de relecture

- Les générateurs existants font environ 1000 lignes chacun : recopier ce format dans la matrice créerait un nouveau bloc difficile à faire évoluer.
- Les variantes récentes savent réécrire l’accueil racine via une liste `PUBLISHED_VERSIONS`, mais cette liste est dupliquée dans les `build.py`.
- Les tests existants ne vérifient pas seulement le swipe : ils protègent aussi les alternatives, la CSP, les favicons, le plein écran, les liens sans `href="#"`, le ZIP et la structure DSFR.
- Le modèle sépare donc le point d’entrée simple, le générateur copiable et le catalogue de publication.

## Périmètre proposé

Le dossier `matrice-slide-ai/` contient au minimum :

```text
matrice-slide-ai/
  README.md
  MODE-OPERATOIRE.md
  __init__.py
  build.py
  create_variant.py
  publish_variant.py
  slides.example.json
  published-versions.example.json
  tests/
    test_matrix_workflow.py
    test_site_contracts.py
  assets/
    favicons/
  source/
    storyboard.example.md
```

`build.py` reste le point d’entrée générique complet pour l’utilisateur. L’implémentation actuelle garde un générateur monolithique copié dans chaque jeu pour préserver l’autonomie ; une factorisation future ne devra pas créer de dépendance runtime vers `matrice-slide-ai/`.

Le générateur doit produire : page principale, alternatives, page accessibilité, Markdown des alternatives, ZIP de slides, CSP, favicons, mode projection, affichage toutes slides, navigation clavier et swipe tactile.

`create_variant.py` doit créer un dossier autonome de nouveau jeu à partir de la matrice. Le dossier généré doit pouvoir être publié sans dépendance d’exécution vers `matrice-slide-ai/`.

Pour lever la tension entre factorisation et autonomie, `create_variant.py` copie dans le dossier généré le code de génération nécessaire. L’option d’un sous-dossier local `generator/` n’est pas retenue à date ; si elle l’était plus tard, elle devrait être copiée dans chaque jeu. Un jeu publié ne doit pas importer du code depuis `../matrice-slide-ai/`.

`published-versions.example.json` propose une source de vérité explicite pour l’accueil racine. Le choix retenu est d’utiliser un catalogue racine versionné au lieu de recopier `PUBLISHED_VERSIONS` dans chaque nouveau `build.py`.

Concrètement, ce catalogue dirait une seule fois :

```json
[
  {
    "slug": "miweb-offre-mutualisee-listes-diffusion-2026-longue",
    "label": "Offre mutualisée listes de diffusion - version longue"
  }
]
```

Le bénéfice attendu est simple : pour publier un nouveau jeu sur l’accueil, `publish_variant.py` ajoute ou met à jour une entrée au catalogue, puis l’accueil se régénère depuis cette liste unique.

## Interface cible

L’interface minimale de création doit rester explicite et non destructive :

```bash
python3 matrice-slide-ai/create_variant.py \
  --slug nouveau-jeu \
  --title "Titre public" \
  --storyboard chemin/storyboard.md \
  --slides-dir chemin/assets/slides
```

Contraintes de l’interface :

- `--slug` doit être un nom de dossier ASCII en minuscules, sans espace, compatible URL ;
- la commande doit refuser d’écraser un dossier existant sans option explicite ;
- la commande doit copier le storyboard dans `source/`, pas seulement le référencer ;
- la commande doit copier les images `slide-*.png` dans `assets/slides/` si `--slides-dir` est fourni ;
- la commande doit créer un `slides.json` à compléter ou initialisé depuis un exemple ;
- la commande ne doit pas modifier `index.html` à la racine ;
- l’ajout à l’accueil racine doit passer par `publish_variant.py`, pas par `create_variant.py`.

L’interface de publication racine doit être séparée de la création :

```bash
python3 matrice-slide-ai/publish_variant.py --slug nouveau-jeu
```

`publish_variant.py` doit ajouter ou mettre à jour l’entrée du jeu dans `published-versions.json`, puis régénérer l’accueil racine depuis ce catalogue. Il doit refuser de publier un jeu dont le dossier, les pages générées, les tests ou le ZIP attendu sont absents.

## Contraintes

- La matrice doit rester compatible avec GitHub Pages statique.
- Les dossiers générés doivent rester autonomes : HTML, JSON, sources, assets, tests, ZIP et code de génération nécessaire.
- Le swipe doit rester intégré par défaut dans le modèle.
- Les tests de contrat doivent vérifier la présence du swipe, du plein écran, des alternatives et des liens de téléchargement.
- Les variantes déjà publiées ne doivent être modifiées que par décision explicite.
- Les URL temporaires de tunnel ne doivent pas devenir des liens durables.
- Aucun chiffre, engagement, audit ou niveau de conformité ne doit être inventé hors source éditoriale.
- Le générateur ne doit pas dépendre d’un service externe pour produire les pages.
- Toute écriture de l’accueil racine doit venir d’une source de vérité identifiable.
- Un build ordinaire de variante doit écrire par défaut seulement dans le dossier de la variante.
- Seul `publish_variant.py` doit modifier `published-versions.json` et l’accueil racine.
- Le schéma `slides.json` doit rester strict : `numero`, `titre`, `image`, `alt`, `description`, `textes_visibles`, `message`.
- Les images listées dans `slides.json` doivent exister dans `assets/slides/`.
- La matrice doit documenter la version ou l’empreinte de matrice utilisée pour générer un jeu, afin de repérer les dérives.

## Mode opératoire cible

1. Préparer les images de slides et le storyboard source.
2. Créer le dossier autonome avec `create_variant.py`.
3. Copier le storyboard dans le nouveau dossier généré.
4. Renseigner `slides.json` avec titres, alternatives, descriptions, textes visibles et message à retenir.
5. Lancer le `build.py` du nouveau jeu.
6. Lancer les tests du nouveau jeu.
7. Valider les pages HTML avec `html-validate` et `vnu-jar`.
8. Tester localement le diaporama, les alternatives et le ZIP.
9. Si nécessaire, exposer temporairement le serveur local avec `localtunnel` pour test iPhone hors réseau local.
10. Ajouter le nouveau jeu à l’accueil racine avec `publish_variant.py` seulement après validation.

## Critères d’acceptation

- Un nouveau jeu peut être créé depuis `matrice-slide-ai/` sans recopier manuellement un ancien dossier.
- Le nouveau jeu généré contient le swipe horizontal dès la première génération.
- Le build produit `index.html`, `alternatives.html`, `accessibilite.html`, `alternatives.md` et un ZIP de slides.
- Les tests de contrat échouent si le swipe, le mode projection ou les alternatives disparaissent.
- La documentation explique clairement quand modifier la matrice et quand rétroporter une amélioration aux anciennes variantes.
- La création d’un nouveau jeu peut être testée dans un dossier temporaire sans modifier l’accueil racine.
- L’ajout à l’accueil racine est une étape explicite, séparée de la simple génération.
- Le dossier généré ne contient aucun import relatif vers `matrice-slide-ai`.
- Le build d’un jeu temporaire n’écrit pas `index.html` racine.
- `create_variant.py` ne propose pas d’option `--publish`.
- `publish_variant.py` refuse de publier un jeu non généré ou non vérifiable.
- Le test de contrat vérifie au minimum : schéma `slides.json`, images présentes, alternatives exposées, swipe, plein écran, CSP sans `unsafe-inline`, favicon locale, absence de `href="#"`, ZIP présent, liens de téléchargement et catalogue racine si publication demandée.

## Passage PDG

Contrôle : auto-vérification PDG, pas une revue indépendante.

Connus connus : les variantes 1 à 4 et les jeux 5 et 6 sont autonomes ; le swipe est commun aux six diaporamas ; GitHub Pages publie des fichiers statiques ; les sorties HTML et ZIP viennent des `build.py`.

Connus inconnus : la stratégie de rétroportage des futures améliorations de matrice vers des jeux déjà publiés reste à décider au cas par cas.

Inconnus connus : « matrice » ne signifie pas moteur central obligatoire ; « générer » ne signifie pas publier ; remplacer les anciens dossiers ou les faire dépendre d’un moteur central est interdit hors décision explicite.

Inconnus inconnus : dérive entre matrice et jeux générés, différences de comportement mobile, stabilité des ZIP et risque qu’un LLM crée seulement un template sans prouver le build réel.

Mauvais chemin d’implémentation : architecture parallèle, import depuis `../matrice-slide-ai/generator`, écriture racine par défaut depuis un build de variante, modification des anciennes variantes sans nécessité, validation limitée à la présence de fichiers.

Garde-fous ajoutés : génération autonome, tests de contrat sur les comportements communs, création testable dans un dossier temporaire sans toucher `index.html`, preuve par génération réelle depuis la matrice.

Comportement existant à préserver : publication statique GitHub Pages ; structure `index.html`, `alternatives.html`, `accessibilite.html`, `slides.json`, `assets/slides/`, `assets/downloads/`, `source/` ; navigation clavier, projection, alternatives textuelles, ZIP et swipe horizontal.

Raccourcis interdits : copier une variante sans nettoyer ses libellés, hand-éditer le HTML généré, publier sans alternatives, traiter une URL `loca.lt` comme preuve de publication, confondre `slides.example.json` avec une variante publiable.

Preuve de régression requise : création et build d’un jeu temporaire depuis `matrice-slide-ai/create_variant.py`, tests unitaires, `html-validate`, `vnu-jar`, contrôle local par serveur HTTP, test iPhone hors réseau local si la navigation tactile change.
