"""Cyberpunk Dual-Theme Vector Header Banner Generator.

Creates bespoke vector SVGs with:
- Left: Character / ASCII art portrait from user photos (moody dark portrait for dark mode,
  sunny sunglasses boat photo for light mode).
- Right: Interactive terminal card matching the exact cyberpunk / synthwave theme.
- Dynamic scanline animation and glowing neon cyber-frame.
"""

import os
import re

OUTPUT_BASE = "banner.svg"

# ASCII Portraits (30 lines x 53 characters each)
DARK_ASCII = [
    '------------------=%@@@@@@@@#------------------------',
    '-------------+@@@@@####****%@@@=:-------------------',
    '------------+@@@#*+++++++#@@#-----------------------',
    '-----------=#%*++=========#@@#=:--------------------',
    '-----------@%*+++==========*@@%:::::::::::::::::::::',
    '----------%@#+++============*@@#::::::::::::::::::::',
    '---------#*++*%@@====*#%#*=+@#::::::::::::::::::::::',
    '--------+#**%@@@*==#%#***+#*+:::::::::::::::::::::::',
    '-------#=**+#%##===#%***+*+:::::::::::::::::::::::::',
    '-------=***%###=-=*#*==+*:::::::::::::::::::::::::::',
    '-------=**%%**=-=##*==++----------------------------',
    '-------+*##%#*==+##*==++----------------------------',
    '-------*+++==---=+*++==-----------------------------',
    '------++=======++-----------------------------------',
    '------==========+----------------+-:----------------',
    '------==========+----------------+=-:---------------',
    '------=======++------------------=-+:---------------',
    '-------=======*#%#+:-------------+-+:---------------',
    '-------=====*%%@%#+-------------+-+:----------------',
    '-------===-*%%%%*+--------------=-+:----------------',
    '-------++=*%%%%%##=-==:-----------------------------',
    '--------++*+*#%#====++=-----------------------------',
    '---------*++++*##*=====-----------------------------',
    '----------*++++%#=====------------------------------',
    '-----------++++*#+==--------------------------------',
    '------------%#*+**+++=-+----------------------------',
    '------------+@%*++##%%###++=------------------------',
    '-----------+@#++##%%%###++=-------------------------',
    '----------+@@#+##%%%%%###*==------------------------',
    '---------+@@@%*##%%%%%####*==-----------------------',
]

LIGHT_ASCII = [
    '-----------------------------------------------------',
    '-----------------------------------------------------',
    '-----------------------------------------------------',
    '-----------------------------------------------------',
    '-------------=-::::--=--=---=------------------------',
    '-----------:..:--:=*+:..:-:.-..:---------------------',
    '--------...=-+*+::**=:::-:...----.-------------------',
    '-------.-==+*##**#%##*++*+=--::.---------------------',
    '-------====#%%@@%%#%##***##*=::::-.------------------',
    '------=-:=#%####*+------*+=-:...::-------------------',
    '------:.=*###****-::..-**=--:.:::--------------------',
    '..:--*==*#%%###*+==--*###*=-...::=-------------------',
    '-.-=*#####%%%%%%####%@%%@%+=-------------------------',
    '=*++#@#####%%%%##*+=*##%#*++===+===------------------',
    ':=-:+%%*#####***=-=*#*:.:-..--==+=*------------------',
    ':....=****######*-+**+--::.....:==#%################%',
    '.:..:..-.*######****####**+--::--+####%###**********#',
    '--.....-.##******#####*=-::-=====:=******==--:-:.-===',
    '....----.#%#*****######**-:-====**++++++++=--=-:--+=+',
    '-.-------#%##**+++*###**+-:..--:-====-==+*****+*#***+',
    '==------=#%####**+=---:..........::::::::--=+********',
    '%%%%%%%%#######**##*-::....-...:::::::::::-==+*******',
    '%%%%%%########******+--===....:::::::::::--=+***+****',
    '%%%%%%%%###*+++++***+=---..:::::::----------+**+++***',
    '%%###%%%#*+=++++++++*++=-:#*-:::------------=**=+=++*',
    '#%##*#%%#+==++=+++++++++***++=------------==-**++=+=+',
    '##**=#%#+===+++++++++++++++++=-----------===-=**++==+',
    '**++==**+===+++++++++++++++++==-::-------=====***+=+*',
    '+=+++=:-++++++++++++++++++++++==-::------====-+******',
    '+**+++-:-+********++++++++++++++=-:---======+==-=**+*',
]


def render_ascii_spans(lines, bg_color, face_fill):
    """Render ASCII lines into SVG <text> elements with distinct background vs subject coloring."""
    output = []
    y_start = 42
    y_step = 9.8

    for i, line in enumerate(lines):
        y = y_start + (i * y_step)
        # Split line into background characters (- : .) vs subject characters
        parts = re.split(r'([-:.]+)', line)
        line_spans = []
        for p in parts:
            if not p:
                continue
            if all(c in '-:.' for c in p):
                line_spans.append(f'<tspan fill="{bg_color}">{p}</tspan>')
            else:
                line_spans.append(f'<tspan fill="{face_fill}">{p}</tspan>')
        spans_str = "".join(line_spans)
        output.append(f'    <text x="26" y="{y:.1f}">{spans_str}</text>')

    return "\n".join(output)


def build_vector_banner(theme="dark"):
    is_light = theme == "light"

    # Theme parameters
    canvas_bg = "#f8fafc" if is_light else "#0b0e14"
    frame_stop0 = "#0284c7" if is_light else "#38bdf8"
    frame_stop45 = "#c0267f" if is_light else "#ff79c6"
    frame_stop100 = "#7c3aed" if is_light else "#bb9af3"
    scan_opacity = "0.55" if is_light else "0.85"
    inner_stroke = "#0284c7" if is_light else "#ffffff"
    inner_stroke_op = "0.20" if is_light else "0.18"

    # Terminal window parameters
    term_bg = "#ffffff" if is_light else "#0d111a"
    term_stroke = "#0284c7" if is_light else "#38bdf8"
    header_bg = "#0284c7" if is_light else "#38bdf8"
    header_text_color = "#ffffff" if is_light else "#0b0e14"
    term_glow = "termGlowLight" if is_light else "termGlowDark"

    # Window control dots
    dot_red = "#ef4444" if is_light else "#ff5f56"
    dot_yellow = "#f59e0b" if is_light else "#ffbd2e"
    dot_green = "#10b981" if is_light else "#27c93f"

    # Terminal details typography
    label_color = "#1e293b" if is_light else "#c0caf5"
    name_color = "#be185d" if is_light else "#ff79c6"
    alias_color = "#6d28d9" if is_light else "#bb9af3"
    degree_color = "#0369a1" if is_light else "#38bdf8"
    dev_color = "#15803d" if is_light else "#4ade80"
    univ_color = "#b45309" if is_light else "#facc15"
    cursor_color = "#0284c7" if is_light else "#38bdf8"

    # ASCII parameters
    if is_light:
        ascii_lines = LIGHT_ASCII
        ascii_bg_dash = "#cbd5e1"
        face_fill = "url(#faceGradLight)"
    else:
        ascii_lines = DARK_ASCII
        ascii_bg_dash = "#1e2438"
        face_fill = "url(#faceGradDark)"

    ascii_rendered = render_ascii_spans(ascii_lines, ascii_bg_dash, face_fill)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 360" width="1000" height="360">
  <defs>
    <!-- Frame Clip -->
    <clipPath id="frameClip"><rect x="10" y="10" width="980" height="340" rx="20" /></clipPath>

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

    <!-- ASCII Face Gradients -->
    <linearGradient id="faceGradDark" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="40%" stop-color="#c0caf5" />
      <stop offset="75%" stop-color="#ff79c6" />
      <stop offset="100%" stop-color="#bb9af3" />
    </linearGradient>
    <linearGradient id="faceGradLight" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0284c7" />
      <stop offset="40%" stop-color="#1e293b" />
      <stop offset="75%" stop-color="#c0267f" />
      <stop offset="100%" stop-color="#7c3aed" />
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
    .ascii-text {{
      font-family: 'Fira Code', 'Courier New', monospace;
      font-size: 9.3px;
      font-weight: 600;
      letter-spacing: 0px;
      white-space: pre;
    }}
    .term-text {{
      font-family: 'Fira Code', 'Courier New', monospace;
      font-size: 15px;
      font-weight: bold;
    }}
    .term-link {{
      text-decoration: none;
      cursor: pointer;
      transition: opacity 0.2s ease;
    }}
    .term-link:hover {{
      opacity: 0.8;
      text-decoration: underline;
    }}
  </style>

  <!-- Canvas Background -->
  <rect x="0" y="0" width="1000" height="360" rx="24" fill="{canvas_bg}" />

  <!-- Inner Clipped Content -->
  <g clip-path="url(#frameClip)">
    <!-- LEFT SIDE: ASCII Character Art Portrait -->
    <g class="ascii-text">
{ascii_rendered}
    </g>

    <!-- RIGHT SIDE: Terminal Window -->
    <g transform="translate(380, 26)">
      <!-- Terminal Outer Frame -->
      <rect x="0" y="0" width="588" height="308" rx="14" fill="{term_bg}" stroke="{term_stroke}" stroke-width="2.5" filter="url(#{term_glow})" />
      
      <!-- Window Title Bar -->
      <path d="M 0,14 A 14,14 0 0,1 14,0 L 574,0 A 14,14 0 0,1 588,14 L 588,38 L 0,38 Z" fill="{header_bg}" />
      
      <!-- Title Bar Prompt -->
      <text x="18" y="25" font-family="'Fira Code', 'Courier New', monospace" font-size="14" font-weight="bold" fill="{header_text_color}" letter-spacing="0.5">root@indoctrinatedrecluse:~</text>
      
      <!-- Window Control Buttons (Top Right) -->
      <circle cx="520" cy="19" r="6" fill="{dot_red}" />
      <circle cx="542" cy="19" r="6" fill="{dot_yellow}" />
      <circle cx="564" cy="19" r="6" fill="{dot_green}" />

      <!-- Terminal Body Content -->
      <g class="term-text">
        <!-- Line 1: Name -->
        <g transform="translate(26, 76)">
          <text x="0" y="0" fill="{label_color}">&gt; Name:</text>
          <text x="100" y="0" fill="{name_color}">Abhishek Mitra</text>
        </g>
        
        <!-- Line 2: Alias -->
        <g transform="translate(26, 120)">
          <text x="0" y="0" fill="{label_color}">&gt; Alias:</text>
          <a href="https://github.com/indoctrinatedrecluse" target="_blank" rel="noopener noreferrer" class="term-link">
            <text x="100" y="0" fill="{alias_color}">indoctrinatedrecluse</text>
          </a>
        </g>
        
        <!-- Line 3: Degree -->
        <g transform="translate(26, 164)">
          <text x="0" y="0" fill="{label_color}">&gt; Degree:</text>
          <text x="105" y="0" fill="{degree_color}">MSCS</text>
        </g>
        
        <!-- Line 4: Development -->
        <g transform="translate(26, 208)">
          <text x="0" y="0" fill="{label_color}">&gt; Development:</text>
          <text x="165" y="0" fill="{dev_color}">Full Stack</text>
        </g>
        
        <!-- Line 5: University -->
        <g transform="translate(26, 252)">
          <text x="0" y="0" fill="{label_color}">&gt; University:</text>
          <a href="https://www.usc.edu" target="_blank" rel="noopener noreferrer" class="term-link">
            <text x="155" y="0" fill="{univ_color}">USC</text>
          </a>
        </g>

        <!-- Line 6: Blinking Terminal Cursor -->
        <g transform="translate(26, 282)">
          <text x="0" y="0" fill="{label_color}">&gt;</text>
          <rect x="20" y="-14" width="10" height="18" fill="{cursor_color}" rx="2">
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

    dark_svg = build_vector_banner(theme="dark")
    light_svg = build_vector_banner(theme="light")

    with open(dark_path, "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open(light_path, "w", encoding="utf-8") as f:
        f.write(light_svg)
    with open(base_path, "w", encoding="utf-8") as f:
        f.write(dark_svg)

    print(f"Generated dual-theme vector banner SVGs for {output}:")
    print(f"  Dark:  {dark_path}")
    print(f"  Light: {light_path}")
    print(f"  Base:  {base_path}")
    return {"dark": dark_path, "light": light_path, "base": base_path}


if __name__ == "__main__":
    generate_banner()
