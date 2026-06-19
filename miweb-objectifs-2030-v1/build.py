#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
SLIDES_PATH = ROOT / "slides.json"
SLIDES_DIR = ROOT / "assets" / "slides"
DOWNLOADS_DIR = ROOT / "assets" / "downloads"
ZIP_NAME = "miweb-objectifs-2030-v1-slides.zip"
ZIP_PATH = DOWNLOADS_DIR / ZIP_NAME

SITE_TITLE = "Objectifs 2030 - Accessibilité numérique"
BASELINE = "MiWeb - Juin 2026"
VERSION_LABEL = "Version 1 - Juin 2026"
SITE_DESCRIPTION = "Version web accessible des slides Objectifs 2030 - Accessibilité numérique, avec navigation clavier et alternatives textuelles."
DSFR_VERSION = "1.14.4"

DSFR_CSS = f"https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@{DSFR_VERSION}/dist/dsfr/dsfr.min.css"
DSFR_UTILITY_CSS = f"https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@{DSFR_VERSION}/dist/utility/utility.min.css"
DSFR_MODULE_JS = f"https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@{DSFR_VERSION}/dist/dsfr/dsfr.module.min.js"
DSFR_NOMODULE_JS = f"https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@{DSFR_VERSION}/dist/dsfr/dsfr.nomodule.min.js"


CUSTOM_CSS = """
.miweb-page-header {
  margin-bottom: 2rem;
}

.miweb-version {
  color: var(--text-mention-grey);
}

.miweb-summary-zone {
  margin-bottom: 2rem;
}

.miweb-slide-controls {
  align-items: center;
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  justify-content: center;
  margin: 1.5rem 0;
}

.miweb-slide-status {
  font-weight: 700;
  margin: 0;
}

.miweb-slide-section {
  margin-bottom: 2.5rem;
}

.miweb-slide-section[hidden] {
  display: none;
}

.miweb-slide-title {
  margin-bottom: 1rem;
}

.miweb-slide-frame {
  margin: 0 auto 1rem;
  max-width: 1120px;
  width: 100%;
}

.miweb-slide-frame img {
  border: 1px solid var(--border-default-grey);
  display: block;
  height: auto;
  width: 100%;
}

.miweb-slide-caption {
  color: var(--text-mention-grey);
  font-size: 0.875rem;
  margin-top: 0.5rem;
  text-align: center;
}

.miweb-text-page {
  max-width: 48rem;
}

.miweb-download-link {
  margin-top: 0.75rem;
}

@media print {
  .fr-skiplinks,
  .fr-header,
  .fr-summary,
  .miweb-slide-controls,
  .fr-footer {
    display: none !important;
  }

  .miweb-slide-section[hidden] {
    display: block !important;
  }

  .miweb-slide-section,
  .miweb-alt-section {
    break-inside: avoid;
    page-break-inside: avoid;
  }

  a[href]::after {
    content: " (" attr(href) ")";
    font-size: 0.85em;
  }
}
"""


MAIN_JS = """
(() => {
  const slides = Array.from(document.querySelectorAll("[data-slide-section]"));
  const summaryLinks = Array.from(document.querySelectorAll("[data-slide-link]"));
  const alternativeButtons = Array.from(document.querySelectorAll("[data-alternative-button]"));
  const previousButton = document.querySelector("[data-slide-previous]");
  const nextButton = document.querySelector("[data-slide-next]");
  const allButton = document.querySelector("[data-slide-all]");
  const status = document.querySelector("[data-slide-status]");
  const total = slides.length;
  let currentIndex = getIndexFromHash();
  let allMode = false;

  function getIndexFromHash() {
    const match = window.location.hash.match(/^#slide-(\\d{2})$/);
    if (!match) return 0;
    const index = Number.parseInt(match[1], 10) - 1;
    return Number.isInteger(index) && index >= 0 && index < total ? index : 0;
  }

  function slideHash(index) {
    return `#slide-${String(index + 1).padStart(2, "0")}`;
  }

  function updateAlternativeAnchor() {
    alternativeButtons.forEach((button) => {
      if (button.id === "alternative-active") button.removeAttribute("id");
    });
    if (alternativeButtons[currentIndex]) alternativeButtons[currentIndex].id = "alternative-active";
  }

  function updateButtons() {
    previousButton.disabled = currentIndex === 0;
    nextButton.disabled = currentIndex === total - 1;
    allButton.setAttribute("aria-pressed", allMode ? "true" : "false");
    allButton.textContent = allMode ? "Revenir au mode diaporama" : "Afficher toutes les slides";
  }

  function updateStatus() {
    status.textContent = allMode ? `Toutes les slides affichées (${total})` : `Slide ${currentIndex + 1} sur ${total}`;
  }

  function applyVisibility() {
    slides.forEach((slide, index) => {
      slide.hidden = !allMode && index !== currentIndex;
    });
  }

  function setUrl(index, replace) {
    const hash = slideHash(index);
    if (window.location.hash === hash) return;
    const method = replace ? "replaceState" : "pushState";
    window.history[method](null, "", hash);
  }

  function focusCurrentTitle() {
    const title = slides[currentIndex].querySelector("[data-slide-title]");
    if (title) title.focus({ preventScroll: false });
  }

  function showSlide(index, options = {}) {
    currentIndex = Math.max(0, Math.min(total - 1, index));
    allMode = false;
    applyVisibility();
    updateAlternativeAnchor();
    updateButtons();
    updateStatus();
    setUrl(currentIndex, options.replace === true);
    if (options.focus === true) focusCurrentTitle();
  }

  function showAllSlides() {
    allMode = true;
    applyVisibility();
    updateAlternativeAnchor();
    updateButtons();
    updateStatus();
  }

  previousButton.addEventListener("click", () => showSlide(currentIndex - 1, { focus: true }));
  nextButton.addEventListener("click", () => showSlide(currentIndex + 1, { focus: true }));
  allButton.addEventListener("click", () => {
    if (allMode) showSlide(currentIndex, { focus: true });
    else showAllSlides();
  });

  summaryLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
      const targetIndex = slides.findIndex((slide) => `#${slide.id}` === link.hash);
      if (targetIndex === -1) return;
      event.preventDefault();
      showSlide(targetIndex, { focus: true });
    });
  });

  window.addEventListener("popstate", () => showSlide(getIndexFromHash(), { replace: true }));

  document.addEventListener("keydown", (event) => {
    if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
    if (["INPUT", "TEXTAREA", "SELECT"].includes(event.target.tagName)) return;
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      showSlide(currentIndex - 1, { focus: true });
    } else if (event.key === "ArrowRight") {
      event.preventDefault();
      showSlide(currentIndex + 1, { focus: true });
    } else if (event.key === "Home") {
      event.preventDefault();
      showSlide(0, { focus: true });
    } else if (event.key === "End") {
      event.preventDefault();
      showSlide(total - 1, { focus: true });
    }
  });

  showSlide(currentIndex, { replace: true });
})();
"""


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def slide_id(slide: dict) -> str:
    return f"slide-{int(slide['numero']):02d}"


def load_slides() -> list[dict]:
    slides = json.loads(SLIDES_PATH.read_text(encoding="utf-8"))
    if len(slides) != 10:
        raise ValueError("slides.json doit contenir exactement 10 slides.")
    required = {"numero", "titre", "image", "alt", "description", "textes_visibles", "message"}
    for slide in slides:
        missing = required - set(slide)
        if missing:
            raise ValueError(f"Slide {slide.get('numero', '?')} incomplète : {sorted(missing)}")
    return slides


def dsfr_assets() -> str:
    return f"""<link rel="stylesheet" href="{DSFR_CSS}">
  <link rel="stylesheet" href="{DSFR_UTILITY_CSS}">"""


def dsfr_scripts(extra_script: str = "") -> str:
    script = f"""<script type="module" src="{DSFR_MODULE_JS}"></script>
  <script nomodule src="{DSFR_NOMODULE_JS}"></script>"""
    if extra_script:
        script += f"\n  <script>{extra_script}</script>"
    return script


def skiplinks(links: list[tuple[str, str]]) -> str:
    items = "\n".join(
        f'        <li><a class="fr-link" href="{esc(href)}">{esc(label)}</a></li>' for label, href in links
    )
    return f"""<div class="fr-skiplinks">
    <nav role="navigation" aria-label="Accès rapide" class="fr-container">
      <ul class="fr-skiplinks__list">
{items}
      </ul>
    </nav>
  </div>"""


def header(home_href: str) -> str:
    return f"""<header role="banner" class="fr-header">
    <div class="fr-header__body">
      <div class="fr-container">
        <div class="fr-header__body-row">
          <div class="fr-header__brand fr-enlarge-link">
            <div class="fr-header__brand-top">
              <div class="fr-header__logo">
                <p class="fr-logo">République<br>Française</p>
              </div>
            </div>
            <div class="fr-header__service">
              <a href="{esc(home_href)}" title="Accueil - {esc(SITE_TITLE)}">
                <p class="fr-header__service-title">{esc(SITE_TITLE)}</p>
              </a>
              <p class="fr-header__service-tagline">{esc(BASELINE)}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>"""


def footer(version_context: bool) -> str:
    links = {
        "Présentation": "./" if version_context else "miweb-objectifs-2030-v1/",
        "Alternatives textuelles": "alternatives.html" if version_context else "miweb-objectifs-2030-v1/alternatives.html",
        "Télécharger les slides": f"assets/downloads/{ZIP_NAME}" if version_context else f"miweb-objectifs-2030-v1/assets/downloads/{ZIP_NAME}",
    }
    items = "\n".join(
        f'              <li class="fr-footer__content-item"><a class="fr-footer__content-link" href="{esc(href)}">{esc(label)}</a></li>'
        for label, href in links.items()
    )
    return f"""<footer class="fr-footer" role="contentinfo" id="footer">
    <div class="fr-container">
      <div class="fr-footer__body">
        <div class="fr-footer__brand">
          <p class="fr-logo">République<br>Française</p>
        </div>
        <div class="fr-footer__content">
          <p class="fr-footer__content-desc">{esc(SITE_TITLE)} - {esc(BASELINE)}.</p>
          <ul class="fr-footer__content-list">
{items}
          </ul>
        </div>
      </div>
      <div class="fr-footer__bottom">
        <p class="fr-footer__bottom-copy">{esc(VERSION_LABEL)}</p>
      </div>
    </div>
  </footer>"""


def breadcrumb(current: str) -> str:
    return f"""<nav role="navigation" class="fr-breadcrumb" aria-label="vous êtes ici :">
    <button class="fr-breadcrumb__button" aria-expanded="false" aria-controls="breadcrumb">Voir le fil d’Ariane</button>
    <div class="fr-collapse" id="breadcrumb">
      <ol class="fr-breadcrumb__list">
        <li><a class="fr-breadcrumb__link" href="../">Versions</a></li>
        <li><a class="fr-breadcrumb__link" href="./">{esc(SITE_TITLE)}</a></li>
        <li><a class="fr-breadcrumb__link" aria-current="page">{esc(current)}</a></li>
      </ol>
    </div>
  </nav>"""


def page(title: str, body: str, skip_links: list[tuple[str, str]], version_context: bool, extra_script: str = "") -> str:
    home_href = "./" if version_context else "./"
    full_title = SITE_TITLE if title == SITE_TITLE else f"{title} - {SITE_TITLE}"
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{esc(SITE_DESCRIPTION)}">
  <title>{esc(full_title)}</title>
  {dsfr_assets()}
  <style>{CUSTOM_CSS}</style>
</head>
<body>
  {skiplinks(skip_links)}
  {header(home_href)}
  {body}
  {footer(version_context)}
  {dsfr_scripts(extra_script)}
</body>
</html>
"""


def render_root() -> str:
    body = f"""<main id="contenu" class="fr-container fr-py-6w">
    <div class="miweb-page-header">
      <h1>{esc(SITE_TITLE)}</h1>
      <p class="fr-text--lead">{esc(BASELINE)}</p>
    </div>
    <section aria-labelledby="versions-title">
      <h2 id="versions-title">Versions disponibles</h2>
      <div class="fr-grid-row fr-grid-row--gutters">
        <div class="fr-col-12 fr-col-md-6">
          <div class="fr-tile fr-enlarge-link">
            <div class="fr-tile__body">
              <h3 class="fr-tile__title"><a href="miweb-objectifs-2030-v1/">Version 1 - Juin 2026</a></h3>
              <p class="fr-tile__desc">Slides accessibles au format web.</p>
            </div>
          </div>
        </div>
      </div>
      <p class="fr-mt-3w">D’autres versions pourront être ajoutées ultérieurement.</p>
    </section>
  </main>"""
    return page(SITE_TITLE, body, [("Accéder au contenu", "#contenu"), ("Accéder au pied de page", "#footer")], False)


def render_summary(slides: list[dict]) -> str:
    items = "\n".join(
        f'        <li><a class="fr-summary__link" data-slide-link href="#{slide_id(slide)}">Slide {slide["numero"]} - {esc(slide["titre"])}</a></li>'
        for slide in slides
    )
    return f"""<nav class="fr-summary" role="navigation" aria-labelledby="summary-title" id="sommaire">
      <h2 class="fr-summary__title" id="summary-title">Sommaire</h2>
      <ol>
{items}
      </ol>
    </nav>"""


def render_slide(slide: dict, total: int) -> str:
    number = int(slide["numero"])
    sid = slide_id(slide)
    texts = "\n".join(f"              <li>{esc(text)}</li>" for text in slide["textes_visibles"])
    button_id = ' id="alternative-active"' if number == 1 else ""
    return f"""      <section class="miweb-slide-section" id="{sid}" data-slide-section aria-labelledby="{sid}-title">
        <h3 class="miweb-slide-title" id="{sid}-title" data-slide-title tabindex="-1">Slide {number} - {esc(slide["titre"])}</h3>
        <figure class="miweb-slide-frame">
          <img src="{esc(slide["image"])}" alt="{esc(slide["alt"])}" width="1672" height="941">
          <figcaption class="miweb-slide-caption">Slide {number} sur {total} - {esc(slide["titre"])}</figcaption>
        </figure>
        <div class="fr-accordions-group" data-fr-group="false">
          <section class="fr-accordion">
            <h4 class="fr-accordion__title">
              <button{button_id} type="button" class="fr-accordion__btn" aria-expanded="false" aria-controls="alternative-{sid}" data-alternative-button>Lire l’alternative textuelle de la slide {number}</button>
            </h4>
            <div id="alternative-{sid}" class="fr-collapse">
              <p>{esc(slide["description"])}</p>
              <h5>Textes visibles</h5>
              <ul>
{texts}
              </ul>
              <h5>Message à retenir</h5>
              <p>{esc(slide["message"])}</p>
            </div>
          </section>
        </div>
      </section>"""


def render_v1_index(slides: list[dict]) -> str:
    rendered_slides = "\n".join(render_slide(slide, len(slides)) for slide in slides)
    body = f"""<main id="contenu" class="fr-container fr-py-4w">
    <div class="miweb-page-header">
      <h1>{esc(SITE_TITLE)}</h1>
      <p><a class="fr-link" href="alternatives.html">Consulter toutes les alternatives textuelles</a></p>
    </div>
    <div class="miweb-summary-zone">
{render_summary(slides)}
    </div>
    <section id="diaporama" aria-labelledby="diaporama-title">
      <h2 id="diaporama-title">Présentation</h2>
      <nav class="miweb-slide-controls" aria-label="Contrôles du diaporama">
        <button type="button" class="fr-btn fr-btn--secondary fr-icon-arrow-left-line fr-btn--icon-left" data-slide-previous>Précédente</button>
        <p class="miweb-slide-status" aria-live="polite" data-slide-status>Slide 1 sur {len(slides)}</p>
        <button type="button" class="fr-btn fr-icon-arrow-right-line fr-btn--icon-right" data-slide-next>Suivante</button>
        <button type="button" class="fr-btn fr-btn--tertiary" aria-pressed="false" data-slide-all>Afficher toutes les slides</button>
        <a class="fr-btn fr-btn--secondary fr-icon-download-line fr-btn--icon-left" href="assets/downloads/{ZIP_NAME}" download>Télécharger les slides au format ZIP</a>
      </nav>
      <div>
{rendered_slides}
      </div>
    </section>
  </main>"""
    skip = [
        ("Accéder au contenu", "#contenu"),
        ("Accéder au sommaire", "#sommaire"),
        ("Accéder au diaporama", "#diaporama"),
        ("Accéder aux alternatives", "#alternative-active"),
        ("Accéder au pied de page", "#footer"),
    ]
    return page(SITE_TITLE, body, skip, True, MAIN_JS)


def render_alternatives(slides: list[dict]) -> str:
    sections = []
    for slide in slides:
        sid = slide_id(slide)
        texts = "\n".join(f"          <li>{esc(text)}</li>" for text in slide["textes_visibles"])
        sections.append(f"""      <section class="miweb-alt-section" id="alternative-{sid}">
        <h2>Slide {slide["numero"]} - {esc(slide["titre"])}</h2>
        <p><a class="fr-link" href="./#{sid}">Voir la slide {slide["numero"]} dans le diaporama</a></p>
        <h3>Description</h3>
        <p>{esc(slide["description"])}</p>
        <h3>Textes visibles</h3>
        <ul>
{texts}
        </ul>
        <h3>Message à retenir</h3>
        <p>{esc(slide["message"])}</p>
      </section>""")
    body = f"""<main id="contenu" class="fr-container fr-py-4w miweb-text-page">
    {breadcrumb("Alternatives textuelles")}
    <h1>Alternatives textuelles</h1>
    <p class="fr-text--lead">{esc(SITE_TITLE)} - {esc(VERSION_LABEL)}</p>
{chr(10).join(sections)}
  </main>"""
    return page("Alternatives textuelles", body, [("Accéder au contenu", "#contenu"), ("Accéder au pied de page", "#footer")], True)


def render_accessibility() -> str:
    body = f"""<main id="contenu" class="fr-container fr-py-4w miweb-text-page">
    {breadcrumb("Accessibilité")}
    <h1>Accessibilité</h1>
    <p class="fr-badge fr-badge--warning">Accessibilité : non auditée</p>
    <dl>
      <dt>Date</dt>
      <dd>Juin 2026</dd>
      <dt>Périmètre</dt>
      <dd>miweb-objectifs-2030-v1</dd>
    </dl>
    <p>Ce site vise une conception accessible, mais aucun audit RGAA complet n’a encore été réalisé.</p>
    <p><a class="fr-link" href="./">Retour vers la présentation</a></p>
  </main>"""
    return page("Accessibilité", body, [("Accéder au contenu", "#contenu"), ("Accéder au pied de page", "#footer")], True)


def render_markdown(slides: list[dict]) -> str:
    parts = [f"# Alternatives textuelles - {SITE_TITLE}", "", f"{BASELINE} - {VERSION_LABEL}", ""]
    for slide in slides:
        parts.extend(
            [
                f"## Slide {slide['numero']} - {slide['titre']}",
                "",
                "### Description",
                "",
                slide["description"],
                "",
                "### Textes visibles",
                "",
            ]
        )
        parts.extend(f"- {text}" for text in slide["textes_visibles"])
        parts.extend(["", "### Message à retenir", "", slide["message"], ""])
    return "\n".join(parts)


def render_readme() -> str:
    return f"""# miweb-objectifs-2030-v1

Site statique GitHub Pages pour les slides accessibles « {SITE_TITLE} ».

## Génération

Depuis ce répertoire :

```bash
python3 build.py
```

Le script lit `slides.json` et génère `index.html`, `alternatives.html`, `accessibilite.html`, `alternatives.md` et `assets/downloads/{ZIP_NAME}`.

## Vérifications attendues

- les 10 images `slide-01.png` à `slide-10.png` sont présentes dans `assets/slides/` ;
- aucun lien `href="#"` n’est généré ;
- la page principale reste lisible sans JavaScript ;
- les alternatives textuelles sont aussi disponibles dans `alternatives.html` et `alternatives.md`.
"""


def write_zip(slides: list[dict]) -> None:
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for slide in slides:
            image_path = ROOT / slide["image"]
            archive.write(image_path, image_path.name)
        archive.write(ROOT / "alternatives.md", "alternatives.md")


def main() -> None:
    slides = load_slides()
    for slide in slides:
        image_path = ROOT / slide["image"]
        if not image_path.is_file():
            raise FileNotFoundError(image_path)

    (REPO_ROOT / "index.html").write_text(render_root(), encoding="utf-8")
    (ROOT / "index.html").write_text(render_v1_index(slides), encoding="utf-8")
    (ROOT / "alternatives.html").write_text(render_alternatives(slides), encoding="utf-8")
    (ROOT / "accessibilite.html").write_text(render_accessibility(), encoding="utf-8")
    (ROOT / "alternatives.md").write_text(render_markdown(slides), encoding="utf-8")
    (ROOT / "README.md").write_text(render_readme(), encoding="utf-8")
    write_zip(slides)


if __name__ == "__main__":
    main()
