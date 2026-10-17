import os
import json
import html
import urllib.request
import urllib.error
from cyber_palette import save_dual_theme_svg

# Config
DEFAULT_USERNAME = "indoctrinatedrecluse"
OUTPUT_DIR = "profile-3d-contrib"
MAX_TILES = 6

# Language -> neon accent (kept in sync with generate_assets.py)
LANG_ACCENTS = {
    "Python": "#38bdf8",
    "JavaScript": "#facc15",
    "TypeScript": "#60a5fa",
    "HTML": "#f87171",
    "C++": "#ec4899",
    "C#": "#3ddc97",
    "Java": "#fbbf24",
    "Go": "#22d3ee",
    "Rust": "#ff79c6",
    "Ruby": "#f87171",
    "PHP": "#818cf8",
    "Odin": "#bb9af3",
    "Nim": "#fbbf24",
    "Elixir": "#7aa2f7",
    "Prolog": "#4ade80",
    "Shell": "#4ade80",
}


def lang_accent(lang):
    return LANG_ACCENTS.get(lang or "", "#7aa2f7")


def fetch_json(url, token=None):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0")
    if token:
        req.add_header("Authorization", f"token {token}")
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP Error fetching {url}: {e.code} - {e.reason}")
        return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def gather_repos(username, token):
    repos = fetch_json(f"https://api.github.com/users/{username}/repos?per_page=100", token) or []
    owned = [
        r for r in repos
        if not r.get("fork") and not r.get("archived") and r.get("name") != username
    ]
    owned.sort(key=lambda r: (-(r.get("stargazers_count") or 0), r.get("updated_at") or ""))
    return owned[:MAX_TILES]


def clip(text, limit):
    text = " ".join(str(text).split())
    return text[:limit] + ("…" if len(text) > limit else "")



def corner_paths(width, height):
    """Neon corner brackets drawn just inside the panel edges."""
    specs = [
        (f"M14 40 L14 22 Q14 14 22 14 L40 14", "#38bdf8"),            # top-left
        (f"M{width - 14} 40 L{width - 14} 22 Q{width - 14} 14 {width - 22} 14 L{width - 40} 14", "#ff79c6"),  # top-right
        (f"M14 {height - 40} L14 {height - 22} Q14 {height - 14} 22 {height - 14} L40 {height - 14}", "#ff79c6"),  # bottom-left
        (f"M{width - 14} {height - 40} L{width - 14} {height - 22} Q{width - 14} {height - 14} {width - 22} {height - 14} L{width - 40} {height - 14}", "#38bdf8"),  # bottom-right
    ]
    return "".join(
        f'\n    <path d="{d}" fill="none" stroke="{c}" stroke-width="2.5" stroke-linecap="round" filter="url(#cornerGlow)" />'
        for d, c in specs
    )


def grid_lines(width, height):
    """Faint neon grid backdrop."""
    parts = []
    for y in range(46, height, 32):
        parts.append(f'<line x1="14" y1="{y}" x2="{width - 14}" y2="{y}" stroke="#3d59a1" stroke-opacity="0.16" stroke-width="1" />')
    for x in range(72, width, 76):
        parts.append(f'<line x1="{x}" y1="14" x2="{x}" y2="{height - 14}" stroke="#3d59a1" stroke-opacity="0.10" stroke-width="1" />')
    return "\n".join(parts)


def generate_featured_svg(username, token, filepath=os.path.join(OUTPUT_DIR, "featured.svg")):
    repos = gather_repos(username, token)

    width, height = 700, 300
    tile_w, tile_h = 204, 92
    gap_x, gap_y = 20, 18
    cols = 3
    top = 84

    tiles = ""
    if repos:
        for i, r in enumerate(repos):
            col = i % cols
            row = i // cols
            x = 24 + col * (tile_w + gap_x)
            y = top + row * (tile_h + gap_y)
            raw_name = r.get("name") or ""
            name = html.escape(raw_name)
            lang = r.get("language")
            accent = lang_accent(lang)
            desc = html.escape(clip(r.get("description") or "no description logged", 32))
            stars = (r.get("stargazers_count") or 0)
            forks = (r.get("forks_count") or 0)
            lang_txt = html.escape(lang or "unknown")
            url = html.escape(r.get("html_url") or f"https://github.com/{username}/{raw_name}")

            tiles += f"""
  <a href="{url}" target="_blank" rel="noopener noreferrer">
    <g class="featured-tile">
      <rect x="{x - 4}" y="{y - 4}" width="{tile_w + 8}" height="{tile_h + 8}" rx="14" fill="{accent}" opacity="0.16" filter="url(#tileGlow)" />
      <rect x="{x}" y="{y}" width="{tile_w}" height="{tile_h}" rx="10" fill="#16161e" stroke="#3d59a1" stroke-opacity="0.9" stroke-width="1.5" class="tile-rect" />
      <rect x="{x + 14}" y="{y + 20}" width="8" height="8" rx="2" fill="{accent}" />
      <text x="{x + 28}" y="{y + 28}" font-family="'Fira Code', monospace" font-size="12" font-weight="bold" fill="#c0caf5" class="tile-title">{name}</text>
      <text x="{x + 14}" y="{y + 50}" font-family="'Fira Code', monospace" font-size="9" fill="#7aa2f7">{desc}</text>
      <text x="{x + 14}" y="{y + 72}" font-family="'Fira Code', monospace" font-size="8" fill="{accent}">{lang_txt.upper()}</text>
      <text x="{x + tile_w - 12}" y="{y + 72}" text-anchor="end" font-family="'Fira Code', monospace" font-size="8" fill="#fbbf24">★ {stars} | FORKS {forks}</text>
    </g>
  </a>"""
    else:
        tiles = f"""
    <text x="{width // 2}" y="{top + tile_h}" text-anchor="middle" font-family="'Fira Code', monospace" font-size="12" fill="#6272a4">// UNABLE TO LOAD PROJECT TELEMETRY //</text>"""

    svg_content = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="vignette" cx="50%" cy="34%" r="85%">
      <stop offset="0%" stop-color="#bb9af3" stop-opacity="0.20" />
      <stop offset="55%" stop-color="#38bdf8" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#1a1b26" stop-opacity="0" />
    </radialGradient>
    <filter id="tileGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
      </feMerge>
    </filter>
    <filter id="cornerGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="2.5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>
  <style>
    a {{
      cursor: pointer;
      text-decoration: none;
    }}
    .tile-rect {{
      transition: stroke-width 0.2s, stroke 0.2s;
    }}
    a:hover .tile-rect {{
      stroke-width: 2.2;
      stroke: #38bdf8;
    }}
    a:hover .tile-title {{
      fill: #ff79c6;
    }}
    .title {{
      font-family: 'Fira Code', 'Courier New', monospace;
      font-size: 16px;
      font-weight: bold;
      fill: #ff79c6;
    }}
    .subtitle {{
      font-family: 'Fira Code', 'Courier New', monospace;
      font-size: 9px;
      fill: #6272a4;
      letter-spacing: 2px;
    }}
    .bg {{
      fill: #1a1b26;
      stroke: #3d59a1;
      stroke-width: 2;
      rx: 14px;
    }}
  </style>

  <rect width="{width}" height="{height}" class="bg" />
  <rect x="2" y="2" width="{width - 4}" height="{height - 4}" rx="12" fill="url(#vignette)" />

  <!-- Neon grid backdrop -->
  {grid_lines(width, height)}

  <g transform="translate(28, 26)">
    <rect x="0" y="0" width="6" height="22" fill="#38bdf8" rx="2" />
    <text x="18" y="16" class="title">FEATURED PROJECTS</text>
    <text x="18" y="29" class="subtitle">AUTO-SELECTED // LATEST SIGNALS</text>
  </g>
  <line x1="28" y1="64" x2="{width - 28}" y2="64" stroke="#3d59a1" stroke-opacity="0.6" stroke-width="1" />

  {corner_paths(width, height)}

  {tiles}
</svg>
"""
    paths = save_dual_theme_svg(svg_content, filepath)
    return paths


if __name__ == "__main__":
    token = os.environ.get("GITHUB_TOKEN")
    username = os.environ.get("GITHUB_REPOSITORY_OWNER") or DEFAULT_USERNAME
    print(f"Running featured generation for user: {username}")
    generate_featured_svg(username, token)
    print("Featured generation finished successfully!")


