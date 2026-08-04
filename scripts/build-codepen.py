#!/usr/bin/env python3
"""Build CodePen payload from index.html (assets → Vercel CDN URLs)."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
ASSET_BASE = "https://tastynoodles.vercel.app/assets/"
OUT = ROOT / "codepen" / "pen-data.json"

PEN_META = {
    "title": "SLURP! — Tastiest Noodles on the Planet 🍜",
    "description": "Comfort-food landing page: SVG splash, 6-bowl menu, CSS bowl builder, pan-India stores, Three.js globe, CollectUI checkout. DEV Frontend Challenge.",
    "tags": ["devchallenge", "frontend", "javascript", "css", "threejs", "alpinejs"],
    "html_pre_processor": "none",
    "css_pre_processor": "none",
    "js_pre_processor": "none",
    "css_external": "https://fonts.googleapis.com/css2?family=Chewy&display=swap",
    "js_external": ";".join([
        "https://cdn.tailwindcss.com",
        "https://cdn.jsdelivr.net/npm/alpinejs@3.14.9/dist/cdn.min.js",
        "https://unpkg.com/lucide@latest",
    ]),
}


def rewrite_assets(text: str) -> str:
    text = text.replace("assets/", ASSET_BASE)
    return text


def extract_block(html: str, start_pat: str, end_pat: str) -> str:
    start = re.search(start_pat, html, re.DOTALL)
    if not start:
        raise ValueError(f"Missing block: {start_pat}")
    end = re.search(end_pat, html[start.end() :], re.DOTALL)
    if not end:
        raise ValueError(f"Missing end: {end_pat}")
    return html[start.end() : start.end() + end.start()]


def main() -> dict:
    html = INDEX.read_text(encoding="utf-8")

    css = extract_block(html, r"<style>\s*", r"\s*</style>")
    alpine_js = extract_block(html, r"<script>\s*\n\s*document\.addEventListener\('alpine:init'", r"</script>\s*</head>")
    alpine_js = "document.addEventListener('alpine:init'" + alpine_js

    body_html = extract_block(html, r"<body[^>]*>\s*", r"\s*<script>\s*\n\s*lucide\.createIcons")
    body_html = body_html.strip()

    footer_js = extract_block(html, r"lucide\.createIcons\(\);\s*", r"</script>\s*<script type=\"module\">")
    footer_js = "lucide.createIcons();\n" + footer_js

    globe_js = extract_block(html, r"<script type=\"module\">\s*", r"\s*</script>\s*</body>")
    globe_js = globe_js.strip()

    css = rewrite_assets(css)
    body_html = rewrite_assets(body_html)
    alpine_js = rewrite_assets(alpine_js)
    footer_js = rewrite_assets(footer_js)
    globe_js = rewrite_assets(globe_js)

    pen_html = f"""<!-- SLURP! — live assets from tastynoodles.vercel.app -->
<div class="bg-amber-50 text-stone-900 font-sans antialiased overflow-x-hidden bg-grid" x-data="slurpApp()" @keydown.escape.window="handleEscape()" :class="cartCount > 0 && !orderPlaced ? 'has-cart-bar' : ''">
{body_html}
<script type="module">
{globe_js}
</script>"""

    pen_js = f"{alpine_js}\n\n{footer_js}"

    payload = {
        **PEN_META,
        "html": pen_html,
        "css": css,
        "js": pen_js,
    }
    return payload


if __name__ == "__main__":
    data = main()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    # Self-contained opener (works on Vercel without fetch)
    opener = ROOT / "codepen" / "index.html"
    data_json = json.dumps(data, ensure_ascii=False)
    data_json_safe = data_json.replace("</", "<\\/")
    opener.write_text(
        f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Open SLURP! on CodePen</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 36rem; margin: 4rem auto; padding: 0 1.5rem; line-height: 1.55; color: #1c1917; }}
    h1 {{ font-size: 1.75rem; margin-bottom: 0.5rem; }}
    p {{ color: #57534e; }}
    .btn {{ display: inline-block; background: #1c1917; color: #fff; border: none; border-radius: 9999px; padding: 0.875rem 1.5rem; font-weight: 700; cursor: pointer; text-decoration: none; }}
    .btn:hover {{ background: #ea580c; }}
    ol {{ padding-left: 1.25rem; }}
    code {{ background: #fef3c7; padding: 0.1rem 0.35rem; border-radius: 0.25rem; }}
  </style>
</head>
<body>
  <h1>SLURP! on CodePen</h1>
  <p>One click opens the full project in the CodePen editor. Images load from the live Vercel deploy.</p>
  <p><button type="button" class="btn" id="open">Open in CodePen</button></p>
  <ol>
    <li>Log in to CodePen (free account works).</li>
    <li>Click <strong>Save</strong> in the editor.</li>
    <li>Set visibility to <strong>Public</strong> and copy your pen URL.</li>
  </ol>
  <p><small>Live site: <a href="https://tastynoodles.vercel.app">tastynoodles.vercel.app</a></small></p>
  <script id="pen-data" type="application/json">{data_json_safe}</script>
  <script>
    document.getElementById('open').addEventListener('click', () => {{
      const data = document.getElementById('pen-data').textContent;
      const form = document.createElement('form');
      form.action = 'https://codepen.io/pen/define';
      form.method = 'POST';
      form.target = '_blank';
      const input = document.createElement('input');
      input.type = 'hidden';
      input.name = 'data';
      input.value = data;
      form.appendChild(input);
      document.body.appendChild(form);
      form.submit();
      form.remove();
    }});
  </script>
</body>
</html>
""",
        encoding="utf-8",
    )

    print(f"Wrote {OUT} ({OUT.stat().st_size // 1024} KB)")
    print(f"Wrote {opener}")
    print(json.dumps({k: (len(v) if isinstance(v, str) else v) for k, v in data.items()}, indent=2))
