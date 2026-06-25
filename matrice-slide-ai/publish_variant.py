#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
CATALOG_PATH = REPO_ROOT / "published-versions.json"
SLUG_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
REQUIRED_OUTPUTS = [
    "index.html",
    "alternatives.html",
    "accessibilite.html",
    "slides.json",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Publier un jeu de slides déjà généré sur l’accueil racine."
    )
    parser.add_argument("--slug", required=True, help="Nom du dossier à publier.")
    return parser.parse_args()


def validate_slug(slug: str) -> None:
    if not SLUG_PATTERN.fullmatch(slug):
        raise ValueError(
            "jeu non vérifiable : le slug doit être un nom de dossier simple."
        )


def load_build_module():
    spec = importlib.util.spec_from_file_location("matrix_build", ROOT / "build.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Impossible de charger matrice-slide-ai/build.py.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def default_catalog(build_module) -> list[dict[str, str]]:
    return [
        {"slug": slug, "label": label}
        for slug, label in build_module.ROOT_CATALOG_BOOTSTRAP
    ]


def validate_catalog_entry(entry: object) -> dict[str, str]:
    if not isinstance(entry, dict):
        raise ValueError("Le catalogue doit contenir des objets JSON.")
    slug = entry.get("slug")
    label = entry.get("label")
    if not isinstance(slug, str) or not isinstance(label, str):
        raise ValueError("Chaque entrée du catalogue doit contenir slug et label.")
    validate_slug(slug)
    if not label.strip():
        raise ValueError("Chaque entrée du catalogue doit avoir un label non vide.")
    return {"slug": slug, "label": label}


def load_catalog(build_module) -> list[dict[str, str]]:
    if not CATALOG_PATH.is_file():
        return default_catalog(build_module)
    raw_catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    if not isinstance(raw_catalog, list):
        raise ValueError("published-versions.json doit contenir une liste.")
    return [validate_catalog_entry(entry) for entry in raw_catalog]


def label_for_variant(target: Path, slug: str) -> str:
    metadata_path = target / "variant.json"
    if metadata_path.is_file():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        site_title = metadata.get("site_title")
        if isinstance(site_title, str) and site_title.strip():
            return site_title.strip()
    return slug.replace("-", " ").title()


def assert_file_exists(path: Path) -> None:
    if not path.is_file():
        raise ValueError(f"jeu non vérifiable : fichier absent {path}")


def verify_variant(slug: str) -> Path:
    target = REPO_ROOT / slug
    if not target.is_dir():
        raise ValueError(f"jeu non vérifiable : dossier absent {slug}")

    for relative_path in REQUIRED_OUTPUTS:
        assert_file_exists(target / relative_path)
    assert_file_exists(target / "assets" / "downloads" / f"{slug}-slides.zip")

    tests_dir = target / "tests"
    if not tests_dir.is_dir():
        raise ValueError(f"jeu non vérifiable : tests absents {tests_dir}")
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(tests_dir)],
        cwd=target,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise ValueError(
            "jeu non vérifiable : les tests du jeu échouent\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return target


def upsert_catalog_entry(
    catalog: list[dict[str, str]],
    slug: str,
    label: str,
) -> list[dict[str, str]]:
    next_catalog = []
    updated = False
    for entry in catalog:
        if entry["slug"] == slug:
            next_catalog.append({"slug": slug, "label": label})
            updated = True
        else:
            next_catalog.append(entry)
    if not updated:
        next_catalog.append({"slug": slug, "label": label})
    return next_catalog


def publish(slug: str) -> None:
    validate_slug(slug)
    target = verify_variant(slug)
    build_module = load_build_module()
    catalog = upsert_catalog_entry(
        load_catalog(build_module),
        slug,
        label_for_variant(target, slug),
    )

    root_html = build_module.render_root(catalog)
    CATALOG_PATH.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (REPO_ROOT / "index.html").write_text(root_html, encoding="utf-8")
    print(f"Jeu publié : {slug}")


def main() -> int:
    try:
        publish(parse_args().slug)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as error:
        print(f"Erreur : {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
