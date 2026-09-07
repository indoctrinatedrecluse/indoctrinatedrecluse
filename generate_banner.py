import os
import base64
from cyber_palette import apply_theme

# Config
SOURCE = "banner.jpg"
OUTPUT = "banner.svg"


def generate_banner(source=SOURCE, output=OUTPUT):
    with open(source, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    # NIGHT palette baked in; apply_theme() flips it to DAY when appropriate.
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 360" width="1000" height="360">
  <defs>
    <clipPath id="frameClip"><rect x="10" y="10" width="980" height="340" rx="20" /></clipPath>
    <linearGradient id="neonFrame" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="45%" stop-color="#ff79c6" />
      <stop offset="100%" stop-color="#bb9af3" />
    </linearGradient>
    <filter id="frameGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>
  <rect x="0" y="0" width="1000" height="360" rx="24" fill="#0f111a" />
  <g clip-path="url(#frameClip)">
    <image href="data:image/jpeg;base64,{b64}" x="10" y="10" width="980" height="340" preserveAspectRatio="xMidYMid slice" />
  </g>
  <rect x="10" y="10" width="980" height="340" rx="20" fill="none" stroke="url(#neonFrame)" stroke-width="5" filter="url(#frameGlow)" />
  <rect x="10" y="10" width="980" height="340" rx="20" fill="none" stroke="#ffffff" stroke-opacity="0.3" stroke-width="1" />
</svg>
"""
    svg = apply_theme(svg)
    with open(output, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Generated banner SVG at {output}")


if __name__ == "__main__":
    generate_banner()
