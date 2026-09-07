import os
import json
import urllib.request
import urllib.error
from cyber_palette import apply_theme

# Config
DEFAULT_USERNAME = "indoctrinatedrecluse"
OUTPUT_DIR = "profile-3d-contrib"


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


def gather_stats(username, token):
    user = fetch_json(f"https://api.github.com/users/{username}", token) or {}
    repos = fetch_json(f"https://api.github.com/users/{username}/repos?per_page=100", token) or []
    owned = [r for r in repos if not r.get("fork") and not r.get("archived")]
    langs = {r.get("language") for r in owned if r.get("language")}
    return {
        "followers": user.get("followers", 0),
        "projects": len(owned),
        "langs": len(langs),
        "stars": sum(r.get("stargazers_count") or 0 for r in owned),
        "forks": sum(r.get("forks_count") or 0 for r in owned),
        "year": (user.get("created_at") or "2021")[:4],
    }


def build_tiles(s):
    return [
        ("SYS.INIT", f"ONLINE SINCE {s['year']}", "ACCOUNT BOOTED", True),
        ("POLYGLOT", f"{s['langs']} LANGUAGES", "5+ LANGUAGE ARSENAL", s["langs"] >= 5),
        ("ARCHITECT", f"{s['projects']} PROJECTS", "10+ PUBLIC PROJECTS", s["projects"] >= 10),
        ("SIGNAL", f"{s['followers']} FOLLOWERS", "10+ FOLLOWERS REQUIRED", s["followers"] >= 10),
        ("STARGAZER", f"{s['stars']} STARS", "25+ STARS REQUIRED", s["stars"] >= 25),
        ("FORKSMITH", f"{s['forks']} FORKS", "10+ FORKS REQUIRED", s["forks"] >= 10),
    ]


def generate_achievements_svg(username, token, filepath):
    stats = gather_stats(username, token)
    tiles = build_tiles(stats)

    width, height = 700, 278
    tile_w, tile_h = 204, 84
    gap_x, gap_y = 20, 14
    cols = 3
    top = 78

    body = ""
    for i, (tid, label, sub, unlocked) in enumerate(tiles):
        col = i % cols
        row = i // cols
        x = 24 + col * (tile_w + gap_x)
        y = top + row * (tile_h + gap_y)
        if unlocked:
            stroke, id_fill, lab_fill, sub_fill = "#ff79c6", "#38bdf8", "#c0caf5", "#7aa2f7"
            status = "UNLOCKED"
            status_fill = "#ff79c6"
        else:
            stroke, id_fill, lab_fill, sub_fill = "#3d59a1", "#3d59a1", "#6272a4", "#3d59a1"
            status = "LOCKED"
            status_fill = "#3d59a1"
        body += f"""
  <g>
    <rect x="{x}" y="{y}" width="{tile_w}" height="{tile_h}" rx="10" fill="#16161e" stroke="{stroke}" stroke-opacity="0.9" stroke-width="1.5" />
    <text x="{x + 14}" y="{y + 24}" font-family="'Fira Code', monospace" font-size="10" font-weight="bold" fill="{id_fill}">{tid}</text>
    <text x="{x + tile_w - 12}" y="{y + 24}" text-anchor="end" font-family="'Fira Code', monospace" font-size="8" fill="{status_fill}">[{status}]</text>
    <text x="{x + 14}" y="{y + 48}" font-family="'Fira Code', monospace" font-size="13" font-weight="bold" fill="{lab_fill}">{label}</text>
    <text x="{x + 14}" y="{y + 68}" font-family="'Fira Code', monospace" font-size="8" letter-spacing="1px" fill="{sub_fill}">{sub}</text>
  </g>"""

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
    <rect x="0" y="0" width="6" height="22" fill="#bb9af3" rx="2" />
    <text x="18" y="16" class="title">SYSTEM ACHIEVEMENTS</text>
    <text x="18" y="29" class="subtitle">UNLOCK PROGRESS // GITHUB TELEMETRY</text>
  </g>
  <line x1="24" y1="60" x2="{width - 24}" y2="60" stroke="#3d59a1" stroke-opacity="0.6" stroke-width="1" />
  {body}
</svg>
"""
    svg_content = apply_theme(svg_content)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated achievements SVG at {filepath}")


if __name__ == "__main__":
    token = os.environ.get("GITHUB_TOKEN")
    username = os.environ.get("GITHUB_REPOSITORY_OWNER") or DEFAULT_USERNAME
    print(f"Running achievements generation for user: {username}")
    generate_achievements_svg(username, token, os.path.join(OUTPUT_DIR, "achievements.svg"))
    print("Achievements generation finished successfully!")

