#!/usr/bin/env python3
"""Generate chopstick theme assets — cursors, dividers, icons, ornaments."""

from __future__ import annotations

import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "chopsticks"

STONE = "#1c1917"
AMBER = "#fbbf24"
ORANGE = "#f97316"
GREY = "#d6d3d1"
GREEN = "#22c55e"
TEAL = "#14b8a6"

SECTIONS = {
    "hero": {"accent": ORANGE, "secondary": AMBER, "wave": ORANGE},
    "menu": {"accent": AMBER, "secondary": ORANGE, "wave": AMBER},
    "build": {"accent": GREEN, "secondary": TEAL, "wave": GREEN},
    "learn": {"accent": TEAL, "secondary": "#fff", "wave": TEAL},
    "story": {"accent": "#8b5cf6", "secondary": "#6366f1", "wave": "#a78bfa"},
    "slurp-code": {"accent": AMBER, "secondary": ORANGE, "wave": AMBER},
    "stores": {"accent": ORANGE, "secondary": AMBER, "wave": ORANGE},
    "reviews": {"accent": "#eab308", "secondary": AMBER, "wave": "#facc15"},
    "spread": {"accent": "#fb923c", "secondary": "#fdba74", "wave": ORANGE},
    "social": {"accent": "#f472b6", "secondary": ORANGE, "wave": "#fb7185"},
    "gift": {"accent": "#dc2626", "secondary": ORANGE, "wave": "#ef4444"},
    "checkout": {"accent": STONE, "secondary": GREY, "wave": "#78716c"},
}

CURSOR_HOTSPOTS = {
    "chopsticks": (16, 16),
    "default": (16, 16),
    "pointer": (4, 2),
    "grab": (8, 8),
    "grabbing": (8, 8),
    "not-allowed": (8, 8),
    "wait": (6, 4),
    "text": (4, 16),
}


def svg_wrap(viewbox: str, inner: str, width: int | None = None, height: int | None = None, *, cursor: bool = False) -> str:
    w = f' width="{width}"' if width else ""
    h = f' height="{height}"' if height else ""
    fill = ' fill="none"' if cursor else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}"{w}{h}{fill} aria-hidden="true">\n'
        f"{inner}\n</svg>\n"
    )


def stick(x1: float, y1: float, x2: float, y2: float, color: str, sw: float = 2.8) -> str:
    return (
        f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>'
    )


def crossed_pair(cx: float, cy: float, span: float, c1: str, c2: str, sw: float = 2.8) -> str:
    s = span / 2
    return "\n".join([
        stick(cx - s, cy - s, cx + s, cy + s, c1, sw),
        stick(cx + s, cy - s, cx - s, cy + s, c2, sw),
    ])


def parallel_pair(cx: float, cy: float, length: float, gap: float, c1: str, c2: str, angle: float = -15) -> str:
    rad = math.radians(angle)
    dx = math.cos(rad) * length / 2
    dy = math.sin(rad) * length / 2
    ox = math.sin(rad) * gap / 2
    oy = -math.cos(rad) * gap / 2
    return "\n".join([
        stick(cx - dx + ox, cy - dy + oy, cx + dx + ox, cy + dy + oy, c1, 2.6),
        stick(cx - dx - ox, cy - dy - oy, cx + dx - ox, cy + dy - oy, c2, 2.6),
    ])


def noodle_wave(y: float, color: str, amp: float = 4) -> str:
    return (
        f'  <path d="M 8 {y} Q 40 {y - amp} 72 {y} T 136 {y} T 200 {y} T 264 {y} T 328 {y} T 392 {y}" '
        f'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" opacity="0.85"/>'
    )


def cursor_chopsticks() -> str:
    """Crossed pair — transparent SVG cursor hotspot at center (16, 16)."""
    return crossed_pair(16, 16, 18, AMBER, ORANGE)


def cursor_default() -> str:
    return cursor_chopsticks()


def cursor_pointer() -> str:
    return "\n".join([
        stick(6, 26, 24, 6, AMBER, 3.2),
        stick(24, 6, 28, 2, STONE, 1.5),
    ])


def cursor_grab() -> str:
    return parallel_pair(16, 16, 20, 6, AMBER, GREY, -20)


def cursor_grabbing() -> str:
    return crossed_pair(16, 16, 14, AMBER, GREY, 3.2)


def cursor_not_allowed() -> str:
    inner = crossed_pair(16, 16, 16, "#ef4444", GREY, 3)
    ring = f'  <circle cx="16" cy="16" r="13" fill="none" stroke="{STONE}" stroke-width="2"/>'
    return ring + "\n" + inner


def cursor_wait() -> str:
    return parallel_pair(16, 16, 22, 5, AMBER, GREY, 0)


def cursor_text() -> str:
    return stick(16, 4, 16, 28, GREY, 2.2)


def section_cursor(name: str) -> str:
    pal = SECTIONS[name]
    if name == "menu":
        return cursor_pointer()
    if name == "build":
        return cursor_grab()
    if name == "story":
        return parallel_pair(16, 16, 20, 5, pal["secondary"], pal["accent"], -25)
    if name in ("gift", "checkout"):
        return parallel_pair(16, 16, 18, 4, pal["accent"], pal["secondary"], 10)
    return crossed_pair(16, 16, 17, pal["accent"], pal["secondary"])


CURSOR_BUILDERS = {
    "default": cursor_default,
    "pointer": cursor_pointer,
    "grab": cursor_grab,
    "grabbing": cursor_grabbing,
    "not-allowed": cursor_not_allowed,
    "wait": cursor_wait,
    "text": cursor_text,
}


def icon_crossed() -> str:
    return crossed_pair(12, 12, 14, AMBER, GREY, 2.4)


def icon_parallel() -> str:
    return parallel_pair(12, 12, 16, 4, AMBER, GREY, 0)


def icon_picking() -> str:
    return cursor_pointer().replace("3.2", "2.6").replace("1.5", "1.2")


def icon_serving() -> str:
    return parallel_pair(12, 12, 14, 5, TEAL, AMBER, -35)


def icon_slurping() -> str:
    return "\n".join([
        stick(4, 18, 14, 8, AMBER, 2.4),
        stick(20, 6, 10, 16, GREY, 2.4),
        f'  <path d="M 16 20 Q 20 22 24 20" fill="none" stroke="{ORANGE}" stroke-width="1.5" stroke-linecap="round"/>',
    ])


def icon_gift_wrap() -> str:
    base = parallel_pair(12, 13, 14, 4, ORANGE, "#dc2626", 15)
    bow = f'  <path d="M 12 6 L 12 10 M 8 8 Q 12 4 16 8" fill="none" stroke="{STONE}" stroke-width="1.5" stroke-linecap="round"/>'
    return base + "\n" + bow


ICON_BUILDERS = {
    "crossed": icon_crossed,
    "parallel": icon_parallel,
    "picking": icon_picking,
    "serving": icon_serving,
    "slurping": icon_slurping,
    "gift-wrap": icon_gift_wrap,
}


def divider_svg(section: str) -> str:
    pal = SECTIONS[section]
    sticks = crossed_pair(36, 22, 20, pal["accent"], pal["secondary"], 3)
    wave = noodle_wave(28, pal["wave"])
    mirror = crossed_pair(360, 22, 20, pal["secondary"], pal["accent"], 3)
    return svg_wrap("0 0 400 40", sticks + "\n" + wave + "\n" + mirror, 400, 40)


def ornament_corner() -> str:
    inner = crossed_pair(14, 14, 12, AMBER, GREY, 2.2)
    return svg_wrap("0 0 28 28", inner, 28, 28)


def rasterize_svg_lines_to_png(svg_body: str, path: Path, size: int = 32) -> None:
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        path.write_bytes(b"")
        return

    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    scale = size / 32.0

    def hex_rgb(h: str) -> tuple[int, int, int]:
        h = h.lstrip("#")
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

    color_map = {
        STONE: hex_rgb(STONE),
        AMBER: hex_rgb(AMBER),
        ORANGE: hex_rgb(ORANGE),
        GREY: hex_rgb(GREY),
        GREEN: hex_rgb(GREEN),
        TEAL: hex_rgb(TEAL),
        "#ef4444": (239, 68, 68),
        "#dc2626": (220, 38, 38),
        "#8b5cf6": (139, 92, 246),
        "#6366f1": (99, 102, 241),
        "#fff": (255, 255, 255),
        "#78716c": (120, 113, 108),
        "#fdba74": (253, 186, 116),
        "#fb7185": (251, 113, 133),
        "#facc15": (250, 204, 21),
    }

    for line in svg_body.splitlines():
        line = line.strip()
        if not line.startswith("<line"):
            continue
        parts = {}
        for token in line.replace("/>", "").split():
            if "=" in token:
                k, v = token.split("=", 1)
                parts[k] = v.strip('"')
        color = color_map.get(parts.get("stroke", STONE), hex_rgb(STONE))
        sw = float(parts.get("stroke-width", "2.8")) * scale
        x1 = float(parts["x1"]) * scale
        y1 = float(parts["y1"]) * scale
        x2 = float(parts["x2"]) * scale
        y2 = float(parts["y2"]) * scale
        draw.line([(x1, y1), (x2, y2)], fill=color + (255,), width=max(1, int(sw)))

    img.save(path, optimize=True)


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    cursor_dir = OUT / "cursors"
    icon_dir = OUT / "icons"
    ornament_dir = OUT / "ornaments"

    chopsticks_body = cursor_chopsticks()
    write_file(cursor_dir / "chopsticks.svg", svg_wrap("0 0 32 32", chopsticks_body, 32, 32, cursor=True))

    for name, builder in CURSOR_BUILDERS.items():
        body = builder()
        svg = svg_wrap("0 0 32 32", body, 32, 32, cursor=True)
        write_file(cursor_dir / f"{name}.svg", svg)
        rasterize_svg_lines_to_png(body, cursor_dir / f"{name}.png")

    for name, builder in ICON_BUILDERS.items():
        write_file(icon_dir / f"{name}.svg", svg_wrap("0 0 24 24", builder(), 24, 24))

    write_file(ornament_dir / "corner.svg", ornament_corner())

    write_file(OUT / "hotspots.json", __import__("json").dumps(CURSOR_HOTSPOTS, indent=2) + "\n")
    print(f"Generated chopstick assets in {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
