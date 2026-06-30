# ShipGuard Visual Fix Plan

Mode: dry-run
Manifest: `visual-tests/_results/fix-manifest.json`
Date: 2026-06-30
Version testée: ShipGuard `2.3.7`

## Résumé

Dry-run exécuté à partir du manifest généré par le dashboard ShipGuard `2.3.7`
via `POST /save-manifest`. Aucun fichier source n'a été modifié. Aucun rebuild,
aucun rerun navigateur et aucune commande Git destructive n'ont été exécutés.

Résultat : le flux lit correctement le manifest, la capture, les coordonnées
d'annotation, la note humaine et les fichiers candidats. L'annotation utilisée
est une note de recette non corrective ; le plan ne propose donc aucune
correction du site MiWeb.

## Test: `pages/checklist-span-operationnel-accessibilite-html`

- Nom : `Accessibilité - Checklist SPAN opérationnel`
- URL : `http://127.0.0.1:8001/checklist-span-operationnel/accessibilite.html`
- Screenshot : `visual-tests/_results/screenshots/checklist-span-operationnel-accessibilite-html.png`
- Action : `validate-and-fix`

### Annotation 1

- Sévérité : `high`
- Note : `Recette 2.3.7 - annotation UI test`
- Région normalisée : `x1=0.2917 y1=0.3649 x2=0.3917 y2=0.4649`
- Région pixels approximative : `x=373..501`, `y=279..356` sur une capture
  `1280 x 765`

Observation visuelle :

La région annotée couvre le badge « Accessibilité : non auditée » et le début
du bloc de métadonnées sous le titre « Accessibilité ». Le rendu est cohérent
avec la page source : badge DSFR warning lisible, texte visible, hiérarchie
stable, aucun écran blanc, aucune erreur navigateur et aucun élément principal
visiblement cassé dans la zone.

### Fichiers candidats

- `checklist-span-operationnel/accessibilite.html` : page HTML générée servie
  par le test.
- `checklist-span-operationnel/build.py` : source génératrice de la page
  `accessibilite.html`, fonction `render_accessibility()`.
- `checklist-span-operationnel/tests/test_site_contracts.py` : tests locaux
  qui chargent `render_accessibility()`.
- `visual-tests/pages/checklist-span-operationnel-accessibilite-html.yaml` :
  manifest ShipGuard du test visuel.
- `visual-tests/_results/screenshots/checklist-span-operationnel-accessibilite-html.png` :
  preuve visuelle analysée.

### Correction envisagée

Aucune correction à appliquer.

Motif :

- la note d'annotation indique un test de recette, pas une demande corrective ;
- la zone annotée correspond à un contenu volontaire de déclaration
  d'accessibilité non auditée ;
- modifier le badge, le texte ou la mise en page serait spéculatif et contraire
  au mode dry-run.

### Limites

- L'analyse ne juge pas la conformité RGAA réelle de la page ; elle vérifie le
  flux ShipGuard annotation -> manifest -> plan dry-run.
- Le mode normal `sg-visual-fix` n'a pas été lancé, car il peut modifier le code
  source, rebuild le site et produire des captures before/after.
- Pour tester un vrai correctif, il faudrait créer une annotation pointant un
  défaut visuel réel ou travailler sur une copie isolée avec modification
  volontaire.

## Contrôles dry-run

- Source modifiée : non.
- Rebuild exécuté : non.
- Browser rerun exécuté : non.
- Git destructif exécuté : non.
- Plan écrit : oui, `visual-tests/_results/visual-fix-plan.md`.
