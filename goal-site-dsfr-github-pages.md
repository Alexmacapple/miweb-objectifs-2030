# Goal - Site DSFR GitHub Pages slides accessibles

## Statut actuel - 2026-06-25

Ce fichier est une archive du goal initial de création de la V1. Il ne décrit plus la procédure active du dépôt.

État courant :

- dépôt actif : `/Users/alex/Claude/projets-heberges/miweb-objectifs-2030` ;
- variantes publiées : V1 à V4, jeu 5 condensé, jeu 6 long ;
- matrice active : `matrice-slide-ai/` ;
- création d’un nouveau jeu : `python3 matrice-slide-ai/create_variant.py ...` ;
- génération : `python3 <dossier-jeu>/build.py` ;
- publication racine : `python3 matrice-slide-ai/publish_variant.py --slug <dossier-jeu>`.

Conserver la suite comme historique de cadrage V1, pas comme consigne opérationnelle actuelle.

Contexte : cwd `/Users/alex/miweb-objectifs-2030`, branche `main` à vérifier.
Périmètre : modifier uniquement `/Users/alex/miweb-objectifs-2030` | Interdit : modifier `/Users/alex/Claude`, copier la contact sheet ou des essais, créer un backend, utiliser Git HTTPS.

Objectif : implémenter, tester, committer et pousser le site statique GitHub Pages v1 conforme à `/Users/alex/miweb-objectifs-2030/prompt-site-dsfr-github-pages.md`, y compris le mode plein écran accessible du diaporama.

Étapes :
1. Pré-vol : exécuter `git -C /Users/alex/miweb-objectifs-2030 rev-parse --show-toplevel`, `git -C /Users/alex/miweb-objectifs-2030 status --short`, `git -C /Users/alex/miweb-objectifs-2030 remote -v`, `ssh-add -l`, `python3 --version`; vérifier prompt, storyboard et 10 PNG `slide-01.png` à `slide-10.png` dans `/Users/alex/Claude/projets-actifs/ay11-snum-schema/projet-note-accessibilite-2030/outputs/ia-slides/2026-06-19-objectifs-2030-miweb-accessibilite-relu-sm/`.
2. Lire entièrement le prompt source et le storyboard `storyboard-slides-accessibilite-2030.md`.
3. Créer la racine versions et `miweb-objectifs-2030-v1/`; copier uniquement les 10 PNG finales dans `assets/slides/`.
4. Rédiger `slides.json` après inspection des PNG : 10 slides avec `titre`, `image`, `alt`, `description`, `textes_visibles`, `message`.
5. Créer `build.py` Python standard; générer `miweb-objectifs-2030-v1/index.html`, `alternatives.html`, `accessibilite.html`, `alternatives.md`, `README.md` et le ZIP.
6. Implémenter DSFR et accessibilité : en-tête, pied de page, sommaire, liens d’évitement réels, accordéons fermés, boutons natifs, focus titre slide, `aria-live`, `aria-pressed`, ancres `#slide-01`, no-JS avec 10 slides visibles et lien vers `alternatives.html`.
7. Implémenter le plein écran du diaporama complet : bouton natif `Plein écran` / `Quitter le plein écran`, cible `#diaporama`, Fullscreen API (`requestFullscreen`, `exitFullscreen`, `fullscreenchange`, `document.fullscreenElement`), contrôles conservés, alternatives accessibles par défilement, absence de piège clavier et fallback natif si l’API est indisponible.
8. Implémenter une CSP compatible GitHub Pages : meta CSP en enforcement, pas de `unsafe-inline`, hash des styles inline, nonce et `strict-dynamic` pour les scripts, ressources DSFR nécessaires autorisées, aucune issue Chrome DevTools liée à une ressource bloquée.
9. Surveiller : arrêter si source manquante, CDN DSFR indisponible, Playwright absent, changements Git non liés, ou alternative non vérifiable contre PNG.
10. Audit statique : 10 images, pages non vides, ZIP, `alternatives.md`, `README.md`, aucun `href="#"`, liens internes et pied de page réels, chemins relatifs, aucun `hidden` initial sur sections de slides, `alt` des images de slides courts et inférieurs ou égaux à 60 caractères, bouton plein écran présent avec `aria-pressed`, code Fullscreen API, styles `#diaporama:fullscreen`, CSP présente sans `unsafe-inline`, et association RGAA 1.9 des images légendées via `figure`, `figcaption`, `role="group"` ou `role="figure"`, `aria-label` strictement identique au `figcaption`.
11. Audit navigateur : depuis `/Users/alex/miweb-objectifs-2030`, lancer `python3 -m http.server 8000`; tester avec Playwright desktop, mobile et JavaScript désactivé toutes les assertions du prompt source, dont le contrôle plein écran si l’environnement l’autorise, ou au minimum sa présence et son état initial; vérifier Lighthouse sans issue Chrome DevTools et sans erreur console.
12. Git : si audits OK, commit conventionnel français, vérifier SSH, pousser `main` vers `git@github.com:Alexmacapple/miweb-objectifs-2030.git`, vérifier GitHub Pages sur `main` racine.
13. Compte rendu : fichiers modifiés, commandes et résultats, URL locale testée, état Git, URL GitHub Pages ou blocage exact.

Si échec : diagnostiquer, corriger une fois si cause locale comprise; sinon arrêter avec blocage précis.

DoD :
- Racine versions et diaporama v1 DSFR accessibles fonctionnent.
- Le diaporama dispose d’un mode plein écran accessible : bouton natif, état `aria-pressed`, synchronisation `fullscreenchange`, contrôles conservés et alternatives accessibles.
- Les images de slides légendées satisfont le contrôle structurel RGAA 1.9 attendu par le pré-audit.
- Les images de slides ont des `alt` courts, l’alternative longue restant dans l’accordéon et la page dédiée.
- La CSP est effective sans `unsafe-inline`, ne bloque pas les ressources DSFR nécessaires et ne génère pas d’issue Chrome DevTools.
- Les 10 PNG relues SM, `slides.json`, pages HTML, `alternatives.md`, `README.md`, `build.py` et ZIP existent et correspondent au prompt source.
- Audits statiques et Playwright desktop, mobile, sans JavaScript passent avec preuves.
- Commit poussé en SSH sur `origin/main`; GitHub Pages vérifié ou blocage externe documenté.
- Aucun fichier hors `/Users/alex/miweb-objectifs-2030` modifié.

Auto-note : ◆ seulement si pré-vols, audits, DoD et preuves sont présents.
