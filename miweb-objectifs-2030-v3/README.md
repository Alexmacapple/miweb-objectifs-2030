# miweb-objectifs-2030-v3

Site statique GitHub Pages pour les slides accessibles « Objectifs 2030 - accessibilité numérique ».

## Accès directs

- [Présentation plein écran](./?projection=1#slide-01)
- [Toutes les slides](./?slides=all#diaporama)

## Génération

Depuis ce répertoire :

```bash
python3 build.py
```

Le script lit `slides.json` et génère `index.html`, `alternatives.html`, `accessibilite.html`, `alternatives.md` et `assets/downloads/miweb-objectifs-2030-v3-slides.zip`.

## Sources V3

- `source/storyboard-v3.md` : storyboard utilisé pour générer la variante V3.
- `slides.json` : titres, alternatives textuelles, descriptions et messages associés aux images publiées.

## Vérifications attendues

- les images listées dans `slides.json` sont présentes dans `assets/slides/` ;
- aucun lien `href="#"` n’est généré ;
- la page principale reste lisible sans JavaScript ;
- les alternatives textuelles sont aussi disponibles dans `alternatives.html` et `alternatives.md`.
