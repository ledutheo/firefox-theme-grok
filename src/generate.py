#!/usr/bin/env python3
"""Génère icônes + images chrome du thème Firefox Grok Night.

Source unique : palette.json + mark.svg.
Sortie : theme/icons/ et theme/images/
"""
from __future__ import annotations

import json
import math
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
# Linux CSD : min / max / close occupent ~140–160 px à droite.
# additional_backgrounds "right top" tombait SUR la croix — on ne l'utilise plus.
WINDOW_CONTROLS = 172
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


def circle_from_photo(src: Path, size: int, out: Path) -> None:
    """Icône circulaire depuis la photo trou noir (fond transparent hors disque)."""
    im = Image.open(src).convert("RGBA")
    side = min(im.size)
    left = (im.size[0] - side) // 2
    top = (im.size[1] - side) // 2
    im = im.crop((left, top, left + side, top + side)).resize(
        (size, size), Image.Resampling.LANCZOS
    )
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((1, 1, size - 2, size - 2), fill=255)
    im.putalpha(mask)
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, "PNG")


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


def star_catalog(count: int, seed: int, y_max: int) -> list[tuple[int, int, int, int, float]]:
    """x, y, rayon, alpha_base, phase — pour faire clignoter sans tout recréer."""
    rng = random.Random(seed)
    stars = []
    for _ in range(count):
        stars.append(
            (
                rng.randint(0, FRAME_W - 1),
                rng.randint(3, y_max),
                rng.choice((0, 0, 0, 1, 1, 2)),
                rng.randint(50, 200),
                rng.random() * 6.28,
            )
        )
    return stars


def paint_star_catalog(
    img: Image.Image,
    stars: list[tuple[int, int, int, int, float]],
    color: tuple[int, int, int],
    t: float,
) -> None:
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for x, y, r, base, phase in stars:
        pulse = 0.45 + 0.55 * (0.5 + 0.5 * math.sin(t * 2.2 + phase))
        a = max(20, min(255, int(base * pulse)))
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(*color, a))
    img.alpha_composite(overlay)


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


def load_logo_variants(size: int) -> list[Image.Image]:
    """Variantes du dossier src/logos + trou noir photoreal. Recadrage circulaire."""
    names = ["wood.jpg", "fur.jpg", "vortex.jpg", "phi.jpg", "seal.jpg"]
    out: list[Image.Image] = []
    photo = SRC / "blackhole.jpg"
    if photo.is_file():
        circle_from_photo(photo, size, ICONS / "_tmp_bh.png")
        out.append(Image.open(ICONS / "_tmp_bh.png").convert("RGBA"))
    for name in names:
        path = SRC / "logos" / name
        if path.is_file():
            dest = ICONS / f"_tmp_{path.stem}.png"
            circle_from_photo(path, size, dest)
            out.append(Image.open(dest).convert("RGBA"))
    return out


def make_frame(
    kind: str,
    logos: list[Image.Image],
    stars: list[tuple[int, int, int, int, float]],
    t: float = 0.0,
) -> Image.Image:
    """Bande d'onglets : barre blanche, ciel d'étoiles, logos à gauche des boutons."""
    if kind == "night":
        left = hex_to_rgb(TOKENS["void"])
        right = (18, 14, 16)
        accent = hex_to_rgb(TOKENS["accent"])
        star = (252, 252, 252)
        bloom_a = 28
    else:
        left = hex_to_rgb(TOKENS["day_chrome"])
        right = (250, 244, 238)
        accent = hex_to_rgb(TOKENS["day_accent"])
        star = (90, 90, 90)
        bloom_a = 18

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

    paint_star_catalog(img, stars, star, t)

    mark_y = (TAB_STRIP - MARK_ON_FRAME) // 2 + 2
    gap = MARK_ON_FRAME + 10
    # de droite à gauche, en laissant la place des boutons de fenêtre
    for i, logo in enumerate(logos):
        mark_x = FRAME_W - WINDOW_CONTROLS - MARK_ON_FRAME - i * gap
        if mark_x < 80:
            break
        glow = 0.75 + 0.25 * (0.5 + 0.5 * math.sin(t * 1.4 + i * 0.9))
        sized = logo.resize((MARK_ON_FRAME, MARK_ON_FRAME), Image.Resampling.LANCZOS)
        if glow < 0.98:
            faded = Image.new("RGBA", sized.size, (0, 0, 0, 0))
            faded.paste(sized, (0, 0))
            alpha = faded.split()[-1].point(lambda a: int(a * glow))
            faded.putalpha(alpha)
            sized = faded
        cx = mark_x + MARK_ON_FRAME / 2
        img.alpha_composite(
            orange_bloom(
                (FRAME_W, FRAME_H),
                accent,
                cx,
                TAB_STRIP / 2,
                36,
                int(bloom_a * glow),
            )
        )
        paste_mark(img, sized, (mark_x, mark_y))

    # Barre blanche collée au sommet de la fenêtre (demandée).
    ImageDraw.Draw(img).rectangle((0, 0, FRAME_W, 2), fill=(252, 252, 252, 255))
    return img


def write_apng(frames: list[Image.Image], dest: Path, fps: int = 8) -> None:
    """Firefox n'anime pas les GIF dans un thème. L'équivalent AMO, c'est l'APNG."""
    tmp = dest.parent / "_apng_frames"
    tmp.mkdir(exist_ok=True)
    for i, frame in enumerate(frames):
        frame.convert("RGBA").save(tmp / f"{i:02d}.png", "PNG")
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-framerate",
            str(fps),
            "-i",
            str(tmp / "%02d.png"),
            "-plays",
            "0",
            "-f",
            "apng",
            str(dest),
        ],
        check=True,
    )
    for leftover in tmp.glob("*.png"):
        leftover.unlink()
    tmp.rmdir()


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
    photo = SRC / "blackhole.jpg"
    if photo.is_file():
        for size in ICON_SIZES:
            circle_from_photo(photo, size, ICONS / f"icon-{size}.png")
    else:
        svg = SRC / "mark.svg"
        for size in ICON_SIZES:
            rsvg(svg, ICONS / f"icon-{size}.png", size)

    wall = SRC / "wallpaper.jpg"
    if wall.is_file():
        Image.open(wall).convert("RGB").save(IMAGES / "ntp-wallpaper.jpg", "JPEG", quality=88)
        newtab = ROOT / "beyond/newtab"
        newtab.mkdir(parents=True, exist_ok=True)
        Image.open(wall).convert("RGB").save(newtab / "wallpaper.jpg", "JPEG", quality=88)
        circle_from_photo(photo, 256, newtab / "mark.png")

    logos = load_logo_variants(MARK_ON_FRAME)
    stars_night = star_catalog(520, seed=1975, y_max=TAB_STRIP - 2)
    stars_day = star_catalog(80, seed=2026, y_max=TAB_STRIP - 2)
    n_frames = 8
    night_frames = [
        make_frame("night", logos, stars_night, t=i / n_frames * 6.28)
        for i in range(n_frames)
    ]
    write_apng(night_frames, IMAGES / "theme_frame.png", fps=7)
    make_frame("day", logos, stars_day, t=0).save(IMAGES / "theme_frame_day.png", "PNG")
    night_frames[0].save(IMAGES / "theme_frame_still.png", "PNG")
    for junk in ICONS.glob("_tmp_*.png"):
        junk.unlink()
    make_glow().save(IMAGES / "glow.png", "PNG")
    # filet blanc, pas orange — chrome façon logo Grok (noir / blanc)
    status = Image.new("RGB", (1080, 80), hex_to_rgb(TOKENS["void"]))
    ImageDraw.Draw(status).rectangle((0, 76, 1080, 80), fill=hex_to_rgb(TOKENS["text"]))
    status.save(IMAGES / "android_status.png", "PNG")
    # Calque 48×48, coin haut-droit des onglets (additional_backgrounds).
    spark = Image.open(ICONS / "icon-48.png").convert("RGBA")
    spark.save(IMAGES / "spark.png", "PNG")
    # Bande visible seule, pour juger sans Firefox.
    night_frames[0].crop((FRAME_W - 1280, 0, FRAME_W, TAB_STRIP)).save(
        IMAGES / "strip-preview.png", "PNG"
    )
    write_css_preview()
    print(f"icônes : {', '.join(str(s) for s in ICON_SIZES)}")
    print(f"images : {IMAGES}")


if __name__ == "__main__":
    main()
