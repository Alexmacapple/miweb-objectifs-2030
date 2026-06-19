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
        cls.index_html = cls.build.render_v1_index(cls.slides)

    def test_slideshow_has_accessible_fullscreen_control(self):
        self.assertIn('data-slide-fullscreen', self.index_html)
        self.assertIn('aria-pressed="false"', self.index_html)
        self.assertIn("Plein écran", self.index_html)
        self.assertIn("Quitter le plein écran", self.index_html)
        self.assertIn("requestFullscreen", self.index_html)
        self.assertIn("exitFullscreen", self.index_html)
        self.assertIn("fullscreenchange", self.index_html)
        self.assertIn("document.fullscreenElement", self.index_html)
        self.assertIn("#diaporama:fullscreen", self.index_html)

    def test_pages_have_content_security_policy_without_unsafe_inline(self):
        self.assertIn('http-equiv="Content-Security-Policy"', self.index_html)
        self.assertIn("default-src", self.index_html)
        self.assertIn("https://cdn.jsdelivr.net", self.index_html)
        self.assertIn("nonce-miweb-static", self.index_html)
        self.assertIn("sha256-", self.index_html)
        self.assertIn("object-src", self.index_html)
        self.assertIn('<style nonce="miweb-static">', self.index_html)
        self.assertNotIn("unsafe-inline", self.index_html)

    def test_slide_figures_have_rgaa_caption_relationship(self):
        parser = FigureParser()
        parser.feed(self.index_html)

        self.assertEqual(10, len(parser.figures))
        for figure in parser.figures:
            caption = figure["figcaption"]
            attrs = figure["attrs"]
            self.assertTrue(caption)
            self.assertEqual("figure", attrs.get("role"))
            self.assertEqual(caption, attrs.get("aria-label"))

    def test_slide_alt_texts_are_short(self):
        for slide in self.slides:
            self.assertLessEqual(
                len(slide["alt"]),
                60,
                f"Slide {slide['numero']} : alt trop long ({len(slide['alt'])} caractères).",
            )


if __name__ == "__main__":
    unittest.main()
