# PRD - Accès rapides du header DSFR

**Statut** : Brouillon
**Date** : 2026-06-20
**Auteur** : Alex + Codex

## Prompt amélioré

Modifier le bloc d’outils du header DSFR pour reprendre les mêmes intitulés que le footer, avec des icônes DSFR, dans une structure conforme quand plusieurs items sont présents.

Les accès rapides du header doivent afficher :

- `Présentation plein écran`
- `Alternatives textuelles`
- `Télécharger les slides`

Le bloc `fr-header__tools-links` doit contenir une liste DSFR :

```html
<div class="fr-header__tools">
  <div class="fr-header__tools-links">
    <ul class="fr-btns-group">
      <li>
        <!-- Item 1 -->
      </li>
      <li>
        <!-- Item 2 -->
      </li>
      <li>
        <!-- Item 3 -->
      </li>
    </ul>
  </div>
</div>
```

Chaque item doit être dans un `<li>`. Ne pas placer de lien ou bouton directement dans `fr-header__tools-links`.

## Objectif

Aligner les accès rapides du header avec ceux du footer, tout en respectant la structure DSFR attendue pour plusieurs actions dans `fr-header__tools-links`.

Le header devient un point d’accès direct aux trois actions principales :

- ouvrir ou préparer la présentation plein écran ;
- consulter les alternatives textuelles ;
- télécharger les slides.

## Contexte

Le header contient actuellement un accès rapide centré sur les alternatives textuelles. Ce choix était cohérent avec un seul item, mais il ne suffit plus si le header reprend les trois accès du footer.

Dès qu’il y a plusieurs items, la structure DSFR attendue est une liste :

```html
<ul class="fr-btns-group">
  <li>...</li>
  <li>...</li>
  <li>...</li>
</ul>
```

## Problème

Le brouillon initial contient deux ambiguïtés :

- il demande un bouton `Plein écran`, alors que le libellé à reprendre depuis le footer est `Présentation plein écran` ;
- il demande de ne pas ajouter de script, alors qu’un bouton plein écran fonctionnel nécessite soit de réutiliser le script existant, soit d’adapter ce script pour gérer un bouton supplémentaire.

Un bouton sans action serait un problème d’accessibilité et d’usage. Un lien avec `href="#"` serait également à exclure.

## Décision

Retenir les libellés du footer comme libellés visibles dans le header :

- `Présentation plein écran`
- `Alternatives textuelles`
- `Télécharger les slides`

Utiliser une liste `<ul class="fr-btns-group">` avec un `<li>` par item.

Pour `Présentation plein écran` :

- sur la page du diaporama, utiliser un `<button type="button">`, car l’ouverture plein écran est une action locale ;
- sur les pages qui ne contiennent pas le diaporama, utiliser un lien vers `./?projection=1#slide-01`, car il s’agit d’une navigation vers la présentation.

Ne pas ajouter de nouveau bloc `<script>`. Si un bouton plein écran est ajouté dans le header de la page diaporama, adapter le script existant plutôt que créer un script séparé.

## Options évaluées

### Option A - Même structure partout avec bouton plein écran

**Principe** : afficher `Présentation plein écran` comme bouton sur toutes les pages.

**Avantages** :

- structure HTML homogène ;
- bouton cohérent avec l’idée d’action.

**Inconvénients** :

- impossible d’activer le plein écran depuis une page qui ne contient pas le diaporama ;
- risque de bouton inactif ou trompeur ;
- nécessite une gestion d’erreur ou de désactivation.

### Option B - Sémantique selon le contexte

**Principe** : bouton sur la page diaporama, lien sur les autres pages.

**Avantages** :

- respecte la sémantique HTML : action locale = bouton, navigation = lien ;
- évite un bouton sans effet ;
- reste compatible avec la contrainte navigateur sur `requestFullscreen()`.

**Inconvénients** :

- le markup varie selon le type de page ;
- le générateur doit connaître le contexte de page.

### Option C - Tout mettre en liens

**Principe** : utiliser trois liens dans le header, y compris pour `Présentation plein écran`.

**Avantages** :

- très simple à générer ;
- cohérent entre toutes les pages.

**Inconvénients** :

- depuis la page diaporama, le lien ne déclenche pas nécessairement le plein écran dans le même geste utilisateur ;
- moins précis sémantiquement pour une action locale.

## Option retenue

Option B : sémantique selon le contexte.

Elle évite de produire un bouton qui ne peut pas fonctionner, tout en permettant l’ouverture plein écran immédiate depuis la page qui contient réellement le diaporama.

## Spécification HTML attendue

### Page diaporama

```html
<div class="fr-header__tools">
  <div class="fr-header__tools-links">
    <ul class="fr-btns-group">
      <li>
        <button
          type="button"
          class="fr-btn fr-icon-expand-left-right-line fr-btn--icon-left"
          data-header-fullscreen
        >
          Présentation plein écran
        </button>
      </li>
      <li>
        <a
          href="alternatives.html"
          class="fr-btn fr-icon-accessibility-line fr-btn--icon-left"
        >
          Alternatives textuelles
        </a>
      </li>
      <li>
        <a
          href="assets/downloads/miweb-objectifs-2030-v1-slides.zip"
          class="fr-btn fr-icon-download-line fr-btn--icon-left"
          download
        >
          Télécharger les slides
        </a>
      </li>
    </ul>
  </div>
</div>
```

### Pages sans diaporama

```html
<div class="fr-header__tools">
  <div class="fr-header__tools-links">
    <ul class="fr-btns-group">
      <li>
        <a
          href="./?projection=1#slide-01"
          class="fr-btn fr-icon-expand-left-right-line fr-btn--icon-left"
        >
          Présentation plein écran
        </a>
      </li>
      <li>
        <a
          href="alternatives.html"
          class="fr-btn fr-icon-accessibility-line fr-btn--icon-left"
        >
          Alternatives textuelles
        </a>
      </li>
      <li>
        <a
          href="assets/downloads/miweb-objectifs-2030-v1-slides.zip"
          class="fr-btn fr-icon-download-line fr-btn--icon-left"
          download
        >
          Télécharger les slides
        </a>
      </li>
    </ul>
  </div>
</div>
```

## Contraintes

- Utiliser `<ul class="fr-btns-group">` dès qu’il y a plusieurs items.
- Placer chaque item dans un `<li>`.
- Ne pas utiliser `href="#"`.
- Ne pas ajouter `target="_blank"`.
- Ne pas modifier la navigation principale.
- Garder le composant mobile DSFR conforme : bouton `Menu`, `fr-header__menu fr-modal`, `fr-header__menu-links`.
- Ne pas ajouter de nouveau bloc `<script>`.
- Adapter le script existant uniquement si nécessaire pour brancher le bouton plein écran du header.
- Conserver les libellés visibles alignés avec le footer.

## Icônes DSFR

- `Présentation plein écran` : `fr-icon-expand-left-right-line`
- `Alternatives textuelles` : `fr-icon-accessibility-line`
- `Télécharger les slides` : `fr-icon-download-line`

## Points de vigilance accessibilité

- Le bouton `Présentation plein écran` doit être atteignable au clavier et déclencher la même action que le bouton plein écran du diaporama.
- Le focus ne doit pas être perdu après l’entrée ou la sortie du plein écran.
- Depuis les pages sans diaporama, utiliser un lien plutôt qu’un bouton pour éviter une action impossible.
- Les libellés visibles doivent être suffisamment explicites sans dépendre uniquement des icônes.
- En mobile, les trois items doivent rester disponibles via le menu DSFR.

## Tests à faire

- Vérifier que `fr-header__tools-links` contient une liste `<ul class="fr-btns-group">`.
- Vérifier que les trois items sont chacun dans un `<li>`.
- Vérifier que le header de la page diaporama contient un bouton `Présentation plein écran`.
- Vérifier que ce bouton déclenche le plein écran depuis la page diaporama.
- Vérifier que les pages sans diaporama utilisent un lien `Présentation plein écran` vers `./?projection=1#slide-01`.
- Vérifier que `Alternatives textuelles` pointe vers `alternatives.html`.
- Vérifier que `Télécharger les slides` pointe vers le ZIP et conserve l’attribut `download`.
- Vérifier que les trois accès restent atteignables en mobile.
- Vérifier la navigation clavier.
- Vérifier qu’aucun `href="#"` n’est généré.

## Changelog

| Date | Auteur | Changement |
|------|--------|------------|
| 2026-06-20 | Alex + Codex | Remplacement du PRD mono-lien par un PRD pour trois accès rapides header DSFR. |
