#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SLUG_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Créer un jeu de slides autonome depuis la matrice."
    )
    parser.add_argument(
        "--slug",
        required=True,
        help="Nom de dossier simple, en minuscules, sans espace ni séparateur de chemin.",
    )
    parser.add_argument("--title", required=True, help="Titre public du jeu de slides.")
    parser.add_argument(
        "--storyboard",
        required=True,
        type=Path,
        help="Chemin du storyboard à copier dans source/storyboard.md.",
    )
    parser.add_argument(
        "--slides-dir",
        type=Path,
        help="Dossier contenant les images slide-*.png à copier.",
    )
    return parser.parse_args()


def validate_slug(slug: str) -> None:
    if not SLUG_PATTERN.fullmatch(slug):
        raise ValueError(
            "--slug doit être un nom de dossier ASCII en minuscules, sans espace ni chemin."
        )


def copy_file(source: Path, target: Path) -> None:
    if not source.is_file():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def copy_slides(slides_dir: Path, target_slides_dir: Path) -> None:
    if not slides_dir.is_dir():
        raise NotADirectoryError(slides_dir)
    slide_paths = sorted(slides_dir.glob("slide-*.png"))
    if not slide_paths:
        raise FileNotFoundError(f"Aucune image slide-*.png dans {slides_dir}")
    target_slides_dir.mkdir(parents=True, exist_ok=True)
    for slide_path in slide_paths:
        copy_file(slide_path, target_slides_dir / slide_path.name)


def write_variant_metadata(target: Path, slug: str, title: str) -> None:
    metadata = {
        "site_title": title,
        "baseline": "Jeu de slides généré",
        "version_label": slug,
        "diaporama_title": f"Présentation - {title}",
        "site_description": f"Version web accessible du jeu de slides « {title} ».",
        "source_label": "Sources du jeu de slides",
    }
    (target / "variant.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def create_variant(args: argparse.Namespace) -> Path:
    validate_slug(args.slug)
    target = Path.cwd() / args.slug
    if target.exists():
        raise FileExistsError(f"Le dossier existe déjà : {target}")

    target.mkdir()
    for directory in [
        target / "assets" / "downloads",
        target / "assets" / "favicons",
        target / "assets" / "slides",
        target / "source",
        target / "tests",
    ]:
        directory.mkdir(parents=True, exist_ok=True)

    copy_file(ROOT / "build.py", target / "build.py")
    copy_file(
        ROOT / "tests" / "test_site_contracts.py",
        target / "tests" / "test_site_contracts.py",
    )
    copy_file(
        ROOT / "assets" / "favicons" / "favicon.ico",
        target / "assets" / "favicons" / "favicon.ico",
    )
    copy_file(ROOT / "slides.example.json", target / "slides.json")
    copy_file(args.storyboard, target / "source" / "storyboard.md")

    source_markdown = args.storyboard.parent / "source.md"
    if source_markdown.is_file():
        copy_file(source_markdown, target / "source" / "source.md")

    if args.slides_dir is not None:
        copy_slides(args.slides_dir, target / "assets" / "slides")

    write_variant_metadata(target, args.slug, args.title)
    return target


def main() -> int:
    try:
        target = create_variant(parse_args())
    except (OSError, ValueError) as error:
        print(f"Erreur : {error}", file=sys.stderr)
        return 1

    print(f"Jeu créé : {target}")
    print("Prochaine étape : compléter slides.json si nécessaire, puis lancer python3 build.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
