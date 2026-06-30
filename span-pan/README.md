# span-pan

Site statique GitHub Pages pour les slides accessibles « SPAN / PAN - accessibilité numérique ».

## Accès directs

- [Présentation plein écran](./?projection=1#slide-01)
- [Toutes les slides](./?slides=all#diaporama)

## Génération

Depuis ce répertoire :

```bash
python3 build.py
```

Le script lit `slides.json` et génère `index.html`, `alternatives.html`, `accessibilite.html`, `alternatives.md` et `assets/downloads/span-pan-slides.zip`.

## Sources du jeu de slides

- `source/Checklist-SPAN.md` : source conservée pour traçabilité.
- `source/SPAN-diff-PAN.md` : source conservée pour traçabilité.
- `source/contact-sheet.png` : source conservée pour traçabilité.
- `source/storyboard.md` : storyboard utilisé pour générer la variante.
- `slides.json` : titres, alternatives textuelles, descriptions et messages associés aux images publiées.

## Vérifications attendues

- les images listées dans `slides.json` sont présentes dans `assets/slides/` ;
- aucun lien `href="#"` n’est généré ;
- la page principale reste lisible sans JavaScript ;
- les alternatives textuelles sont aussi disponibles dans `alternatives.html` et `alternatives.md`.
