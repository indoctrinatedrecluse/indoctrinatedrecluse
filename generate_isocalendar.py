import os
import json
import datetime
import urllib.request

# Config
DEFAULT_USERNAME = "indoctrinatedrecluse"
OUTPUT_DIR = "profile-3d-contrib"
API = "https://api.github.com/graphql"

# Contribution level -> neon palette (0..4). GraphQL returns `level` as an ENUM
# STRING (e.g. "FIRST_QUARTILE"), so map enum names and raw ints defensively.
LEVEL_ENUM = {
    "NONE": 0,
    "FIRST_QUARTILE": 1,
    "SECOND_QUARTILE": 2,
    "THIRD_QUARTILE": 3,
    "FOURTH_QUARTILE": 4,
}
LEVEL_COLORS = {0: "#16161e", 1: "#3d59a1", 2: "#7aa2f7", 3: "#bb9af3", 4: "#ff79c6"}

QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
            contributionLevel
          }
        }
      }
    }
  }
}
"""


def normalize_level(level):
    if isinstance(level, int):
        return level if 0 <= level <= 4 else 0
    return LEVEL_ENUM.get(level, 0)


def fetch_contributions(username, token):
    """Return {'ok': True, 'weeks', 'total', 'year'} or {'ok': False, 'error'}."""
    if not token:
        return {"ok": False, "error": "no GITHUB_TOKEN available"}
    now = datetime.datetime.now(datetime.timezone.utc)
    year = now.year
    # contributionsCollection requires from/to within the SAME calendar year
    # (a rolling 365-day window is rejected by the API).
    fr = datetime.datetime(year, 1, 1, tzinfo=datetime.timezone.utc)
    to = now.replace(hour=23, minute=59, second=59, microsecond=0)
    body = json.dumps({
        "query": QUERY,
        "variables": {
            "login": username,
            "from": fr.isoformat(),
            "to": to.isoformat(),
        },
    }).encode()
    req = urllib.request.Request(API, data=body, method="POST")
    req.add_header("User-Agent", "Mozilla/5.0")
    req.add_header("Authorization", f"token {token}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode())
        if data.get("errors"):
            error = json.dumps(data["errors"])[:200]
            print(f"GraphQL errors: {error}")
            return {"ok": False, "error": error}
        user = (data.get("data") or {}).get("user") or {}
        cal = user.get("contributionsCollection") or {}
        calendar = cal.get("contributionCalendar") or {}
        weeks = calendar.get("weeks", [])
        if not weeks:
            return {"ok": False, "error": "contributionsCollection returned no weeks"}
        return {
            "ok": True,
            "weeks": weeks,
            "total": calendar.get("totalContributions", 0),
            "year": year,
        }
    except Exception as e:
        error = str(e)[:200]
        print(f"GraphQL request failed: {error}")
        return {"ok": False, "error": error}


def build_grid(result, pad_l, pad_top, step):
    cells = []
    for wi, week in enumerate(result["weeks"]):
        for di, day in enumerate(week.get("contributionDays") or []):
            level = normalize_level(day.get("contributionLevel", day.get("level", 0)))
            fill = LEVEL_COLORS.get(level, "#16161e")
            cells.append(
                f'<rect x="{pad_l + wi * step}" y="{pad_top + di * step}" width="10" height="10" rx="2" fill="{fill}" />'
            )
    return "\n".join(cells)


def generate_isocalendar_svg(username, token, filepath):
    result = fetch_contributions(username, token)

    if result.get("ok"):
        n_weeks = len(result["weeks"])
        width = max(720, 24 + n_weeks * 13 + 16)
        grid = build_grid(result, 24, 92, 13)
        total_text = f"{result['total']} CONTRIBUTIONS"
        foot_text = f"CALENDAR YEAR {result['year']} // NEON HEAT MAP"
        standby = ""
        diag = ""
    else:
        width = 720
        grid = ""
        total_text = "SYNC PENDING"
        foot_text = "RUN DASHBOARD WORKFLOW TO INITIALIZE GRID"
        standby = f"""
  <rect x="24" y="92" width="{width - 48}" height="112" rx="10" fill="none" stroke="#3d59a1" stroke-width="1.5" stroke-dasharray="6 5" />"""
        safe = str(result.get("error", "unknown")).replace("--", "-").replace("\n", " ")
        diag = f"<!-- standby reason: {safe} -->"

    height = 236
    legend = "".join(
        f'<rect x="{24 + idx * 18}" y="222" width="10" height="10" rx="2" fill="{LEVEL_COLORS[idx]}" />'
        for idx in range(5)
    )

    svg_content = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
{diag}
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
    .total {{
      font-family: 'Fira Code', 'Courier New', monospace;
      font-size: 12px;
      font-weight: bold;
      fill: #38bdf8;
      text-anchor: end;
    }}
    .foot {{
      font-family: 'Fira Code', 'Courier New', monospace;
      font-size: 9px;
      fill: #6272a4;
      letter-spacing: 1px;
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
    <text x="18" y="16" class="title">COMMIT GRID</text>
    <text x="18" y="29" class="subtitle">CONTRIBUTION TELEMETRY // GITHUB GRAPHQL</text>
  </g>
  <text x="{width - 24}" y="42" class="total">{total_text}</text>
  {standby}
  {grid}
  <text x="{width - 24}" y="222" class="foot" text-anchor="end">{foot_text}</text>
  {legend}
</svg>
"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated isocalendar SVG at {filepath}")


if __name__ == "__main__":
    token = os.environ.get("GITHUB_TOKEN")
    username = os.environ.get("GITHUB_REPOSITORY_OWNER") or DEFAULT_USERNAME
    print(f"Running isocalendar generation for user: {username}")
    generate_isocalendar_svg(username, token, os.path.join(OUTPUT_DIR, "isocalendar.svg"))
    print("Isocalendar generation finished successfully!")

