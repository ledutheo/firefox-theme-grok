#!/usr/bin/env bash
# Copie userChrome.css + userContent.css dans le profil Firefox par défaut.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/beyond/userChrome"

profile=""
for base in "$HOME/.mozilla/firefox" "$HOME/.mozilla/firefox-esr" "$HOME/.config/mozilla/firefox"; do
  ini="$base/profiles.ini"
  [ -f "$ini" ] || continue
  path="$(awk -F= '
    /^\[Install/ { in_install=1; next }
    /^\[/ { in_install=0 }
    in_install && $1=="Default" { print $2; exit }
  ' "$ini")"
  if [ -z "$path" ]; then
    path="$(awk -F= '
      /^\[Profile/ { p=1; def=0 }
      p && $1=="Default" && $2==1 { def=1 }
      p && $1=="Path" { last=$2 }
      p && def && last { print last; exit }
    ' "$ini")"
  fi
  [ -n "$path" ] || continue
  if [[ "$path" == /* ]]; then
    profile="$path"
  else
    profile="$base/$path"
  fi
  [ -d "$profile" ] && break
done

if [ -z "$profile" ] || [ ! -d "$profile" ]; then
  echo "aucun profil Firefox trouvé" >&2
  exit 1
fi

mkdir -p "$profile/chrome"
cp "$SRC/userChrome.css" "$profile/chrome/userChrome.css"
cp "$SRC/userContent.css" "$profile/chrome/userContent.css"

pref="$profile/user.js"
touch "$pref"
line='user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);'
grep -Fqx "$line" "$pref" 2>/dev/null || printf '%s\n' "$line" >>"$pref"

echo "chrome : $profile/chrome/"
echo "pref   : $line"
echo "redémarre Firefox."
