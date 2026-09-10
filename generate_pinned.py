import os
import json
import html
import re
import urllib.request
import urllib.error
from cyber_palette import apply_theme

# Config
DEFAULT_USERNAME = "indoctrinatedrecluse"
OUTPUT_DIR = "profile-3d-contrib"
MAX_TILES = 6

# Language -> neon accent (aligned with cyber_palette.DAY_MAP for day/night consistency)
LANG_ACCENTS = {
    "Python": "#38bdf8",
    "JavaScript": "#facc15",
    "TypeScript": "#7aa2f7",
    "HTML": "#f87171",
    "C#": "#4ade80",
    "Java": "#fbbf24",
    "Go": "#38bdf8",
    "Rust": "#ff79c6",
    "C++": "#ff79c6",
    "Shell": "#4ade80",
    "PHP": "#bb9af3",
    "Ruby": "#f87171",
    "C": "#7aa2f7",
    "Swift": "#fb923c",
    "Kotlin": "#bb9af3",
}

GRAPHQL_QUERY = """
query($login: String!) {
  user(login: $login) {
    pinnedItems(first: 6, types: [REPOSITORY]) {
      nodes {
        ... on Repository {
          name
          description
          forkCount
          stargazerCount
          url
          isFork
          primaryLanguage {
            name
          }
        }
      }
    }
  }
}
"""


def lang_accent(lang):
    return LANG_ACCENTS.get(lang or "", "#7aa2f7")


def clip(text, limit):
    text = " ".join(str(text).split())
    return text[:limit] + ("…" if len(text) > limit else "")


def fetch_pinned_graphql(username, token):
    if not token:
        return None
    url = "https://api.github.com/graphql"
    body = json.dumps({
        "query": GRAPHQL_QUERY,
        "variables": {"login": username},
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("User-Agent", "Mozilla/5.0")
    req.add_header("Authorization", f"token {token}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        if data.get("errors"):
            print(f"GraphQL errors: {json.dumps(data['errors'])[:200]}")
            return None
        nodes = (
            data.get("data", {})
            .get("user", {})
            .get("pinnedItems", {})
            .get("nodes", [])
        )
        repos = []
        for n in nodes:
            if not n:
                continue
            lang = (n.get("primaryLanguage") or {}).get("name") or "Unknown"
            repos.append({
                "name": n.get("name", ""),
                "description": n.get("description") or "",
                "language": lang,
                "stargazers_count": n.get("stargazerCount", 0),
                "forks_count": n.get("forkCount", 0),
                "url": n.get("url", f"https://github.com/{username}/{n.get('name', '')}"),
            })
        return repos if repos else None
    except Exception as e:
        print(f"GraphQL pinned fetch error: {e}")
        return None


def fetch_pinned_scrape(username):
    url = f"https://github.com/{username}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8")
    except Exception as e:
        print(f"Scrape pinned fetch error: {e}")
        return None

    pinned_blocks = re.findall(r'<div class="[^"]*pinned-item-list-item-content[^"]*">([\s\S]*?)</li>', content)
    if not pinned_blocks:
        return None

    repos = []
    for block in pinned_blocks:
        repo_m = re.search(r'<span class="repo"[^>]*>([^<]+)</span>', block)
        if not repo_m:
            continue
        repo = repo_m.group(1).strip()

        desc_m = re.search(r'<p class="[^"]*pinned-item-desc[^"]*">([\s\S]*?)</p>', block)
        desc = ""
        if desc_m:
            desc = re.sub(r'<[^>]+>', '', desc_m.group(1))
            desc = " ".join(desc.split())
            desc = html.unescape(desc)

        lang_m = re.search(r'<span itemprop="programmingLanguage">([^<]+)</span>', block)
        lang = lang_m.group(1).strip() if lang_m else "Unknown"

        stars_m = re.search(r'href="[^"]+/stargazers"[^>]*>[\s\S]*?([0-9,]+)\s*</a>', block)
        stars = int(stars_m.group(1).replace(",", "")) if stars_m else 0

        forks_m = re.search(r'href="[^"]+/forks"[^>]*>[\s\S]*?([0-9,]+)\s*</a>', block)
        forks = int(forks_m.group(1).replace(",", "")) if forks_m else 0

        repos.append({
            "name": repo,
            "description": desc,
            "language": lang,
            "stargazers_count": stars,
            "forks_count": forks,
            "url": f"https://github.com/{username}/{repo}",
        })
    return repos if repos else None


def gather_pinned_repos(username, token):
    # Primary: query GitHub GraphQL for the user's pinned repositories
    repos = fetch_pinned_graphql(username, token)
    if repos is not None:
        print(f"Fetched {len(repos)} pinned repositories via GraphQL.")
        return repos[:MAX_TILES]

    # Fallback: scrape user's public GitHub profile directly for pinned items (e.g. tokenless local runs)
    repos = fetch_pinned_scrape(username)
    if repos is not None:
        print(f"Scraped {len(repos)} pinned repositories from public profile.")
        return repos[:MAX_TILES]

    print("No pinned repositories retrieved from GitHub.")
    return []


def corner_paths(width, height):
    """Neon corner brackets drawn just inside the panel edges."""
    specs = [
        (f"M14 40 L14 22 Q14 14 22 14 L40 14", "#38bdf8"),
        (f"M{width - 14} 40 L{width - 14} 22 Q{width - 14} 14 {width - 22} 14 L{width - 40} 14", "#ff79c6"),
        (f"M14 {height - 40} L14 {height - 22} Q14 {height - 14} 22 {height - 14} L40 {height - 14}", "#ff79c6"),
        (f"M{width - 14} {height - 40} L{width - 14} {height - 22} Q{width - 14} {height - 14} {width - 22} {height - 14} L{width - 40} {height - 14}", "#38bdf8"),
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


def generate_pinned_svg(username, token, filepath):
    repos = gather_pinned_repos(username, token)

    width = 700
    cols = 2
    tile_w = 316
    tile_h = 88
    gap_x = 20
    gap_y = 14
    top = 82

    num_rows = max(1, (len(repos) + 1) // 2) if repos else 1
    height = top + num_rows * tile_h + (num_rows - 1) * gap_y + 22 if repos else 220

    tiles = ""
    if repos:
        for i, r in enumerate(repos):
            col = i % cols
            row = i // cols
            x = 24 + col * (tile_w + gap_x)
            y = top + row * (tile_h + gap_y)
            name = html.escape(clip(r.get("name") or "", 22))
            lang = r.get("language") or "Unknown"
            accent = lang_accent(lang)
            desc_raw = r.get("description") or "curated system repository // no telemetry logged"
            desc = html.escape(clip(desc_raw, 44))
            stars = r.get("stargazers_count", 0)
            forks = r.get("forks_count", 0)
            lang_txt = html.escape(lang)

            tiles += f"""
  <g>
    <rect x="{x - 3}" y="{y - 3}" width="{tile_w + 6}" height="{tile_h + 6}" rx="12" fill="{accent}" opacity="0.14" filter="url(#tileGlow)" />
    <rect x="{x}" y="{y}" width="{tile_w}" height="{tile_h}" rx="10" fill="#16161e" stroke="#3d59a1" stroke-opacity="0.9" stroke-width="1.5" />
    <circle cx="{x + 18}" cy="{y + 22}" r="3.5" fill="{accent}" />
    <text x="{x + 28}" y="{y + 26}" font-family="'Fira Code', monospace" font-size="12" font-weight="bold" fill="#c0caf5">{name}</text>
    <rect x="{x + tile_w - 58}" y="{y + 14}" width="46" height="15" rx="3" fill="#1a1b26" stroke="#3d59a1" stroke-width="1" />
    <text x="{x + tile_w - 35}" y="{y + 25}" text-anchor="middle" font-family="'Fira Code', monospace" font-size="8" fill="#ff79c6">PINNED</text>
    <text x="{x + 18}" y="{y + 48}" font-family="'Fira Code', monospace" font-size="9" fill="#7aa2f7">{desc}</text>
    <rect x="{x + 18}" y="{y + 67}" width="6" height="6" rx="1.5" fill="{accent}" />
    <text x="{x + 29}" y="{y + 73}" font-family="'Fira Code', monospace" font-size="8" font-weight="bold" fill="{accent}">{lang_txt.upper()}</text>
    <text x="{x + tile_w - 14}" y="{y + 73}" text-anchor="end" font-family="'Fira Code', monospace" font-size="8" fill="#fbbf24">★ {stars}  ⑂ {forks}</text>
  </g>"""
    else:
        tiles = f"""
  <text x="{width // 2}" y="{top + 50}" text-anchor="middle" font-family="'Fira Code', monospace" font-size="12" fill="#6272a4">// NO PINNED TELEMETRY DETECTED //</text>"""

    svg_content = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="vignette" cx="50%" cy="34%" r="85%">
      <stop offset="0%" stop-color="#bb9af3" stop-opacity="0.20" />
      <stop offset="55%" stop-color="#38bdf8" stop-opacity="0.08" />
      <stop offset="100%" stop-color="#1a1b26" stop-opacity="0" />
    </radialGradient>
    <filter id="tileGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5" result="blur" />
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

  {grid_lines(width, height)}

  <g transform="translate(28, 26)">
    <rect x="0" y="0" width="6" height="22" fill="#ff79c6" rx="2" />
    <text x="18" y="16" class="title">PINNED REPOSITORIES</text>
    <text x="18" y="29" class="subtitle">PRIMARY CORES // DIRECT PROTOCOL ACCESS</text>
  </g>
  <line x1="28" y1="64" x2="{width - 28}" y2="64" stroke="#3d59a1" stroke-opacity="0.6" stroke-width="1" />

  {corner_paths(width, height)}

  {tiles}
</svg>
"""
    svg_content = apply_theme(svg_content)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated pinned repos SVG at {filepath}")


if __name__ == "__main__":
    token = os.environ.get("GITHUB_TOKEN")
    username = os.environ.get("GITHUB_REPOSITORY_OWNER") or DEFAULT_USERNAME
    print(f"Running pinned repos generation for user: {username}")
    generate_pinned_svg(username, token, os.path.join(OUTPUT_DIR, "pinned.svg"))
    print("Pinned repos generation finished successfully!")

