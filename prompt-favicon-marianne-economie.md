# Prompt optimisé — Remplacement de favicon par celle d’economie.gouv.fr

## Rôle

Agis comme un développeur front-end senior spécialisé en sites statiques GitHub Pages, HTML, Python, DSFR et gestion propre des favicons.

## Objectif

Remplacer la favicon actuellement utilisée sur le site statique :

{url_site_cible}

par la favicon officielle utilisée sur :

{url_source_favicon}

Le site cible correspond au dépôt local :

{repo_local}

et à la version située dans :

{dossier_version}

## Variables

- {url_source_favicon} = https://www.economie.gouv.fr/
- {url_site_cible} = https://alexmacapple.github.io/miweb-objectifs-2030/miweb-objectifs-2030-v1/#slide-01
- {repo_local} = chemin local du dépôt GitHub `Alexmacapple/miweb-objectifs-2030`
- {dossier_version} = miweb-objectifs-2030-v1
- {autorisation_usage_marianne} = oui/non
- {branche_git} = main ou branche de travail à créer

## Contrainte de conformité obligatoire

Avant toute modification, vérifie la valeur de `{autorisation_usage_marianne}`.

Si `{autorisation_usage_marianne}` n’est pas explicitement égal à `oui`, ne copie pas la favicon Marianne d’economie.gouv.fr.

Explique brièvement qu’il faut une autorisation ou une légitimité d’usage pour reprendre un signe graphique officiel de l’État, puis propose une alternative sûre : conserver une favicon neutre, DSFR-compatible, non trompeuse, qui n’utilise pas la Marianne ni le bloc-marque officiel.

Si `{autorisation_usage_marianne}` vaut `oui`, effectue la modification technique demandée.

## Tâches détaillées

1. Ouvre le dépôt local `{repo_local}`.

2. Crée ou utilise la branche `{branche_git}`.

3. Inspecte la structure du site, en particulier :

   - `{dossier_version}/build.py`
   - `{dossier_version}/index.html`
   - `{dossier_version}/alternatives.html`
   - `{dossier_version}/accessibilite.html`
   - le dossier `{dossier_version}/assets/`

4. Identifie la favicon actuellement en place.

   Le projet semble générer ses fichiers HTML via `build.py`.

   Ne modifie pas seulement les fichiers HTML générés si la source de génération doit aussi être mise à jour.

   Mets à jour la source canonique de la favicon dans `build.py` afin que les prochaines générations conservent la bonne favicon.

5. Récupère proprement la favicon utilisée par `{url_source_favicon}` :

   - inspecte les balises `<link rel="icon">`, `<link rel="shortcut icon">`, `<link rel="apple-touch-icon">` et éventuels manifests ;
   - si aucune balise explicite n’est trouvée, vérifie le fallback `/favicon.ico` ;
   - télécharge uniquement le fichier favicon nécessaire ;
   - conserve le format original si possible.

6. Place la favicon dans un chemin local stable, par exemple :

   - `{dossier_version}/assets/favicons/favicon.ico`
   - ou `{dossier_version}/assets/favicons/favicon.svg`
   - ou `{dossier_version}/assets/favicons/favicon.png`

7. Remplace la favicon actuelle par une référence locale, pas par une URL externe distante.

8. Mets à jour toutes les pages concernées via le générateur :

   - `index.html`
   - `alternatives.html`
   - `accessibilite.html`
   - éventuellement l’`index.html` racine si nécessaire.

9. Vérifie que le chemin de favicon fonctionne correctement sur GitHub Pages avec le sous-répertoire :

   - `/miweb-objectifs-2030/miweb-objectifs-2030-v1/`
   - et avec les liens relatifs depuis les pages HTML générées.

10. Régénère le site avec :

```bash
python3 miweb-objectifs-2030-v1/build.py
```
