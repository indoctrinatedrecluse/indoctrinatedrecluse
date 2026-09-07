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
DAY_MAP = [
    ("#0f111a", "#e9e4f6"),   # banner outer canvas
    ("#1a1b26", "#f6f3fc"),   # card background / caret-off / bg panels
    ("#16161e", "#ede9fb"),   # tiles / empty contribution cells
    ("#c0caf5", "#232635"),   # bright body text
    ("#e2e8f0", "#2b3147"),   # bright body text (language rows)
    ("#7aa2f7", "#41529f"),   # secondary blue text
    ("#6272a4", "#5c6080"),   # muted text / subtitles
    ("#3d59a1", "#6e7bb0"),   # borders / dim accents
    ("#ff79c6", "#c2257a"),   # pink accents
    ("#38bdf8", "#0284c7"),   # cyan accents
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
