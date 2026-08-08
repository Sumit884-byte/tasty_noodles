#!/usr/bin/env python3
"""Generate Stack Your Bowl orbit ring SVG — rangoli rings + garnish icons."""

from __future__ import annotations

import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "build-orbit-ring.svg"

CX, CY = 256, 256
ORANGE = "#ea580c"
AMBER = "#fbbf24"
STONE = "#1c1917"
GREEN = "#22c55e"
NORI = "#14532d"
CHILI = "#dc2626"


def ring_circles() -> str:
    lines = [
        f'    <circle cx="{CX}" cy="{CY}" r="228" stroke="{ORANGE}" stroke-width="2.5" stroke-dasharray="10 8" opacity="0.55"/>',
        f'    <circle cx="{CX}" cy="{CY}" r="188" stroke="{AMBER}" stroke-width="1.5" opacity="0.4"/>',
        f'    <circle cx="{CX}" cy="{CY}" r="148" stroke="{ORANGE}" stroke-width="1.5" stroke-dasharray="4 7" opacity="0.35"/>',
    ]
    for deg in range(0, 360, 15):
        rad = math.radians(deg - 90)
        x = CX + 168 * math.cos(rad)
        y = CY + 168 * math.sin(rad)
        lines.append(
            f'    <circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{ORANGE}" opacity="0.45"/>'
        )
    return "\n".join(lines)


def icon_chopsticks() -> str:
    return f"""    <g stroke="{STONE}" stroke-width="2" stroke-linecap="round">
      <line x1="-6" y1="-14" x2="6" y2="14" stroke="{AMBER}" stroke-width="3"/>
      <line x1="6" y1="-14" x2="-6" y2="14" stroke="#d6d3d1" stroke-width="3"/>
    </g>"""


def icon_egg() -> str:
    return f"""    <g>
      <ellipse cx="0" cy="4" rx="14" ry="11" fill="#fef3c7" stroke="{STONE}" stroke-width="2"/>
      <circle cx="0" cy="6" r="5" fill="{AMBER}" opacity="0.9"/>
    </g>"""


def icon_nori() -> str:
    return f"""    <path d="M-14,8 L-10,-6 L-4,2 L2,-8 L8,0 L14,-4 L14,10 L-14,10 Z"
          fill="{NORI}" stroke="{STONE}" stroke-width="1.8" stroke-linejoin="round"/>"""


def icon_chili() -> str:
    return f"""    <g>
      <circle cx="0" cy="0" r="11" fill="{CHILI}" stroke="{STONE}" stroke-width="2"/>
      <circle cx="-3" cy="-3" r="2.5" fill="#fff" opacity="0.55"/>
    </g>"""


def icon_noodle() -> str:
    return f"""    <path d="M-12,6 A14,14 0 1,1 10,-8" fill="none" stroke="{AMBER}" stroke-width="3.5"
          stroke-linecap="round"/>"""


def icon_scallion() -> str:
    greens = []
    for i, (x, y, rot) in enumerate([(-8, -2, -25), (0, 2, 15), (8, -1, 35), (-2, 8, -10)]):
        greens.append(
            f'      <rect x="{x}" y="{y}" width="10" height="3" rx="1.5" fill="{GREEN}" '
            f'transform="rotate({rot} {x + 5} {y + 1.5})"/>'
        )
    return "    <g>\n" + "\n".join(greens) + "\n    </g>"


ICONS = [
    icon_chopsticks,
    icon_egg,
    icon_nori,
    icon_chili,
    icon_noodle,
    icon_scallion,
]


def garnish_orbit() -> str:
    lines: list[str] = []
    radius = 198
    for i, icon_fn in enumerate(ICONS):
        angle = i * 60
        lines.append(f'  <g transform="rotate({angle} {CX} {CY})">')
        lines.append(f'    <g transform="translate({CX} {CY - radius})">')
        lines.append(icon_fn())
        lines.append("    </g>")
        lines.append("  </g>")
    return "\n".join(lines)


def build_svg() -> str:
    return f"""<svg width="512" height="512" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <title>Bowl builder garnish orbit</title>
  <g fill="none">
{ring_circles()}
  </g>
{garnish_orbit()}
</svg>
"""


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build_svg())
    print(OUT)


if __name__ == "__main__":
    main()
