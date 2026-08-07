#!/usr/bin/env python3
"""Generate store section mandala flowers with Gemini and remove backgrounds."""

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

PROMPTS = {
    "stores-flower-orange.png": (
        "Generate a single ornate Indian mandala-style decorative flower illustration "
        "for a website corner background. Warm orange line art (#ea580c) with subtle "
        "peach fills on petals. Intricate concentric circles, layered curved petals, "
        "rangoli-inspired symmetry, centered composition. Plain solid pure white "
        "background (#FFFFFF) only. No text, no shadow, no border, no other objects."
    ),
    "stores-flower-green.png": (
        "Generate a single ornate Indian mandala-style decorative flower illustration "
        "for a website corner background. Rich green line art (#15803d) with subtle "
        "mint fills on petals. Intricate concentric circles, layered curved petals, "
        "rangoli-inspired symmetry, centered composition. Plain solid pure white "
        "background (#FFFFFF) only. No text, no shadow, no border, no other objects."
    ),
}

MODELS = [
    "gemini-2.5-flash-image",
    "gemini-2.0-flash-preview-image-generation",
    "gemini-3.1-flash-image",
]


def get_client() -> genai.Client:
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise SystemExit("Set GEMINI_API_KEY or GOOGLE_API_KEY")
    # Prefer GEMINI_API_KEY when both are set (SDK otherwise picks GOOGLE_API_KEY).
    if os.environ.get("GEMINI_API_KEY"):
        os.environ.pop("GOOGLE_API_KEY", None)
    return genai.Client(api_key=api_key)


def generate_image(client: genai.Client, prompt: str) -> Image.Image:
    last_error: Exception | None = None
    for model in MODELS:
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"],
                    image_config=types.ImageConfig(aspect_ratio="1:1"),
                ),
            )
        except Exception as exc:  # noqa: BLE001 - try next model
            last_error = exc
            print(f"  model {model} failed: {exc}", file=sys.stderr)
            continue

        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.data:
                print(f"  generated with {model}")
                return Image.open(io.BytesIO(part.inline_data.data)).convert("RGBA")

        last_error = RuntimeError(f"{model} returned no image")

    raise RuntimeError(f"All models failed. Last error: {last_error}")


def remove_white_background(image: Image.Image, threshold: int = 245) -> Image.Image:
    rgba = image.convert("RGBA")
    pixels = rgba.load()
    width, height = rgba.size

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if r >= threshold and g >= threshold and b >= threshold:
                pixels[x, y] = (r, g, b, 0)

    return rgba


def remove_background(image: Image.Image) -> Image.Image:
    try:
        from rembg import remove  # type: ignore

        result = remove(image.convert("RGBA"))
        if isinstance(result, bytes):
            return Image.open(io.BytesIO(result)).convert("RGBA")
        return result.convert("RGBA")
    except ImportError:
        print("  rembg not installed, using white-key removal", file=sys.stderr)
        return remove_white_background(image)


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    client = get_client()

    for filename, prompt in PROMPTS.items():
        out_path = ASSETS / filename
        raw_path = ASSETS / filename.replace(".png", "-raw.png")
        print(f"Generating {filename}...")
        image = generate_image(client, prompt)
        image.save(raw_path)
        print(f"  saved raw -> {raw_path.name}")

        transparent = remove_background(image)
        transparent.save(out_path, optimize=True)
        print(f"  saved transparent -> {out_path.name}")


if __name__ == "__main__":
    main()
