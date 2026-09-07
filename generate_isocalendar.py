import os
import json
import datetime
import urllib.request

# Config
DEFAULT_USERNAME = "indoctrinatedrecluse"
OUTPUT_DIR = "profile-3d-contrib"
API = "https://api.github.com/graphql"

# Contribution level -> neon palette (0..4)
LEVEL_COLORS = {0: "#16161e", 1: "#3d59a1", 2: "#7aa2f7", 3: "#bb9af3", 4: "#ff79c6"}

QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      totalContributions
      contributionCalendar {
        weeks {
          contributionDays {
            date
            contributionCount
            level
          }
        }
      }
    }
  }
}
"""


def fetch_contributions(username, token):
    if not token:
        print("No GITHUB_TOKEN available; writing standby grid.")
        return None
    now = datetime.datetime.now(datetime.timezone.utc)
    to = now.replace(hour=23, minute=59, second=59, microsecond=0)
    fr = to - datetime.timedelta(days=364)
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
            print(f"GraphQL errors: {data['errors']}")
            return None
        cal = (data.get("data") or {}).get("user", {}).get("contributionsCollection", {})
        if not cal:
            print("No contributionsCollection returned; writing standby grid.")
            return None
        weeks = cal.get("contributionCalendar", {}).get("weeks", [])
        total = cal.get("totalContributions", 0)
        days = {}
        for week in weeks:
            for day in week.get("contributionDays", []):
                days[day["date"]] = (day.get("contributionCount", 0), day.get("level", 0))
        return {"days": days, "total": total, "from": fr.date()}
    except Exception as e:
        print(f"GraphQL request failed: {e}")
        return None


def render_grid(data, pad_l, pad_top, step):
    if not data:
        return ""
    days = data["days"]
    start = data["from"]
    cells = []
    for i in range(365):
        day = start + datetime.timedelta(days=i)
        dkey = day.isoformat()
        count, level = days.get(dkey, (0, 0))
        col = i // 7
        row = day.weekday()
        x = pad_l + col * step
        y = pad_top + row * step
        fill = LEVEL_COLORS.get(level, "#16161e")
        cells.append(f'<rect x="{x}" y="{y}" width="10" height="10" rx="2" fill="{fill}" />')
    return "\n".join(cells)


def generate_isocalendar_svg(username, token, filepath):
    data = fetch_contributions(username, token)

    width, height = 720, 236
    pad_l, pad_top, step = 24, 92, 13
    grid = render_grid(data, pad_l, pad_top, step)

    if data:
        total_text = f"{data['total']} CONTRIBUTIONS // 365D"
        footer = "PAST 365 DAYS OF ACTIVITY // NEON HEAT MAP"
        standby = ""
    else:
        total_text = "SYNC PENDING"
        footer = "RUN DASHBOARD WORKFLOW TO INITIALIZE GRID"
        standby = f"""
  <rect x="24" y="92" width="{width - 48}" height="112" rx="10" fill="none" stroke="#3d59a1" stroke-width="1.5" stroke-dasharray="6 5" />"""

    legend = "".join(
        f'<rect x="{pad_l + idx * 18}" y="222" width="10" height="10" rx="2" fill="{LEVEL_COLORS[idx]}" />'
        for idx in range(5)
    )

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
    <text x="18" y="16" class="title">COMMIT GRID // LAST 365 DAYS</text>
    <text x="18" y="29" class="subtitle">CONTRIBUTION TELEMETRY // GITHUB GRAPHQL</text>
  </g>
  <text x="{width - 24}" y="42" class="total">{total_text}</text>
  {standby}
  {grid}
  <text x="{width - 24}" y="222" class="foot" text-anchor="end">{footer}</text>
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

