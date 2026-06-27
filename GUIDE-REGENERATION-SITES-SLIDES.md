# Guide - Régénérer un site GitHub Pages depuis un jeu de slides

PDG-LARGE-FILE-JUSTIFICATION: ce guide dépasse 200 lignes parce qu’il sert de mode opératoire autonome pour régénérer un site complet depuis un jeu de slides, avec contrat de résultat, structure de fichiers, schéma `slides.json`, transcriptions, génération, validation HTML, inspection locale, publication GitHub Pages et checklist finale. Le découper ferait perdre le fil d’exécution attendu pour les prochaines variantes.

Ce document est le mode opératoire réutilisable pour publier un nouveau site statique à partir d’un jeu de slides images. Il reprend le modèle MiWeb existant : présentation web, mode projection, téléchargement ZIP, page d’accessibilité et transcriptions complètes.

Il doit être utilisé pour les prochaines variantes thématiques ou versions nommées du dépôt, sans modifier les variantes déjà publiées `miweb-objectifs-2030-v1` à `miweb-objectifs-2030-v4`.

## Déclencheur

Utiliser ce guide quand il faut publier un nouveau site GitHub Pages à partir :

- d’un dossier contenant des images `slide-01.png`, `slide-02.png`, etc., ou des images préfixées comme `checklist-span-slide-01.png` ;
- d’un storyboard ou d’une note source ;
- d’une demande de publication avec alternatives textuelles ;
- d’une variante thématique qui ne remplace pas V1, V2, V3 ou V4.

Ne pas utiliser ce guide pour modifier une slide isolée dans une version déjà publiée, corriger une faute dans un HTML généré, ou créer un nouveau framework de site.

## Contrat de résultat

Chaque variante publiée doit produire un dossier autonome contenant :

- `index.html` : présentation web accessible avec navigation clavier ;
- `alternatives.html` : transcriptions complètes des slides ;
- `alternatives.md` : version Markdown des transcriptions ;
- `accessibilite.html` : état d’accessibilité du site ;
- `assets/slides/` : images publiées ;
- `assets/downloads/` : ZIP des slides et transcriptions ;
- `assets/favicons/` : favicon locale ;
- `source/` : source éditoriale, storyboard, contact sheet et reçus utiles ;
- `slides.json` : source canonique des titres, descriptions, textes visibles et messages ;
- `build.py` : générateur autonome de la variante ;
- `tests/` : tests de contrat du site.

La variante doit être listée sur l’accueil racine seulement après génération, vérification et passage explicite par `matrice-slide-ai/publish_variant.py`.

## Invariants

- Ne jamais modifier `miweb-objectifs-2030-v1`, `miweb-objectifs-2030-v2`, `miweb-objectifs-2030-v3` ou `miweb-objectifs-2030-v4` pour publier une nouvelle variante.
- Ne jamais publier une image sans transcription dans `slides.json`.
- Ne jamais inventer de chiffre, seuil, engagement, audit ou conformité absents de la source.
- Ne jamais déclarer la variante conforme RGAA sans audit dédié.
- Ne jamais livrer uniquement les images : `alternatives.html` et `alternatives.md` sont obligatoires.
- Ne jamais hand-edit `index.html`, `alternatives.html`, `alternatives.md`, `accessibilite.html` ou le ZIP après génération ; modifier la source puis relancer `build.py`.
- Ne pas ajouter de framework, de route, de page ou de composant décoratif hors besoin de publication.

## Entrées attendues

Avant de générer le site, vérifier que les éléments suivants existent :

- dossier d’images validées ;
- nombre exact de slides ;
- source éditoriale validée ;
- storyboard ou trame de génération ;
- contact sheet si plusieurs images ont été générées ;
- nom du dossier public de variante ;
- libellé public à afficher sur l’accueil racine.

Exemple de nommage :

```text
miweb-offre-mutualisee-listes-diffusion-2026-condensee
miweb-offre-mutualisee-listes-diffusion-2026-longue
```

## Préparation du dossier avec la matrice

Créer le dossier de variante depuis la matrice, sans écraser une variante publiée :

```bash
python3 matrice-slide-ai/create_variant.py \
  --slug <dossier> \
  --title "Titre public" \
  --storyboard /chemin/vers/storyboard.md \
  --slides-dir /chemin/vers/images
```

La commande copie `build.py`, les tests, le favicon, le storyboard, `slides.json` et les images `slide-*.png`. Elle ne change ni `index.html` racine ni `published-versions.json`.

Si les images source sont préfixées, déclarer ce préfixe au lieu de renommer à la main :

```bash
python3 matrice-slide-ai/create_variant.py \
  --slug <dossier> \
  --title "Titre public" \
  --storyboard /chemin/vers/storyboard.md \
  --slides-dir /chemin/vers/images \
  --slide-prefix checklist-span-
```

La matrice copie alors `checklist-span-slide-01.png` vers `assets/slides/slide-01.png`.

## `slides.json`

`slides.json` est la source canonique des transcriptions. Le HTML, le Markdown et le ZIP doivent être régénérés depuis ce fichier.

Chaque entrée doit contenir :

```json
{
  "numero": 1,
  "titre": "Titre de la slide",
  "image": "assets/slides/slide-01.png",
  "alt": "Alternative courte.",
  "description": "Description complète de l’image et de sa structure.",
  "textes_visibles": [
    "Texte visible 1",
    "Texte visible 2"
  ],
  "message": "Message à retenir."
}
```

Règles :

- `numero` commence à 1 et suit l’ordre réel des images ;
- `image` pointe vers un fichier existant dans `assets/slides/` ;
- `alt` reste court, idéalement moins de 60 caractères ;
- `description` décrit la scène, la structure et les informations utiles non portées par l’alt court ;
- `textes_visibles` reprend les textes de la slide, sans corriger silencieusement le sens ;
- `message` formule l’idée à retenir sans inventer de conclusion.

## Métadonnées du jeu

La création écrit `variant.json` avec les libellés publics du jeu. Adapter ce fichier seulement si le titre, la description ou le libellé de source doivent changer.

Ne plus modifier `PUBLISHED_VERSIONS`, `LATEST_VERSION_SLUG` ou `ROOT_CATALOG_BOOTSTRAP` dans un `build.py` de variante pour publier l’accueil racine. Le catalogue racine appartient à `published-versions.json` et se met à jour avec `publish_variant.py`. Dans la matrice, `ROOT_CATALOG_BOOTSTRAP` sert seulement de graine de compatibilité si le catalogue racine n’existe pas encore.

Conserver le comportement existant :

- navigation clavier ;
- mode projection ;
- affichage de toutes les slides ;
- accordéons d’alternatives dans la présentation ;
- page `alternatives.html` ;
- génération `alternatives.md` ;
- ZIP contenant les slides et `alternatives.md` ;
- page `accessibilite.html` marquée non auditée.

## Génération

Depuis la racine du dépôt :

```bash
python3 <dossier>/build.py
```

Optimiser les images avant cette étape. Si des PNG sont optimisés ou remplacés après génération, relancer `python3 <dossier>/build.py` pour reconstruire le ZIP.

Le script doit générer :

- `<dossier>/index.html` ;
- `<dossier>/alternatives.html` ;
- `<dossier>/accessibilite.html` ;
- `<dossier>/alternatives.md` ;
- `<dossier>/README.md` ;
- `<dossier>/assets/downloads/<dossier>-slides.zip`.

Le build ordinaire ne doit pas écrire `index.html` racine.

## Publication racine

Après génération, tests et validation HTML :

```bash
python3 matrice-slide-ai/publish_variant.py --slug <dossier>
```

La commande vérifie le jeu, met à jour `published-versions.json`, puis régénère uniquement `index.html` racine.

## Vérifications obligatoires

Contrôles de contenu :

```bash
python3 -m json.tool <dossier>/slides.json >/dev/null
find <dossier>/assets/slides -name 'slide-*.png' | sort | wc -l
```

Tests de contrat :

```bash
scripts/validate_variant.sh <dossier>
```

Ce script lance les tests de contrat, `html-validate` et `vnu-jar`. Dans un environnement sandboxé, les validateurs `npx` peuvent demander un accès réseau.

Validation HTML directe si nécessaire :

```bash
npx --yes html-validate <dossier>/index.html <dossier>/alternatives.html <dossier>/accessibilite.html index.html
npx --yes vnu-jar --errors-only <dossier>/index.html <dossier>/alternatives.html <dossier>/accessibilite.html index.html
```

Contrôle des transcriptions :

```bash
rg "Alternatives textuelles|Textes visibles|Message à retenir" <dossier>/index.html <dossier>/alternatives.html <dossier>/alternatives.md
```

Contrôle des chemins :

```bash
rg '<img src="assets/slides/slide-' <dossier>/index.html
rg 'href="#"' <dossier>/index.html <dossier>/alternatives.html <dossier>/accessibilite.html
```

Contrôle des accents après modification de Markdown :

```bash
bash /Users/alex/Claude/scripts/check-accents.sh <fichier.md>
```

## Inspection locale

Démarrer un serveur local depuis la racine du dépôt :

```bash
scripts/serve-local.sh 8000
```

Inspecter au navigateur :

```text
http://127.0.0.1:8000/<dossier>/
http://127.0.0.1:8000/<dossier>/?projection=1#slide-01
http://127.0.0.1:8000/<dossier>/?slides=all#diaporama
http://127.0.0.1:8000/<dossier>/alternatives.html
http://127.0.0.1:8000/
```

Vérifier manuellement :

- la variante apparaît sur l’accueil racine ;
- les images s’affichent ;
- le mode projection reste accessible ;
- chaque slide dispose d’un accordéon d’alternative ;
- `alternatives.html` liste toutes les slides ;
- la navigation par swipe horizontal fonctionne et reste couverte par les tests de contrat ;
- le ZIP est téléchargeable ;
- aucune version publiée ne change hors décision explicite.

## Prévisualisation depuis un autre Mac du réseau local

Utiliser cette section quand Alex veut tester depuis un MacBook Air, un iPad ou un autre poste avant publication GitHub Pages.

Le serveur ne doit pas être lié à `127.0.0.1`, car cette adresse ne répond que depuis la machine qui lance le serveur. Il faut écouter sur toutes les interfaces réseau avec `0.0.0.0`, puis utiliser l’adresse IP locale du Mac qui héberge le dépôt.

Depuis la racine du dépôt, vérifier d’abord si un port est déjà occupé :

```bash
lsof -nP -iTCP:8000 -sTCP:LISTEN
```

Si le port `8000` est déjà utilisé, choisir un autre port, par exemple `8001`.

Récupérer l’adresse IP locale du Mac Studio :

```bash
for iface in en0 en1 en2 bridge0; do
  ip=$(ipconfig getifaddr "$iface" 2>/dev/null || true)
  [ -n "$ip" ] && printf '%s %s\n' "$iface" "$ip"
done
```

Démarrer le serveur accessible sur le réseau local :

```bash
python3 -m http.server 8001 --bind 0.0.0.0
```

Tester depuis le Mac qui héberge le serveur avec l’adresse IP locale, pas seulement avec `127.0.0.1` :

```bash
curl -I http://<ip-locale>:8001/<dossier>/
curl -I http://<ip-locale>:8001/<dossier>/alternatives.html
```

URL à donner pour test depuis le MacBook Air :

```text
http://<ip-locale>:8001/<dossier>/
http://<ip-locale>:8001/<dossier>/?projection=1#slide-01
http://<ip-locale>:8001/<dossier>/?slides=all#diaporama
http://<ip-locale>:8001/<dossier>/alternatives.html
```

Points de vigilance :

- si `127.0.0.1:<port>` répond mais pas `<ip-locale>:<port>`, le serveur n’est probablement pas lié à `0.0.0.0` ou un pare-feu bloque l’accès ;
- si un autre service répond sur `127.0.0.1:<port>`, tester avec l’IP locale permet de confirmer le serveur réellement exposé sur le réseau ;
- les deux machines doivent être sur le même réseau local ;
- ne pas utiliser cette URL locale comme preuve de publication GitHub Pages : elle sert seulement à la prévisualisation avant push.

## Prévisualisation hors réseau local avec tunnel public

Utiliser cette section quand Alex n’est pas sur le même réseau local que le Mac Studio. Dans ce cas, l’URL `http://<ip-locale>:<port>/...` ne suffit pas : il faut exposer temporairement le serveur local via un tunnel public.

Préférer un serveur local lié à `127.0.0.1`, puis exposer seulement ce port avec le tunnel :

```bash
python3 -m http.server 8010 --bind 127.0.0.1
```

Dans un autre terminal, lancer un tunnel temporaire :

```bash
npx --yes localtunnel --port 8010 --local-host 127.0.0.1
```

Le tunnel affiche une URL publique de type :

```text
https://<nom-temporaire>.loca.lt
```

Tester systématiquement les deux pages avant de communiquer l’URL :

```bash
curl -L --max-time 30 -s -o /tmp/preview-condensee.html -w '%{http_code} %{size_download}\n' \
  https://<nom-temporaire>.loca.lt/miweb-offre-mutualisee-listes-diffusion-2026-condensee/

curl -L --max-time 30 -s -o /tmp/preview-longue.html -w '%{http_code} %{size_download}\n' \
  https://<nom-temporaire>.loca.lt/miweb-offre-mutualisee-listes-diffusion-2026-longue/
```

Les deux commandes doivent répondre `200` avec une taille non nulle. Vérifier aussi que le serveur Python local reçoit les requêtes.

Exemple historique de tunnel temporaire utilisé pour la prévisualisation du 24 juin 2026 :

```text
https://forty-flies-cross.loca.lt/miweb-offre-mutualisee-listes-diffusion-2026-condensee/
https://forty-flies-cross.loca.lt/miweb-offre-mutualisee-listes-diffusion-2026-longue/
```

Validation iPhone hors réseau local du 25 juin 2026 :

- serveur local : `python3 -m http.server 8010 --bind 127.0.0.1` ;
- tunnel public temporaire : `npx --yes localtunnel --port 8010 --local-host 127.0.0.1` ;
- chemins validés sur iPhone : `miweb-offre-mutualisee-listes-diffusion-2026-condensee/#slide-06` et `miweb-offre-mutualisee-listes-diffusion-2026-longue/#slide-06` ;
- objectif du test : vérifier la navigation par swipe horizontal des jeux 5 et 6 avant généralisation aux variantes 1 à 4 et push.

Points de vigilance :

- l’URL `loca.lt` est temporaire et reste active seulement tant que le serveur local et le tunnel restent ouverts ;
- ce tunnel n’est pas une preuve de publication GitHub Pages ;
- si un tunnel Cloudflare rapide renvoie `404` sans requête visible dans le serveur Python, ne pas le communiquer : relancer le tunnel ou utiliser `localtunnel`.

## Git et publication

Avant commit :

```bash
git status --short
git diff --stat
git diff -- DEMARCHE-VERSIONS.md README.md GUIDE-REGENERATION-SITES-SLIDES.md index.html published-versions.json <dossier>/slides.json <dossier>/build.py
```

Ne pas ajouter :

- `.DS_Store` ;
- `__pycache__/` ;
- captures temporaires ;
- caches de tests ;
- sorties locales non liées à la variante.

Après push GitHub Pages, vérifier l’URL publique :

```text
https://alexmacapple.github.io/miweb-objectifs-2030/<dossier>/
https://alexmacapple.github.io/miweb-objectifs-2030/<dossier>/alternatives.html
```

Pour éviter un push silencieux bloqué par une invite Git, pousser avec :

```bash
scripts/push-pages.sh
```

## Checklist finale

- [ ] Le dossier de variante est autonome.
- [ ] Les images validées sont dans `assets/slides/`.
- [ ] `slides.json` contient une entrée par slide.
- [ ] Chaque image a un `alt`, une `description`, des `textes_visibles` et un `message`.
- [ ] `build.py` a été lancé.
- [ ] Le build ordinaire n’a pas publié l’accueil racine.
- [ ] `alternatives.html` et `alternatives.md` existent.
- [ ] Le ZIP contient les images et `alternatives.md`.
- [ ] `scripts/validate_variant.sh <dossier>` passe, ou l’écart réseau sandbox est documenté.
- [ ] `publish_variant.py` a été lancé après les vérifications.
- [ ] `published-versions.json` contient la nouvelle variante.
- [ ] L’accueil racine liste la nouvelle variante.
- [ ] V1, V2, V3 et V4 n’ont pas été modifiées.
- [ ] Les Markdown modifiés passent `check-accents.sh`.
