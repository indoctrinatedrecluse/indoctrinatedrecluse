import os
import base64
from cyber_palette import save_dual_theme_svg

# Config
SOURCE = "banner.jpg"
OUTPUT = "banner.svg"


def generate_banner(source=SOURCE, output=OUTPUT):
    with open(source, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 360" width="1000" height="360">
  <defs>
    <clipPath id="frameClip"><rect x="10" y="10" width="980" height="340" rx="20" /></clipPath>
    <linearGradient id="neonFrame" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="45%" stop-color="#ff79c6" />
      <stop offset="100%" stop-color="#bb9af3" />
    </linearGradient>
    <linearGradient id="scanlineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0" />
      <stop offset="25%" stop-color="#38bdf8" stop-opacity="0.8" />
      <stop offset="50%" stop-color="#ff79c6" stop-opacity="1" />
      <stop offset="75%" stop-color="#bb9af3" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#bb9af3" stop-opacity="0" />
    </linearGradient>
    <filter id="frameGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    <filter id="hudGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
  </defs>

  <!-- Canvas Background -->
  <rect x="0" y="0" width="1000" height="360" rx="24" fill="#0f111a" />

  <!-- Base Image -->
  <g clip-path="url(#frameClip)">
    <image href="data:image/jpeg;base64,{b64}" x="10" y="10" width="980" height="340" preserveAspectRatio="xMidYMid slice" />
    
    <!-- Cyber Scanline Animation -->
    <rect x="10" y="10" width="980" height="2" fill="url(#scanlineGrad)" opacity="0.85" filter="url(#frameGlow)">
      <animate attributeName="y" values="10;346;10" dur="7s" repeatCount="indefinite" />
    </rect>
  </g>

  <!-- Glowing Outer Frame -->
  <rect x="10" y="10" width="980" height="340" rx="20" fill="none" stroke="url(#neonFrame)" stroke-width="4" filter="url(#frameGlow)" />
  <rect x="10" y="10" width="980" height="340" rx="20" fill="none" stroke="#ffffff" stroke-opacity="0.25" stroke-width="1" />

  <!-- Cyber HUD Overlays -->
  <g font-family="'Fira Code', 'Courier New', monospace" font-size="10" font-weight="bold" filter="url(#hudGlow)">
    <!-- Top-Right HUD Badge -->
    <rect x="760" y="24" width="210" height="24" rx="6" fill="#1a1b26" fill-opacity="0.85" stroke="#3d59a1" stroke-width="1.2" />
    <circle cx="776" cy="36" r="3.5" fill="#38bdf8">
      <animate attributeName="opacity" values="1;0.2;1" dur="1.8s" repeatCount="indefinite" />
    </circle>
    <text x="788" y="40" fill="#7aa2f7" letter-spacing="1">SYS.CORE // ACTIVE</text>

    <!-- Bottom-Left Telemetry Tag -->
    <rect x="28" y="312" width="240" height="24" rx="6" fill="#1a1b26" fill-opacity="0.85" stroke="#3d59a1" stroke-width="1.2" />
    <circle cx="44" cy="324" r="3.5" fill="#ff79c6">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="2.2s" repeatCount="indefinite" />
    </circle>
    <text x="56" y="328" fill="#c0caf5" letter-spacing="1">PROTOCOL // CYBER-SYNAPSE</text>
  </g>
</svg>
"""
    paths = save_dual_theme_svg(svg, output)
    return paths


if __name__ == "__main__":
    generate_banner()

