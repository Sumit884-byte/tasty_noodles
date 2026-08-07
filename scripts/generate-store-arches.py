#!/usr/bin/env python3
"""Generate store-section jharokha arch decorations and remove backgrounds."""

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
    "stores-arch-left.png": (
        "Generate a tall vertical Indian jharokha arch window illustration for a website "
        "left sidebar decoration. Hand-drawn ink sketch style with warm orange (#ea580c) "
        "line art. Ornate Mughal-style pointed arch frame with intricate floral vine "
        "patterns inside and two small peacocks among the foliage. Vertical portrait "
        "orientation, full height decorative panel. Plain solid pure white background only. "
        "No text, no shadow, no border frame around the image."
    ),
    "stores-arch-right.png": (
        "Generate a vertical Indian pavilion arch illustration for a website right sidebar "
        "decoration. Hand-drawn ink sketch style with warm orange (#ea580c) line art. "
        "Ornate pointed arch frame containing a banyan tree inside a small open pavilion "
        "or gazebo structure. Decorative traditional Indian architectural motif. Vertical "
        "portrait orientation. Plain solid pure white background only. No text, no shadow, "
        "no border around the image."
    ),
}

TARGET_HEIGHTS = {
    "stores-arch-left.png": 720,
    "stores-arch-right.png": 560,
}

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


def generate_image(client: genai.Client, prompt: str) -> Image.Image:
    last_error: Exception | None = None
    for model in MODELS:
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
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
    try:
        from rembg import remove  # type: ignore

        result = remove(image.convert("RGBA"))
        if isinstance(result, bytes):
            return Image.open(io.BytesIO(result)).convert("RGBA")
        return result.convert("RGBA")
    except ImportError:
        rgba = image.convert("RGBA")
        pixels = rgba.load()
        width, height = rgba.size
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                if r >= 245 and g >= 245 and b >= 245:
                    pixels[x, y] = (r, g, b, 0)
        return rgba


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    client = get_client()

    for filename, prompt in PROMPTS.items():
        raw_path = ASSETS / filename.replace(".png", "-raw.png")
        out_path = ASSETS / filename
        target_h = TARGET_HEIGHTS[filename]

        print(f"Generating {filename}...")
        image = generate_image(client, prompt)
        image.save(raw_path)
        print(f"  saved raw -> {raw_path.name}")

        transparent = remove_background(image)
        w, h = transparent.size
        target_w = int(w * (target_h / h))
        transparent = transparent.resize((target_w, target_h), Image.Resampling.LANCZOS)
        transparent.save(out_path, optimize=True)
        print(f"  saved transparent -> {out_path.name}")


if __name__ == "__main__":
    main()
