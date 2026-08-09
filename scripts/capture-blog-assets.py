#!/usr/bin/env python3
"""Capture section screenshots and full-page scroll video for blog-post.md."""

from __future__ import annotations

import asyncio
import shutil
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SECTIONS_DIR = ASSETS / "blog-sections"
BASE_URL = "http://127.0.0.1:8080/"
VIEWPORT = {"width": 1440, "height": 900}

SECTIONS = [
    ("hero", "Hero — noodle splash landing"),
    ("menu", "The Noodle Vault — menu cards"),
    ("build", "Build Your Bowl — CSS plate preview"),
    ("story", "Galactic Slurp — Three.js globe story"),
    ("stores", "Pan India Store Finder"),
    ("reviews", "Slurp Squad — testimonials"),
    ("social", "Social Feed Preview"),
    ("gift", "Gift a Bowl"),
    ("support", "Slurp Support — contact and FAQ"),
    ("checkout", "CollectUI Checkout Flow"),
]

LEGACY_ALIASES = {
    "hero": ASSETS / "blog-cover.png",
    "build": ASSETS / "build-your-bowl.png",
}


async def wait_for_page(page) -> None:
    await page.goto(BASE_URL, wait_until="networkidle", timeout=120_000)
    await page.wait_for_timeout(2500)
    # Dismiss splash overlay if present (hero CTA may have opened it on prior visit).
    close = page.locator('[aria-label="Close splash"], button:has-text("Close")').first
    if await close.count():
        try:
            await close.click(timeout=1500)
            await page.wait_for_timeout(400)
        except Exception:
            pass


async def capture_sections(page) -> list[Path]:
    SECTIONS_DIR.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []

    for section_id, _label in SECTIONS:
        locator = page.locator(f"#{section_id}")
        await locator.scroll_into_view_if_needed()
        await page.wait_for_timeout(800)

        out = SECTIONS_DIR / f"{section_id}.png"
        await locator.screenshot(path=str(out), animations="disabled")
        saved.append(out)

        alias = LEGACY_ALIASES.get(section_id)
        if alias:
            shutil.copy2(out, alias)
            saved.append(alias)

    return saved


async def smooth_scroll(page, duration_ms: int = 45_000) -> None:
    metrics = await page.evaluate(
        """() => ({
            height: Math.max(
              document.body.scrollHeight,
              document.documentElement.scrollHeight
            ),
            viewport: window.innerHeight
        })"""
    )
    total = max(metrics["height"] - metrics["viewport"], 0)
    steps = 180
    delay = duration_ms / steps

    await page.evaluate("window.scrollTo(0, 0)")
    await page.wait_for_timeout(600)

    for i in range(steps + 1):
        y = int(total * (i / steps))
        await page.evaluate("(y) => window.scrollTo(0, y)", y)
        await page.wait_for_timeout(delay)


async def capture_scroll_video(page, context) -> Path:
    video_path = ASSETS / "blog-scroll-demo.webm"
    if video_path.exists():
        video_path.unlink()

    await wait_for_page(page)
    await smooth_scroll(page, duration_ms=50_000)
    await page.wait_for_timeout(800)

    video = page.video
    await page.close()
    await context.close()

    if video is None:
        raise RuntimeError("Playwright did not record video")

    raw = await video.path()
    shutil.move(raw, video_path)
    return video_path


async def main() -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # Section screenshots (no video).
        shot_context = await browser.new_context(
            viewport=VIEWPORT,
            device_scale_factor=1,
        )
        shot_page = await shot_context.new_page()
        await wait_for_page(shot_page)
        section_paths = await capture_sections(shot_page)
        await shot_context.close()

        # Scroll demo video.
        video_context = await browser.new_context(
            viewport=VIEWPORT,
            device_scale_factor=1,
            record_video_dir=str(ASSETS),
            record_video_size={"width": VIEWPORT["width"], "height": VIEWPORT["height"]},
        )
        video_page = await video_context.new_page()
        video_path = await capture_scroll_video(video_page, video_context)

        await browser.close()

    print("Saved section screenshots:")
    for path in section_paths:
        print(f"  {path} ({path.stat().st_size // 1024} KB)")
    print(f"Saved scroll video: {video_path} ({video_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    asyncio.run(main())
