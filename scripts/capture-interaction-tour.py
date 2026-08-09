#!/usr/bin/env python3
"""Record a desktop interaction tour for blog-post.md (Playwright + timed clicks)."""

from __future__ import annotations

import asyncio
import shutil
from pathlib import Path

from playwright.async_api import Page, async_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "blog"
BASE_URL = "http://127.0.0.1:8080/"
VIEWPORT = {"width": 1440, "height": 900}


async def wait_for_page(page: Page) -> None:
    await page.goto(BASE_URL, wait_until="networkidle", timeout=120_000)
    await page.wait_for_timeout(2000)
    dismiss = page.locator('button:has-text("Wipe Screen")').first
    if await dismiss.count():
        try:
            await dismiss.click(timeout=1500)
            await page.wait_for_timeout(400)
        except Exception:
            pass


async def scroll_to(page: Page, selector: str) -> None:
    locator = page.locator(selector).first
    await locator.scroll_into_view_if_needed()
    await page.wait_for_timeout(700)


async def run_interaction_tour(page: Page) -> None:
    """Timed click sequence — keep delays in sync with interaction-voiceover-script.md."""
    await wait_for_page(page)
    await page.wait_for_timeout(1500)

    # 1. Hero splash
    catch_btn = page.locator("#hero button").filter(has_text="TRY AND CATCH").first
    await catch_btn.scroll_into_view_if_needed()
    await page.wait_for_timeout(800)
    await catch_btn.click()
    await page.wait_for_timeout(7500)

    dismiss_splash = page.locator('button:has-text("Wipe Screen")').first
    await dismiss_splash.wait_for(state="visible", timeout=8000)
    await page.wait_for_timeout(1500)
    await dismiss_splash.click()
    await page.wait_for_timeout(2000)

    # 2. Desktop nav — jump to Menu
    menu_nav = page.locator('.site-nav-link[href="#menu"]').first
    await menu_nav.click()
    await page.wait_for_timeout(2500)

    # 3. Menu peacock show-more
    await scroll_to(page, "#menu")
    menu_more = page.locator("#menu .section-show-more-btn").first
    await menu_more.click()
    await page.wait_for_timeout(3500)

    # 4. Build Your Bowl
    build_nav = page.locator('.site-nav-link[href="#build"]').first
    await build_nav.click()
    await page.wait_for_timeout(2000)

    await scroll_to(page, "#build")
    broth = page.locator("#build .build-chip").filter(has_text="Dragon Chili").first
    await broth.click()
    await page.wait_for_timeout(1200)

    noodles = page.locator("#build .build-chip").filter(has_text="Hand-Pulled Thick").first
    await noodles.click()
    await page.wait_for_timeout(1200)

    topping = page.locator("#build .build-chip").filter(has_text="Jammy Egg").first
    await topping.click()

    lock_btn = page.locator("#build button").filter(has_text="Lock In My Plate").first
    await lock_btn.click()
    await page.wait_for_timeout(2000)

    buy_btn = page.locator("#build .build-choice__btn--buy").first
    await buy_btn.click()
    await page.wait_for_timeout(3000)

    # 5. Gift pickers
    gift_nav = page.locator('.site-nav-link[href="#gift"]').first
    await gift_nav.click()
    await page.wait_for_timeout(2000)
    await scroll_to(page, "#gift")

    location_toggle = page.locator("#gift-location").first
    await location_toggle.click()
    await page.wait_for_timeout(1200)

    location_option = page.locator('ul[aria-labelledby="gift-location-label"] .collect-picker__option').first
    await location_option.click()
    await page.wait_for_timeout(2000)

    preset_toggle = page.locator("#gift-preset").first
    await preset_toggle.click()
    await page.wait_for_timeout(1200)

    preset_option = page.locator('ul[aria-labelledby="gift-preset-label"] .collect-picker__option').first
    await preset_option.click()
    await page.wait_for_timeout(2500)

    # 6. Support FAQ + peacock
    support_nav = page.locator('.site-nav-link[href="#support"]').first
    await support_nav.click()
    await page.wait_for_timeout(2000)
    await scroll_to(page, "#support")

    faq_btn = page.locator("#support [role='listitem'] button").first
    await faq_btn.click()
    await page.wait_for_timeout(2500)

    support_more = page.locator("#support .section-show-more-btn").first
    if await support_more.is_visible():
        await support_more.click()
        await page.wait_for_timeout(3000)

    # 7. Checkout nav (optional quick peek)
    checkout_nav = page.locator('.site-nav-link[href="#checkout"], .collect-btn--nav').first
    await checkout_nav.click()
    await page.wait_for_timeout(2500)
    await scroll_to(page, "#checkout")
    await page.wait_for_timeout(2000)


async def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    raw_webm = ASSETS / "interaction-tour-raw.webm"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport=VIEWPORT,
            device_scale_factor=1,
            record_video_dir=str(ASSETS),
            record_video_size={"width": VIEWPORT["width"], "height": VIEWPORT["height"]},
        )
        page = await context.new_page()
        await run_interaction_tour(page)

        video = page.video
        await page.close()
        await context.close()
        await browser.close()

        if video is None:
            raise RuntimeError("Playwright did not record video")

        recorded = await video.path()
        shutil.move(recorded, raw_webm)

    print(f"Saved raw interaction tour: {raw_webm} ({raw_webm.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    asyncio.run(main())
