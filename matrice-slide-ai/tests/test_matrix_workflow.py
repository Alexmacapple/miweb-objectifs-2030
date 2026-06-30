import sys
import json
import shutil
import unittest
from pathlib import Path
from subprocess import PIPE, run
from tempfile import TemporaryDirectory


class MatrixWorkflowTest(unittest.TestCase):
    def read_sensitive_root_files(self, repo):
        sensitive_paths = [
            repo / "index.html",
            repo / "published-versions.json",
        ]
        return {
            path.name: path.read_text(encoding="utf-8")
            for path in sensitive_paths
            if path.exists()
        }

    def assert_generated_files_are_autonomous(self, target):
        forbidden_references = [
            "matrice-slide-ai",
            "../matrice-slide-ai",
            "matrice_slide_ai",
        ]
        checked_suffixes = {".html", ".json", ".md", ".py"}
        generated_files = [
            path
            for path in target.rglob("*")
            if path.is_file() and path.suffix in checked_suffixes
        ]

        self.assertTrue(
            generated_files,
            msg="Aucun fichier texte généré n'a été trouvé dans la variante.",
        )
        for path in generated_files:
            content = path.read_text(encoding="utf-8")
            for forbidden_reference in forbidden_references:
                with self.subTest(path=path, reference=forbidden_reference):
                    self.assertNotIn(forbidden_reference, content)

    def test_create_variant_copies_sources_without_publishing(self):
        repo = Path(__file__).resolve().parents[2]

        with TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "jeu-test"
            source_slides_dir = (
                repo
                / "miweb-offre-mutualisee-listes-diffusion-2026-longue"
                / "assets"
                / "slides"
            )
            root_files_before = self.read_sensitive_root_files(repo)
            result = run(
                [
                    sys.executable,
                    str(repo / "matrice-slide-ai" / "create_variant.py"),
                    "--slug",
                    "jeu-test",
                    "--title",
                    "Jeu test",
                    "--storyboard",
                    str(
                        repo
                        / "miweb-offre-mutualisee-listes-diffusion-2026-longue"
                        / "source"
                        / "storyboard.md"
                    ),
                    "--slides-dir",
                    str(source_slides_dir),
                ],
                cwd=tmp_dir,
                stdout=PIPE,
                stderr=PIPE,
                text=True,
            )

            self.assertEqual(
                0,
                result.returncode,
                msg=(
                    "create_variant.py a échoué.\n"
                    f"stdout:\n{result.stdout}\n"
                    f"stderr:\n{result.stderr}"
                ),
            )
            self.assertEqual(
                root_files_before,
                self.read_sensitive_root_files(repo),
                msg="La création autonome ne doit pas modifier les fichiers racine.",
            )

            self.assertTrue((target / "build.py").is_file())
            self.assertTrue((target / "slides.json").is_file())
            self.assertIn(
                "Jeu test",
                (target / "variant.json").read_text(encoding="utf-8"),
            )
            self.assertTrue((target / "source" / "storyboard.md").is_file())
            source_slide_names = sorted(
                path.name for path in source_slides_dir.glob("slide-*.png")
            )
            target_slide_names = sorted(
                path.name
                for path in (target / "assets" / "slides").glob("slide-*.png")
            )
            self.assertTrue(
                source_slide_names,
                msg="Aucune image slide-*.png trouvée dans le dossier source.",
            )
            self.assertEqual(
                source_slide_names,
                target_slide_names,
                msg="La variante doit copier toutes les images slide-*.png.",
            )
            for slide_name in source_slide_names:
                with self.subTest(slide=slide_name):
                    self.assertEqual(
                        (source_slides_dir / slide_name).read_bytes(),
                        (
                            target
                            / "assets"
                            / "slides"
                            / slide_name
                        ).read_bytes(),
                        msg=f"L'image {slide_name} doit être copiée à l'identique.",
                    )
            self.assert_generated_files_are_autonomous(target)

            build_result = run(
                [sys.executable, str(target / "build.py")],
                cwd=target,
                stdout=PIPE,
                stderr=PIPE,
                text=True,
            )
            self.assertEqual(
                0,
                build_result.returncode,
                msg=(
                    "Le build du jeu généré a échoué.\n"
                    f"stdout:\n{build_result.stdout}\n"
                    f"stderr:\n{build_result.stderr}"
                ),
            )
            self.assertFalse(
                (target.parent / "index.html").exists(),
                msg="Le build ordinaire du jeu ne doit pas écrire l’accueil parent.",
            )
            self.assertIn(
                "Jeu test",
                (target / "index.html").read_text(encoding="utf-8"),
            )
            self.assertEqual(
                root_files_before,
                self.read_sensitive_root_files(repo),
                msg="Le build du jeu temporaire ne doit pas modifier les fichiers racine.",
            )

            tests_result = run(
                [
                    sys.executable,
                    "-m",
                    "unittest",
                    "discover",
                    "-s",
                    str(target / "tests"),
                ],
                cwd=target,
                stdout=PIPE,
                stderr=PIPE,
                text=True,
            )
            self.assertEqual(
                0,
                tests_result.returncode,
                msg=(
                    "Les tests du jeu généré ont échoué.\n"
                    f"stdout:\n{tests_result.stdout}\n"
                    f"stderr:\n{tests_result.stderr}"
                ),
            )

    def test_create_variant_accepts_prefixed_slide_sources(self):
        repo = Path(__file__).resolve().parents[2]

        with TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            source_slides_dir = tmp_path / "source-slides"
            source_slides_dir.mkdir()
            for index in range(1, 4):
                source = (
                    repo
                    / "miweb-offre-mutualisee-listes-diffusion-2026-longue"
                    / "assets"
                    / "slides"
                    / f"slide-{index:02}.png"
                )
                shutil.copy2(
                    source,
                    source_slides_dir / f"checklist-span-slide-{index:02}.png",
                )

            result = run(
                [
                    sys.executable,
                    str(repo / "matrice-slide-ai" / "create_variant.py"),
                    "--slug",
                    "jeu-prefixe",
                    "--title",
                    "Jeu préfixé",
                    "--storyboard",
                    str(
                        repo
                        / "miweb-offre-mutualisee-listes-diffusion-2026-longue"
                        / "source"
                        / "storyboard.md"
                    ),
                    "--slides-dir",
                    str(source_slides_dir),
                    "--slide-prefix",
                    "checklist-span-",
                ],
                cwd=tmp_path,
                stdout=PIPE,
                stderr=PIPE,
                text=True,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            copied_names = sorted(
                path.name
                for path in (tmp_path / "jeu-prefixe" / "assets" / "slides").glob("*.png")
            )
            self.assertEqual(
                ["slide-01.png", "slide-02.png", "slide-03.png"],
                copied_names,
            )

    def test_publish_variant_requires_generated_outputs(self):
        repo = Path(__file__).resolve().parents[2]

        root_files_before = self.read_sensitive_root_files(repo)
        result = run(
            [
                sys.executable,
                str(repo / "matrice-slide-ai" / "publish_variant.py"),
                "--slug",
                "jeu-absent",
            ],
            cwd=repo,
            text=True,
            stderr=PIPE,
        )

        self.assertNotEqual(0, result.returncode)
        self.assertEqual(
            root_files_before,
            self.read_sensitive_root_files(repo),
            msg="Une publication invalide ne doit pas modifier les fichiers racine.",
        )
        self.assertIn("jeu non vérifiable", result.stderr)

    def test_publish_variant_updates_catalog_and_root_after_build(self):
        repo = Path(__file__).resolve().parents[2]

        with TemporaryDirectory() as tmp_dir:
            temp_repo = Path(tmp_dir) / "repo"
            temp_repo.mkdir()
            shutil.copytree(
                repo / "matrice-slide-ai",
                temp_repo / "matrice-slide-ai",
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
            (temp_repo / "published-versions.json").write_text(
                "[]\n",
                encoding="utf-8",
            )

            create_result = run(
                [
                    sys.executable,
                    str(temp_repo / "matrice-slide-ai" / "create_variant.py"),
                    "--slug",
                    "jeu-test",
                    "--title",
                    "Jeu test",
                    "--storyboard",
                    str(
                        repo
                        / "miweb-offre-mutualisee-listes-diffusion-2026-longue"
                        / "source"
                        / "storyboard.md"
                    ),
                    "--slides-dir",
                    str(
                        repo
                        / "miweb-offre-mutualisee-listes-diffusion-2026-longue"
                        / "assets"
                        / "slides"
                    ),
                ],
                cwd=temp_repo,
                stdout=PIPE,
                stderr=PIPE,
                text=True,
            )
            self.assertEqual(0, create_result.returncode, create_result.stderr)

            build_result = run(
                [sys.executable, str(temp_repo / "jeu-test" / "build.py")],
                cwd=temp_repo / "jeu-test",
                stdout=PIPE,
                stderr=PIPE,
                text=True,
            )
            self.assertEqual(0, build_result.returncode, build_result.stderr)

            publish_result = run(
                [
                    sys.executable,
                    str(temp_repo / "matrice-slide-ai" / "publish_variant.py"),
                    "--slug",
                    "jeu-test",
                ],
                cwd=temp_repo,
                stdout=PIPE,
                stderr=PIPE,
                text=True,
            )
            self.assertEqual(
                0,
                publish_result.returncode,
                msg=(
                    "publish_variant.py a échoué.\n"
                    f"stdout:\n{publish_result.stdout}\n"
                    f"stderr:\n{publish_result.stderr}"
                ),
            )

            catalog = json.loads(
                (temp_repo / "published-versions.json").read_text(encoding="utf-8")
            )
            self.assertEqual(
                [{"slug": "jeu-test", "label": "Jeu test"}],
                catalog,
            )
            root_html = (temp_repo / "index.html").read_text(encoding="utf-8")
            self.assertIn('href="jeu-test/"', root_html)
            self.assertIn("Jeu test", root_html)
            self.assertIn(
                "jeu-test/assets/downloads/jeu-test-slides.zip",
                root_html,
            )
            self.assertNotIn("matrice-slide-ai", root_html)

    def test_publish_variant_rejects_stale_generated_pages(self):
        repo = Path(__file__).resolve().parents[2]

        with TemporaryDirectory() as tmp_dir:
            temp_repo = Path(tmp_dir) / "repo"
            temp_repo.mkdir()
            shutil.copytree(
                repo / "matrice-slide-ai",
                temp_repo / "matrice-slide-ai",
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
            (temp_repo / "published-versions.json").write_text(
                "[]\n",
                encoding="utf-8",
            )
            (temp_repo / "index.html").write_text(
                "<!doctype html><title>Racine intacte</title>\n",
                encoding="utf-8",
            )

            create_result = run(
                [
                    sys.executable,
                    str(temp_repo / "matrice-slide-ai" / "create_variant.py"),
                    "--slug",
                    "jeu-test",
                    "--title",
                    "Jeu test",
                    "--storyboard",
                    str(
                        repo
                        / "miweb-offre-mutualisee-listes-diffusion-2026-longue"
                        / "source"
                        / "storyboard.md"
                    ),
                    "--slides-dir",
                    str(
                        repo
                        / "miweb-offre-mutualisee-listes-diffusion-2026-longue"
                        / "assets"
                        / "slides"
                    ),
                ],
                cwd=temp_repo,
                stdout=PIPE,
                stderr=PIPE,
                text=True,
            )
            self.assertEqual(0, create_result.returncode, create_result.stderr)

            build_result = run(
                [sys.executable, str(temp_repo / "jeu-test" / "build.py")],
                cwd=temp_repo / "jeu-test",
                stdout=PIPE,
                stderr=PIPE,
                text=True,
            )
            self.assertEqual(0, build_result.returncode, build_result.stderr)

            root_files_before = self.read_sensitive_root_files(temp_repo)
            slides_path = temp_repo / "jeu-test" / "slides.json"
            slides = json.loads(slides_path.read_text(encoding="utf-8"))
            slides[0]["titre"] = "Titre modifié après génération"
            slides_path.write_text(
                json.dumps(slides, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            publish_result = run(
                [
                    sys.executable,
                    str(temp_repo / "matrice-slide-ai" / "publish_variant.py"),
                    "--slug",
                    "jeu-test",
                ],
                cwd=temp_repo,
                stdout=PIPE,
                stderr=PIPE,
                text=True,
            )

            self.assertNotEqual(0, publish_result.returncode)
            self.assertEqual(
                root_files_before,
                self.read_sensitive_root_files(temp_repo),
                msg="Une variante périmée ne doit pas modifier les fichiers racine.",
            )
            self.assertIn("artefacts générés périmés", publish_result.stderr)

    def test_variant_build_does_not_publish_root_index(self):
        repo = Path(__file__).resolve().parents[2]
        variant_slugs = [
            "miweb-objectifs-2030-v1",
            "miweb-objectifs-2030-v2",
            "miweb-objectifs-2030-v3",
            "miweb-objectifs-2030-v4",
            "miweb-offre-mutualisee-listes-diffusion-2026-condensee",
            "miweb-offre-mutualisee-listes-diffusion-2026-longue",
        ]

        for slug in variant_slugs:
            with self.subTest(slug=slug), TemporaryDirectory() as tmp_dir:
                temp_repo = Path(tmp_dir) / "repo"
                temp_repo.mkdir()
                root_index = temp_repo / "index.html"
                root_index.write_text(
                    "<!doctype html><title>Accueil racine intact</title>\n",
                    encoding="utf-8",
                )
                shutil.copytree(
                    repo / slug,
                    temp_repo / slug,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
                )

                root_before = root_index.read_text(encoding="utf-8")
                build_result = run(
                    [
                        sys.executable,
                        str(temp_repo / slug / "build.py"),
                    ],
                    cwd=temp_repo / slug,
                    stdout=PIPE,
                    stderr=PIPE,
                    text=True,
                )

                self.assertEqual(0, build_result.returncode, build_result.stderr)
                self.assertEqual(
                    root_before,
                    root_index.read_text(encoding="utf-8"),
                    msg=(
                        "Le build d'une variante ne doit pas publier "
                        f"l'accueil racine : {slug}"
                    ),
                )


if __name__ == "__main__":
    unittest.main()
