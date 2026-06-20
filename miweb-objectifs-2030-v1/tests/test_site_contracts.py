from __future__ import annotations

import importlib.util
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_PATH = ROOT / "build.py"


class FigureParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.figures = []
        self._current = None
        self._in_figcaption = False
        self._caption_parts = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "figure":
            self._current = {"attrs": attrs_dict, "figcaption": ""}
        elif tag == "figcaption" and self._current is not None:
            self._in_figcaption = True
            self._caption_parts = []

    def handle_endtag(self, tag):
        if tag == "figcaption" and self._current is not None:
            self._current["figcaption"] = " ".join("".join(self._caption_parts).split())
            self._in_figcaption = False
        elif tag == "figure" and self._current is not None:
            self.figures.append(self._current)
            self._current = None

    def handle_data(self, data):
        if self._in_figcaption:
            self._caption_parts.append(data)


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self._stack = []
        self._current = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self._stack.append((tag, attrs_dict))
        if tag == "a":
            self._current = {"attrs": attrs_dict, "text": [], "ancestors": list(self._stack[:-1])}

    def handle_endtag(self, tag):
        if tag == "a" and self._current is not None:
            self._current["text"] = " ".join("".join(self._current["text"]).split())
            self.links.append(self._current)
            self._current = None
        for index in range(len(self._stack) - 1, -1, -1):
            if self._stack[index][0] == tag:
                del self._stack[index:]
                break

    def handle_data(self, data):
        if self._current is not None:
            self._current["text"].append(data)


def load_build_module():
    spec = importlib.util.spec_from_file_location("miweb_build", BUILD_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Impossible de charger build.py.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SiteContractsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = load_build_module()
        cls.slides = cls.build.load_slides()
        cls.root_html = cls.build.render_root()
        cls.index_html = cls.build.render_v1_index(cls.slides)
        cls.alternatives_html = cls.build.render_alternatives(cls.slides)

    def test_slideshow_has_accessible_fullscreen_control(self):
        self.assertIn('data-slide-fullscreen', self.index_html)
        self.assertIn('aria-pressed="false"', self.index_html)
        self.assertIn("Activer le plein écran", self.index_html)
        self.assertNotIn(
            '<button type="button" class="fr-btn fr-btn--secondary" aria-pressed="false" data-slide-fullscreen>Plein écran</button>',
            self.index_html,
        )
        self.assertIn("Quitter le plein écran", self.index_html)
        self.assertIn("requestFullscreen", self.index_html)
        self.assertIn("exitFullscreen", self.index_html)
        self.assertIn("fullscreenchange", self.index_html)
        self.assertIn("document.fullscreenElement", self.index_html)
        self.assertIn("#diaporama:fullscreen", self.index_html)

    def test_show_all_slides_button_uses_dsfr_secondary_variant(self):
        self.assertIn(
            '<button type="button" class="fr-btn fr-btn--secondary" aria-pressed="false" data-slide-all>Afficher toutes les slides</button>',
            self.index_html,
        )
        self.assertNotIn(
            '<button type="button" class="fr-btn fr-btn--tertiary" aria-pressed="false" data-slide-all>Afficher toutes les slides</button>',
            self.index_html,
        )

    def test_fullscreen_projection_has_dedicated_accessible_controls(self):
        self.assertIn('data-projection-controls', self.index_html)
        self.assertIn('aria-label="Contrôles de projection"', self.index_html)
        self.assertIn('data-projection-previous', self.index_html)
        self.assertIn('data-projection-next', self.index_html)
        self.assertIn('data-projection-exit', self.index_html)
        self.assertIn('aria-label="Slide précédente"', self.index_html)
        self.assertIn('aria-label="Slide suivante"', self.index_html)
        self.assertIn('role="status"', self.index_html)
        self.assertIn('aria-live="polite"', self.index_html)
        self.assertIn('aria-atomic="true"', self.index_html)
        self.assertIn('data-projection-status', self.index_html)

    def test_fullscreen_projection_styles_hide_page_controls_and_keep_alternative(self):
        self.assertIn(
            "#diaporama:fullscreen .miweb-slide-controls {\n  display: none;\n}",
            self.index_html,
        )
        self.assertIn(
            "#diaporama:fullscreen .miweb-projection-controls {\n  align-items: center;",
            self.index_html,
        )
        self.assertIn(
            "#diaporama:fullscreen #diaporama-title,\n#diaporama:fullscreen .miweb-slide-title {",
            self.index_html,
        )
        self.assertIn("clip-path: inset(50%);", self.index_html)
        self.assertIn(
            "#diaporama:fullscreen .fr-accordions-group {\n  box-sizing: border-box;\n  margin-left: auto;",
            self.index_html,
        )
        self.assertIn(
            "#diaporama:fullscreen .fr-accordions-group {\n  box-sizing: border-box;\n  margin-left: auto;\n  margin-right: auto;\n  max-width: min(96vw, 1600px);\n  width: 100%;\n}",
            self.index_html,
        )

    def test_fullscreen_projection_script_preserves_focus_and_keyboard_exit(self):
        self.assertIn("function isProjectionActive()", self.index_html)
        self.assertIn("projectionExitButton.focus({ preventScroll: true });", self.index_html)
        self.assertIn("fullscreenButton.focus({ preventScroll: true });", self.index_html)
        self.assertIn(
            "if (options.focus === true && !isProjectionActive()) focusCurrentTitle();",
            self.index_html,
        )
        self.assertIn("if (allMode) showSlide(currentIndex, { replace: true });", self.index_html)
        self.assertIn("projectionPreviousButton.disabled = currentIndex === 0;", self.index_html)
        self.assertIn("projectionNextButton.disabled = currentIndex === total - 1;", self.index_html)
        self.assertNotIn('event.key === "Escape"', self.index_html)

    def test_projection_url_prepares_fullscreen_without_auto_launch(self):
        self.assertIn('data-projection-link', self.index_html)
        self.assertIn("const projectionRequested = isProjectionRequested();", self.index_html)
        self.assertIn('const projectionLinks = Array.from(document.querySelectorAll("[data-projection-link]"));', self.index_html)
        self.assertIn("function updateHeaderFullscreenButtons(active)", self.index_html)
        self.assertIn("function isProjectionRequested()", self.index_html)
        self.assertIn("new URLSearchParams(window.location.search)", self.index_html)
        self.assertIn('["1", "true"].includes(params.get("projection"))', self.index_html)
        self.assertIn("function prepareProjectionFromUrl()", self.index_html)
        self.assertIn("if (!projectionRequested) return;", self.index_html)
        self.assertIn("fullscreenTarget.scrollIntoView({ block: \"start\" });", self.index_html)
        self.assertIn("fullscreenButton.focus({ preventScroll: true });", self.index_html)
        self.assertIn("function activateProjectionFromLink(event, link)", self.index_html)
        self.assertIn("event.preventDefault();", self.index_html)
        self.assertIn("window.history.pushState(null, \"\", link.getAttribute(\"href\"));", self.index_html)
        self.assertIn("showSlide(0, { replace: true });", self.index_html)
        self.assertIn("toggleFullscreen().catch(() => updateFullscreenButton());", self.index_html)
        self.assertIn('const headerFullscreenButton = event.target.closest("[data-header-fullscreen]");', self.index_html)
        self.assertIn("if (!headerFullscreenButton) return;", self.index_html)
        self.assertIn("const url = `${window.location.pathname}${window.location.search}${hash}`;", self.index_html)
        self.assertIn("window.history[method](null, \"\", url);", self.index_html)
        self.assertIn("function initializeSlideshow()", self.index_html)
        self.assertIn("showSlide(currentIndex, { replace: true, updateUrl: !allSlidesRequested });", self.index_html)
        self.assertIn("prepareProjectionFromUrl();", self.index_html)
        self.assertNotIn("prepareProjectionFromUrl();\n  toggleFullscreen()", self.index_html)
        self.assertNotIn("prepareProjectionFromUrl();\n  fullscreenTarget.requestFullscreen()", self.index_html)

    def test_all_slides_url_and_footer_link_show_every_slide(self):
        self.assertIn(
            '<a class="fr-footer__content-link" href="./?slides=all#diaporama" data-show-all-link>Afficher toutes les slides</a>',
            self.index_html,
        )
        self.assertIn(
            '<a class="fr-footer__content-link" href="miweb-objectifs-2030-v1/?slides=all#diaporama">Afficher toutes les slides</a>',
            self.root_html,
        )
        self.assertIn('const showAllLinks = Array.from(document.querySelectorAll("[data-show-all-link]"));', self.index_html)
        self.assertIn("const allSlidesRequested = isAllSlidesRequested();", self.index_html)
        self.assertIn("function isAllSlidesRequested()", self.index_html)
        self.assertIn('params.get("slides") === "all"', self.index_html)
        self.assertIn("function prepareAllSlidesFromUrl()", self.index_html)
        self.assertIn("if (!allSlidesRequested) return;", self.index_html)
        self.assertIn("showAllSlides();", self.index_html)
        self.assertIn("allButton.focus({ preventScroll: true });", self.index_html)
        self.assertIn("function showAllSlidesFromLink(event, link)", self.index_html)
        self.assertIn("window.history.pushState(null, \"\", link.getAttribute(\"href\"));", self.index_html)
        self.assertIn("showAllLinks.forEach((link) => {", self.index_html)
        self.assertIn("initializeSlideshow();", self.index_html)

    def test_pages_have_content_security_policy_without_unsafe_inline(self):
        self.assertIn('http-equiv="Content-Security-Policy"', self.index_html)
        self.assertIn("default-src", self.index_html)
        self.assertIn("https://cdn.jsdelivr.net", self.index_html)
        self.assertIn("nonce-miweb-static", self.index_html)
        self.assertIn("sha256-", self.index_html)
        self.assertIn("object-src", self.index_html)
        self.assertIn('<style nonce="miweb-static">', self.index_html)
        self.assertNotIn("strict-dynamic", self.index_html)
        self.assertNotIn("unsafe-inline", self.index_html)

    def test_pages_use_local_official_favicon(self):
        self.assertIn(
            '<link rel="icon" href="assets/favicons/favicon.ico" type="image/vnd.microsoft.icon">',
            self.index_html,
        )
        self.assertIn(
            '<link rel="icon" href="miweb-objectifs-2030-v1/assets/favicons/favicon.ico" type="image/vnd.microsoft.icon">',
            self.root_html,
        )
        self.assertNotIn("data:image/svg+xml", self.index_html)
        self.assertNotIn("data:image/svg+xml", self.root_html)

    def test_local_favicon_asset_is_present(self):
        favicon_path = ROOT / "assets" / "favicons" / "favicon.ico"
        self.assertTrue(favicon_path.is_file(), "La favicon locale doit être versionnée dans assets/favicons/.")
        self.assertGreater(favicon_path.stat().st_size, 1000)
        self.assertEqual(b"\x00\x00\x01\x00", favicon_path.read_bytes()[:4])

    def test_header_tools_use_dsfr_quick_access_group(self):
        parser = LinkParser()
        parser.feed(self.index_html)
        links = [
            link for link in parser.links
            if link["text"] == "Alternatives textuelles"
            and "fr-header__tools-links" in [attrs.get("class", "") for _, attrs in link["ancestors"]]
        ]

        self.assertEqual(1, len(links))
        link = links[0]
        self.assertEqual("alternatives.html", link["attrs"].get("href"))
        self.assertEqual(
            "fr-btn fr-icon-accessibility-line fr-btn--icon-left",
            link["attrs"].get("class"),
        )
        self.assertNotIn("target", link["attrs"])
        ancestor_classes = [attrs.get("class", "") for _, attrs in link["ancestors"]]
        self.assertIn("fr-header__tools-links", ancestor_classes)
        self.assertIn("fr-header__tools", ancestor_classes)
        self.assertIn("fr-btns-group", ancestor_classes)
        self.assertNotIn(
            '<p><a class="fr-link" href="alternatives.html">Consulter toutes les alternatives textuelles</a></p>',
            self.index_html,
        )
        self.assertNotIn("Consulter toutes les alternatives textuelles", self.index_html)
        self.assertIn(
            '<button type="button" class="fr-btn fr-icon-expand-left-right-line fr-btn--icon-left" data-header-fullscreen>Présentation plein écran</button>',
            self.index_html,
        )
        self.assertIn(
            '<a href="assets/downloads/miweb-objectifs-2030-v1-slides.zip" class="fr-btn fr-icon-download-line fr-btn--icon-left" download>Télécharger les slides</a>',
            self.index_html,
        )
        self.assertNotIn('href="#"', self.index_html)
        self.assertIn(
            '<a href="./?projection=1#slide-01" class="fr-btn fr-icon-expand-left-right-line fr-btn--icon-left">Présentation plein écran</a>',
            self.alternatives_html,
        )
        self.assertNotIn("data-header-fullscreen", self.alternatives_html)

    def test_header_uses_dsfr_mobile_menu_structure_for_tools_links(self):
        self.assertIn('<header role="banner" class="fr-header">', self.index_html)
        self.assertIn('<div class="fr-header__navbar">', self.index_html)
        self.assertIn(
            '<button data-fr-opened="false" aria-controls="modal-menu" title="Menu" type="button" id="button-menu" class="fr-btn--menu fr-btn">Menu</button>',
            self.index_html,
        )
        self.assertIn('<ul class="fr-btns-group">', self.index_html)
        self.assertIn('<div class="fr-header__menu fr-modal" id="modal-menu">', self.index_html)
        self.assertNotIn('id="modal-menu" aria-labelledby="button-menu"', self.index_html)
        self.assertIn('<button aria-controls="modal-menu" title="Fermer" type="button" class="fr-btn--close fr-btn">Fermer</button>', self.index_html)
        self.assertIn('<div class="fr-header__menu-links"></div>', self.index_html)
        self.assertNotIn(".fr-header .fr-header__tools-links {", self.index_html)
        self.assertNotIn(".fr-header .fr-header__tools-links .fr-btn {", self.index_html)

    def test_footer_keeps_only_main_links_without_bottom_separator(self):
        self.assertIn('<footer role="contentinfo" class="fr-footer" id="footer">', self.index_html)
        self.assertIn(
            '<a class="fr-footer__content-link" href="./?projection=1#slide-01" data-projection-link>Présentation plein écran</a>',
            self.index_html,
        )
        self.assertIn(
            '<a class="fr-footer__content-link" href="miweb-objectifs-2030-v1/?projection=1#slide-01">Présentation plein écran</a>',
            self.root_html,
        )
        self.assertNotIn('<a class="fr-footer__content-link" href="./">Présentation</a>', self.index_html)
        self.assertIn("Alternatives textuelles", self.index_html)
        self.assertIn("Télécharger les slides", self.index_html)
        self.assertNotIn('<div class="fr-footer__bottom">', self.index_html)
        self.assertNotIn("fr-footer__bottom-copy", self.index_html)
        self.assertNotIn("<p class=\"fr-footer__bottom-copy\">Version 1 - Juin 2026</p>", self.index_html)
        self.assertIn(
            "#footer {\n  box-shadow: inset 0 2px 0 0 var(--border-action-high-blue-france);\n}",
            self.index_html,
        )
        self.assertNotIn(".miweb-footer", self.index_html)

    def test_slide_alternative_buttons_include_slide_titles(self):
        for slide in self.slides:
            expected = f"Lire l’alternative textuelle de la slide {slide['numero']} - {slide['titre']}"
            self.assertIn(expected, self.index_html)
        self.assertIn("Lire l’alternative textuelle de la slide 10 - Suivre sans figer trop tôt", self.index_html)
        self.assertNotIn("Lire l’alternative textuelle de la slide 10 -  - Suivre sans figer trop tôt", self.index_html)

    def test_slide_figures_have_short_numbered_caption_relationship(self):
        parser = FigureParser()
        parser.feed(self.index_html)

        self.assertEqual(10, len(parser.figures))
        for index, figure in enumerate(parser.figures, start=1):
            expected = f"Slide {index} sur 10"
            caption = figure["figcaption"]
            attrs = figure["attrs"]
            self.assertEqual(expected, caption)
            self.assertEqual("figure", attrs.get("role"))
            self.assertEqual(expected, attrs.get("aria-label"))
        self.assertIn('<figcaption class="miweb-slide-caption">Slide 10 sur 10</figcaption>', self.index_html)
        self.assertNotIn('<figcaption class="miweb-slide-caption">Slide 10 sur 10 - Suivre sans figer trop tôt</figcaption>', self.index_html)

    def test_slide_alt_texts_are_short(self):
        for slide in self.slides:
            self.assertLessEqual(
                len(slide["alt"]),
                60,
                f"Slide {slide['numero']} : alt trop long ({len(slide['alt'])} caractères).",
            )


if __name__ == "__main__":
    unittest.main()
