#!/usr/bin/env python3
"""Generate store-section elephant sketch and remove background."""

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

PROMPT = (
    "Generate a single cute Indian elephant sketch illustration for a food website sidebar. "
    "Hand-drawn pencil and ink sketch style with warm orange decorative blanket on its back. "
    "Elephant facing right, full body visible, playful friendly character. "
    "Plain solid pure white background only. No text, no shadow, no border, no other objects."
)

MODELS = [
    "gemini-2.5-flash-image",
    "gemini-3.1-flash-image",
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
                    image_config=types.ImageConfig(aspect_ratio="3:4"),
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


def remove_background(image: Image.Image) -> Image.Image:
    from rembg import remove  # type: ignore

    result = remove(image.convert("RGBA"))
    if isinstance(result, bytes):
        return Image.open(io.BytesIO(result)).convert("RGBA")
    return result.convert("RGBA")


def write_embedded_svg(image: Image.Image, out_path: Path) -> None:
    import base64

    w, h = image.size
    buf = io.BytesIO()
    image.save(buf, format="PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true">\n'
        f'  <image width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" '
        f'xlink:href="data:image/png;base64,{b64}"/>\n'
        f"</svg>\n"
    )
    out_path.write_text(svg)


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    raw_path = ASSETS / "stores-elephant-raw.png"
    out_path = ASSETS / "stores-elephant.png"
    svg_path = ASSETS / "stores-elephant.svg"

    print("Generating stores-elephant.png + stores-elephant.svg...")
    image = generate_image(get_client())
    image.save(raw_path)
    print(f"  saved raw -> {raw_path.name}")

    transparent = remove_background(image)
    w, h = transparent.size
    target_h = 640
    target_w = int(w * (target_h / h))
    transparent = transparent.resize((target_w, target_h), Image.Resampling.LANCZOS)
    transparent.save(out_path, optimize=True)
    print(f"  saved transparent -> {out_path.name}")
    write_embedded_svg(transparent, svg_path)
    print(f"  saved embedded SVG -> {svg_path.name}")


if __name__ == "__main__":
    main()
