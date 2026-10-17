import os
import json
import html
import datetime
import urllib.request
import urllib.error
from cyber_palette import save_dual_theme_svg

# Config
DEFAULT_USERNAME = "indoctrinatedrecluse"
OUTPUT_DIR = "profile-3d-contrib"
MAX_ROWS = 6


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


def fmt_rel(iso):
    try:
        dt = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
        secs = (datetime.datetime.now(datetime.timezone.utc) - dt).total_seconds()
        if secs < 0:
            secs = 0
        m, h, d = int(secs // 60), int(secs // 3600), int(secs // 86400)
        if m < 60:
            return f"{m}m"
        if h < 24:
            return f"{h}h"
        if d < 30:
            return f"{d}d"
        return f"{d // 30}mo"
    except Exception:
        return ""


def clip(text, limit):
    text = " ".join(str(text).split())
    return text[:limit] + ("…" if len(text) > limit else "")


def event_row(ev):
    typ = ev.get("type", "")
    full_repo = (ev.get("repo") or {}).get("name", "")
    repo = full_repo.split("/")[-1] if "/" in full_repo else full_repo
    payload = ev.get("payload") or {}
    when = fmt_rel(ev.get("created_at", ""))
    repo_url = f"https://github.com/{full_repo}" if full_repo else f"https://github.com/{DEFAULT_USERNAME}"

    if typ == "PushEvent":
        commits = payload.get("commits") or []
        msg = clip((commits[0].get("message") or "").splitlines()[0], 46) if commits else f"{payload.get('size', 1)} commits"
        return ("PUSH", "#38bdf8", repo, msg, when, repo_url)
    if typ == "CreateEvent":
        ref = payload.get("ref") or payload.get("ref_type", "repository")
        return ("CREATE", "#4ade80", repo, clip(ref, 46), when, repo_url)
    if typ == "DeleteEvent":
        return ("DELETE", "#f87171", repo, clip(payload.get("ref_type", ""), 46), when, repo_url)
    if typ == "PullRequestEvent":
        pr = payload.get("pull_request") or {}
        return (f"PR·{payload.get('action', '')}".upper(), "#bb9af3", repo, clip(pr.get("title", ""), 46), when, repo_url)
    if typ == "IssuesEvent":
        iss = payload.get("issue") or {}
        return (f"ISSUE·{payload.get('action', '')}".upper(), "#facc15", repo, clip(iss.get("title", ""), 46), when, repo_url)
    if typ == "IssueCommentEvent":
        iss = payload.get("issue") or {}
        return ("COMMENT", "#7aa2f7", repo, clip("on " + str(iss.get("title", "")), 46), when, repo_url)
    if typ == "PullRequestReviewEvent":
        return ("REVIEW", "#bb9af3", repo, "pull request review", when, repo_url)
    if typ == "ForkEvent":
        return ("FORK", "#ff79c6", repo, "forked repository", when, repo_url)
    if typ == "WatchEvent":
        return ("STAR", "#fbbf24", repo, "starred repository", when, repo_url)
    if typ == "ReleaseEvent":
        rel = payload.get("release") or {}
        return ("RELEASE", "#fb923c", repo, clip(rel.get("tag_name", ""), 46), when, repo_url)
    if typ == "PublicEvent":
        return ("PUBLIC", "#4ade80", repo, "open sourced", when, repo_url)
    return (typ.replace("Event", "").upper(), "#7aa2f7", repo, "", when, repo_url)


def generate_activity_svg(username, token, filepath=os.path.join(OUTPUT_DIR, "activity.svg")):
    events = fetch_json(f"https://api.github.com/users/{username}/events/public?per_page=100", token) or []
    rows = []
    seen = set()
    for ev in events:
        row = event_row(ev)
        key = (row[0], row[2], row[3])
        if key in seen:
            continue
        seen.add(key)
        rows.append(row)
        if len(rows) >= MAX_ROWS:
            break

    width, height = 660, 250
    row_h = 28
    y_start = 86

    body = ""
    if rows:
        for i, (tag, tag_color, repo, msg, when, repo_url) in enumerate(rows):
            y = y_start + i * row_h
            safe_url = html.escape(repo_url)
            body += f"""
    <a href="{safe_url}" target="_blank" rel="noopener noreferrer">
      <g class="activity-row">
        <text x="24" y="{y}" class="tag" fill="{tag_color}">[{tag}]</text>
        <text x="106" y="{y}" class="repo">{html.escape(repo)}</text>
        <text x="236" y="{y}" class="msg">{html.escape(msg)}</text>
        <text x="636" y="{y}" class="time" text-anchor="end">{when}</text>
      </g>
    </a>"""
    else:
        body = f"""
    <text x="330" y="{y_start + row_h}" text-anchor="middle" class="empty">// NO RECENT PUBLIC SIGNALS //</text>"""

    svg_content = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    a {{
      cursor: pointer;
      text-decoration: none;
    }}
    .activity-row text.repo {{
      transition: fill 0.2s;
    }}
    a:hover .activity-row text.repo {{
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
    .tag {{
      font-family: 'Fira Code', 'Courier New', monospace;
      font-size: 9px;
      font-weight: bold;
      letter-spacing: 1px;
    }}
    .repo {{
      font-family: 'Fira Code', 'Courier New', monospace;
      font-size: 12px;
      fill: #c0caf5;
      font-weight: bold;
    }}
    .msg {{
      font-family: 'Fira Code', 'Courier New', monospace;
      font-size: 10px;
      fill: #7aa2f7;
    }}
    .time {{
      font-family: 'Fira Code', 'Courier New', monospace;
      font-size: 10px;
      fill: #6272a4;
    }}
    .empty {{
      font-family: 'Fira Code', 'Courier New', monospace;
      font-size: 12px;
      fill: #6272a4;
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
    <text x="18" y="16" class="title">LIVE FEED: RECENT ACTIVITY</text>
    <text x="18" y="29" class="subtitle">LAST PUBLIC SIGNALS // GITHUB EVENTS API</text>
  </g>
  <line x1="24" y1="64" x2="{width - 24}" y2="64" stroke="#3d59a1" stroke-opacity="0.6" stroke-width="1" />
  {body}
</svg>
"""
    paths = save_dual_theme_svg(svg_content, filepath)
    return paths


if __name__ == "__main__":
    token = os.environ.get("GITHUB_TOKEN")
    username = os.environ.get("GITHUB_REPOSITORY_OWNER") or DEFAULT_USERNAME
    print(f"Running activity generation for user: {username}")
    generate_activity_svg(username, token)
    print("Activity generation finished successfully!")


