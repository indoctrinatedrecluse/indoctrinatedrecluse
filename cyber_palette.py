"""Cyberpunk day/night palette switching.

NIGHT is the classic Tokyo-Night dark look (default, identity mapping).
DAY is a lighter "synthwave morning" palette for 06:00-17:59 UTC.

Every generated SVG goes through apply_theme() before being written, so a
single ordered hex remap keeps every widget consistent on both palettes.
"""

import os
import datetime

# Ordered (night_source_hex, day_hex) replacements. Order matters: targets are
# never also sources, so a simple str.replace chain is safe.
#
# DAY is tuned for legibility on light backgrounds: near-white lavender panels,
# deep slate text, and darker-but-still-neon accents (pink-600 / sky-700 /
# violet-600). #3d59a1 does double duty as border AND level-1 grid cells, so it
# maps to a mid indigo (#6d79b5) that reads clearly both ways.
DAY_MAP = [
    ("#0f111a", "#ecebf7"),   # banner outer canvas
    ("#00000f", "#ecebf7"),   # 3D calendar background
    ("#1a1b26", "#f6f3fd"),   # card background / caret-off / bg panels
    ("#16161e", "#e8e4f6"),   # tiles / empty contribution cells
    ("#1e1e2e", "#dcd7eb"),   # progress bar empty track
    ("#eeeeff", "#1e2335"),   # 3D calendar bright text
    ("#c0caf5", "#1e2335"),   # bright body text
    ("#e2e8f0", "#262c46"),   # bright body text (language rows)
    ("#7aa2f7", "#5865b0"),   # secondary blue text
    ("#6272a4", "#5e6380"),   # muted text / subtitles
    ("#aaaaaa", "#5e6380"),   # 3D calendar muted text
    ("#3d59a1", "#6d79b5"),   # borders / level-1 grid cells
    ("#ff79c6", "#c0267f"),   # pink accents
    ("#38bdf8", "#0277bd"),   # cyan accents
    ("#bb9af3", "#7c3aed"),   # purple accents
    ("#4ade80", "#15803d"),   # green tags
    ("#f87171", "#dc2626"),   # red tags
    ("#facc15", "#a16207"),   # yellow tags
    ("#fbbf24", "#b45309"),   # amber tags
    ("#fb923c", "#c2410c"),   # orange tags
]


def current_theme():
    """Return 'night' or 'day'. THEME env overrides; otherwise UTC clock decides."""
    explicit = os.environ.get("THEME", "").strip().lower()
    if explicit in ("night", "day"):
        return explicit
    hour = datetime.datetime.now(datetime.timezone.utc).hour
    return "day" if 6 <= hour < 18 else "night"


def apply_theme(svg, theme=None):
    """Recolor an SVG string for the given theme ('night' | 'day' | 'auto')."""
    theme = (theme or current_theme()).lower()
    if theme != "day":
        return svg
    for source, target in DAY_MAP:
        svg = svg.replace(source, target)
    return svg


def save_dual_theme_svg(svg_night, filepath):
    """Save an SVG string as dark, light, and default variants.

    For example, filepath 'profile-3d-contrib/stats.svg' generates:
      - 'profile-3d-contrib/stats-dark.svg'
      - 'profile-3d-contrib/stats-light.svg'
      - 'profile-3d-contrib/stats.svg' (matches dark for fallback)
    """
    dirname, basename = os.path.split(filepath)
    if dirname:
        os.makedirs(dirname, exist_ok=True)

    name, ext = os.path.splitext(basename)
    dark_path = os.path.join(dirname, f"{name}-dark{ext}")
    light_path = os.path.join(dirname, f"{name}-light{ext}")
    default_path = filepath

    svg_light = apply_theme(svg_night, "day")

    with open(dark_path, "w", encoding="utf-8") as f:
        f.write(svg_night)
    with open(light_path, "w", encoding="utf-8") as f:
        f.write(svg_light)
    with open(default_path, "w", encoding="utf-8") as f:
        f.write(svg_night)

    print(f"Generated dual-theme SVGs for {filepath}:")
    print(f"  Dark:  {dark_path}")
    print(f"  Light: {light_path}")
    print(f"  Base:  {default_path}")
    return {"dark": dark_path, "light": light_path, "base": default_path}


def recolor_file_to_light(dark_filepath, light_filepath=None):
    """Read an existing dark SVG file and write a light-themed version."""
    if not os.path.exists(dark_filepath):
        print(f"Warning: {dark_filepath} does not exist, cannot recolor.")
        return None
    if not light_filepath:
        dirname, basename = os.path.split(dark_filepath)
        name, ext = os.path.splitext(basename)
        light_filepath = os.path.join(dirname, f"{name}-light{ext}")

    with open(dark_filepath, "r", encoding="utf-8") as f:
        svg_content = f.read()

    svg_light = apply_theme(svg_content, "day")
    with open(light_filepath, "w", encoding="utf-8") as f:
        f.write(svg_light)
    print(f"Recolored {dark_filepath} -> {light_filepath}")
    return light_filepath

