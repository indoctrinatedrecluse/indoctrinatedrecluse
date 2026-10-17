"""Cyberpunk Dual-Theme Anime Avatar + Interactive Terminal Banner Generator.

Creates custom banners featuring:
- Unified full banner (banner-dark.svg, banner-light.svg, banner.svg)
- Modular interactive clickable cards for GitHub README:
  1. Avatar Card (banner-avatar-dark.svg / light): Anime portrait with cyber scanline
     linking to live portfolio website.
  2. Identity Card (banner-tile-identity-dark.svg / light): Terminal bio & alias
     linking directly to GitHub profile.
  3. College Card (banner-tile-college-dark.svg / light): USC Degree & credential details
     linking directly to official degree credential on LinkedIn.
  4. Portfolio Card (banner-tile-portfolio-dark.svg / light): Live interactive portfolio
     deck linking directly to Flutter portfolio.
- Automated dynamic README injection between BANNER_TILES_START and BANNER_TILES_END.
"""

import os
import base64
from cyber_palette import update_readme_section

OUTPUT_BASE = "banner.svg"
AVATAR_DARK = os.path.join("refs", "avatar_dark_opt.jpg")
AVATAR_LIGHT = os.path.join("refs", "avatar_light_opt.jpg")

PORTFOLIO_URL = "https://portfolio-flutter-78bcf.web.app/"
DEGREE_CREDENTIAL_URL = (
    "https://media.licdn.com/dms/image/v2/D4D2DAQFsywd5sLJt7w/"
    "profile-treasury-document-cover-images_800/B4DaFJCWhgJ8A8-/0/"
    "1792226717161?e=1792832400&amp;v=beta&amp;t=_-g4akjeL9-jbv3YNtT42UijJLaUaHW9xrQpacOz3-Q"
)
GITHUB_URL = "https://github.com/indoctrinatedrecluse"


def encode_image_base64(path):
    if not os.path.exists(path):
        alt_path = path.replace("_opt.jpg", ".jpg")
        if os.path.exists(alt_path):
            path = alt_path
        else:
            raise FileNotFoundError(f"Avatar image not found at {path}")
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_theme_colors(is_light):
    return {
        "canvas_bg": "#f8fafc" if is_light else "#0b0e14",
        "frame_stop0": "#0284c7" if is_light else "#38bdf8",
        "frame_stop45": "#c0267f" if is_light else "#ff79c6",
        "frame_stop100": "#7c3aed" if is_light else "#bb9af3",
        "scan_opacity": "0.45" if is_light else "0.75",
        "inner_stroke": "#0284c7" if is_light else "#ffffff",
        "inner_stroke_op": "0.20" if is_light else "0.18",
        "term_bg": "#ffffff" if is_light else "#0d111a",
        "term_stroke": "#0284c7" if is_light else "#38bdf8",
        "header_bg": "#0284c7" if is_light else "#38bdf8",
        "header_text_color": "#ffffff" if is_light else "#0b0e14",
        "tag_bg": "#f1f5f9" if is_light else "#16161e",
        "dot_red": "#ef4444" if is_light else "#ff5f56",
        "dot_yellow": "#f59e0b" if is_light else "#ffbd2e",
        "dot_green": "#10b981" if is_light else "#27c93f",
        "label_color": "#334155" if is_light else "#c0caf5",
        "name_color": "#be185d" if is_light else "#ff79c6",
        "alias_color": "#6d28d9" if is_light else "#bb9af3",
        "degree_color": "#0369a1" if is_light else "#38bdf8",
        "dev_color": "#15803d" if is_light else "#4ade80",
        "college_color": "#b45309" if is_light else "#facc15",
        "portfolio_color": "#0284c7" if is_light else "#38bdf8",
        "cursor_color": "#0284c7" if is_light else "#38bdf8",
        "hud_badge_bg": "#f1f5f9" if is_light else "#16161e",
        "hud_badge_stroke": "#0284c7" if is_light else "#38bdf8",
        "hud_text": "#0369a1" if is_light else "#38bdf8",
    }


def build_banner_svg(theme="dark"):
    is_light = theme == "light"
    avatar_path = AVATAR_LIGHT if is_light else AVATAR_DARK
    avatar_b64 = encode_image_base64(avatar_path)
    c = get_theme_colors(is_light)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 360" width="1000" height="360">
  <defs>
    <clipPath id="frameClip"><rect x="10" y="10" width="980" height="340" rx="20" /></clipPath>
    <clipPath id="avatarClip"><rect x="18" y="18" width="290" height="324" rx="16" /></clipPath>
    <linearGradient id="neonFrame" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{c['frame_stop0']}" />
      <stop offset="45%" stop-color="{c['frame_stop45']}" />
      <stop offset="100%" stop-color="{c['frame_stop100']}" />
    </linearGradient>
    <linearGradient id="scanlineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{c['frame_stop0']}" stop-opacity="0" />
      <stop offset="25%" stop-color="{c['frame_stop0']}" stop-opacity="0.8" />
      <stop offset="50%" stop-color="{c['frame_stop45']}" stop-opacity="1" />
      <stop offset="75%" stop-color="{c['frame_stop100']}" stop-opacity="0.8" />
      <stop offset="100%" stop-color="{c['frame_stop100']}" stop-opacity="0" />
    </linearGradient>
    <filter id="frameGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <style>
    .term-text {{
      font-family: 'Fira Code', 'Courier New', monospace;
      font-size: 13.5px;
      font-weight: bold;
    }}
    .term-link {{
      text-decoration: none;
      cursor: pointer;
    }}
    .term-link:hover text {{
      text-decoration: underline;
      filter: brightness(1.2);
    }}
  </style>

  <rect x="0" y="0" width="1000" height="360" rx="24" fill="{c['canvas_bg']}" />

  <g clip-path="url(#frameClip)">
    <g clip-path="url(#avatarClip)">
      <image href="data:image/jpeg;base64,{avatar_b64}" x="18" y="18" width="290" height="324" preserveAspectRatio="xMidYMid slice" />
    </g>
    <rect x="18" y="18" width="290" height="324" rx="16" fill="none" stroke="url(#neonFrame)" stroke-width="2.5" filter="url(#frameGlow)" />
    <rect x="18" y="18" width="290" height="324" rx="16" fill="none" stroke="#ffffff" stroke-opacity="0.25" stroke-width="1" />

    <g transform="translate(324, 18)">
      <rect x="0" y="0" width="658" height="324" rx="16" fill="{c['term_bg']}" stroke="{c['term_stroke']}" stroke-width="2.5" />
      <path d="M 0,16 A 16,16 0 0,1 16,0 L 642,0 A 16,16 0 0,1 658,16 L 658,38 L 0,38 Z" fill="{c['header_bg']}" />
      <text x="18" y="25" font-family="'Fira Code', monospace" font-size="14" font-weight="bold" fill="{c['header_text_color']}" letter-spacing="0.5">root@indoctrinatedrecluse:~</text>
      
      <circle cx="590" cy="19" r="6" fill="{c['dot_red']}" />
      <circle cx="612" cy="19" r="6" fill="{c['dot_yellow']}" />
      <circle cx="634" cy="19" r="6" fill="{c['dot_green']}" />

      <g class="term-text">
        <g transform="translate(24, 76)">
          <text x="0" y="0" fill="{c['label_color']}">&gt; Name:</text>
          <text x="96" y="0" fill="{c['name_color']}">Abhishek Mitra</text>
        </g>
        
        <g transform="translate(24, 112)">
          <text x="0" y="0" fill="{c['label_color']}">&gt; Alias:</text>
          <a href="{GITHUB_URL}" target="_blank" rel="noopener noreferrer" class="term-link">
            <text x="96" y="0" fill="{c['alias_color']}">indoctrinatedrecluse &#x2197;</text>
          </a>
        </g>
        
        <g transform="translate(24, 148)">
          <text x="0" y="0" fill="{c['label_color']}">&gt; Degree:</text>
          <text x="100" y="0" fill="{c['degree_color']}">MSCS</text>
        </g>
        
        <g transform="translate(24, 184)">
          <text x="0" y="0" fill="{c['label_color']}">&gt; Development:</text>
          <text x="156" y="0" fill="{c['dev_color']}">Full Stack</text>
        </g>
        
        <g transform="translate(24, 220)">
          <text x="0" y="0" fill="{c['label_color']}">&gt; College:</text>
          <a href="{DEGREE_CREDENTIAL_URL}" target="_blank" rel="noopener noreferrer" class="term-link">
            <text x="110" y="0" fill="{c['college_color']}">University of Southern California &#x2197;</text>
          </a>
        </g>

        <g transform="translate(24, 256)">
          <text x="0" y="0" fill="{c['label_color']}">&gt; Portfolio:</text>
          <a href="{PORTFOLIO_URL}" target="_blank" rel="noopener noreferrer" class="term-link">
            <text x="126" y="0" fill="{c['portfolio_color']}">Click here for portfolio &#x2197;</text>
          </a>
        </g>

        <g transform="translate(24, 290)">
          <text x="0" y="0" fill="{c['label_color']}">&gt;</text>
          <rect x="18" y="-13" width="10" height="17" fill="{c['cursor_color']}" rx="2">
            <animate attributeName="opacity" values="1;0.1;1" dur="1s" repeatCount="indefinite" />
          </rect>
        </g>
      </g>
    </g>

    <rect x="10" y="10" width="980" height="2" fill="url(#scanlineGrad)" opacity="{c['scan_opacity']}" filter="url(#frameGlow)">
      <animate attributeName="y" values="10;346;10" dur="7s" repeatCount="indefinite" />
    </rect>
  </g>

  <rect x="10" y="10" width="980" height="340" rx="20" fill="none" stroke="url(#neonFrame)" stroke-width="3.5" filter="url(#frameGlow)" />
  <rect x="10" y="10" width="980" height="340" rx="20" fill="none" stroke="{c['inner_stroke']}" stroke-opacity="{c['inner_stroke_op']}" stroke-width="1" />
</svg>
"""


def build_avatar_card_svg(theme="dark"):
    is_light = theme == "light"
    avatar_path = AVATAR_LIGHT if is_light else AVATAR_DARK
    avatar_b64 = encode_image_base64(avatar_path)
    c = get_theme_colors(is_light)

    w, h = 310, 326
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <clipPath id="avatarClip"><rect x="10" y="10" width="{w - 20}" height="{h - 20}" rx="14" /></clipPath>
    <linearGradient id="avatarFrame" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{c['frame_stop0']}" />
      <stop offset="45%" stop-color="{c['frame_stop45']}" />
      <stop offset="100%" stop-color="{c['frame_stop100']}" />
    </linearGradient>
    <linearGradient id="scanlineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{c['frame_stop0']}" stop-opacity="0" />
      <stop offset="50%" stop-color="{c['frame_stop45']}" stop-opacity="0.9" />
      <stop offset="100%" stop-color="{c['frame_stop100']}" stop-opacity="0" />
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="{w}" height="{h}" rx="18" fill="{c['canvas_bg']}" />

  <g clip-path="url(#avatarClip)">
    <image href="data:image/jpeg;base64,{avatar_b64}" x="10" y="10" width="{w - 20}" height="{h - 20}" preserveAspectRatio="xMidYMid slice" />
    <rect x="10" y="10" width="{w - 20}" height="2.5" fill="url(#scanlineGrad)" opacity="{c['scan_opacity']}" filter="url(#glow)">
      <animate attributeName="y" values="10;{h - 12};10" dur="6s" repeatCount="indefinite" />
    </rect>
  </g>

  <!-- High-tech HUD Brackets -->
  <path d="M 12,32 L 12,14 Q 12,12 14,12 L 32,12" fill="none" stroke="{c['frame_stop0']}" stroke-width="2.5" />
  <path d="M {w - 12},32 L {w - 12},14 Q {w - 12},12 {w - 14},12 L {w - 32},12" fill="none" stroke="{c['frame_stop45']}" stroke-width="2.5" />
  <path d="M 12,{h - 32} L 12,{h - 14} Q 12,{h - 12} 14,{h - 12} L 32,{h - 12}" fill="none" stroke="{c['frame_stop45']}" stroke-width="2.5" />
  <path d="M {w - 12},{h - 32} L {w - 12},{h - 14} Q {w - 12},{h - 12} {w - 14},{h - 12} L {w - 32},{h - 12}" fill="none" stroke="{c['frame_stop0']}" stroke-width="2.5" />

  <!-- Outer Neon Glowing Frame -->
  <rect x="10" y="10" width="{w - 20}" height="{h - 20}" rx="14" fill="none" stroke="url(#avatarFrame)" stroke-width="2.5" filter="url(#glow)" />

  <!-- Bottom HUD Status Overlay -->
  <g transform="translate(18, {h - 42})">
    <rect x="0" y="0" width="{w - 36}" height="24" rx="6" fill="{c['hud_badge_bg']}" fill-opacity="0.9" stroke="{c['hud_badge_stroke']}" stroke-width="1" />
    <circle cx="14" cy="12" r="3.5" fill="{c['dot_green']}">
      <animate attributeName="opacity" values="1;0.3;1" dur="1.8s" repeatCount="indefinite" />
    </circle>
    <text x="25" y="16" font-family="'Fira Code', monospace" font-size="8.5" font-weight="bold" fill="{c['hud_text']}" letter-spacing="0.5">SYSTEM // AURA LINK ACTIVE</text>
  </g>
</svg>
"""


def build_identity_card_svg(theme="dark"):
    is_light = theme == "light"
    c = get_theme_colors(is_light)
    w, h = 650, 102

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <filter id="termGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="{c['frame_stop0']}" flood-opacity="0.15" />
    </filter>
  </defs>

  <style>
    .mono {{
      font-family: 'Fira Code', 'Courier New', monospace;
    }}
  </style>

  <!-- Card Background -->
  <rect x="2" y="2" width="{w - 4}" height="{h - 4}" rx="12" fill="{c['term_bg']}" stroke="{c['term_stroke']}" stroke-width="2" filter="url(#termGlow)" />

  <!-- Window Header Bar -->
  <path d="M 2,14 A 12,12 0 0,1 14,2 L {w - 14},2 A 12,12 0 0,1 {w - 2},14 L {w - 2},26 L 2,26 Z" fill="{c['header_bg']}" />
  <text x="14" y="18" class="mono" font-size="11" font-weight="bold" fill="{c['header_text_color']}">root@indoctrinatedrecluse:~ (identity.protocol)</text>
  
  <circle cx="{w - 48}" cy="14" r="4.5" fill="{c['dot_red']}" />
  <circle cx="{w - 32}" cy="14" r="4.5" fill="{c['dot_yellow']}" />
  <circle cx="{w - 16}" cy="14" r="4.5" fill="{c['dot_green']}" />

  <!-- Top-Right Action Badge -->
  <g transform="translate({w - 150}, 34)">
    <rect x="0" y="0" width="136" height="20" rx="4" fill="{c['tag_bg']}" stroke="{c['alias_color']}" stroke-width="1" />
    <text x="68" y="14" text-anchor="middle" class="mono" font-size="8.5" font-weight="bold" fill="{c['alias_color']}">GITHUB PROFILE &#x2197;</text>
  </g>

  <!-- Body Content -->
  <g class="mono" font-size="12" font-weight="bold">
    <g transform="translate(18, 50)">
      <text x="0" y="0" fill="{c['label_color']}">&gt; Name:</text>
      <text x="96" y="0" fill="{c['name_color']}">Abhishek Mitra</text>
    </g>
    <g transform="translate(18, 71)">
      <text x="0" y="0" fill="{c['label_color']}">&gt; Alias:</text>
      <text x="96" y="0" fill="{c['alias_color']}">@indoctrinatedrecluse &#x2197;</text>
    </g>
    <g transform="translate(18, 92)">
      <text x="0" y="0" fill="{c['label_color']}">&gt; Role :</text>
      <text x="96" y="0" fill="{c['dev_color']}">Full Stack Developer // Software Engineering</text>
    </g>
  </g>
</svg>
"""


def build_college_card_svg(theme="dark"):
    is_light = theme == "light"
    c = get_theme_colors(is_light)
    w, h = 650, 102

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <filter id="termGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="{c['college_color']}" flood-opacity="0.15" />
    </filter>
  </defs>

  <style>
    .mono {{
      font-family: 'Fira Code', 'Courier New', monospace;
    }}
  </style>

  <!-- Card Background -->
  <rect x="2" y="2" width="{w - 4}" height="{h - 4}" rx="12" fill="{c['term_bg']}" stroke="{c['college_color']}" stroke-width="2" filter="url(#termGlow)" />

  <!-- Left Accent Bar -->
  <rect x="2" y="14" width="4" height="74" rx="2" fill="{c['college_color']}" />

  <!-- Top-Right Action Badge -->
  <g transform="translate({w - 176}, 14)">
    <rect x="0" y="0" width="162" height="20" rx="4" fill="{c['tag_bg']}" stroke="{c['college_color']}" stroke-width="1" />
    <text x="81" y="14" text-anchor="middle" class="mono" font-size="8.5" font-weight="bold" fill="{c['college_color']}">&#x2605; USC CREDENTIAL &#x2197;</text>
  </g>

  <!-- Body Content -->
  <g class="mono">
    <g transform="translate(18, 35)">
      <text x="0" y="0" font-size="12" font-weight="bold" fill="{c['label_color']}">&gt; Degree :</text>
      <text x="96" y="0" font-size="12" font-weight="bold" fill="{c['degree_color']}">MS in Computer Science (MSCS)</text>
    </g>
    <g transform="translate(18, 62)">
      <text x="0" y="0" font-size="12" font-weight="bold" fill="{c['label_color']}">&gt; College:</text>
      <text x="96" y="0" font-size="13.5" font-weight="bold" fill="{c['college_color']}">University of Southern California &#x2197;</text>
    </g>
    <g transform="translate(18, 88)">
      <text x="0" y="0" font-size="11" font-weight="bold" fill="{c['label_color']}">&gt; Status :</text>
      <text x="96" y="0" font-size="11" font-weight="bold" fill="{c['dev_color']}">Official Degree Credential Conferred // Verified &#x2197;</text>
    </g>
  </g>
</svg>
"""


def build_portfolio_card_svg(theme="dark"):
    is_light = theme == "light"
    c = get_theme_colors(is_light)
    w, h = 650, 102

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <filter id="termGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="{c['portfolio_color']}" flood-opacity="0.18" />
    </filter>
  </defs>

  <style>
    .mono {{
      font-family: 'Fira Code', 'Courier New', monospace;
    }}
  </style>

  <!-- Card Background -->
  <rect x="2" y="2" width="{w - 4}" height="{h - 4}" rx="12" fill="{c['term_bg']}" stroke="{c['portfolio_color']}" stroke-width="2" filter="url(#termGlow)" />

  <!-- Left Accent Bar -->
  <rect x="2" y="14" width="4" height="74" rx="2" fill="{c['portfolio_color']}" />

  <!-- Top-Right Action Badge -->
  <g transform="translate({w - 156}, 14)">
    <rect x="0" y="0" width="142" height="20" rx="4" fill="{c['tag_bg']}" stroke="{c['portfolio_color']}" stroke-width="1" />
    <text x="71" y="14" text-anchor="middle" class="mono" font-size="8.5" font-weight="bold" fill="{c['portfolio_color']}">&#x26A1; LIVE PORTFOLIO &#x2197;</text>
  </g>

  <!-- Body Content -->
  <g class="mono">
    <g transform="translate(18, 35)">
      <text x="0" y="0" font-size="12" font-weight="bold" fill="{c['label_color']}">&gt; Portfolio:</text>
      <text x="110" y="0" font-size="12" font-weight="bold" fill="{c['portfolio_color']}">https://portfolio-flutter-78bcf.web.app/ &#x2197;</text>
    </g>
    <g transform="translate(18, 62)">
      <text x="0" y="0" font-size="11.5" font-weight="bold" fill="{c['label_color']}">&gt; UI Stack :</text>
      <text x="110" y="0" font-size="11.5" font-weight="bold" fill="{c['alias_color']}">Flutter Web UI // Interactive Cyber Deck</text>
    </g>
    <g transform="translate(18, 88)">
      <text x="0" y="0" font-size="11.5" font-weight="bold" fill="{c['label_color']}">&gt; Protocol :</text>
      <text x="110" y="0" font-size="11.5" font-weight="bold" fill="{c['dev_color']}">[CLICK HERE TO LAUNCH PORTFOLIO] &#x2197;</text>
      <rect x="424" y="-10" width="8" height="13" rx="1.5" fill="{c['cursor_color']}">
        <animate attributeName="opacity" values="1;0.1;1" dur="1s" repeatCount="indefinite" />
      </rect>
    </g>
  </g>
</svg>
"""


def build_banner_readme_table():
    return f"""<table border="0" width="100%" cellpadding="0" cellspacing="0">
  <tr>
    <td width="33%" rowspan="3" align="center" valign="middle">
      <a href="{PORTFOLIO_URL}" target="_blank" rel="noopener noreferrer">
        <picture>
          <source media="(prefers-color-scheme: dark)" srcset="./banner-avatar-dark.svg" />
          <source media="(prefers-color-scheme: light)" srcset="./banner-avatar-light.svg" />
          <img src="./banner-avatar-dark.svg" width="100%" alt="Abhishek Mitra Avatar" />
        </picture>
      </a>
    </td>
    <td width="67%" align="center">
      <a href="{GITHUB_URL}" target="_blank" rel="noopener noreferrer">
        <picture>
          <source media="(prefers-color-scheme: dark)" srcset="./banner-tile-identity-dark.svg" />
          <source media="(prefers-color-scheme: light)" srcset="./banner-tile-identity-light.svg" />
          <img src="./banner-tile-identity-dark.svg" width="100%" alt="GitHub Profile: @indoctrinatedrecluse" />
        </picture>
      </a>
    </td>
  </tr>
  <tr>
    <td width="67%" align="center">
      <a href="{DEGREE_CREDENTIAL_URL}" target="_blank" rel="noopener noreferrer">
        <picture>
          <source media="(prefers-color-scheme: dark)" srcset="./banner-tile-college-dark.svg" />
          <source media="(prefers-color-scheme: light)" srcset="./banner-tile-college-light.svg" />
          <img src="./banner-tile-college-dark.svg" width="100%" alt="USC Degree Credential: University of Southern California" />
        </picture>
      </a>
    </td>
  </tr>
  <tr>
    <td width="67%" align="center">
      <a href="{PORTFOLIO_URL}" target="_blank" rel="noopener noreferrer">
        <picture>
          <source media="(prefers-color-scheme: dark)" srcset="./banner-tile-portfolio-dark.svg" />
          <source media="(prefers-color-scheme: light)" srcset="./banner-tile-portfolio-light.svg" />
          <img src="./banner-tile-portfolio-dark.svg" width="100%" alt="Live Portfolio Website: Click here for portfolio" />
        </picture>
      </a>
    </td>
  </tr>
</table>"""


def update_readme_banner(readme_path="README.md"):
    table_html = build_banner_readme_table()
    return update_readme_section("<!-- BANNER_TILES_START -->", "<!-- BANNER_TILES_END -->", table_html, readme_path)


def generate_banner(output=OUTPUT_BASE):
    dirname, basename = os.path.split(output)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    name, ext = os.path.splitext(basename)

    # 1. Unified Full Banner (Dark, Light, Base)
    dark_path = os.path.join(dirname, f"{name}-dark{ext}") if dirname else f"{name}-dark{ext}"
    light_path = os.path.join(dirname, f"{name}-light{ext}") if dirname else f"{name}-light{ext}"
    base_path = output

    dark_svg = build_banner_svg(theme="dark")
    light_svg = build_banner_svg(theme="light")

    with open(dark_path, "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open(light_path, "w", encoding="utf-8") as f:
        f.write(light_svg)
    with open(base_path, "w", encoding="utf-8") as f:
        f.write(dark_svg)

    # 2. Modular Interactive Tiles (Avatar, Identity, College, Portfolio)
    tiles = [
        ("banner-avatar", build_avatar_card_svg),
        ("banner-tile-identity", build_identity_card_svg),
        ("banner-tile-college", build_college_card_svg),
        ("banner-tile-portfolio", build_portfolio_card_svg),
    ]

    for prefix, builder in tiles:
        d_svg = builder(theme="dark")
        l_svg = builder(theme="light")
        d_file = os.path.join(dirname, f"{prefix}-dark.svg") if dirname else f"{prefix}-dark.svg"
        l_file = os.path.join(dirname, f"{prefix}-light.svg") if dirname else f"{prefix}-light.svg"
        b_file = os.path.join(dirname, f"{prefix}.svg") if dirname else f"{prefix}.svg"
        with open(d_file, "w", encoding="utf-8") as f:
            f.write(d_svg)
        with open(l_file, "w", encoding="utf-8") as f:
            f.write(l_svg)
        with open(b_file, "w", encoding="utf-8") as f:
            f.write(d_svg)

    # 3. Dynamic README Injection
    update_readme_banner()

    print(f"Generated dual-theme interactive banner SVGs and updated README.")
    return {"dark": dark_path, "light": light_path, "base": base_path}


if __name__ == "__main__":
    generate_banner()
