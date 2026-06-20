# Audit RGAA 4.1.2 - Objectifs 2030 - accessibilité numérique

Date : 20 juin 2026

Commit audité : `e123cd2`

Tag de retour arrière : `site-revert-2026-06-20-e123cd2`

Site local audité : `http://127.0.0.1:8000/`

Site publié de référence : `https://alexmacapple.github.io/miweb-objectifs-2030/`

Référentiel : RGAA 4.1.2, 106 critères, 13 thématiques.

## Périmètre

Pages testées :

- `index.html`
- `miweb-objectifs-2030-v1/index.html`
- `miweb-objectifs-2030-v1/alternatives.html`
- `miweb-objectifs-2030-v1/accessibilite.html`

Contenus et fonctionnalités testés :

- diaporama v1 ;
- alternatives textuelles ;
- page accessibilité ;
- navigation DSFR desktop et mobile ;
- mode toutes les slides ;
- mode projection par URL ;
- contrôles clavier ;
- consultation sans JavaScript ;
- téléchargement ZIP des slides.

## Outils et preuves

Commandes exécutées :

```bash
python3 -m unittest discover -s miweb-objectifs-2030-v1/tests
npx --yes html-validate miweb-objectifs-2030-v1/index.html miweb-objectifs-2030-v1/alternatives.html miweb-objectifs-2030-v1/accessibilite.html index.html
npx --yes vnu-jar --errors-only miweb-objectifs-2030-v1/index.html miweb-objectifs-2030-v1/alternatives.html miweb-objectifs-2030-v1/accessibilite.html index.html
npx --yes @axe-core/cli http://127.0.0.1:8000/ http://127.0.0.1:8000/miweb-objectifs-2030-v1/ http://127.0.0.1:8000/miweb-objectifs-2030-v1/alternatives.html http://127.0.0.1:8000/miweb-objectifs-2030-v1/accessibilite.html --tags wcag2a,wcag2aa,wcag21a,wcag21aa --stdout
npx --yes pa11y <url> --standard WCAG2AA
```

Résultats :

- tests unitaires : 16 tests OK ;
- `html-validate` : aucune erreur ;
- `vnu-jar` : aucune erreur ;
- axe-core 4.11.1 : 0 violation sur les 4 pages ;
- axe-core : 1 contrôle incomplet par page sur les contrastes de liens DSFR, lié à des fonds en gradient ou pseudo-éléments que l’outil ne sait pas résoudre ;
- contrôle manuel des contrastes actionnables via Chromium : contraste minimal calculé 5,74:1, hors composants désactivés ;
- `pa11y` : aucune issue sur les 4 pages ;
- liens, fragments et ressources locales : OK ;
- 10 images de slides présentes, format `1672 x 941`, RGB ;
- ZIP présent, avec les 10 PNG et `alternatives.md` ;
- arbre d’accessibilité Chrome DevTools : contrôles principaux nommés et exposés ;
- tests Playwright : navigation au clavier, focus programmatique, no-JS, menu mobile, mode toutes les slides et URL `?projection=1#slide-04` OK ;
- reflow 320 px et espacement de texte : pas de défilement horizontal global détecté.

## Synthèse

Aucune non-conformité RGAA bloquante ou mineure n’a été détectée sur le périmètre audité.

Le site est techniquement conforme sur les critères RGAA applicables au périmètre testé.

| Statut | Nombre |
|---|---:|
| Conforme | 52 |
| Non conforme | 0 |
| Non applicable | 54 |
| Non testé | 0 |

Taux de conformité RGAA sur critères applicables :

```text
52 / (52 + 0) * 100 = 100 %
```

État proposé sur ce périmètre : totalement conforme.

Important : ce rapport ne remplace pas une certification externe ni une campagne avec utilisateurs ou lecteurs d’écran réels. Il constitue un audit technique complet du site statique audité localement, avec revue manuelle et automatisée des 106 critères.

## Points de vigilance hors non-conformité

1. La page `accessibilite.html` indique encore que le site est non audité. Si le résultat de cet audit doit être publié, cette page devra être mise à jour localement puis validée avant commit/push.
2. Le lien de pied de page `Présentation plein écran` possède une URL de repli valide (`?projection=1#slide-01`) et peut être intercepté en JavaScript sur la page diaporama pour déclencher le plein écran. Ce fonctionnement reste défendable car le lien conserve une destination réelle, mais le bouton du header et le bouton du diaporama restent la sémantique la plus stricte pour l’action de plein écran.
3. Les slides sont des images texte. Le site fournit un mécanisme de remplacement textuel adjacent via accordéon et page dédiée, ce qui évite une non-conformité sur le périmètre audité. Une version HTML native des slides resterait encore plus robuste à long terme.
4. Les tests de technologies d’assistance ont été faits par arbre d’accessibilité Chromium, axe-core et inspection DOM. Aucun test VoiceOver/NVDA manuel n’a été exécuté dans cette passe.

## Synthèse par thématique

| Thématique | C | NC | NA | NT | Taux |
|---|---:|---:|---:|---:|---:|
| 1. Images | 8 | 0 | 1 | 0 | 100 % |
| 2. Cadres | 0 | 0 | 2 | 0 | NA |
| 3. Couleurs | 3 | 0 | 0 | 0 | 100 % |
| 4. Multimédia | 0 | 0 | 13 | 0 | NA |
| 5. Tableaux | 0 | 0 | 8 | 0 | NA |
| 6. Liens | 2 | 0 | 0 | 0 | 100 % |
| 7. Scripts | 4 | 0 | 1 | 0 | 100 % |
| 8. Éléments obligatoires | 7 | 0 | 3 | 0 | 100 % |
| 9. Structuration | 3 | 0 | 1 | 0 | 100 % |
| 10. Présentation | 13 | 0 | 1 | 0 | 100 % |
| 11. Formulaires | 1 | 0 | 12 | 0 | 100 % |
| 12. Navigation | 7 | 0 | 4 | 0 | 100 % |
| 13. Consultation | 4 | 0 | 8 | 0 | 100 % |

## Détail des critères RGAA

| Critère | Statut | Justification synthétique |
|---|---|---|
| 1.1 | C | Les 10 images de slides portent un attribut `alt`. |
| 1.2 | NA | Aucune image décorative structurée comme image n’a été identifiée. |
| 1.3 | C | Les alternatives courtes identifient le rôle du visuel sans dupliquer la description longue. |
| 1.4 | C | Les descriptions détaillées associées aux slides sont pertinentes. |
| 1.5 | C | Les descriptions détaillées sont disponibles dans l’accordéon adjacent et dans `alternatives.html`. |
| 1.6 | C | Chaque slide image texte dispose d’une description détaillée. |
| 1.7 | C | Les descriptions détaillées sont adjacentes via accordéon et accessibles aussi en page dédiée. |
| 1.8 | C | Les slides images texte disposent d’un mécanisme de remplacement textuel adjacent et d’une page alternative. |
| 1.9 | C | Chaque slide est dans une `figure` avec `figcaption`, `role="figure"` et `aria-label` identique au `figcaption`. |
| 2.1 | NA | Aucun cadre ou iframe. |
| 2.2 | NA | Aucun cadre ou iframe. |
| 3.1 | C | L’information n’est pas portée uniquement par la couleur ; les alternatives textuelles restituent les informations des visuels. |
| 3.2 | C | Aucun contraste insuffisant détecté ; contraste actionnable minimal calculé à 5,74:1. |
| 3.3 | C | Les composants d’interface DSFR et boutons personnalisés restent perceptibles ; aucune violation axe/pa11y. |
| 4.1 | NA | Aucun média temporel pré-enregistré. |
| 4.2 | NA | Aucun sous-titre synchronisé attendu. |
| 4.3 | NA | Aucun média temporel synchronisé. |
| 4.4 | NA | Aucun média temporel synchronisé. |
| 4.5 | NA | Aucun média temporel nécessitant audiodescription. |
| 4.6 | NA | Aucun média temporel avec audiodescription. |
| 4.7 | NA | Aucun média temporel. |
| 4.8 | NA | Aucun média non temporel hors images déjà traitées en thématique 1. |
| 4.9 | NA | Aucun média non temporel hors images déjà traitées en thématique 1. |
| 4.10 | NA | Aucun son déclenché automatiquement. |
| 4.11 | NA | Aucun lecteur média temporel. |
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
| 6.1 | C | Les intitulés de liens sont explicites dans leur contexte. |
| 6.2 | C | Tous les liens ont un intitulé ; aucun `href="#"` ou `href=""`. |
| 7.1 | C | Les scripts exposent noms, rôles et états ; axe, pa11y et arbre AX OK. |
| 7.2 | C | La page principale reste exploitable sans JavaScript : toutes les slides sont visibles et les alternatives restent accessibles. |
| 7.3 | C | Les actions scripts sont contrôlables au clavier : boutons natifs, flèches, Home, End, accordéons, menu mobile. |
| 7.4 | C | Les changements de contexte sont déclenchés par action utilisateur et restent contrôlables. |
| 7.5 | NA | Aucun message d’alerte non sollicité. |
| 8.1 | C | Doctype HTML présent sur les 4 pages. |
| 8.2 | C | Code HTML valide selon `html-validate` et `vnu-jar`. |
| 8.3 | C | `lang="fr"` présent sur les 4 pages. |
| 8.4 | C | Code de langue pertinent. |
| 8.5 | C | Titre de page présent sur les 4 pages. |
| 8.6 | C | Titres de page pertinents. |
| 8.7 | NA | Aucun changement de langue significatif dans le contenu audité. |
| 8.8 | NA | Aucun changement de langue à restituer. |
| 8.9 | C | Aucune balise utilisée uniquement à des fins de présentation n’a été détectée. |
| 8.10 | NA | Aucun changement de direction de lecture. |
| 9.1 | C | Hiérarchie de titres cohérente sur les pages auditées. |
| 9.2 | C | Structure documentaire cohérente : header, main, navigation, footer. |
| 9.3 | C | Listes structurées correctement ; aucune violation axe/pa11y. |
| 9.4 | NA | Aucune citation à structurer. |
| 10.1 | C | Présentation contrôlée par CSS sans perte d’information. |
| 10.2 | C | Les contenus restent présents sans CSS. |
| 10.3 | C | L’ordre DOM reste compréhensible sans CSS. |
| 10.4 | C | Le site reste consultable en petit viewport ; pas de blocage lié au redimensionnement du texte détecté. |
| 10.5 | C | Déclarations de couleurs et fonds cohérentes ; aucun problème de contraste confirmé. |
| 10.6 | C | Les liens sont identifiables autrement que par la couleur via les conventions DSFR. |
| 10.7 | C | La prise de focus reste visible sur les composants contrôlés. |
| 10.8 | C | Les contenus masqués par JavaScript le sont avec `hidden` et ne reçoivent pas le focus. |
| 10.9 | C | L’information ne dépend pas uniquement de la forme, de la taille ou de la position. |
| 10.10 | C | Aucun contenu visible n’est restitué uniquement par positionnement CSS. |
| 10.11 | C | À 320 px de largeur et 256 px de hauteur, pas de défilement horizontal global. |
| 10.12 | C | L’espacement de texte redéfini ne provoque pas de perte de contenu ou de fonctionnalité détectée. |
| 10.13 | C | Les contenus additionnels activables restent contrôlables par l’utilisateur. |
| 10.14 | NA | Aucun contenu additionnel CSS-only au survol ou focus. |
| 11.1 | NA | Aucun champ de formulaire. |
| 11.2 | NA | Aucun champ de formulaire. |
| 11.3 | NA | Aucun champ de formulaire. |
| 11.4 | NA | Aucun champ de formulaire. |
| 11.5 | NA | Aucun champ de formulaire. |
| 11.6 | NA | Aucun regroupement de champs. |
| 11.7 | NA | Aucun regroupement de champs. |
| 11.8 | NA | Aucune liste de choix. |
| 11.9 | C | Les boutons présents ont un intitulé accessible et pertinent. |
| 11.10 | NA | Aucun contrôle de saisie. |
| 11.11 | NA | Aucun contrôle de saisie. |
| 11.12 | NA | Aucun formulaire modifiant ou transmettant des données. |
| 11.13 | NA | Aucun champ de saisie. |
| 12.1 | C | Plusieurs systèmes de navigation sont disponibles : accès rapides, header/footer, sommaire, fil d’Ariane sur les pages v1. |
| 12.2 | C | Navigation et zones récurrentes placées de manière cohérente. |
| 12.3 | NA | Aucun plan du site. |
| 12.4 | NA | Aucun plan du site. |
| 12.5 | NA | Aucun moteur de recherche. |
| 12.6 | C | Les zones principales peuvent être atteintes ou évitées via liens d’évitement et landmarks. |
| 12.7 | C | Liens d’évitement présents et ciblant des ancres réelles. |
| 12.8 | C | Ordre de tabulation cohérent avec l’ordre DOM et les interactions testées. |
| 12.9 | C | Aucun piège clavier détecté, y compris dans le diaporama et le menu mobile. |
| 12.10 | NA | Aucun raccourci clavier à une seule touche de caractère. |
| 12.11 | C | Accordéons et menu mobile sont atteignables et contrôlables au clavier. |
| 13.1 | NA | Aucune limite de temps. |
| 13.2 | C | Aucune nouvelle fenêtre ouverte sans action utilisateur. |
| 13.3 | NA | Aucun document bureautique téléchargeable ; le ZIP contient des PNG et `alternatives.md`. |
| 13.4 | NA | Aucun document bureautique téléchargeable. |
| 13.5 | NA | Aucun contenu cryptique identifié. |
| 13.6 | NA | Aucun contenu en mouvement. |
| 13.7 | NA | Aucun flash ou changement brusque de luminosité. |
| 13.8 | NA | Aucun contenu clignotant. |
| 13.9 | C | Le contenu reste consultable en orientation portrait et paysage. |
| 13.10 | C | Les fonctionnalités sont disponibles par gestes simples : liens et boutons natifs. |
| 13.11 | C | Les actions au pointeur sont des activations simples, sans geste complexe ni déclenchement irréversible. |
| 13.12 | NA | Aucune fonctionnalité liée au mouvement de l’appareil ou de l’utilisateur. |

## Références

- RGAA 4.1.2, critères et tests : <https://accessibilite.numerique.gouv.fr/methode/criteres-et-tests/>
- Portail officiel de l’accessibilité numérique : <https://accessibilite.numerique.gouv.fr/>
- Kit d’audit RGAA : <https://accessibilite.numerique.gouv.fr/ressources/kit-audit/>

## Conclusion

Le site audité ne présente pas de non-conformité RGAA détectée sur le périmètre testé.

La seule action recommandée avant publication d’un statut d’accessibilité est éditoriale : décider si la page `accessibilite.html` doit rester prudente ou être mise à jour pour refléter cet audit.
