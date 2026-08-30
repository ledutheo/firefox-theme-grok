#!/usr/bin/env bash
# Charge Grok Night dans Firefox.
# Release Mozilla refuse les thèmes non signés en permanent :
#   → about:debugging (temporaire) marche toujours
#   → sideload XPI : ESR / Dev / pref xpinstall.signatures.required = false
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
"$ROOT/scripts/build.sh" >/dev/null
XPI="$ROOT/dist/grok-night.xpi"
GECKO_ID="grok-night@ledutheo"
FIREFOX_APP_ID="{ec8030f7-c20a-464f-9b0e-13a3a9e97384}"

echo "XPI : $XPI"
echo
echo "Install temporaire (marche sur Firefox Release) :"
echo "  1. about:debugging#/runtime/this-firefox"
echo "  2. Charger un module temporaire"
echo "  3. choisir $ROOT/theme/manifest.json"
echo

install_xpi_into() {
  mkdir -p "$1"
  cp "$XPI" "$1/$GECKO_ID.xpi"
  chmod 644 "$1/$GECKO_ID.xpi"
  echo "sideload : $1/$GECKO_ID.xpi"
}

install_xpi_into "$HOME/.mozilla/extensions/$FIREFOX_APP_ID"
install_xpi_into "$HOME/.config/mozilla/extensions/$FIREFOX_APP_ID"

# profils
for base in \
  "$HOME/.mozilla/firefox" \
  "$HOME/.mozilla/firefox-esr" \
  "$HOME/.config/mozilla/firefox"
do
  ini="$base/profiles.ini"
  [ -f "$ini" ] || continue
  while IFS= read -r path; do
    [ -n "$path" ] || continue
    if [[ "$path" == /* ]]; then
      profile="$path"
    else
      profile="$base/$path"
    fi
    [ -d "$profile" ] || continue
    install_xpi_into "$profile/extensions"
  done < <(awk -F= '
    /^\[/ { in_profile = ($0 ~ /^\[Profile/) }
    in_profile && $1 == "Path" { print $2 }
  ' "$ini")
done

echo
echo "Sideload posé. Firefox Release le grise tant qu'il n'est pas signé AMO."
echo "Pour du permanent : ESR, ou soumettre dist/grok-night.xpi sur addons.mozilla.org."
