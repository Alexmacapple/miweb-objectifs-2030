# ShipGuard Visual Fix Plan

Mode: dry-run
Manifest: `visual-tests/_results/fix-manifest.json`
Date: 2026-06-30 08:50 CEST
Version testee: ShipGuard `2.3.5` cote Codex

## Resume

Dry-run execute a partir du manifest genere par le dashboard ShipGuard `2.3.5`
via `POST /save-manifest`. Aucun fichier source n'a ete modifie. Aucun rebuild,
aucun rerun navigateur et aucune commande Git n'ont ete executes.

Resultat : le workflow lit correctement le manifest, la capture, les
coordonnees d'annotation et les fichiers candidats. L'annotation utilisee est
une note de recette non corrective ; le plan ne propose donc aucune correction
du site MiWeb.

## Test: `pages/root-index`

- URL : `http://127.0.0.1:8001/`
- Screenshot : `visual-tests/_results/screenshots/root-index.png`
- Action : `validate-and-fix`

### Annotation 1

- Region normalisee : `x1=0.10 y1=0.10 x2=0.20 y2=0.20`
- Region pixels approximative : `x=128..256`, `y=162..324` sur une capture
  `1280 x 1620`
- Note : `recette 2.3.5`

Observation visuelle :

La region annotee couvre le debut du titre principal et l'espace superieur de
la page d'accueil. Aucun defaut visuel evident n'est present dans cette zone :
le titre est lisible, la hierarchie est stable, le logo Republique Francaise
est visible dans l'en-tete, et les cartes de versions s'affichent correctement.
La note est une annotation de recette, pas une demande corrective.

### Fichiers candidats

- `index.html` : page HTML racine servie par le test.
- `matrice-slide-ai/publish_variant.py` : publication du catalogue racine.
- `published-versions.json` : catalogue racine consomme par l'accueil.
- `visual-tests/pages/root-index.yaml` : manifest ShipGuard du test visuel.
- `visual-tests/_results/screenshots/root-index.png` : preuve visuelle analysee.

### Correction envisagee

Aucune correction a appliquer.

Motif :

- l'annotation est une note de recette ;
- la region ne montre pas de defaut de rendu evident ;
- appliquer une correction source serait speculatif et contraire au mode
  dry-run.

### Limites

- L'analyse ne juge pas la conformite RGAA reelle de la page ; elle verifie le
  flux ShipGuard annotation -> manifest -> plan dry-run.
- Le mode normal `sg-visual-fix` n'a pas ete lance, car il peut modifier le
  code source.
- Pour tester un vrai correctif, il faudrait creer une annotation pointant un
  defaut visuel reel et accepter des modifications locales non commitees.

## Controles dry-run

- Source modifiee : non.
- Rebuild execute : non.
- Browser rerun execute : non.
- Git execute : non.
- Plan ecrit : oui, `visual-tests/_results/visual-fix-plan.md`.
