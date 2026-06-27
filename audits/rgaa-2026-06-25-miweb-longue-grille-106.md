# Grille RGAA 4.1.2 - 106 critères - Offre mutualisée de listes de diffusion

Date : 25 juin 2026

Périmètre audité : page principale de la variante `miweb-offre-mutualisee-listes-diffusion-2026-longue`.

URL locale utilisée : `http://127.0.0.1:8002/miweb-offre-mutualisee-listes-diffusion-2026-longue/`

Référentiel : RGAA 4.1.2, 106 critères, 13 thématiques.

## Limite de statut

Cette grille donne un statut opérationnel `C / NC / NA` sur le périmètre testé.

Elle ne doit pas être utilisée seule comme déclaration réglementaire définitive, car le comportement réellement annoncé par lecteur d’écran pour les régions live et les changements de slide doit encore être confirmé par écoute humaine.

Légende :

- `C` : conforme sur le périmètre testé.
- `NC` : non conforme détecté.
- `NA` : non concerné sur le périmètre testé.

## Preuves exécutées

Commandes et contrôles réalisés :

```bash
python3 -m unittest discover -s miweb-offre-mutualisee-listes-diffusion-2026-longue/tests
npx --yes html-validate miweb-offre-mutualisee-listes-diffusion-2026-longue/index.html miweb-offre-mutualisee-listes-diffusion-2026-longue/alternatives.html miweb-offre-mutualisee-listes-diffusion-2026-longue/accessibilite.html index.html
npx --yes vnu-jar --errors-only miweb-offre-mutualisee-listes-diffusion-2026-longue/index.html miweb-offre-mutualisee-listes-diffusion-2026-longue/alternatives.html miweb-offre-mutualisee-listes-diffusion-2026-longue/accessibilite.html index.html
```

Résultats :

- tests unitaires : 6 tests OK ;
- `html-validate` : aucune erreur ;
- `vnu-jar` : aucune erreur ;
- AccessLint sur DOM rendu : aucune violation ;
- inspection DOM : aucun identifiant dupliqué, aucune référence ARIA cassée, images avec alternatives présentes ;
- trace interactive : changement de slide, focus sur le titre courant, statut `aria-live="polite"` mis à jour, ancre `#alternative-active` mise à jour ;
- limite restante : annonce réelle VoiceOver/NVDA des régions live non écoutée humainement.

## Synthèse

| Statut | Nombre |
|---|---:|
| Conforme | 52 |
| Non conforme | 0 |
| Non concerné | 54 |
| Total | 106 |

Taux indicatif sur critères applicables :

```text
52 / (52 + 0) * 100 = 100 %
```

Ce taux est indicatif pour le périmètre testé. Il ne vaut pas déclaration de conformité tant que les validations humaines restantes ne sont pas terminées.

## Synthèse par thématique

| Thématique | C | NC | NA |
|---|---:|---:|---:|
| 1. Images | 8 | 0 | 1 |
| 2. Cadres | 0 | 0 | 2 |
| 3. Couleurs | 3 | 0 | 0 |
| 4. Multimédia | 0 | 0 | 13 |
| 5. Tableaux | 0 | 0 | 8 |
| 6. Liens | 2 | 0 | 0 |
| 7. Scripts | 4 | 0 | 1 |
| 8. Éléments obligatoires | 7 | 0 | 3 |
| 9. Structuration de l’information | 3 | 0 | 1 |
| 10. Présentation de l’information | 13 | 0 | 1 |
| 11. Formulaires | 1 | 0 | 12 |
| 12. Navigation | 7 | 0 | 4 |
| 13. Consultation | 4 | 0 | 8 |

## Grille des 106 critères

| Critère | Statut | Justification synthétique |
|---|---|---|
| 1.1 | C | Les 6 images de slides portent une alternative textuelle. |
| 1.2 | NA | Aucune image décorative structurée comme image n’a été identifiée. |
| 1.3 | C | Les alternatives courtes décrivent la fonction informative des slides. |
| 1.4 | C | Les descriptions détaillées associées aux slides sont pertinentes sur le périmètre relu. |
| 1.5 | C | Les descriptions détaillées sont restituées dans les accordéons adjacents. |
| 1.6 | C | Chaque slide image texte dispose d’une description détaillée. |
| 1.7 | C | Les descriptions détaillées sont adjacentes aux images via accordéons. |
| 1.8 | C | Les images texte disposent d’un mécanisme de remplacement textuel. |
| 1.9 | C | Les images de slides sont reliées à une légende dans une figure. |
| 2.1 | NA | Aucun cadre ou iframe. |
| 2.2 | NA | Aucun cadre ou iframe. |
| 3.1 | C | L’information n’est pas donnée uniquement par la couleur. |
| 3.2 | C | Aucun contraste insuffisant détecté par AccessLint sur le DOM rendu. |
| 3.3 | C | Aucun défaut de contraste de composant d’interface détecté. |
| 4.1 | NA | Aucun média temporel préenregistré. |
| 4.2 | NA | Aucun média temporel avec sous-titres synchronisés. |
| 4.3 | NA | Aucun média temporel synchronisé. |
| 4.4 | NA | Aucun média temporel synchronisé avec sous-titres. |
| 4.5 | NA | Aucun média temporel nécessitant une audiodescription. |
| 4.6 | NA | Aucun média temporel avec audiodescription. |
| 4.7 | NA | Aucun média temporel. |
| 4.8 | NA | Aucun média non temporel hors images déjà traitées en thématique 1. |
| 4.9 | NA | Aucun média non temporel hors images déjà traitées en thématique 1. |
| 4.10 | NA | Aucun son déclenché automatiquement. |
| 4.11 | NA | Aucun lecteur de média temporel. |
| 4.12 | NA | Aucun média non temporel interactif. |
| 4.13 | NA | Aucun composant média à tester. |
| 5.1 | NA | Aucun tableau de données complexe. |
| 5.2 | NA | Aucun tableau de données complexe. |
| 5.3 | NA | Aucun tableau de mise en forme. |
| 5.4 | NA | Aucun tableau de données avec titre. |
| 5.5 | NA | Aucun tableau de données. |
| 5.6 | NA | Aucun tableau de données. |
| 5.7 | NA | Aucun tableau de données. |
| 5.8 | NA | Aucun tableau de mise en forme. |
| 6.1 | C | Les liens sont explicites dans leur contexte. |
| 6.2 | C | Chaque lien possède un intitulé accessible. |
| 7.1 | C | Les scripts exposent noms, rôles, états et changements de slide au DOM ; écoute lecteur d’écran encore à confirmer. |
| 7.2 | C | Sans JavaScript, les contenus essentiels restent disponibles. |
| 7.3 | C | Les scripts sont contrôlables au clavier et au pointeur. |
| 7.4 | C | Les changements de contexte sont déclenchés par action utilisateur ou restent contrôlables. |
| 7.5 | NA | Aucun message d’alerte non sollicité. |
| 8.1 | C | Type de document HTML présent. |
| 8.2 | C | Code source valide selon `html-validate` et `vnu-jar`. |
| 8.3 | C | Langue par défaut présente : `lang="fr"`. |
| 8.4 | C | Code de langue pertinent pour le contenu. |
| 8.5 | C | Titre de page présent. |
| 8.6 | C | Titre de page pertinent. |
| 8.7 | NA | Aucun changement de langue significatif identifié. |
| 8.8 | NA | Aucun changement de langue à restituer. |
| 8.9 | C | Aucune balise utilisée uniquement à des fins de présentation n’a été détectée. |
| 8.10 | NA | Aucun changement de direction de lecture. |
| 9.1 | C | Hiérarchie de titres cohérente sur la page principale. |
| 9.2 | C | Structure documentaire cohérente : en-tête, contenu principal, navigation, pied de page. |
| 9.3 | C | Les listes sont structurées correctement. |
| 9.4 | NA | Aucune citation à structurer. |
| 10.1 | C | L’information ne dépend pas uniquement de la forme, taille ou position. |
| 10.2 | C | Les contenus visibles porteurs d’information restent présents sans CSS. |
| 10.3 | C | L’ordre DOM reste compréhensible sans CSS. |
| 10.4 | C | Aucun blocage de lisibilité au zoom ou redimensionnement n’a été détecté. |
| 10.5 | C | Les déclarations de couleurs de fond et de police ne produisent pas de défaut confirmé. |
| 10.6 | C | Les liens restent identifiables par les conventions visuelles DSFR. |
| 10.7 | C | La prise de focus est visible sur les éléments interactifs contrôlés. |
| 10.8 | C | Les contenus masqués par le diaporama utilisent `hidden` et ne restent pas focusables. |
| 10.9 | C | L’information ne dépend pas uniquement de la forme, taille ou position. |
| 10.10 | C | Aucun contenu visible n’est restitué uniquement par positionnement CSS. |
| 10.11 | C | Pas de défilement horizontal global détecté sur petit viewport. |
| 10.12 | C | L’espacement du texte ne provoque pas de perte de contenu détectée. |
| 10.13 | C | Les contenus additionnels activables restent contrôlables. |
| 10.14 | NA | Aucun contenu additionnel CSS-only au survol ou au focus. |
| 11.1 | NA | Aucun champ de formulaire. |
| 11.2 | NA | Aucun champ de formulaire. |
| 11.3 | NA | Aucun champ de formulaire répété. |
| 11.4 | NA | Aucun champ de formulaire. |
| 11.5 | NA | Aucun champ de même nature à regrouper. |
| 11.6 | NA | Aucun regroupement de champs. |
| 11.7 | NA | Aucun regroupement de champs. |
| 11.8 | NA | Aucune liste de choix. |
| 11.9 | C | Les boutons présents ont un intitulé accessible et pertinent. |
| 11.10 | NA | Aucun contrôle de saisie. |
| 11.11 | NA | Aucun contrôle de saisie. |
| 11.12 | NA | Aucun formulaire modifiant ou transmettant des données. |
| 11.13 | NA | Aucun champ de saisie. |
| 12.1 | C | Plusieurs systèmes de navigation sont disponibles : accès rapides, navigation principale, sommaire, pied de page. |
| 12.2 | C | Les zones de navigation récurrentes sont placées de manière cohérente. |
| 12.3 | NA | Aucun plan du site sur ce périmètre. |
| 12.4 | NA | Aucun plan du site sur ce périmètre. |
| 12.5 | NA | Aucun moteur de recherche. |
| 12.6 | C | Les zones principales peuvent être atteintes ou évitées via liens d’évitement et landmarks. |
| 12.7 | C | Liens d’évitement présents et ciblant des ancres réelles. |
| 12.8 | C | Ordre de tabulation cohérent dans les parcours testés. |
| 12.9 | C | Aucun piège clavier détecté dans le diaporama ou les contrôles. |
| 12.10 | NA | Aucun raccourci clavier à touche de caractère. |
| 12.11 | C | Les contenus additionnels activables sont atteignables et contrôlables au clavier. |
| 13.1 | NA | Aucune limite de temps. |
| 13.2 | C | Aucune nouvelle fenêtre ouverte sans action utilisateur. |
| 13.3 | NA | Aucun document bureautique téléchargeable. |
| 13.4 | NA | Aucun document bureautique téléchargeable. |
| 13.5 | NA | Aucun contenu cryptique identifié. |
| 13.6 | NA | Aucun contenu en mouvement nécessitant contrôle. |
| 13.7 | NA | Aucun flash ou changement brusque de luminosité. |
| 13.8 | NA | Aucun contenu clignotant ou mouvement automatique identifié. |
| 13.9 | C | Le contenu reste consultable quelle que soit l’orientation. |
| 13.10 | C | Les fonctionnalités disponibles par geste peuvent aussi être utilisées par geste simple ou commande clavier. |
| 13.11 | C | Les actions au pointeur sont simples et non irréversibles. |
| 13.12 | NA | Aucune fonctionnalité impliquant un mouvement de l’appareil ou vers l’appareil. |

## Réserves humaines restantes

Les critères suivants sont marqués conformes ou non concernés sur la base du DOM, du clavier et des outils, mais restent à confirmer par écoute humaine si le livrable doit servir à une déclaration :

- 7.1 : annonce réelle des changements de slide et des régions live par VoiceOver/NVDA ;
- 12.8 et 12.9 : parcours clavier complet en navigateur graphique sur tous les modes ;
- 13.9 : vérification visuelle finale portrait/paysage sur appareils réels si publication mobile critique.
