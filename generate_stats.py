import os
import json
import urllib.request
import urllib.error

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
        ("FOLLOWERS", str(user.get("followers", 0))),
        ("FOLLOWING", str(user.get("following", 0))),
        ("PROJECTS", str(len(owned))),
        ("TOTAL STARS", str(total_stars)),
        ("TOTAL FORKS", str(total_forks)),
        ("MEMBER SINCE", joined),
    ]


def generate_stats_svg(metrics, filepath):
    if metrics is None:
        return
    width, height = 980, 150
    margin = 28
    count = len(metrics)
    cell_w = (width - 2 * margin) / count

    cells = []
    for idx, (label, value) in enumerate(metrics):
        center_x = margin + cell_w * idx + cell_w / 2
        cells.append(f"""
    <g>
      <text x="{center_x:.1f}" y="108" text-anchor="middle" class="cell-label">{label}</text>
      <text x="{center_x:.1f}" y="136" text-anchor="middle" class="cell-value" filter="url(#glow)">{value}</text>
    </g>""")

    svg_content = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
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
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated profile telemetry SVG at {filepath}")


if __name__ == "__main__":
    token = os.environ.get("GITHUB_TOKEN")
    username = os.environ.get("GITHUB_REPOSITORY_OWNER") or DEFAULT_USERNAME
    print(f"Running stats generation for user: {username}")
    metrics = gather_metrics(username, token)
    generate_stats_svg(metrics, os.path.join(OUTPUT_DIR, "stats.svg"))
    print("Stats generation finished successfully!")
