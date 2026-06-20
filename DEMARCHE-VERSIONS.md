# Démarche de publication des variantes

Cette procédure sert à publier une nouvelle variante `miweb-objectifs-2030-vN` en conservant le fonctionnement de la V1/V2. Par défaut, seules les images de slides et les alternatives textuelles changent.

## Sources

- Images validées : dossier `outputs/ia-slides/...` du projet actif.
- Site publié : `/Users/alex/Claude/projets-heberges/miweb-objectifs-2030`.
- Source éditoriale : note validée utilisée pour produire le storyboard de la variante.

## Étapes

1. Créer le dossier de variante à partir de la dernière version publiée.
2. Copier les images validées `slide-01.png` à `slide-NN.png` dans `assets/slides/`, selon le nombre réel de slides de la variante.
3. Copier le storyboard de génération dans `source/storyboard-vN.md`.
4. Mettre à jour `slides.json` : titre, alternative courte, description, textes visibles et message.
5. Adapter `build.py` si la nouvelle version n’est pas encore listée dans `PUBLISHED_VERSIONS`.
6. Lancer `python3 miweb-objectifs-2030-vN/build.py`.
7. Vérifier :
   - `python3 -m unittest discover -s miweb-objectifs-2030-vN/tests` ;
   - `npx --yes html-validate miweb-objectifs-2030-vN/index.html miweb-objectifs-2030-vN/alternatives.html miweb-objectifs-2030-vN/accessibilite.html index.html` ;
   - `npx --yes vnu-jar --errors-only miweb-objectifs-2030-vN/index.html miweb-objectifs-2030-vN/alternatives.html miweb-objectifs-2030-vN/accessibilite.html index.html`.
8. Inspecter localement au navigateur :
   - `miweb-objectifs-2030-vN/#slide-01` ;
   - `miweb-objectifs-2030-vN/?projection=1#slide-01` ;
   - `miweb-objectifs-2030-vN/alternatives.html`.
9. Mettre à jour le README racine et pousser sur GitHub Pages.

## Variantes publiées

- V1 : variante initiale de 10 slides.
- V2 : variante de 10 slides centrée sur la chaîne qualité durable.
- V3 : variante de 8 slides centrée sur la dette visible, les portes qualité, le run, la mutualisation et les arbitrages.

## Points de vigilance

- Ne pas modifier une version déjà publiée pour créer une variante.
- Ne pas publier une image sans alternative textuelle correspondante.
- Ne pas inventer de chiffre, de seuil ou d’engagement absent de la note source.
- Ne pas présenter la variante comme auditée RGAA sans audit dédié.
- Garder l’accueil racine cohérent avec la dernière version publiée.
