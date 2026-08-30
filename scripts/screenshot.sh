#!/usr/bin/env bash
# Rend hero.png (1280×800, AMO) et og.png (1280×640) depuis docs/mockup.html.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
IMG="$ROOT/docs/img"
mkdir -p "$IMG"
cp "$ROOT/theme/icons/icon-128.png" "$IMG/icon-128.png"
cp "$ROOT/theme/icons/icon-48.png" "$IMG/icon-48.png"

PROFILE="$(mktemp -d)"
cleanup() { rm -rf "$PROFILE"; }
trap cleanup EXIT

# Profil jetable : pas d'onboarding, fond noir.
cat > "$PROFILE/user.js" <<'EOF'
user_pref("browser.startup.homepage_override.mstone", "ignore");
user_pref("startup.homepage_welcome_url", "");
user_pref("toolkit.telemetry.reportingpolicy.firstRun", false);
user_pref("datareporting.policy.dataSubmissionEnabled", false);
user_pref("browser.aboutwelcome.enabled", false);
user_pref("browser.shell.checkDefaultBrowser", false);
user_pref("privacy.trackingprotection.enabled", false);
EOF

MOCK="file://$ROOT/docs/mockup.html"
OUT="$IMG/hero.png"

firefox --headless --profile "$PROFILE" --window-size=1280,800 \
  --screenshot="$OUT" "$MOCK" >/dev/null 2>&1 || {
  echo "firefox --screenshot a échoué" >&2
  exit 1
}

python3 - "$OUT" "$IMG/og.png" <<'PY'
from pathlib import Path
import sys
from PIL import Image

hero = Image.open(sys.argv[1]).convert("RGB")
# Firefox headless peut ajouter un liseré : on recadre pile 1280×800 si plus grand.
w, h = hero.size
if w != 1280 or h != 800:
    hero = hero.crop((0, 0, min(1280, w), min(800, h)))
    if hero.size != (1280, 800):
        canvas = Image.new("RGB", (1280, 800), (10, 10, 10))
        canvas.paste(hero, (0, 0))
        hero = canvas
    hero.save(sys.argv[1], "PNG")
# OG : 1280×640 — on garde le chrome, on coupe le bas de page.
og = hero.crop((0, 0, 1280, 640))
og.save(sys.argv[2], "PNG")
print(sys.argv[1], hero.size)
print(sys.argv[2], og.size)
PY
