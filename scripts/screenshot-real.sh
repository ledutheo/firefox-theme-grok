#!/usr/bin/env bash
# Capture Firefox Developer Edition AVEC le thème chargé (signatures off).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
IMG="$ROOT/docs/img"
XPI="$ROOT/dist/grok-night.xpi"
[ -f "$XPI" ] || { echo "build d'abord : $XPI" >&2; exit 1; }
command -v firefox-developer-edition >/dev/null || {
  echo "firefox-developer-edition introuvable" >&2
  exit 1
}

PROFILE="$(mktemp -d)"
cleanup() { rm -rf "$PROFILE"; }
trap cleanup EXIT

mkdir -p "$PROFILE/extensions"
cp "$XPI" "$PROFILE/extensions/{509635ca-327f-493d-a156-277548d25172}.xpi"

cat > "$PROFILE/user.js" <<EOF
user_pref("xpinstall.signatures.required", false);
user_pref("extensions.langpacks.signatures.required", false);
user_pref("extensions.autoDisableScopes", 0);
user_pref("extensions.enabledScopes", 15);
user_pref("extensions.startupScanScopes", 15);
user_pref("browser.aboutwelcome.enabled", false);
user_pref("startup.homepage_welcome_url", "");
user_pref("startup.homepage_override_url", "");
user_pref("browser.startup.homepage_override.mstone", "ignore");
user_pref("browser.shell.checkDefaultBrowser", false);
user_pref("datareporting.policy.dataSubmissionEnabled", false);
user_pref("toolkit.telemetry.reportingpolicy.firstRun", false);
user_pref("app.update.enabled", false);
user_pref("app.update.auto", false);
user_pref("identity.fxaccounts.enabled", false);
user_pref("devtools.devedition.promo.enabled", false);
user_pref("browser.startup.page", 1);
user_pref("browser.startup.homepage", "file://$ROOT/docs/content.html");
user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);
EOF

# Premier lancement : installe le thème. Second : capture.
firefox-developer-edition --headless --profile "$PROFILE" --window-size=1280,800 \
  "about:blank" >/dev/null 2>&1 &
PID=$!
sleep 4
kill "$PID" 2>/dev/null || true
wait "$PID" 2>/dev/null || true

OUT="$IMG/firefox-real.png"
firefox-developer-edition --headless --profile "$PROFILE" --window-size=1280,800 \
  --screenshot="$OUT" "file://$ROOT/docs/content.html" >/dev/null 2>&1 || {
  echo "screenshot réel échoué" >&2
  exit 1
}
python3 - "$OUT" <<'PY'
from PIL import Image
import sys
im = Image.open(sys.argv[1])
print(sys.argv[1], im.size)
PY
