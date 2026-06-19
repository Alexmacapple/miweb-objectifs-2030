# miweb-objectifs-2030-v1

Site statique GitHub Pages pour les slides accessibles « Objectifs 2030 - accessibilité numérique ».

## Génération

Depuis ce répertoire :

```bash
python3 build.py
```

Le script lit `slides.json` et génère `index.html`, `alternatives.html`, `accessibilite.html`, `alternatives.md` et `assets/downloads/miweb-objectifs-2030-v1-slides.zip`.

## Vérifications attendues

- les 10 images `slide-01.png` à `slide-10.png` sont présentes dans `assets/slides/` ;
- aucun lien `href="#"` n’est généré ;
- la page principale reste lisible sans JavaScript ;
- les alternatives textuelles sont aussi disponibles dans `alternatives.html` et `alternatives.md`.
