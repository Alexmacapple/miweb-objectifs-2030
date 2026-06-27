#!/usr/bin/env bash
set -euo pipefail

port="${1:-8000}"

echo "Serveur local : http://127.0.0.1:${port}/"
echo "Arrêt : Ctrl+C"
python3 -m http.server "$port" --bind 127.0.0.1
