from __future__ import annotations

import importlib.util
import html
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD_PATH = ROOT / "build.py"


class ImageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.images: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "img":
            self.images.append({key: value or "" for key, value in attrs})


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
        cls.accessibilite_html = cls.build.render_accessibility()
        cls.alternatives_md = cls.build.render_markdown(cls.slides)

    def test_slides_json_matches_images(self):
        self.assertEqual(6, len(self.slides))
        for slide in self.slides:
            image_path = ROOT / slide["image"]
            self.assertTrue(image_path.is_file(), image_path)
            self.assertGreater(image_path.stat().st_size, 1000)
            self.assertLessEqual(len(slide["alt"]), 80)
            self.assertTrue(slide["description"])
            self.assertTrue(slide["textes_visibles"])
            self.assertTrue(slide["message"])

    def test_variant_pages_expose_transcriptions(self):
        self.assertIn("Alternatives textuelles", self.index_html)
        self.assertIn("Textes visibles", self.index_html)
        self.assertIn("Message à retenir", self.index_html)
        self.assertIn("Alternatives textuelles", self.alternatives_html)
        self.assertIn("Textes visibles", self.alternatives_html)
        self.assertIn("Message à retenir", self.alternatives_html)
        self.assertIn("# Alternatives textuelles", self.alternatives_md)
        for slide in self.slides:
            escaped_title = html.escape(slide["titre"], quote=True)
            escaped_description = html.escape(slide["description"], quote=True)
            self.assertIn(escaped_title, self.index_html)
            self.assertIn(escaped_title, self.alternatives_html)
            self.assertIn(escaped_description, self.alternatives_html)
            self.assertIn(slide["message"], self.alternatives_md)

    def test_slideshow_keeps_projection_and_all_slides_controls(self):
        self.assertIn(self.build.DIAPORAMA_TITLE, self.index_html)
        self.assertIn("data-slide-previous", self.index_html)
        self.assertIn("data-slide-next", self.index_html)
        self.assertIn("data-slide-fullscreen", self.index_html)
        self.assertIn("data-slide-all", self.index_html)
        self.assertIn("data-projection-controls", self.index_html)
        self.assertIn("requestFullscreen", self.index_html)
        self.assertIn("exitFullscreen", self.index_html)
        self.assertIn('addEventListener("touchstart"', self.index_html)
        self.assertIn('addEventListener("touchend"', self.index_html)
        self.assertIn("swipeMinDistance", self.index_html)
        self.assertIn("?projection=1#slide-01", self.index_html)
        self.assertIn("?slides=all#diaporama", self.index_html)

    def test_images_have_alt_and_stable_dimensions(self):
        parser = ImageParser()
        parser.feed(self.index_html)
        slide_images = [image for image in parser.images if image.get("src", "").startswith("assets/slides/")]
        self.assertEqual(len(self.slides), len(slide_images))
        self.assertEqual({("1672", "941")}, {(image.get("width"), image.get("height")) for image in slide_images})
        for image in slide_images:
            self.assertTrue(image.get("alt"))

    def test_root_lists_all_published_versions(self):
        self.assertIn("Versions disponibles", self.root_html)
        for slug, label in self.build.PUBLISHED_VERSIONS:
            self.assertIn(f'href="{slug}/"', self.root_html)
            self.assertIn(label, self.root_html)
        self.assertIn(f"{self.build.LATEST_VERSION_SLUG}/alternatives.html", self.root_html)

    def test_security_and_assets_contracts(self):
        self.assertIn('http-equiv="Content-Security-Policy"', self.index_html)
        self.assertIn("nonce-miweb-static", self.index_html)
        self.assertNotIn("unsafe-inline", self.index_html)
        self.assertNotIn('href="#"', self.index_html)
        self.assertNotIn('href="#"', self.alternatives_html)
        favicon_path = ROOT / "assets" / "favicons" / "favicon.ico"
        self.assertTrue(favicon_path.is_file())
        self.assertEqual(b"\x00\x00\x01\x00", favicon_path.read_bytes()[:4])


if __name__ == "__main__":
    unittest.main()
