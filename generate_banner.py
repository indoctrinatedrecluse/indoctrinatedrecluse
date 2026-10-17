"""Cyberpunk Dual-Theme Anime Avatar + Interactive Terminal Banner Generator.

Creates custom banners featuring:
- Left: AI-stylized anime/digital art portrait matching the user's likeness
  (Moody cyberpunk hoodie for dark mode, sunny day on the water with sunglasses for light mode).
- Right: Interactive terminal card with clickable links to GitHub, degree credential at USC,
  and live portfolio website.
- Dynamic scanline sweep and glowing neon cyberpunk borders.
"""

import os
import base64

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
        # Fallback to non-optimized path if needed
        alt_path = path.replace("_opt.jpg", ".jpg")
        if os.path.exists(alt_path):
            path = alt_path
        else:
            raise FileNotFoundError(f"Avatar image not found at {path}")
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def build_banner_svg(theme="dark"):
    is_light = theme == "light"

    # Load appropriate avatar image
    avatar_path = AVATAR_LIGHT if is_light else AVATAR_DARK
    avatar_b64 = encode_image_base64(avatar_path)

    # Theme palette parameters
    canvas_bg = "#f8fafc" if is_light else "#0b0e14"
    frame_stop0 = "#0284c7" if is_light else "#38bdf8"
    frame_stop45 = "#c0267f" if is_light else "#ff79c6"
    frame_stop100 = "#7c3aed" if is_light else "#bb9af3"
    scan_opacity = "0.45" if is_light else "0.75"
    inner_stroke = "#0284c7" if is_light else "#ffffff"
    inner_stroke_op = "0.20" if is_light else "0.18"

    # Terminal card styling
    term_bg = "#ffffff" if is_light else "#0d111a"
    term_stroke = "#0284c7" if is_light else "#38bdf8"
    header_bg = "#0284c7" if is_light else "#38bdf8"
    header_text_color = "#ffffff" if is_light else "#0b0e14"
    term_glow = "termGlowLight" if is_light else "termGlowDark"

    # Control dots
    dot_red = "#ef4444" if is_light else "#ff5f56"
    dot_yellow = "#f59e0b" if is_light else "#ffbd2e"
    dot_green = "#10b981" if is_light else "#27c93f"

    # Typography colors
    label_color = "#1e293b" if is_light else "#c0caf5"
    name_color = "#be185d" if is_light else "#ff79c6"
    alias_color = "#6d28d9" if is_light else "#bb9af3"
    degree_color = "#0369a1" if is_light else "#38bdf8"
    dev_color = "#15803d" if is_light else "#4ade80"
    college_color = "#b45309" if is_light else "#facc15"
    portfolio_color = "#0284c7" if is_light else "#38bdf8"
    cursor_color = "#0284c7" if is_light else "#38bdf8"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 360" width="1000" height="360">
  <defs>
    <!-- Outer Frame Clip -->
    <clipPath id="frameClip"><rect x="10" y="10" width="980" height="340" rx="20" /></clipPath>

    <!-- Avatar Left Frame Clip -->
    <clipPath id="avatarClip"><rect x="18" y="18" width="290" height="324" rx="16" /></clipPath>

    <!-- Glowing Frame Gradient -->
    <linearGradient id="neonFrame" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{frame_stop0}" />
      <stop offset="45%" stop-color="{frame_stop45}" />
      <stop offset="100%" stop-color="{frame_stop100}" />
    </linearGradient>

    <!-- Scanline Gradient -->
    <linearGradient id="scanlineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{frame_stop0}" stop-opacity="0" />
      <stop offset="25%" stop-color="{frame_stop0}" stop-opacity="0.8" />
      <stop offset="50%" stop-color="{frame_stop45}" stop-opacity="1" />
      <stop offset="75%" stop-color="{frame_stop100}" stop-opacity="0.8" />
      <stop offset="100%" stop-color="{frame_stop100}" stop-opacity="0" />
    </linearGradient>

    <!-- Avatar Inner Rim Gradient -->
    <linearGradient id="avatarBorder" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{frame_stop0}" />
      <stop offset="50%" stop-color="{frame_stop45}" />
      <stop offset="100%" stop-color="{frame_stop100}" />
    </linearGradient>

    <!-- Glow Filters -->
    <filter id="frameGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    <filter id="termGlowDark" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#38bdf8" flood-opacity="0.18" />
    </filter>
    <filter id="termGlowLight" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0284c7" flood-opacity="0.12" />
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

  <!-- Canvas Background -->
  <rect x="0" y="0" width="1000" height="360" rx="24" fill="{canvas_bg}" />

  <!-- Inner Clipped Content -->
  <g clip-path="url(#frameClip)">
    <!-- LEFT SIDE: Anime Avatar Portrait -->
    <g clip-path="url(#avatarClip)">
      <image href="data:image/jpeg;base64,{avatar_b64}" x="18" y="18" width="290" height="324" preserveAspectRatio="xMidYMid slice" />
    </g>
    <!-- Avatar Glowing Inner Border -->
    <rect x="18" y="18" width="290" height="324" rx="16" fill="none" stroke="url(#avatarBorder)" stroke-width="2.5" filter="url(#frameGlow)" />
    <rect x="18" y="18" width="290" height="324" rx="16" fill="none" stroke="#ffffff" stroke-opacity="0.25" stroke-width="1" />

    <!-- RIGHT SIDE: Interactive Terminal Window -->
    <g transform="translate(324, 18)">
      <!-- Terminal Outer Frame -->
      <rect x="0" y="0" width="658" height="324" rx="16" fill="{term_bg}" stroke="{term_stroke}" stroke-width="2.5" filter="url(#{term_glow})" />
      
      <!-- Window Title Bar -->
      <path d="M 0,16 A 16,16 0 0,1 16,0 L 642,0 A 16,16 0 0,1 658,16 L 658,38 L 0,38 Z" fill="{header_bg}" />
      
      <!-- Title Bar Text -->
      <text x="18" y="25" font-family="'Fira Code', 'Courier New', monospace" font-size="14" font-weight="bold" fill="{header_text_color}" letter-spacing="0.5">root@indoctrinatedrecluse:~</text>
      
      <!-- Window Control Buttons (Top Right) -->
      <circle cx="590" cy="19" r="6" fill="{dot_red}" />
      <circle cx="612" cy="19" r="6" fill="{dot_yellow}" />
      <circle cx="634" cy="19" r="6" fill="{dot_green}" />

      <!-- Terminal Body Content -->
      <g class="term-text">
        <!-- Line 1: Name -->
        <g transform="translate(24, 76)">
          <text x="0" y="0" fill="{label_color}">&gt; Name:</text>
          <text x="96" y="0" fill="{name_color}">Abhishek Mitra</text>
        </g>
        
        <!-- Line 2: Alias -->
        <g transform="translate(24, 112)">
          <text x="0" y="0" fill="{label_color}">&gt; Alias:</text>
          <a href="{GITHUB_URL}" target="_blank" rel="noopener noreferrer" class="term-link">
            <text x="96" y="0" fill="{alias_color}">indoctrinatedrecluse</text>
          </a>
        </g>
        
        <!-- Line 3: Degree -->
        <g transform="translate(24, 148)">
          <text x="0" y="0" fill="{label_color}">&gt; Degree:</text>
          <text x="100" y="0" fill="{degree_color}">MSCS</text>
        </g>
        
        <!-- Line 4: Development -->
        <g transform="translate(24, 184)">
          <text x="0" y="0" fill="{label_color}">&gt; Development:</text>
          <text x="156" y="0" fill="{dev_color}">Full Stack</text>
        </g>
        
        <!-- Line 5: College / University with degree credential link -->
        <g transform="translate(24, 220)">
          <text x="0" y="0" fill="{label_color}">&gt; College:</text>
          <a href="{DEGREE_CREDENTIAL_URL}" target="_blank" rel="noopener noreferrer" class="term-link">
            <text x="110" y="0" fill="{college_color}">University of Southern California &#x2197;</text>
          </a>
        </g>

        <!-- Line 6: Portfolio Website Link -->
        <g transform="translate(24, 256)">
          <text x="0" y="0" fill="{label_color}">&gt; Portfolio:</text>
          <a href="{PORTFOLIO_URL}" target="_blank" rel="noopener noreferrer" class="term-link">
            <text x="126" y="0" fill="{portfolio_color}">Click here for portfolio &#x2197;</text>
          </a>
        </g>

        <!-- Line 7: Blinking Terminal Cursor -->
        <g transform="translate(24, 290)">
          <text x="0" y="0" fill="{label_color}">&gt;</text>
          <rect x="18" y="-13" width="10" height="17" fill="{cursor_color}" rx="2">
            <animate attributeName="opacity" values="1;0.1;1" dur="1s" repeatCount="indefinite" />
          </rect>
        </g>
      </g>
    </g>

    <!-- Animated Cyber Scanline -->
    <rect x="10" y="10" width="980" height="2" fill="url(#scanlineGrad)" opacity="{scan_opacity}" filter="url(#frameGlow)">
      <animate attributeName="y" values="10;346;10" dur="7s" repeatCount="indefinite" />
    </rect>
  </g>

  <!-- Glowing Outer Frame -->
  <rect x="10" y="10" width="980" height="340" rx="20" fill="none" stroke="url(#neonFrame)" stroke-width="3.5" filter="url(#frameGlow)" />
  <rect x="10" y="10" width="980" height="340" rx="20" fill="none" stroke="{inner_stroke}" stroke-opacity="{inner_stroke_op}" stroke-width="1" />
</svg>
"""


def generate_banner(output=OUTPUT_BASE):
    dirname, basename = os.path.split(output)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    name, ext = os.path.splitext(basename)

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

    print(f"Generated dual-theme anime avatar banner SVGs for {output}:")
    print(f"  Dark:  {dark_path}")
    print(f"  Light: {light_path}")
    print(f"  Base:  {base_path}")
    return {"dark": dark_path, "light": light_path, "base": base_path}


if __name__ == "__main__":
    generate_banner()
