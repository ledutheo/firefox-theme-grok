#!/usr/bin/env python3
"""Génère icônes + images chrome du thème Firefox Grok Night.

Source unique : palette.json + mark.svg.
Sortie : theme/icons/ et theme/images/
"""
from __future__ import annotations

import json
import random
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
THEME = ROOT / "theme"
ICONS = THEME / "icons"
IMAGES = THEME / "images"
PALETTE = json.loads((SRC / "palette.json").read_text(encoding="utf-8"))
TOKENS = PALETTE["tokens"]

FRAME_W, FRAME_H = 3000, 200
# Le chrome visible (onglets) fait ~40–48 px de haut. Tout ce qui est
# plus bas dans l'image 200 px disparaît. Identité collée en haut à droite.
MARK_ON_FRAME = 32
TAB_STRIP = 48
ICON_SIZES = (16, 32, 48, 96, 128)


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    v = value.lstrip("#")
    return int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16)


def rsvg(svg: Path, png: Path, size: int) -> None:
    png.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "rsvg-convert",
            "-w",
            str(size),
            "-h",
            str(size),
            "-o",
            str(png),
            str(svg),
        ],
        check=True,
    )


def lerp(a: int, b: int, t: float) -> int:
    return int(round(a + (b - a) * t))


def gradient_row(left: tuple[int, int, int], right: tuple[int, int, int], width: int) -> list[tuple[int, int, int]]:
    return [
        (
            lerp(left[0], right[0], x / (width - 1)),
            lerp(left[1], right[1], x / (width - 1)),
            lerp(left[2], right[2], x / (width - 1)),
        )
        for x in range(width)
    ]


def paint_stars(img: Image.Image, count: int, color: tuple[int, int, int], seed: int) -> None:
    rng = random.Random(seed)
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for _ in range(count):
        x = rng.randint(0, w - 1)
        y = rng.randint(0, h - 1)
        r = rng.choice((0, 0, 0, 1, 1, 2))
        a = rng.randint(40, 180)
        star = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(star).ellipse((x - r, y - r, x + r, y + r), fill=(*color, a))
        img.alpha_composite(star)


def orange_bloom(size: tuple[int, int], color: tuple[int, int, int], cx: float, cy: float, radius: float, alpha: int) -> Image.Image:
    w, h = size
    bloom = Image.new("RGBA", size, (0, 0, 0, 0))
    overlay = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.ellipse(
        (cx - radius, cy - radius, cx + radius, cy + radius),
        fill=(*color, alpha),
    )
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=radius * 0.45))
    bloom.alpha_composite(overlay)
    return bloom


def paste_mark(frame: Image.Image, mark: Image.Image, xy: tuple[int, int]) -> None:
    frame.alpha_composite(mark.convert("RGBA"), xy)


def make_frame(kind: str, mark: Image.Image) -> Image.Image:
    """Chrome réel : void, étoiles, halo à droite, petite marque. Pas de billboard."""
    if kind == "night":
        left = hex_to_rgb(TOKENS["void"])
        right = (22, 14, 12)
        accent = hex_to_rgb(TOKENS["accent"])
        star = (252, 252, 252)
        seed = 1975
        n_stars = 160
        bloom_a = 38
    else:
        left = hex_to_rgb(TOKENS["day_chrome"])
        right = (250, 244, 238)
        accent = hex_to_rgb(TOKENS["day_accent"])
        star = (90, 90, 90)
        seed = 2026
        n_stars = 24
        bloom_a = 28

    img = Image.new("RGBA", (FRAME_W, FRAME_H), (*left, 255))
    px = img.load()
    row = gradient_row(left, right, FRAME_W)
    for x, color in enumerate(row):
        for y in range(FRAME_H):
            v = 1.0 - abs((y / (FRAME_H - 1)) - 0.5) * 0.08
            px[x, y] = (
                int(color[0] * v),
                int(color[1] * v),
                int(color[2] * v),
                255,
            )

    # Étoiles surtout dans la bande d'onglets (haut), pas au milieu de l'image.
    paint_stars(img, n_stars, star, seed)
    bloom = orange_bloom(
        (FRAME_W, FRAME_H),
        accent,
        FRAME_W - 90,
        TAB_STRIP / 2,
        90,
        bloom_a + 16,
    )
    img.alpha_composite(bloom)

    # Filet orange type grok.com, collé au bord haut — toujours visible.
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, FRAME_W, 2), fill=(*accent, 220))

    mark_x = FRAME_W - MARK_ON_FRAME - 14
    mark_y = (TAB_STRIP - MARK_ON_FRAME) // 2
    paste_mark(
        img,
        mark.resize((MARK_ON_FRAME, MARK_ON_FRAME), Image.Resampling.LANCZOS),
        (mark_x, mark_y),
    )
    return img


def make_glow() -> Image.Image:
    """Calque additionnel : halo orange, ancré à droite (additional_backgrounds)."""
    w, h = 640, 200
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    accent = hex_to_rgb(TOKENS["accent"])
    bloom = orange_bloom((w, h), accent, w * 0.78, h / 2, 140, 42)
    img.alpha_composite(bloom)
    return img


def make_android_status() -> Image.Image:
    """Bande 1080x80 — utile si un fork Android applique theme_frame."""
    color = hex_to_rgb(TOKENS["void"])
    img = Image.new("RGB", (1080, 80), color)
    draw = ImageDraw.Draw(img)
    accent = hex_to_rgb(TOKENS["accent"])
    draw.rectangle((0, 76, 1080, 80), fill=accent)
    return img


def write_css_preview() -> None:
    """Petit SVG « about:newtab » pour se juger sans Firefox."""
    t = TOKENS
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="800" viewBox="0 0 1280 800">
  <rect width="1280" height="800" fill="{t['void']}"/>
  <rect x="0" y="0" width="1280" height="88" fill="{t['chrome']}"/>
  <rect x="16" y="28" width="180" height="44" rx="8" fill="{t['elevated']}"/>
  <rect x="204" y="28" width="220" height="44" rx="8" fill="{t['panel']}"/>
  <rect x="204" y="70" width="220" height="3" fill="{t['accent']}"/>
  <rect x="440" y="32" width="520" height="36" rx="18" fill="{t['field']}" stroke="{t['line']}"/>
  <circle cx="1210" cy="50" r="14" fill="{t['accent']}"/>
  <text x="40" y="56" fill="{t['text_dim']}" font-family="sans-serif" font-size="14">about:newtab</text>
  <text x="250" y="56" fill="{t['text']}" font-family="sans-serif" font-size="14">grok.com</text>
  <text x="640" y="400" fill="{t['text']}" font-family="sans-serif" font-size="48" text-anchor="middle">Grok Night</text>
  <text x="640" y="448" fill="{t['text_dim']}" font-family="sans-serif" font-size="18" text-anchor="middle">void {t['void']} · accent {t['accent']}</text>
</svg>
"""
    (SRC / "preview-chrome.svg").write_text(svg, encoding="utf-8")


def main() -> None:
    ICONS.mkdir(parents=True, exist_ok=True)
    IMAGES.mkdir(parents=True, exist_ok=True)
    svg = SRC / "mark.svg"
    for size in ICON_SIZES:
        rsvg(svg, ICONS / f"icon-{size}.png", size)

    mark_128 = Image.open(ICONS / "icon-128.png")
    make_frame("night", mark_128).save(IMAGES / "theme_frame.png", "PNG")
    make_frame("day", mark_128).save(IMAGES / "theme_frame_day.png", "PNG")
    make_glow().save(IMAGES / "glow.png", "PNG")
    make_android_status().save(IMAGES / "android_status.png", "PNG")
    # Calque 48×48, coin haut-droit des onglets (additional_backgrounds).
    spark = Image.open(ICONS / "icon-48.png").convert("RGBA")
    spark.save(IMAGES / "spark.png", "PNG")
    # Bande visible seule, pour juger sans Firefox.
    frame = Image.open(IMAGES / "theme_frame.png")
    frame.crop((FRAME_W - 1280, 0, FRAME_W, TAB_STRIP)).save(IMAGES / "strip-preview.png", "PNG")
    write_css_preview()
    print(f"icônes : {', '.join(str(s) for s in ICON_SIZES)}")
    print(f"images : {IMAGES}")


if __name__ == "__main__":
    main()
