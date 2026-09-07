import os

# Config
OUTPUT_DIR = "profile-3d-contrib"

# (subsystem label, status, color, fast_blink)
ROWS = [
    ("UPLINK // API", "ONLINE", "#38bdf8", False),
    ("CONTRIBUTION MATRIX", "SYNCED", "#bb9af3", False),
    ("LANGUAGE CORE", "CALIBRATED", "#bb9af3", False),
    ("STREAK ENGINE", "STANDBY", "#6272a4", True),
    ("PROFILE TELEMETRY", "NOMINAL", "#38bdf8", False),
    ("NEURAL LINK", "ESTABLISHED", "#ff79c6", True),
]

TICKER = [
    "UPLINK STABLE // NO INTRUSIONS DETECTED",
    "MONITORING CONTRIBUTION STREAMS // ALL CLEAR",
    "ALL SYSTEMS NOMINAL // AWAITING INPUT",
]


def build_rows():
    parts = []
    y = 100
    for idx, (label, status, color, blink) in enumerate(ROWS):
        dur = "0.9s" if blink else "2.4s"
        parts.append(f"""
    <g>
      <text x="30" y="{y}" class="row-label">{label}</text>
      <text x="608" y="{y}" text-anchor="end" class="row-status" fill="{color}">{status}</text>
      <circle cx="626" cy="{y - 4}" r="3" fill="{color}">
        <animate attributeName="opacity" values="1;0.15;1" keyTimes="0;0.5;1" dur="{dur}" begin="{idx * 0.3:.2f}s" repeatCount="indefinite" />
      </circle>
    </g>""")
        y += 24
    return "".join(parts), y


def build_ticker():
    n = len(TICKER)
    slot = 3.6
    period = slot * n
    parts = []
    for idx, msg in enumerate(TICKER):
        kt = f"0;{0.15 / period:.6f};{(slot - 0.3) / period:.6f};{slot / period:.6f};1"
        parts.append(f"""
    <text x="0" y="0" opacity="0">
      <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="{kt}" dur="{period:.2f}s" begin="{idx * slot:.2f}s" repeatCount="indefinite" />
      {msg}
    </text>""")
    return "".join(parts), period


def generate_system_status_svg(filepath):
    rows, rows_end = build_rows()
    ticker, _ = build_ticker()

    width, height = 660, 224
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
    .row-label {{
      font-family: 'Fira Code', 'Courier New', monospace;
      font-size: 11px;
      fill: #7aa2f7;
    }}
    .row-status {{
      font-family: 'Fira Code', 'Courier New', monospace;
      font-size: 9px;
      font-weight: bold;
      letter-spacing: 1px;
    }}
    .ticker {{
      font-family: 'Fira Code', 'Courier New', monospace;
      font-size: 10px;
      fill: #ff79c6;
    }}
    .bg {{
      fill: #1a1b26;
      stroke: #3d59a1;
      stroke-width: 2;
      rx: 12px;
    }}
  </style>

  <rect width="{width}" height="{height}" class="bg" />

  <!-- Header -->
  <g transform="translate(24, 24)">
    <rect x="0" y="0" width="6" height="22" fill="#38bdf8" rx="2" />
    <text x="18" y="16" class="title">SYSTEM STATUS</text>
    <text x="18" y="29" class="subtitle">UPTIME MONITOR // ALL SYSTEMS NOMINAL</text>
  </g>

  <!-- Scanline -->
  <rect x="-120" y="60" width="120" height="2" fill="#ff79c6" opacity="0.7">
    <animate attributeName="x" values="-120;{width + 60}" dur="3.2s" repeatCount="indefinite" />
  </rect>
  <line x1="24" y1="74" x2="{width - 24}" y2="74" stroke="#3d59a1" stroke-opacity="0.6" stroke-width="1" />

  {rows}

  <!-- Ticker footer -->
  <line x1="24" y1="{rows_end + 10}" x2="{width - 24}" y2="{rows_end + 10}" stroke="#3d59a1" stroke-opacity="0.4" stroke-width="1" />
  <g transform="translate(30, {rows_end + 36})" class="ticker">{ticker}
  </g>
</svg>
"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated system status SVG at {filepath}")


if __name__ == "__main__":
    generate_system_status_svg(os.path.join(OUTPUT_DIR, "system-status.svg"))
    print("System status generation finished successfully!")
