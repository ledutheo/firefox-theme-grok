#!/usr/bin/env python3
"""Vérifie le thème : JSONC, fichiers, locales, taille header."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


def load_jsonc(path: Path) -> object:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"(^|[^:])//[^\n]*", r"\1", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        errors.append(f"{path.relative_to(ROOT)} : JSONC invalide ({exc})")
        return None


def need(path: Path) -> None:
    if not path.is_file():
        errors.append(f"manque {path.relative_to(ROOT)}")


manifest = load_jsonc(ROOT / "theme/manifest.json")
if isinstance(manifest, dict):
    gecko = manifest.get("browser_specific_settings", {}).get("gecko", {})
    if gecko.get("id") != "grok-night@ledutheo":
        errors.append("id gecko inattendu")
    if "theme" not in manifest or "dark_theme" not in manifest:
        errors.append("theme / dark_theme manquant")
    colors = manifest.get("theme", {}).get("colors", {})
    if len(colors) < 30:
        errors.append(f"trop peu de couleurs ({len(colors)})")
    for hex_key, value in colors.items():
        if not (isinstance(value, str) and re.fullmatch(r"#[0-9A-Fa-f]{6}", value)):
            errors.append(f"couleur non #RRGGBB : {hex_key}={value!r}")

need(ROOT / "theme/icons/icon-48.png")
need(ROOT / "theme/icons/icon-128.png")
need(ROOT / "theme/images/theme_frame.png")
need(ROOT / "theme/_locales/fr/messages.json")
need(ROOT / "theme/_locales/en/messages.json")
need(ROOT / "src/palette.json")
need(ROOT / "src/firefox-color.json")
need(ROOT / "docs/img/hero.png")
need(ROOT / "docs/img/icon-128.png")

for loc in ("fr", "en"):
    data = load_jsonc(ROOT / f"theme/_locales/{loc}/messages.json")
    if isinstance(data, dict) and "extensionName" not in data:
        errors.append(f"locale {loc} sans extensionName")

frame = ROOT / "theme/images/theme_frame.png"
if frame.is_file():
    try:
        from PIL import Image

        im = Image.open(frame)
        if im.size[1] < 180:
            errors.append(f"theme_frame trop bas ({im.size})")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"theme_frame illisible : {exc}")

if errors:
    print("lint KO")
    for item in errors:
        print(" -", item)
    sys.exit(1)
print("lint OK")
