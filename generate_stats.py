import os
import json
import urllib.request
import urllib.error
from cyber_palette import save_dual_theme_svg

# Config
DEFAULT_USERNAME = "indoctrinatedrecluse"
OUTPUT_DIR = "profile-3d-contrib"


def fetch_json(url, token=None):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0")
    if token:
        req.add_header("Authorization", f"token {token}")
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP Error fetching {url}: {e.code} - {e.reason}")
        return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def gather_metrics(username, token):
    user = fetch_json(f"https://api.github.com/users/{username}", token)
    if not user:
        print("Could not fetch user profile; skipping stats card.")
        return None
    repos = fetch_json(f"https://api.github.com/users/{username}/repos?per_page=100", token)
    owned = [r for r in (repos or []) if not r.get("fork") and not r.get("archived")]
    total_stars = sum(r.get("stargazers_count") or 0 for r in owned)
    total_forks = sum(r.get("forks_count") or 0 for r in owned)
    joined = (user.get("created_at") or "2021")[:4]
    return [
        ("FOLLOWERS", str(user.get("followers", 0)), f"https://github.com/{username}?tab=followers"),
        ("FOLLOWING", str(user.get("following", 0)), f"https://github.com/{username}?tab=following"),
        ("PROJECTS", str(len(owned)), f"https://github.com/{username}?tab=repositories"),
        ("TOTAL STARS", str(total_stars), f"https://github.com/{username}?tab=repositories&amp;q=&amp;type=&amp;language=&amp;sort=stargazers"),
        ("TOTAL FORKS", str(total_forks), f"https://github.com/{username}?tab=repositories"),
        ("MEMBER SINCE", joined, f"https://github.com/{username}"),
    ]


def generate_stats_svg(metrics, filepath=os.path.join(OUTPUT_DIR, "stats.svg")):
    if metrics is None:
        return None
    width, height = 980, 150
    margin = 28
    count = len(metrics)
    cell_w = (width - 2 * margin) / count

    cells = []
    for idx, (label, value, url) in enumerate(metrics):
        center_x = margin + cell_w * idx + cell_w / 2
        cells.append(f"""
    <a href="{url}" target="_blank" rel="noopener noreferrer">
      <rect x="{margin + cell_w * idx + 4}" y="78" width="{cell_w - 8}" height="62" rx="8" fill="#16161e" fill-opacity="0.3" class="cell-hover" />
      <text x="{center_x:.1f}" y="104" text-anchor="middle" class="cell-label">{label}</text>
      <text x="{center_x:.1f}" y="132" text-anchor="middle" class="cell-value" filter="url(#glow)">{value}</text>
    </a>""")

    svg_content = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    a {{
      cursor: pointer;
      text-decoration: none;
    }}
    .cell-hover {{
      transition: fill-opacity 0.2s, stroke 0.2s;
      stroke: transparent;
      stroke-width: 1;
    }}
    a:hover .cell-hover {{
      fill-opacity: 0.8;
      stroke: #38bdf8;
    }}
    a:hover .cell-value {{
      fill: #ff79c6;
    }}
    .title {{
      font-family: 'Fira Code', 'Courier New', monospace;
      font-size: 17px;
      font-weight: bold;
      fill: #ff79c6;
    }}
    .subtitle {{
      font-family: 'Fira Code', 'Courier New', monospace;
      font-size: 10px;
      fill: #6272a4;
      letter-spacing: 2px;
    }}
    .cell-label {{
      font-family: 'Fira Code', 'Courier New', monospace;
      font-size: 10px;
      fill: #7aa2f7;
      letter-spacing: 1.5px;
    }}
    .cell-value {{
      font-family: 'Fira Code', 'Courier New', monospace;
      font-size: 26px;
      font-weight: bold;
      fill: #38bdf8;
    }}
    .bg {{
      fill: #1a1b26;
      stroke: #3d59a1;
      stroke-width: 2;
      rx: 14px;
    }}
  </style>

  <defs>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Background Panel -->
  <rect width="{width}" height="{height}" class="bg" />

  <!-- Header Section -->
  <g transform="translate(28, 26)">
    <rect x="0" y="0" width="6" height="22" fill="#38bdf8" rx="2" filter="url(#glow)" />
    <text x="18" y="17" class="title">SYSTEM CORE: PROFILE TELEMETRY</text>
    <text x="18" y="31" class="subtitle">LIVE ACCOUNT SIGNALS // AUTOMATED DAILY SYNC</text>
  </g>
  <line x1="28" y1="68" x2="{width - 28}" y2="68" stroke="#3d59a1" stroke-opacity="0.6" stroke-width="1" />

  <!-- Metric Cells -->
  {''.join(cells)}
</svg>
"""
    paths = save_dual_theme_svg(svg_content, filepath)
    return paths


if __name__ == "__main__":
    token = os.environ.get("GITHUB_TOKEN")
    username = os.environ.get("GITHUB_REPOSITORY_OWNER") or DEFAULT_USERNAME
    print(f"Running stats generation for user: {username}")
    metrics = gather_metrics(username, token)
    generate_stats_svg(metrics)
    print("Stats generation finished successfully!")

