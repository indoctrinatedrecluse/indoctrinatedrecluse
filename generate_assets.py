import os
import sys
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

def get_languages(username, token):
    # 1. Fetch repositories
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
    print(f"Fetching repos for {username}...")
    repos = fetch_json(repos_url, token)
    if not repos:
        print("No repositories found or error occurred.")
        return {}

    lang_bytes = {}
    for repo in repos:
        # Skip forks and archived repos
        if repo.get("fork") or repo.get("archived"):
            continue
        
        repo_name = repo.get("name")
        langs_url = repo.get("languages_url")
        print(f"Fetching languages for {repo_name}...")
        langs = fetch_json(langs_url, token)
        if langs:
            for lang, bytes_count in langs.items():
                lang_bytes[lang] = lang_bytes.get(lang, 0) + bytes_count

    return lang_bytes

def get_neon_colors(lang):
    # Map common languages to premium cyberpunk gradients
    color_map = {
        "Python": ("#38bdf8", "#0284c7"),      # Cyan to Dark Blue
        "JavaScript": ("#fbbf24", "#d97706"),  # Yellow to Amber
        "TypeScript": ("#60a5fa", "#2563eb"),  # Neon Blue to Cobalt
        "HTML": ("#f87171", "#dc2626"),        # Red to Dark Red
        "CSS": ("#c084fc", "#7c3aed"),         # Purple to Violet
        "C++": ("#ec4899", "#db2777"),         # Pink to Dark Pink
        "SQL": ("#22d3ee", "#0891b2"),         # Light Cyan to Teal
        "Shell": ("#4ade80", "#16a34a"),       # Neon Green to Forest Green
        "Go": ("#22d3ee", "#0284c7"),          # Sky Blue
        "Rust": ("#fb923c", "#ea580c"),        # Orange to Red-Orange
    }
    
    if lang in color_map:
        return color_map[lang]
        
    # Generate HSL hash-based neon color for others
    hue = abs(hash(lang)) % 360
    return (f"hsl({hue}, 95%, 65%)", f"hsl({hue}, 95%, 45%)")

def generate_languages_svg(lang_bytes, filepath):
    if not lang_bytes:
        # Fallback empty state
        lang_bytes = {"No Data": 100}

    total_bytes = sum(lang_bytes.values())
    sorted_langs = sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True)
    
    # Calculate dimensions
    row_height = 45
    header_height = 80
    footer_height = 20
    width = 600
    height = header_height + (len(sorted_langs) * row_height) + footer_height

    # Generate gradients and rows
    gradients = ""
    rows = ""
    
    for idx, (lang, bytes_count) in enumerate(sorted_langs):
        percentage = (bytes_count / total_bytes) * 100
        color_light, color_dark = get_neon_colors(lang)
        lang_id = lang.replace(" ", "_").replace("#", "sharp").replace("+", "plus")
        
        # Linear Gradient SVG
        gradients += f"""
    <linearGradient id="grad_{lang_id}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{color_light}" />
      <stop offset="100%" stop-color="{color_dark}" />
    </linearGradient>"""

        # Row Layout
        y_pos = header_height + (idx * row_height)
        fill_width = int(450 * (percentage / 100))
        
        rows += f"""
    <!-- Row {idx}: {lang} -->
    <g transform="translate(30, {y_pos})">
      <text x="0" y="12" fill="#e2e8f0" font-family="'Fira Code', 'Courier New', monospace" font-size="14" font-weight="bold">{lang}</text>
      <text x="540" y="12" fill="{color_light}" font-family="'Fira Code', 'Courier New', monospace" font-size="14" font-weight="bold" text-anchor="end">{percentage:.1f}%</text>
      <rect x="0" y="22" width="540" height="8" fill="#1e1e2e" rx="4" />
      <rect x="0" y="22" width="{fill_width}" height="8" fill="url(#grad_{lang_id})" rx="4" filter="url(#glow)" />
    </g>"""

    svg_content = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .title {{
      font-family: 'Fira Code', 'Courier New', monospace;
      font-size: 18px;
      font-weight: bold;
      fill: #ff79c6;
    }}
    .subtitle {{
      font-family: 'Fira Code', 'Courier New', monospace;
      font-size: 10px;
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
  
  <defs>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    {gradients}
  </defs>

  <!-- Background Panel -->
  <rect width="{width}" height="{height}" class="bg" />

  <!-- Header Section -->
  <g transform="translate(30, 35)">
    <rect x="0" y="0" width="6" height="24" fill="#38bdf8" rx="2" filter="url(#glow)" />
    <text x="18" y="18" class="title">SYSTEM CORE: LANGUAGE MATRIX</text>
    <text x="18" y="32" class="subtitle">ALL REGISTERED COGNITIVE LANGUAGES IN NON-FORK REPOS</text>
  </g>

  <!-- Language Rows -->
  {rows}
</svg>
"""

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated language matrix SVG at {filepath}")

def generate_glowing_line(filepath):
    svg_content = """<svg width="800" height="8" viewBox="0 0 800 8" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="cyberGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="50%" stop-color="#ff79c6" />
      <stop offset="100%" stop-color="#bb9af3" />
    </linearGradient>
    <filter id="lineGlow" x="-10%" y="-100%" width="120%" height="300%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>
  <rect x="10" y="2" width="780" height="4" rx="2" fill="url(#cyberGradient)" filter="url(#lineGlow)" />
</svg>
"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated glowing line divider SVG at {filepath}")

if __name__ == "__main__":
    token = os.environ.get("GITHUB_TOKEN")
    username = os.environ.get("GITHUB_REPOSITORY_OWNER")
    
    if not username:
        username = DEFAULT_USERNAME
        print(f"Using default username: {username}")
        
    print(f"Running assets generation for user: {username}")
    
    lang_bytes = get_languages(username, token)
    
    # Write output to the profile-3d-contrib directory
    languages_path = os.path.join(OUTPUT_DIR, "languages.svg")
    glowing_line_path = os.path.join(OUTPUT_DIR, "glowing-line.svg")
    
    generate_languages_svg(lang_bytes, languages_path)
    generate_glowing_line(glowing_line_path)
    print("Assets generation finished successfully!")
