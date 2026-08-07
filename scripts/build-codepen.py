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
        "https://unpkg.com/lucide@latest",
    ]),
}

ALPINE_CDN = "https://cdn.jsdelivr.net/npm/alpinejs@3.14.9/dist/cdn.min.js"

# CodePen injects js_external before pen JS, so Alpine must load AFTER slurpApp registers.
ALPINE_BOOTSTRAP = f"""
// CodePen loads external JS before pen JS — defer Alpine until slurpApp is registered.
(function () {{
  if (document.querySelector('script[data-slurp-alpine]')) return;
  var s = document.createElement('script');
  s.src = '{ALPINE_CDN}';
  s.defer = true;
  s.dataset.slurpAlpine = '1';
  document.head.appendChild(s);
}})();
"""


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


def extract_body_inner(html: str) -> str:
    """Body inner HTML — opening tag may contain ``>`` inside quoted attributes."""
    start = re.search(r"<body\b", html, re.IGNORECASE)
    if not start:
        raise ValueError("Missing <body>")
    i = start.end()
    in_quote: str | None = None
    while i < len(html):
        ch = html[i]
        if in_quote:
            if ch == in_quote:
                in_quote = None
        elif ch in "\"'":
            in_quote = ch
        elif ch == ">":
            i += 1
            break
        i += 1
    rest = html[i:]
    end = re.search(r"\s*<script>\s*\n\s*lucide\.createIcons\(\)", rest, re.DOTALL)
    if not end:
        raise ValueError("Missing lucide.createIcons() script after body")
    return rest[: end.start()].strip()


def main() -> dict:
    html = INDEX.read_text(encoding="utf-8")

    css = extract_block(html, r"<style>\s*", r"\s*</style>")
    alpine_js = extract_block(html, r"<script>\s*\n\s*document\.addEventListener\('alpine:init'", r"</script>\s*</head>")
    alpine_js = "document.addEventListener('alpine:init'" + alpine_js

    body_html = extract_body_inner(html)

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

    pen_js = f"{alpine_js}\n\n{footer_js}\n{ALPINE_BOOTSTRAP}"

    payload = {
        **PEN_META,
        "html": pen_html,
        "css": css,
        "js": pen_js,
    }

    if re.search(r"\n0 && !orderPlaced", pen_html):
        raise ValueError("Body extraction looks corrupt — check extract_body_inner()")
    if len(css) < 1000 or len(pen_js) < 1000 or len(body_html) < 1000:
        raise ValueError("CodePen export looks truncated")

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
    body {{ font-family: system-ui, sans-serif; max-width: 42rem; margin: 3rem auto; padding: 0 1.5rem 4rem; line-height: 1.6; color: #1c1917; }}
    h1 {{ font-size: 1.875rem; margin-bottom: 0.35rem; }}
    h2 {{ font-size: 1.125rem; margin: 2rem 0 0.75rem; }}
    p {{ color: #57534e; }}
    .hero {{ background: linear-gradient(135deg, #fff7ed, #fef3c7); border: 1px solid #fed7aa; border-radius: 1.25rem; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem; }}
    .hero a {{ color: #c2410c; font-weight: 700; }}
    .btn {{ display: inline-block; background: #1c1917; color: #fff; border: none; border-radius: 9999px; padding: 0.875rem 1.5rem; font-weight: 700; cursor: pointer; font-size: 1rem; }}
    .btn:hover {{ background: #ea580c; }}
    ol, ul {{ padding-left: 1.25rem; color: #57534e; }}
    li {{ margin-bottom: 0.5rem; }}
    code {{ background: #fef3c7; padding: 0.1rem 0.35rem; border-radius: 0.25rem; font-size: 0.9em; }}
    .links {{ display: flex; flex-wrap: wrap; gap: 0.75rem; margin-top: 1rem; }}
    .links a {{ color: #c2410c; font-weight: 600; text-decoration: none; border-bottom: 1px solid #fdba74; }}
  </style>
</head>
<body>
  <div class="hero">
    <p style="margin:0;font-size:0.75rem;font-weight:800;letter-spacing:0.08em;text-transform:uppercase;color:#9a3412;">Live demo</p>
    <p style="margin:0.35rem 0 0;"><a href="https://tastynoodles.vercel.app">tastynoodles.vercel.app</a> — full SLURP! site on Vercel</p>
  </div>
  <h1>Deploy SLURP! on CodePen</h1>
  <p>This page loads the full HTML, CSS, and JavaScript into the CodePen editor. Bowl photos and logos load from the live Vercel deploy, so you don't upload assets separately.</p>
  <p><button type="button" class="btn" id="open">Open in CodePen</button></p>

  <h2>Steps</h2>
  <ol>
    <li>Click <strong>Open in CodePen</strong> above (create a free CodePen account if needed).</li>
    <li>Review the pen in the editor — HTML, CSS, and JS are pre-filled.</li>
    <li>Click <strong>Save</strong>, name your pen, and set visibility to <strong>Public</strong>.</li>
    <li>Copy your pen URL from the browser and share it.</li>
  </ol>

  <h2>After you edit the repo</h2>
  <p>Regenerate this export whenever <code>index.html</code> changes:</p>
  <p><code>python3 scripts/build-codepen.py</code></p>
  <p>Then redeploy to Vercel so <code>/codepen/</code> stays in sync.</p>

  <div class="links">
    <a href="https://tastynoodles.vercel.app">Live demo</a>
    <a href="https://github.com/Sumit884-byte/tasty_noodles">GitHub</a>
    <a href="https://dev.to/challenges/frontend-2026-07-29">DEV Challenge</a>
  </div>
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
