import os

# Config
OUTPUT_DIR = "profile-3d-contrib"

# Rotating role lines (same phrasing the demo typing SVG used)
ROLES = [
    "Software Engineer",
    "Full-Stack Developer",
    "Creative Problem Solver",
    "Tech Explorer",
]

# Font metrics estimate: Fira Code / monospace advance ~= 0.6 * font-size.
FONT_SIZE = 24
CHAR_ADVANCE = 15.0
SLOT = 4.0          # seconds each role is shown
FADE_IN = 0.2       # seconds of fade-in
FADE_OUT = 0.4      # seconds of fade-out at the end of a role's slot


def generate_typing_svg(filepath):
    width = 680
    center_x = width // 2
    baseline_y = 46
    caret_w = 11
    caret_h = 26
    caret_y = baseline_y - caret_h - 2
    period = SLOT * len(ROLES)

    groups = []
    for idx, role in enumerate(ROLES):
        text_w = len(role) * CHAR_ADVANCE
        caret_x = center_x + text_w / 2 + 8
        key_times = [0.0, FADE_IN / period, (SLOT - FADE_OUT) / period, SLOT / period, 1.0]
        kt = ";".join(f"{v:.6f}" for v in key_times)
        groups.append(f"""
  <g opacity="0">
    <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="{kt}" dur="{period:.2f}s" begin="{idx * SLOT:.2f}s" repeatCount="indefinite" />
    <text x="{center_x}" y="{baseline_y}" text-anchor="middle"
          font-family="'Fira Code', 'Consolas', 'Courier New', monospace"
          font-size="{FONT_SIZE}" fill="#ff79c6">{role}</text>
    <rect x="{caret_x:.1f}" y="{caret_y}" width="{caret_w}" height="{caret_h}" fill="#ff79c6">
      <animate attributeName="fill" values="#ff79c6;#1a1b26;#ff79c6" keyTimes="0;0.5;1" dur="1s" begin="{idx * SLOT:.2f}s" repeatCount="indefinite" />
    </rect>
  </g>""")

    svg_content = f"""<svg width="{width}" height="64" viewBox="0 0 {width} 64" xmlns="http://www.w3.org/2000/svg">
{''.join(groups)}
</svg>
"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated typing SVG at {filepath}")


if __name__ == "__main__":
    generate_typing_svg(os.path.join(OUTPUT_DIR, "typing.svg"))
    print("Typing generation finished successfully!")
