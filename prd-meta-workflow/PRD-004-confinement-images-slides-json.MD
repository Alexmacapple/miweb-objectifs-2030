# PRD-004 : Confinement des images `slides.json`

**Statut** : Implémenté localement
**Date** : 2026-06-30
**Auteur** : Alex
**Source** : recette ShipGuard 2.3.7, bug `SG-Z2-002`, lecture de `matrice-slide-ai/build.py` et des `build.py` autonomes existants

---

## Vision

Le quoi : les chemins d'images déclarés dans `slides.json` doivent être
confinés au dossier public `assets/slides/` de la variante.

Le pourquoi : `slides.json` est une source de build. Si son champ `image`
peut pointer vers n'importe quel fichier existant sous ou hors du dossier de
variante, le HTML et le ZIP peuvent publier un fichier qui ne fait pas partie du
contrat des slides. Le mécanisme robuste est de transformer `image` en chemin
relatif contrôlé : préfixe attendu, normalisation, refus des chemins absolus,
refus de `..`, existence réelle sous `assets/slides/`.

Le comment : renvoyé au Plan d'implémentation.

## Exemple bout-en-bout (projeté)

Un agent met à jour `slides.json` pendant la préparation d'une variante.

Cas valide :

```json
{
  "image": "assets/slides/slide-01.png"
}
```

Le build résout ce chemin sous le dossier de la variante, vérifie que le fichier
existe dans `assets/slides/`, génère le HTML et ajoute l'image au ZIP.

Cas invalide :

```json
{
  "image": "../secret.png"
}
```

Le build échoue avant génération avec une erreur explicite indiquant que
`slides.json` ne peut référencer que des images sous `assets/slides/`.

Même refus pour :

```json
{
  "image": "source/image-interne.png"
}
```

Le ZIP et le HTML ne doivent jamais utiliser un chemin d'image qui n'a pas passé
ce garde.

---

## Contexte

Dans [matrice-slide-ai/build.py](../matrice-slide-ai/build.py), `load_slides()`
vérifie que chaque slide possède un champ `image`, mais ne vérifie pas la zone
autorisée.

Le build vérifie ensuite seulement l'existence du fichier :

```python
image_path = ROOT / slide["image"]
if not image_path.is_file():
    raise FileNotFoundError(image_path)
```

Le ZIP utilise la même donnée :

```python
image_path = ROOT / slide["image"]
archive.write(image_path, image_path.name)
```

ShipGuard a remonté `SG-Z2-002` : `slides.json` peut référencer des fichiers
hors `assets/slides/`.

La même mécanique existe dans les `build.py` autonomes déjà publiés ou prêts à
publier. La matrice protège les futures variantes, mais elle ne corrige pas les
copies déjà présentes. Le périmètre du PRD couvre donc :

- `matrice-slide-ai/build.py`, source des futurs jeux ;
- les `build.py` des variantes actuelles ;
- les tests qui prouvent que le contrat reste valide pour la matrice et pour les
  variantes existantes.

## Problème

Le contrat documentaire dit que les images listées dans `slides.json` sont dans
`assets/slides/`, mais le code accepte tout fichier existant résolu depuis
`ROOT / slide["image"]`.

Risques :

- chemin `../...` qui sort du dossier de variante ;
- fichier interne comme `source/...` publié par erreur dans le HTML ou le ZIP ;
- dérive entre les tests, qui comptent les images `slide-*.png`, et la source
  réelle utilisée par le build ;
- régression silencieuse si un générateur ou un agent écrit un mauvais chemin.

## Solution

Centraliser la résolution et la validation des chemins d'images de slides :

- ajouter une fonction dédiée, par exemple
  `resolve_slide_image_path(image: str) -> Path` ;
- refuser les chemins absolus ;
- refuser tout chemin contenant `..` après normalisation ;
- exiger le préfixe logique `assets/slides/` ;
- exiger que le fichier résolu existe et reste sous `ROOT / "assets" / "slides"`,
  y compris si le chemin passe par un lien symbolique ;
- appeler cette fonction depuis `load_slides()` pour que toute slide retournée
  soit déjà validée avant `render_slide()` ;
- conserver dans `slide["image"]` la chaîne relative publique
  `assets/slides/...`, car cette valeur est utilisée comme `src` HTML ;
- utiliser cette fonction dans `write_zip()` et dans les tests de contrat ;
- ajouter des tests de régression sur `../...` et `source/...`.

Comme les variantes sont autonomes, le garde doit être copié dans chaque
`build.py` concerné. Il ne faut pas introduire de dépendance d'exécution des
variantes vers `matrice-slide-ai/`.

Exception contrôlée : quand la matrice lit `slides.example.json`, elle vérifie
le confinement du chemin mais pas l'existence du fichier, car la matrice source
n'embarque pas les images publiques. Tout vrai `slides.json` de variante exige
en revanche que le fichier existe sous `assets/slides/`.

Contrat d'implémentation attendu pour éviter les vérifications fragiles :

```python
def resolve_slide_image_path(image: str, require_exists: bool = True) -> Path:
    relative_path = Path(image)
    if relative_path.is_absolute():
        raise ValueError(...)
    if relative_path.parts[:2] != ("assets", "slides"):
        raise ValueError(...)
    candidate = (ROOT / relative_path).resolve()
    slides_root = SLIDES_DIR.resolve()
    candidate.relative_to(slides_root)
    if require_exists and not candidate.is_file():
        raise FileNotFoundError(candidate)
    return candidate
```

Le `ValueError` doit mentionner `assets/slides` pour rendre l'erreur
diagnostiquable dans les tests et dans la sortie du build.

## Options évaluées

### Option A (retenue) : garde centralisé dans `build.py`

**Avantages** :
- protège tous les usages de `slide["image"]` au même endroit ;
- évite une divergence entre le HTML, le ZIP et les prévalidations ;
- reste compatible avec les `slides.json` existants ;
- donne une erreur claire au moment du build.

**Inconvénients** :
- ajoute une petite fonction de résolution à maintenir ;
- impose de mettre à jour les tests de contrat pour couvrir ce garde.
- doit être propagé dans les `build.py` autonomes existants, car ils ne
  dépendent pas de la matrice à l'exécution.

### Option B : contrôle uniquement dans les tests

**Avantages** :
- changement minimal du runtime de build ;
- détecte les mauvais chemins pendant la validation standard.

**Inconvénients** :
- ne protège pas un build lancé sans tests ;
- laisse `write_zip()` et `main()` dépendre d'une convention non défendue ;
- ne corrige pas la faiblesse signalée dans le code de production.

### Option C : correction au moment de la création des variantes

**Avantages** :
- empêche la plupart des mauvais `slides.json` générés par la matrice ;
- utile pour améliorer l'ergonomie de création.

**Inconvénients** :
- ne protège pas les modifications manuelles de `slides.json` ;
- ne couvre pas les variantes existantes ;
- ne protège pas `build.py`, qui reste la dernière barrière avant publication.

## Décision

Retenir l'option A : le build doit porter le garde de sécurité, car il est le
dernier point commun avant génération HTML et ZIP.

Les tests peuvent compléter ce garde, mais ne doivent pas en être la seule
protection.

Le changement doit préserver l'autonomie des variantes : la correction est
dupliquée dans les `build.py` existants si nécessaire, au lieu d'ajouter un
import commun vers la matrice.

## Plan d'implémentation

1. Ajouter un helper de test dans `matrice-slide-ai/tests` qui crée une variante
   temporaire via `create_variant.py`, altère son `slides.json`, puis lance son
   `build.py`.
2. Ajouter un test de régression qui construit un
   `slides.json` temporaire avec `../...` et vérifie que le build échoue avec
   une erreur explicite.
3. Ajouter un second cas avec `source/...` pour vérifier que les fichiers
   internes existants ne peuvent pas être référencés comme slides.
4. Ajouter un cas positif avec `assets/slides/slide-01.png` pour vérifier qu'un
   chemin valide continue à construire le HTML et le ZIP.
5. Vérifier que les deux tests invalides échouent avant la correction du build.
6. Ajouter dans `matrice-slide-ai/build.py` une fonction de résolution qui
   retourne le chemin `Path` validé sous `assets/slides/`.
7. Appeler ce garde depuis `load_slides()` sans remplacer la valeur publique
   `slide["image"]`, afin que le rendu HTML continue à produire un `src`
   relatif.
8. Remplacer l'accès direct `ROOT / slide["image"]` dans `write_zip()` par cette
   fonction.
9. Supprimer la prévalidation redondante dans `main()` ou la remplacer par un
   appel au même garde, sans créer de deuxième logique.
10. Propager le même garde aux `build.py` autonomes actuels, sans créer de
   dépendance d'exécution vers `matrice-slide-ai/`.
11. Adapter les tests de contrat pour vérifier que chaque image déclarée commence
   par `assets/slides/` et reste dans ce dossier.
12. Lancer les tests matrice et `scripts/validate_variant.sh` sur les variantes
   principales.

## Métriques de succès

- Les tests de régression couvrent un `slides.json` contenant
  `"image": "../secret.png"` et un autre contenant
  `"image": "source/image-interne.png"`.
- Les deux builds invalides échouent avec une erreur contenant
  `assets/slides`.
- Un test positif couvre `"image": "assets/slides/slide-01.png"` et vérifie que
  le build réussit, que le HTML contient `src="assets/slides/slide-01.png"` et
  que le ZIP contient `slide-01.png`.
- Le garde utilise `Path.resolve()` et `relative_to()` ou une vérification
  équivalente, pas un simple test de chaîne `startswith`.
- `load_slides()` refuse les chemins invalides avant tout appel à
  `render_v1_index()`, `render_alternatives()` ou `write_zip()`.
- `render_slide()` continue à produire un `src` HTML relatif sous
  `assets/slides/`.
- `rg "ROOT / slide\\[\"image\"\\]" --glob build.py .` ne trouve aucun accès
  direct restant.
- `python3 -m unittest discover -s matrice-slide-ai/tests` réussit.
- `scripts/validate_variant.sh miweb-objectifs-2030-v1` réussit.
- Les autres variantes principales passent avec `scripts/validate_variant.sh`
  ou les exceptions sont documentées explicitement.
- Aucun `build.py` de variante n'importe `matrice-slide-ai` pour ce garde.

## Changelog

| Date | Auteur | Changement |
|------|--------|------------|
| 2026-06-30 | Alex + Codex | Implémentation locale du PRD |
| 2026-06-30 | Alex + Codex | Ajout explicite du test positif de chemin valide |
| 2026-06-30 | Alex + Codex | Élargissement explicite aux variantes autonomes existantes |
| 2026-06-30 | Alex + Codex | Réduction des ambiguïtés d'implémentation |
| 2026-06-30 | Alex + Codex | Création du PRD |
