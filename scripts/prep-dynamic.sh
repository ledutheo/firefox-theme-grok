#!/usr/bin/env bash
# Copie images + icônes dans beyond/dynamic/ pour un chargement about:debugging autonome.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/src/generate.py"
mkdir -p "$ROOT/beyond/dynamic/images"
cp -a "$ROOT/theme/images/." "$ROOT/beyond/dynamic/images/"
cp "$ROOT/theme/icons/icon-48.png" "$ROOT/beyond/dynamic/icon-48.png"
cp "$ROOT/theme/icons/icon-96.png" "$ROOT/beyond/dynamic/icon-96.png"
echo "dynamic prêt : $ROOT/beyond/dynamic/manifest.json"
