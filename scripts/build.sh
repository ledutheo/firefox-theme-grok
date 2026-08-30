#!/usr/bin/env bash
# Empaquette le thème statique en XPI (zip). Pas besoin du binaire "zip".
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
THEME="$ROOT/theme"
DIST="$ROOT/dist"
XPI="$DIST/grok-night.xpi"

python3 "$ROOT/src/generate.py"

mkdir -p "$DIST"
python3 - "$THEME" "$XPI" <<'PY'
import json, re, sys, zipfile
from pathlib import Path

theme, xpi = Path(sys.argv[1]), Path(sys.argv[2])
manifest_text = (theme / "manifest.json").read_text(encoding="utf-8")
# Firefox accepte le JSONC ; on vérifie quand même que ça parse.
stripped = re.sub(r"/\*.*?\*/", "", manifest_text, flags=re.S)
stripped = re.sub(r"(^|[^:])//[^\n]*", r"\1", stripped)
json.loads(stripped)

skip_dir = {".git"}
# Paquet = uniquement ce que le manifest référence (+ locales + icônes).
keep_prefix = (
    "manifest.json",
    "_locales/",
    "icons/",
    "images/theme_frame.png",
)
with zipfile.ZipFile(xpi, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for path in sorted(theme.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(theme).as_posix()
        if any(part in skip_dir for part in path.parts):
            continue
        if not any(rel == p or rel.startswith(p) for p in keep_prefix):
            continue
        zf.write(path, rel)
print(xpi)
PY

python3 - "$XPI" <<'PY'
import zipfile, sys
from pathlib import Path
xpi = Path(sys.argv[1])
with zipfile.ZipFile(xpi) as zf:
    names = zf.namelist()
print(f"{xpi} ({xpi.stat().st_size} octets)")
for n in names:
    print(" ", n)
if "manifest.json" not in names:
    raise SystemExit("manifest.json absent du XPI")
PY
