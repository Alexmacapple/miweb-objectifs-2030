#!/usr/bin/env python3
# PDG-LARGE-FILE-JUSTIFICATION: générateur autonome copié de la V2 pour que la V3 reste publiable et vérifiable sans dépendre d’un outillage racine non stabilisé.
from __future__ import annotations

import html
import json
import base64
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
SLIDES_PATH = ROOT / "slides.json"
SLIDES_DIR = ROOT / "assets" / "slides"
DOWNLOADS_DIR = ROOT / "assets" / "downloads"
VERSION_SLUG = ROOT.name
VERSION_NUMBER = VERSION_SLUG.rsplit("-v", 1)[-1]
ZIP_NAME = f"{VERSION_SLUG}-slides.zip"
ZIP_PATH = DOWNLOADS_DIR / ZIP_NAME
LATEST_VERSION_SLUG = VERSION_SLUG
PUBLISHED_VERSIONS = [
    ("miweb-objectifs-2030-v1", "Version 1 - Juin 2026"),
    ("miweb-objectifs-2030-v2", "Version 2 - Juin 2026"),
    ("miweb-objectifs-2030-v3", "Version 3 - Juin 2026"),
]

SITE_TITLE = "Objectifs 2030 - accessibilité numérique"
BASELINE = "MiWeb - Juin 2026"
VERSION_LABEL = f"Version {VERSION_NUMBER} - Juin 2026"
SITE_DESCRIPTION = "Version web accessible des slides Objectifs 2030 - accessibilité numérique, avec navigation clavier et alternatives textuelles."
DSFR_VERSION = "1.14.4"

DSFR_CSS = f"https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@{DSFR_VERSION}/dist/dsfr/dsfr.min.css"
DSFR_UTILITY_CSS = f"https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@{DSFR_VERSION}/dist/utility/utility.min.css"
DSFR_MODULE_JS = f"https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@{DSFR_VERSION}/dist/dsfr/dsfr.module.min.js"
DSFR_NOMODULE_JS = f"https://cdn.jsdelivr.net/npm/@gouvfr/dsfr@{DSFR_VERSION}/dist/dsfr/dsfr.nomodule.min.js"
SCRIPT_NONCE = "miweb-static"

FAVICON_REL_PATH = "assets/favicons/favicon.ico"
FAVICON_TYPE = "image/vnd.microsoft.icon"


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

.miweb-projection-controls {
  display: none;
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
  touch-action: pan-y;
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

#footer {
  background-color: #ffffff;
  box-shadow: inset 0 2px 0 0 var(--border-action-high-blue-france);
  color: #3a3a3a;
}

#footer .fr-footer__content-link {
  background-color: #ffffff;
  color: #3a3a3a;
}

#diaporama:fullscreen {
  background: var(--background-default-grey);
  box-sizing: border-box;
  overflow: auto;
  padding: clamp(0.75rem, 2vw, 2rem);
}

#diaporama:fullscreen .miweb-slide-controls {
  display: none;
}

#diaporama:fullscreen .miweb-projection-controls {
  align-items: center;
  background: var(--background-default-grey);
  border: 1px solid var(--border-default-grey);
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
  margin: 0 auto 1rem;
  max-width: min(100%, 56rem);
  padding: 0.5rem;
  position: sticky;
  top: 0;
  z-index: 2;
}

#diaporama:fullscreen #diaporama-title,
#diaporama:fullscreen .miweb-slide-title {
  border: 0;
  clip: rect(0 0 0 0);
  clip-path: inset(50%);
  height: 1px;
  margin: -1px;
  overflow: hidden;
  padding: 0;
  position: absolute;
  white-space: nowrap;
  width: 1px;
}

#diaporama:fullscreen .miweb-slide-section {
  margin-bottom: 0;
}

#diaporama:fullscreen .miweb-slide-frame {
  max-width: min(96vw, 1600px);
}

#diaporama:fullscreen .fr-accordions-group {
  box-sizing: border-box;
  margin-left: auto;
  margin-right: auto;
  max-width: min(96vw, 1600px);
  width: 100%;
}

@media (max-width: 36em) {
  #diaporama:fullscreen .miweb-projection-controls {
    align-items: stretch;
  }

  #diaporama:fullscreen .miweb-projection-controls .fr-btn {
    flex: 1 1 9rem;
    justify-content: center;
  }
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
  const projectionLinks = Array.from(document.querySelectorAll("[data-projection-link]"));
  const showAllLinks = Array.from(document.querySelectorAll("[data-show-all-link]"));
  const alternativeButtons = Array.from(document.querySelectorAll("[data-alternative-button]"));
  const previousButton = document.querySelector("[data-slide-previous]");
  const nextButton = document.querySelector("[data-slide-next]");
  const allButton = document.querySelector("[data-slide-all]");
  const fullscreenButton = document.querySelector("[data-slide-fullscreen]");
  const fullscreenTarget = document.querySelector("#diaporama");
  const status = document.querySelector("[data-slide-status]");
  const projectionPreviousButton = document.querySelector("[data-projection-previous]");
  const projectionNextButton = document.querySelector("[data-projection-next]");
  const projectionExitButton = document.querySelector("[data-projection-exit]");
  const projectionStatus = document.querySelector("[data-projection-status]");
  const total = slides.length;
  let currentIndex = getIndexFromHash();
  let allMode = false;
  let wasProjectionActive = false;
  const projectionRequested = isProjectionRequested();
  const allSlidesRequested = isAllSlidesRequested();
  let touchTracking = false;
  let touchStartX = 0;
  let touchStartY = 0;
  let touchLastX = 0;
  let touchLastY = 0;
  const swipeMinDistance = 48;
  const swipeDirectionRatio = 1.4;

  function getIndexFromHash() {
    const match = window.location.hash.match(/^#slide-(\\d{2})$/);
    if (!match) return 0;
    const index = Number.parseInt(match[1], 10) - 1;
    return Number.isInteger(index) && index >= 0 && index < total ? index : 0;
  }

  function slideHash(index) {
    return `#slide-${String(index + 1).padStart(2, "0")}`;
  }

  function isProjectionRequested() {
    const params = new URLSearchParams(window.location.search);
    return ["1", "true"].includes(params.get("projection"));
  }

  function isAllSlidesRequested() {
    const params = new URLSearchParams(window.location.search);
    return params.get("slides") === "all";
  }

  function isProjectionActive() {
    return document.fullscreenElement === fullscreenTarget;
  }

  function currentSlideTitle() {
    const title = slides[currentIndex].querySelector("[data-slide-title]");
    if (!title) return "";
    return title.textContent.replace(/^Slide \\d+\\s+-\\s+/, "").trim();
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
    if (projectionPreviousButton) projectionPreviousButton.disabled = currentIndex === 0;
    if (projectionNextButton) projectionNextButton.disabled = currentIndex === total - 1;
    allButton.setAttribute("aria-pressed", allMode ? "true" : "false");
    allButton.textContent = allMode ? "Revenir au mode diaporama" : "Afficher toutes les slides";
    moveFocusFromUnavailableProjectionTarget();
  }

  function moveFocusFromUnavailableProjectionTarget() {
    if (!isProjectionActive()) return;
    const active = document.activeElement;
    const activeSlide = active && active.closest ? active.closest("[data-slide-section]") : null;
    if (activeSlide && activeSlide.hidden && projectionExitButton) {
      projectionExitButton.focus({ preventScroll: true });
      return;
    }
    if (active === projectionPreviousButton && projectionPreviousButton.disabled) {
      const target = projectionNextButton && !projectionNextButton.disabled ? projectionNextButton : projectionExitButton;
      if (target) target.focus({ preventScroll: true });
    } else if (active === projectionNextButton && projectionNextButton.disabled) {
      const target = projectionPreviousButton && !projectionPreviousButton.disabled ? projectionPreviousButton : projectionExitButton;
      if (target) target.focus({ preventScroll: true });
    }
  }

  function updateStatus() {
    status.textContent = allMode ? `Toutes les slides affichées (${total})` : `Slide ${currentIndex + 1} sur ${total}`;
    if (projectionStatus) projectionStatus.textContent = `Slide ${currentIndex + 1} sur ${total} - ${currentSlideTitle()}`;
  }

  function updateFullscreenButton() {
    if (!fullscreenButton) return;
    const active = isProjectionActive();
    fullscreenButton.setAttribute("aria-pressed", active ? "true" : "false");
    fullscreenButton.textContent = active ? "Mode projection actif" : "Activer le plein écran";
    updateHeaderFullscreenButtons(active);
    if (active && !wasProjectionActive && projectionExitButton) {
      projectionExitButton.focus({ preventScroll: true });
    } else if (!active && wasProjectionActive) {
      fullscreenButton.focus({ preventScroll: true });
    }
    wasProjectionActive = active;
  }

  function updateHeaderFullscreenButtons(active) {
    document.querySelectorAll("[data-header-fullscreen]").forEach((button) => {
      button.setAttribute("aria-pressed", active ? "true" : "false");
      button.textContent = active ? "Mode projection actif" : "Présentation plein écran";
    });
  }

  async function toggleFullscreen() {
    if (!fullscreenButton || fullscreenButton.disabled || !fullscreenTarget) return;
    if (document.fullscreenElement) {
      await document.exitFullscreen();
    } else {
      if (allMode) showSlide(currentIndex, { replace: true });
      await fullscreenTarget.requestFullscreen();
    }
    updateFullscreenButton();
  }

  function prepareProjectionFromUrl() {
    if (!projectionRequested) return;
    if (!fullscreenButton || fullscreenButton.disabled || !fullscreenTarget) return;
    const prepare = () => {
      fullscreenTarget.scrollIntoView({ block: "start" });
      fullscreenButton.focus({ preventScroll: true });
    };
    if (document.readyState === "complete") {
      prepare();
    } else {
      window.addEventListener("load", prepare, { once: true });
    }
  }

  function prepareAllSlidesFromUrl() {
    if (!allSlidesRequested) return;
    showAllSlides();
    const prepare = () => {
      fullscreenTarget.scrollIntoView({ block: "start" });
      allButton.focus({ preventScroll: true });
    };
    if (document.readyState === "complete") {
      prepare();
    } else {
      window.addEventListener("load", prepare, { once: true });
    }
  }

  function activateProjectionFromLink(event, link) {
    if (!fullscreenButton || fullscreenButton.disabled || !fullscreenTarget) return;
    event.preventDefault();
    window.history.pushState(null, "", link.getAttribute("href"));
    showSlide(0, { replace: true });
    toggleFullscreen().catch(() => updateFullscreenButton());
  }

  function showAllSlidesFromLink(event, link) {
    if (!allButton || !fullscreenTarget) return;
    event.preventDefault();
    window.history.pushState(null, "", link.getAttribute("href"));
    showAllSlides();
    fullscreenTarget.scrollIntoView({ block: "start" });
    allButton.focus({ preventScroll: true });
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
    const url = `${window.location.pathname}${window.location.search}${hash}`;
    window.history[method](null, "", url);
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
    if (options.updateUrl !== false) setUrl(currentIndex, options.replace === true);
    if (options.focus === true && !isProjectionActive()) focusCurrentTitle();
    moveFocusFromUnavailableProjectionTarget();
  }

  function showAllSlides() {
    allMode = true;
    applyVisibility();
    updateAlternativeAnchor();
    updateButtons();
    updateStatus();
  }

  function isInteractiveSwipeTarget(target) {
    if (!target || !target.closest) return false;
    return Boolean(target.closest("a, button, input, textarea, select, summary, [role='button'], .fr-accordion"));
  }

  function canStartSwipe(event) {
    return !allMode
      && event.touches.length === 1
      && fullscreenTarget.contains(event.target)
      && !isInteractiveSwipeTarget(event.target);
  }

  function startSwipe(event) {
    if (!canStartSwipe(event)) return;
    const touch = event.touches[0];
    touchTracking = true;
    touchStartX = touch.clientX;
    touchStartY = touch.clientY;
    touchLastX = touch.clientX;
    touchLastY = touch.clientY;
  }

  function trackSwipe(event) {
    if (!touchTracking || event.touches.length !== 1) return;
    const touch = event.touches[0];
    touchLastX = touch.clientX;
    touchLastY = touch.clientY;
  }

  function endSwipe() {
    if (!touchTracking) return;
    touchTracking = false;
    const deltaX = touchLastX - touchStartX;
    const deltaY = touchLastY - touchStartY;
    const horizontal = Math.abs(deltaX);
    const vertical = Math.abs(deltaY);
    if (horizontal < swipeMinDistance || horizontal < vertical * swipeDirectionRatio) return;
    showSlide(currentIndex + (deltaX < 0 ? 1 : -1), { focus: false });
  }

  previousButton.addEventListener("click", () => showSlide(currentIndex - 1, { focus: true }));
  nextButton.addEventListener("click", () => showSlide(currentIndex + 1, { focus: true }));
  allButton.addEventListener("click", () => {
    if (allMode) showSlide(currentIndex, { focus: true });
    else showAllSlides();
  });
  if (projectionPreviousButton) {
    projectionPreviousButton.addEventListener("click", () => showSlide(currentIndex - 1, { focus: true }));
  }
  if (projectionNextButton) {
    projectionNextButton.addEventListener("click", () => showSlide(currentIndex + 1, { focus: true }));
  }
  if (projectionExitButton) {
    projectionExitButton.addEventListener("click", () => {
      if (document.fullscreenElement) document.exitFullscreen().catch(() => updateFullscreenButton());
    });
  }

  if (fullscreenButton) {
    if (!document.fullscreenEnabled || !fullscreenTarget || !fullscreenTarget.requestFullscreen) {
      fullscreenButton.disabled = true;
      fullscreenButton.textContent = "Plein écran indisponible";
      document.querySelectorAll("[data-header-fullscreen]").forEach((button) => {
        button.disabled = true;
        button.textContent = "Plein écran indisponible";
      });
    } else {
      fullscreenButton.addEventListener("click", () => {
        toggleFullscreen().catch(() => updateFullscreenButton());
      });
      document.addEventListener("fullscreenchange", updateFullscreenButton);
    }
    updateFullscreenButton();
  }

  document.addEventListener("click", (event) => {
    const headerFullscreenButton = event.target.closest("[data-header-fullscreen]");
    if (!headerFullscreenButton) return;
    event.preventDefault();
    toggleFullscreen().catch(() => updateFullscreenButton());
  });

  projectionLinks.forEach((link) => {
    link.addEventListener("click", (event) => activateProjectionFromLink(event, link));
  });

  showAllLinks.forEach((link) => {
    link.addEventListener("click", (event) => showAllSlidesFromLink(event, link));
  });

  summaryLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
      const targetIndex = slides.findIndex((slide) => `#${slide.id}` === link.hash);
      if (targetIndex === -1) return;
      event.preventDefault();
      showSlide(targetIndex, { focus: true });
    });
  });

  fullscreenTarget.addEventListener("touchstart", startSwipe, { passive: true });
  fullscreenTarget.addEventListener("touchmove", trackSwipe, { passive: true });
  fullscreenTarget.addEventListener("touchend", endSwipe);
  fullscreenTarget.addEventListener("touchcancel", () => {
    touchTracking = false;
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

  function initializeSlideshow() {
    showSlide(currentIndex, { replace: true, updateUrl: !allSlidesRequested });
    if (allSlidesRequested) {
      prepareAllSlidesFromUrl();
      return;
    }
    prepareProjectionFromUrl();
  }

  initializeSlideshow();
})();
"""


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def csp_hash(value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).digest()
    return f"'sha256-{base64.b64encode(digest).decode('ascii')}'"


def content_security_policy(extra_script: str = "") -> str:
    script_sources = ["'self'", f"'nonce-{SCRIPT_NONCE}'", "https://cdn.jsdelivr.net"]
    if extra_script:
        script_sources.append(csp_hash(extra_script))
    directives = [
        ("default-src", ["'self'"]),
        ("base-uri", ["'self'"]),
        ("object-src", ["'none'"]),
        ("script-src", script_sources),
        ("style-src", ["'self'", "https://cdn.jsdelivr.net", f"'nonce-{SCRIPT_NONCE}'", csp_hash(CUSTOM_CSS)]),
        ("img-src", ["'self'", "data:", "https://cdn.jsdelivr.net"]),
        ("font-src", ["'self'", "https://cdn.jsdelivr.net", "data:"]),
        ("connect-src", ["'self'", "https://cdn.jsdelivr.net"]),
        ("form-action", ["'self'"]),
        ("upgrade-insecure-requests", []),
    ]
    return "; ".join(
        f"{name} {' '.join(values)}" if values else name
        for name, values in directives
    )


def slide_id(slide: dict) -> str:
    return f"slide-{int(slide['numero']):02d}"


def resolve_slide_image_path(image: str, require_exists: bool = True) -> Path:
    if not isinstance(image, str):
        raise ValueError("slides.json ne peut référencer que des images sous assets/slides/.")
    relative_path = Path(image)
    if (
        relative_path.is_absolute()
        or relative_path.parts[:2] != ("assets", "slides")
        or ".." in relative_path.parts
    ):
        raise ValueError(
            "slides.json ne peut référencer que des images sous assets/slides/ : "
            f"{image}"
        )
    candidate = (ROOT / relative_path).resolve()
    slides_root = SLIDES_DIR.resolve()
    try:
        candidate.relative_to(slides_root)
    except ValueError as exc:
        raise ValueError(
            "slides.json ne peut référencer que des images sous assets/slides/ : "
            f"{image}"
        ) from exc
    if require_exists and not candidate.is_file():
        raise FileNotFoundError(candidate)
    return candidate


def load_slides() -> list[dict]:
    slides = json.loads(SLIDES_PATH.read_text(encoding="utf-8"))
    if not slides:
        raise ValueError("slides.json doit contenir au moins une slide.")
    required = {"numero", "titre", "image", "alt", "description", "textes_visibles", "message"}
    for expected_numero, slide in enumerate(slides, start=1):
        missing = required - set(slide)
        if missing:
            raise ValueError(f"Slide {slide.get('numero', '?')} incomplète : {sorted(missing)}")
        resolve_slide_image_path(slide["image"])
        if int(slide["numero"]) != expected_numero:
            raise ValueError(
                f"Numéro de slide inattendu : {slide['numero']} au lieu de {expected_numero}."
            )
    return slides


def dsfr_assets() -> str:
    return f"""<link rel="stylesheet" href="{DSFR_CSS}">
  <link rel="stylesheet" href="{DSFR_UTILITY_CSS}">"""


def dsfr_scripts(extra_script: str = "") -> str:
    script = f"""<script nonce="{SCRIPT_NONCE}" type="module" src="{DSFR_MODULE_JS}"></script>
  <script nonce="{SCRIPT_NONCE}" nomodule src="{DSFR_NOMODULE_JS}"></script>"""
    if extra_script:
        script += f"\n  <script nonce=\"{SCRIPT_NONCE}\">{extra_script}</script>"
    return script


def favicon_href(version_context: bool) -> str:
    return FAVICON_REL_PATH if version_context else f"{ROOT.name}/{FAVICON_REL_PATH}"


def skiplinks(links: list[tuple[str, str]]) -> str:
    items = "\n".join(
        f'        <li><a class="fr-link" href="{esc(href)}">{esc(label)}</a></li>' for label, href in links
    )
    return f"""<div class="fr-skiplinks">
    <nav aria-label="Accès rapide" class="fr-container">
      <ul class="fr-skiplinks__list">
{items}
      </ul>
    </nav>
  </div>"""


def header(home_href: str, version_context: bool, slideshow_context: bool = False) -> str:
    tools = ""
    navbar = ""
    menu = ""
    if version_context:
        projection_item = (
            '<button type="button" class="fr-btn fr-icon-expand-left-right-line fr-btn--icon-left" data-header-fullscreen>Présentation plein écran</button>'
            if slideshow_context
            else '<a href="./?projection=1#slide-01" class="fr-btn fr-icon-expand-left-right-line fr-btn--icon-left">Présentation plein écran</a>'
        )
        navbar = """              <div class="fr-header__navbar">
                <button data-fr-opened="false" aria-controls="modal-menu" title="Menu" type="button" id="button-menu" class="fr-btn--menu fr-btn">Menu</button>
              </div>
"""
        tools = f"""          <div class="fr-header__tools">
            <div class="fr-header__tools-links">
              <ul class="fr-btns-group">
                <li>
                  {projection_item}
                </li>
                <li>
                  <a href="alternatives.html" class="fr-btn fr-icon-accessibility-line fr-btn--icon-left">Alternatives textuelles</a>
                </li>
                <li>
                  <a href="assets/downloads/{ZIP_NAME}" class="fr-btn fr-icon-download-line fr-btn--icon-left" download>Télécharger les slides</a>
                </li>
              </ul>
            </div>
          </div>
"""
        menu = """    <div class="fr-header__menu fr-modal" id="modal-menu">
      <div class="fr-container">
        <button aria-controls="modal-menu" title="Fermer" type="button" class="fr-btn--close fr-btn">Fermer</button>
        <div class="fr-header__menu-links"></div>
      </div>
    </div>
"""
    return f"""<header role="banner" class="fr-header">
    <div class="fr-header__body">
      <div class="fr-container">
        <div class="fr-header__body-row">
          <div class="fr-header__brand fr-enlarge-link">
            <div class="fr-header__brand-top">
              <div class="fr-header__logo">
                <p class="fr-logo">République<br>Française</p>
              </div>
{navbar.rstrip()}
            </div>
            <div class="fr-header__service">
              <a href="{esc(home_href)}" title="Accueil - {esc(SITE_TITLE)}">
                <p class="fr-header__service-title">{esc(SITE_TITLE)}</p>
              </a>
              <p class="fr-header__service-tagline">{esc(BASELINE)}</p>
            </div>
          </div>
{tools.rstrip()}
        </div>
      </div>
    </div>
{menu.rstrip()}
  </header>"""


def footer(version_context: bool) -> str:
    links = {
        "Présentation plein écran": "./?projection=1#slide-01" if version_context else f"{LATEST_VERSION_SLUG}/?projection=1#slide-01",
        "Afficher toutes les slides": "./?slides=all#diaporama" if version_context else f"{LATEST_VERSION_SLUG}/?slides=all#diaporama",
        "Alternatives textuelles": "alternatives.html" if version_context else f"{LATEST_VERSION_SLUG}/alternatives.html",
        "Télécharger les slides": f"assets/downloads/{ZIP_NAME}" if version_context else f"{LATEST_VERSION_SLUG}/assets/downloads/{ZIP_NAME}",
    }
    items = "\n".join(
        (
            f'              <li class="fr-footer__content-item"><a class="fr-footer__content-link" href="{esc(href)}"'
            f'{" data-projection-link" if version_context and label == "Présentation plein écran" else ""}'
            f'{" data-show-all-link" if version_context and label == "Afficher toutes les slides" else ""}>{esc(label)}</a></li>'
        )
        for label, href in links.items()
    )
    return f"""<footer role="contentinfo" class="fr-footer" id="footer">
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
    </div>
  </footer>"""


def breadcrumb(current: str) -> str:
    return f"""<nav class="fr-breadcrumb" aria-label="vous êtes ici :">
    <button type="button" class="fr-breadcrumb__button" aria-expanded="false" aria-controls="breadcrumb">Voir le fil d’Ariane</button>
    <div class="fr-collapse" id="breadcrumb">
      <ol class="fr-breadcrumb__list">
        <li><a class="fr-breadcrumb__link" href="../">Versions</a></li>
        <li><a class="fr-breadcrumb__link" href="./">{esc(SITE_TITLE)}</a></li>
        <li><a class="fr-breadcrumb__link" aria-current="page">{esc(current)}</a></li>
      </ol>
    </div>
  </nav>"""


def page(
    title: str,
    body: str,
    skip_links: list[tuple[str, str]],
    version_context: bool,
    extra_script: str = "",
    slideshow_context: bool = False,
) -> str:
    home_href = "./" if version_context else "./"
    full_title = SITE_TITLE if title == SITE_TITLE else f"{title} - {SITE_TITLE}"
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Security-Policy" content="{html.escape(content_security_policy(extra_script), quote=False)}">
  <meta name="description" content="{esc(SITE_DESCRIPTION)}">
  <link rel="icon" href="{esc(favicon_href(version_context))}" type="{FAVICON_TYPE}">
  <title>{esc(full_title)}</title>
  {dsfr_assets()}
  <style nonce="{SCRIPT_NONCE}">{CUSTOM_CSS}</style>
</head>
<body>
  {skiplinks(skip_links)}
  {header(home_href, version_context, slideshow_context)}
  {body}
  {footer(version_context)}
  {dsfr_scripts(extra_script)}
</body>
</html>
"""


def render_root() -> str:
    version_tiles = "\n".join(
        f"""        <div class="fr-col-12 fr-col-md-6">
          <div class="fr-tile fr-enlarge-link">
            <div class="fr-tile__body">
              <h3 class="fr-tile__title"><a href="{esc(slug)}/">{esc(label)}</a></h3>
              <p class="fr-tile__desc">Slides accessibles au format web.</p>
            </div>
          </div>
        </div>"""
        for slug, label in PUBLISHED_VERSIONS
    )
    body = f"""<main id="contenu" class="fr-container fr-py-6w">
    <div class="miweb-page-header">
      <h1>{esc(SITE_TITLE)}</h1>
      <p class="fr-text--lead">{esc(BASELINE)}</p>
    </div>
    <section aria-labelledby="versions-title">
      <h2 id="versions-title">Versions disponibles</h2>
      <div class="fr-grid-row fr-grid-row--gutters">
{version_tiles}
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
    return f"""<nav class="fr-summary" aria-labelledby="summary-title" id="sommaire">
      <h2 class="fr-summary__title" id="summary-title">Sommaire</h2>
      <ol>
{items}
      </ol>
    </nav>"""


def render_slide(slide: dict, total: int) -> str:
    number = int(slide["numero"])
    sid = slide_id(slide)
    caption = f"Slide {number} sur {total}"
    alternative_label = f"Lire l’alternative textuelle de la slide {number} - {slide['titre']}"
    texts = "\n".join(f"              <li>{esc(text)}</li>" for text in slide["textes_visibles"])
    button_id = ' id="alternative-active"' if number == 1 else ""
    return f"""      <section class="miweb-slide-section" id="{sid}" data-slide-section aria-labelledby="{sid}-title">
        <h3 class="miweb-slide-title" id="{sid}-title" data-slide-title tabindex="-1">Slide {number} - {esc(slide["titre"])}</h3>
        <figure class="miweb-slide-frame" role="figure" aria-label="{esc(caption)}">
          <img src="{esc(slide["image"])}" alt="{esc(slide["alt"])}" width="1672" height="941">
          <figcaption class="miweb-slide-caption">{esc(caption)}</figcaption>
        </figure>
        <div class="fr-accordions-group" data-fr-group="false">
          <section class="fr-accordion">
            <h4 class="fr-accordion__title">
              <button{button_id} type="button" class="fr-accordion__btn" aria-expanded="false" aria-controls="alternative-{sid}" data-alternative-button>{esc(alternative_label)}</button>
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
    </div>
    <div class="miweb-summary-zone">
{render_summary(slides)}
    </div>
    <section id="diaporama" aria-labelledby="diaporama-title">
      <h2 id="diaporama-title">Présentation MiWeb V{esc(VERSION_NUMBER)}</h2>
      <nav class="miweb-slide-controls" aria-label="Contrôles du diaporama">
        <button type="button" class="fr-btn fr-btn--secondary fr-icon-arrow-left-line fr-btn--icon-left" data-slide-previous>Précédente</button>
        <p class="miweb-slide-status" aria-live="polite" data-slide-status>Slide 1 sur {len(slides)}</p>
        <button type="button" class="fr-btn fr-icon-arrow-right-line fr-btn--icon-right" data-slide-next>Suivante</button>
        <button type="button" class="fr-btn fr-btn--secondary" aria-pressed="false" data-slide-fullscreen>Activer le plein écran</button>
        <button type="button" class="fr-btn fr-btn--secondary" aria-pressed="false" data-slide-all>Afficher toutes les slides</button>
        <a class="fr-btn fr-btn--secondary fr-icon-download-line fr-btn--icon-left" href="assets/downloads/{ZIP_NAME}" download>Télécharger les slides au format ZIP</a>
      </nav>
      <div class="miweb-projection-controls" role="group" aria-label="Contrôles de projection" data-projection-controls>
        <button type="button" class="fr-btn fr-btn--secondary fr-icon-arrow-left-line fr-btn--icon-left" aria-label="Slide précédente" data-projection-previous>Précédente</button>
        <button type="button" class="fr-btn fr-icon-arrow-right-line fr-btn--icon-right" aria-label="Slide suivante" data-projection-next>Suivante</button>
        <button type="button" class="fr-btn fr-btn--secondary" data-projection-exit>Quitter le plein écran</button>
        <p class="fr-sr-only" role="status" aria-live="polite" aria-atomic="true" data-projection-status>Slide 1 sur {len(slides)} - {esc(slides[0]["titre"])}</p>
      </div>
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
    return page(SITE_TITLE, body, skip, True, MAIN_JS, slideshow_context=True)


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
      <dd>{esc(VERSION_SLUG)}</dd>
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
    return f"""# {VERSION_SLUG}

Site statique GitHub Pages pour les slides accessibles « {SITE_TITLE} ».

## Accès directs

- [Présentation plein écran](./?projection=1#slide-01)
- [Toutes les slides](./?slides=all#diaporama)

## Génération

Depuis ce répertoire :

```bash
python3 build.py
```

Le script lit `slides.json` et génère `index.html`, `alternatives.html`, `accessibilite.html`, `alternatives.md` et `assets/downloads/{ZIP_NAME}`.

## Sources V{VERSION_NUMBER}

- `source/storyboard-v{VERSION_NUMBER}.md` : storyboard utilisé pour générer la variante V{VERSION_NUMBER}.
- `slides.json` : titres, alternatives textuelles, descriptions et messages associés aux images publiées.

## Vérifications attendues

- les images listées dans `slides.json` sont présentes dans `assets/slides/` ;
- aucun lien `href="#"` n’est généré ;
- la page principale reste lisible sans JavaScript ;
- les alternatives textuelles sont aussi disponibles dans `alternatives.html` et `alternatives.md`.
"""


def write_zip(slides: list[dict]) -> None:
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for slide in slides:
            image_path = resolve_slide_image_path(slide["image"])
            archive.write(image_path, image_path.name)
        archive.write(ROOT / "alternatives.md", "alternatives.md")


def main() -> None:
    slides = load_slides()

    (ROOT / "index.html").write_text(render_v1_index(slides), encoding="utf-8")
    (ROOT / "alternatives.html").write_text(render_alternatives(slides), encoding="utf-8")
    (ROOT / "accessibilite.html").write_text(render_accessibility(), encoding="utf-8")
    (ROOT / "alternatives.md").write_text(render_markdown(slides), encoding="utf-8")
    (ROOT / "README.md").write_text(render_readme(), encoding="utf-8")
    write_zip(slides)


if __name__ == "__main__":
    main()
