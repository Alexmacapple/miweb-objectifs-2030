#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: scripts/validate_variant.sh <slug>" >&2
  exit 2
fi

slug="$1"
if [ ! -d "$slug" ]; then
  echo "Erreur : dossier absent : $slug" >&2
  exit 1
fi

python3 -m unittest discover -s "$slug/tests"
npx --yes html-validate "$slug/index.html" "$slug/alternatives.html" "$slug/accessibilite.html" index.html
npx --yes vnu-jar --errors-only "$slug/index.html" "$slug/alternatives.html" "$slug/accessibilite.html" index.html
