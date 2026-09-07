import os
import json
import html
import urllib.request
import urllib.error
from cyber_palette import apply_theme

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
    "CSS": "#c084fc",
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
    "Svelte": "#fb923c",
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


def generate_featured_svg(username, token, filepath):
    repos = gather_repos(username, token)

    width, height = 700, 278
    tile_w, tile_h = 204, 84
    gap_x, gap_y = 20, 14
    cols = 3
    top = 78

    body = ""
    if repos:
        for i, r in enumerate(repos):
            col = i % cols
            row = i // cols
            x = 24 + col * (tile_w + gap_x)
            y = top + row * (tile_h + gap_y)
            name = html.escape(r.get("name") or "")
            lang = r.get("language")
            accent = lang_accent(lang)
            desc = html.escape(clip(r.get("description") or "no description logged", 32))
            stars = (r.get("stargazers_count") or 0)
            forks = (r.get("forks_count") or 0)
            lang_txt = html.escape(lang or "unknown")
            body += f"""
  <g>
    <rect x="{x}" y="{y}" width="{tile_w}" height="{tile_h}" rx="10" fill="#16161e" stroke="#3d59a1" stroke-opacity="0.9" stroke-width="1.5" />
    <rect x="{x + 14}" y="{y + 18}" width="8" height="8" rx="2" fill="{accent}" />
    <text x="{x + 28}" y="{y + 26}" font-family="'Fira Code', monospace" font-size="12" font-weight="bold" fill="#c0caf5">{name}</text>
    <text x="{x + 14}" y="{y + 48}" font-family="'Fira Code', monospace" font-size="9" fill="#7aa2f7">{desc}</text>
    <text x="{x + 14}" y="{y + 66}" font-family="'Fira Code', monospace" font-size="8" fill="{accent}">{lang_txt.upper()}</text>
    <text x="{x + tile_w - 12}" y="{y + 66}" text-anchor="end" font-family="'Fira Code', monospace" font-size="8" fill="#fbbf24">★ {stars} | FORKS {forks}</text>
  </g>"""
    else:
        body = f"""
    <text x="350" y="{top + tile_h}" text-anchor="middle" font-family="'Fira Code', monospace" font-size="12" fill="#6272a4">// UNABLE TO LOAD PROJECT TELEMETRY //</text>"""

    svg_content = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
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
      rx: 12px;
    }}
  </style>

  <rect width="{width}" height="{height}" class="bg" />

  <g transform="translate(24, 24)">
    <rect x="0" y="0" width="6" height="22" fill="#38bdf8" rx="2" />
    <text x="18" y="16" class="title">FEATURED PROJECTS</text>
    <text x="18" y="29" class="subtitle">AUTO-SELECTED // LATEST SIGNALS</text>
  </g>
  <line x1="24" y1="60" x2="{width - 24}" y2="60" stroke="#3d59a1" stroke-opacity="0.6" stroke-width="1" />
  {body}
</svg>
"""
    svg_content = apply_theme(svg_content)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated featured SVG at {filepath}")


if __name__ == "__main__":
    token = os.environ.get("GITHUB_TOKEN")
    username = os.environ.get("GITHUB_REPOSITORY_OWNER") or DEFAULT_USERNAME
    print(f"Running featured generation for user: {username}")
    generate_featured_svg(username, token, os.path.join(OUTPUT_DIR, "featured.svg"))
    print("Featured generation finished successfully!")
