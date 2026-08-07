#!/usr/bin/env python3
"""Generate Noodle Vault → Build section divider reference art with Gemini.

The site renders a CSS/SVG divider in index.html (`.vault-divider__band`).
This script produces optional reference PNGs in assets/ — not required at runtime.
"""

from __future__ import annotations

import io
import os
import sys
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

# Final divider asset — wide shallow strip between #menu and #build
TARGET_WIDTH = 1440
TARGET_HEIGHT = 480
TARGET_ASPECT = TARGET_WIDTH / TARGET_HEIGHT  # 3:1

PROMPT = (
    f"Generate a single wide horizontal website section divider illustration. "
    f"Canvas size: exactly {TARGET_WIDTH} pixels wide × {TARGET_HEIGHT} pixels tall "
    f"({TARGET_WIDTH}:{TARGET_HEIGHT} aspect ratio, 3:1 panoramic strip). "
    f"Layout rules for this shallow banner: "
    f"(1) Keep all artwork inside the canvas — nothing cropped at edges. "
    f"(2) Center a top-down ramen bowl occupying roughly 35% of canvas width and 70% of canvas height. "
    f"(3) Extend flowing noodle-wave bands and crossed chopsticks symmetrically left and right "
    f"into the remaining horizontal space — art should read left-to-right across the full "
    f"{TARGET_WIDTH}px width. "
    f"(4) Steam wisps rise only within the top 25% of the canvas. "
    f"(5) Leave ~5% quiet margin on left, right, top, and bottom. "
    f"Style: warm orange (#ea580c) and amber (#fbbf24) line art with subtle peach fills, "
    f"rangoli-inspired dots and concentric arcs, Indian-Asian fusion editorial ink look. "
    f"Center bowl: broth, noodle swirl, chashu, egg, scallion, nori. "
    f"Background: plain solid pure white (#FFFFFF) only — no gradient, no texture. "
    f"No text, no drop shadow, no outer border frame, no watermark, no extra objects."
)

# Closest supported Gemini aspect ratio to 3:1 (script resizes to TARGET_* after generation)
GEMINI_ASPECT_RATIO = "16:9"

MODELS = [
    "gemini-2.5-flash-image",
    "gemini-3.1-flash-image",
    "gemini-2.0-flash-preview-image-generation",
]


def get_client() -> genai.Client:
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise SystemExit("Set GEMINI_API_KEY or GOOGLE_API_KEY")
    if os.environ.get("GEMINI_API_KEY"):
        os.environ.pop("GOOGLE_API_KEY", None)
    return genai.Client(api_key=api_key)


def generate_image(client: genai.Client) -> Image.Image:
    last_error: Exception | None = None
    for model in MODELS:
        try:
            response = client.models.generate_content(
                model=model,
                contents=PROMPT,
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio=GEMINI_ASPECT_RATIO),
                ),
            )
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            print(f"  model {model} failed: {exc}", file=sys.stderr)
            continue

        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.data:
                print(f"  generated with {model}")
                return Image.open(io.BytesIO(part.inline_data.data)).convert("RGBA")

        last_error = RuntimeError(f"{model} returned no image")

    raise RuntimeError(f"All models failed. Last error: {last_error}")


def remove_background(image: Image.Image, threshold: int = 248, soft: int = 18) -> Image.Image:
    """White-key removal — keeps full panoramic art (rembg crops wing details)."""
    rgba = image.convert("RGBA")
    pixels = rgba.load()
    width, height = rgba.size
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            m = min(r, g, b)
            if m >= threshold:
                pixels[x, y] = (r, g, b, 0)
            elif m >= threshold - soft:
                fade = (threshold - m) / soft
                pixels[x, y] = (r, g, b, int(255 * fade))
    return rgba


def crop_to_content(image: Image.Image, pad: int = 16) -> Image.Image:
    bbox = image.split()[-1].getbbox()
    if not bbox:
        return image
    x0, y0, x1, y1 = bbox
    x0 = max(0, x0 - pad)
    y0 = max(0, y0 - pad)
    x1 = min(image.width, x1 + pad)
    y1 = min(image.height, y1 + pad)
    return image.crop((x0, y0, x1, y1))


MATTE = (255, 251, 235)  # #fffbeb — matches .vault-divider / #build bg


def flatten_on_matte(image: Image.Image, matte: tuple[int, int, int] = MATTE) -> Image.Image:
    flat = Image.new("RGB", image.size, matte)
    flat.paste(image, (0, 0), image)
    return flat


def write_svg(image: Image.Image, out_path: Path) -> None:
    w, h = image.size
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true">\n'
        f'  <title>Vault to bowl divider</title>\n'
        f'  <image width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" '
        f'xlink:href="vault-divider.png"/>\n'
        f"</svg>\n"
    )
    out_path.write_text(svg)


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    raw_path = ASSETS / "vault-divider-raw.png"
    png_path = ASSETS / "vault-divider.png"
    svg_path = ASSETS / "vault-divider.svg"

    print("Generating vault-divider (PNG + transparent SVG)...")
    image = generate_image(get_client())
    image.save(raw_path)
    print(f"  saved raw -> {raw_path.name}")

    transparent = crop_to_content(remove_background(image))
    # Fit art into exact divider dimensions (letterbox on cream if aspect differs)
    scale = min(TARGET_WIDTH / transparent.width, TARGET_HEIGHT / transparent.height)
    fitted_w = int(transparent.width * scale)
    fitted_h = int(transparent.height * scale)
    fitted = transparent.resize((fitted_w, fitted_h), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (TARGET_WIDTH, TARGET_HEIGHT), (*MATTE, 255))
    offset_x = (TARGET_WIDTH - fitted_w) // 2
    offset_y = (TARGET_HEIGHT - fitted_h) // 2
    canvas.paste(fitted, (offset_x, offset_y), fitted)
    flattened = flatten_on_matte(canvas)
    flattened.save(png_path, optimize=True)
    print(f"  saved {TARGET_WIDTH}x{TARGET_HEIGHT} cream-matte -> {png_path.name}")

    write_svg(flattened, svg_path)
    print(f"  saved SVG -> {svg_path.name}")


if __name__ == "__main__":
    main()
