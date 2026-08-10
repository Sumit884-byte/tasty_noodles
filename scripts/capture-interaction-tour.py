#!/usr/bin/env python3
"""Record a desktop interaction tour for blog-post.md (Playwright + timed clicks).

Writes a JSON interaction timeline alongside the raw webm so plan-interaction-voiceover.py
can align narration to on-screen actions.
"""

from __future__ import annotations

import asyncio
import json
import shutil
import time
from dataclasses import dataclass, field
from pathlib import Path

from playwright.async_api import Page, async_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "blog"
BASE_URL = "http://127.0.0.1:8080/"
VIEWPORT = {"width": 1440, "height": 900}
TIMELINE_FILE = ASSETS / "interaction-tour-timeline.json"


@dataclass
class Timeline:
    """Tracks elapsed ms and logs interaction events for voiceover planning."""

    started_at: float = field(default_factory=time.monotonic)
    events: list[dict] = field(default_factory=list)

    @property
    def elapsed_ms(self) -> int:
        return int((time.monotonic() - self.started_at) * 1000)

    def log(self, action: str, **fields) -> None:
        self.events.append({"elapsed_ms": self.elapsed_ms, "action": action, **fields})

    async def wait(self, page: Page, ms: int, action: str = "wait", **fields) -> None:
        if action != "wait":
            self.log(action, wait_ms=ms, **fields)
        await page.wait_for_timeout(ms)

    async def click(self, page: Page, locator, **fields) -> None:
        self.log("click", **fields)
        await locator.click()

    async def scroll_to(self, page: Page, selector: str, **fields) -> None:
        self.log("scroll", selector=selector, **fields)
        locator = page.locator(selector).first
        await locator.scroll_into_view_if_needed()
        await page.wait_for_timeout(700)

    def to_json(self) -> dict:
        return {
            "base_url": BASE_URL,
            "viewport": VIEWPORT,
            "events": self.events,
            "total_ms": self.elapsed_ms,
        }


async def wait_for_page(page: Page, tl: Timeline) -> None:
    tl.log("navigate", url=BASE_URL)
    await page.goto(BASE_URL, wait_until="networkidle", timeout=120_000)
    await tl.wait(page, 2000, action="page_ready")
    dismiss = page.locator('button:has-text("Wipe Screen")').first
    if await dismiss.count():
        try:
            await tl.click(page, dismiss, selector='button:has-text("Wipe Screen")', section="hero", label="dismiss_splash")
            await tl.wait(page, 400)
        except Exception:
            pass


async def run_interaction_tour(page: Page, tl: Timeline) -> None:
    """Timed click sequence — events logged with monotonic elapsed_ms."""
    await wait_for_page(page, tl)
    await tl.wait(page, 1500, action="intro_hold", section="hero", label="intro")

    # 1. Hero splash
    catch_btn = page.locator("#hero button").filter(has_text="TRY AND CATCH").first
    await catch_btn.scroll_into_view_if_needed()
    await tl.wait(page, 800, section="hero", label="pre_catch")
    await tl.click(page, catch_btn, selector="#hero button", section="hero", label="TRY AND CATCH")
    await tl.wait(page, 7500, section="hero", label="splash_playing")

    dismiss_splash = page.locator('button:has-text("Wipe Screen")').first
    await dismiss_splash.wait_for(state="visible", timeout=8000)
    await tl.wait(page, 1500, section="hero", label="splash_visible")
    await tl.click(page, dismiss_splash, selector='button:has-text("Wipe Screen")', section="hero", label="dismiss_splash")
    await tl.wait(page, 2000, section="hero", label="post_splash")

    # 2. Desktop nav — jump to Menu
    menu_nav = page.locator('.site-nav-link[href="#menu"]').first
    await tl.click(page, menu_nav, selector='.site-nav-link[href="#menu"]', section="nav", label="Menu")
    await tl.wait(page, 2500, section="menu", label="menu_scroll")

    # 3. Menu peacock show-more
    await tl.scroll_to(page, "#menu", section="menu", label="menu_section")
    menu_more = page.locator("#menu .section-show-more-btn").first
    await tl.click(page, menu_more, selector="#menu .section-show-more-btn", section="menu", label="peacock_show_more")
    await tl.wait(page, 3500, section="menu", label="menu_expanded")

    # 4. Build Your Bowl
    build_nav = page.locator('.site-nav-link[href="#build"]').first
    await tl.click(page, build_nav, selector='.site-nav-link[href="#build"]', section="nav", label="Build")
    await tl.wait(page, 2000, section="build", label="build_scroll")

    await tl.scroll_to(page, "#build", section="build", label="build_section")
    broth = page.locator("#build .build-chip").filter(has_text="Dragon Chili").first
    await tl.click(page, broth, selector="#build .build-chip", section="build", label="Dragon Chili")
    await tl.wait(page, 1200, section="build", label="broth_selected")

    noodles = page.locator("#build .build-chip").filter(has_text="Hand-Pulled Thick").first
    await tl.click(page, noodles, selector="#build .build-chip", section="build", label="Hand-Pulled Thick")
    await tl.wait(page, 1200, section="build", label="noodle_selected")

    topping = page.locator("#build .build-chip").filter(has_text="Jammy Egg").first
    await tl.click(page, topping, selector="#build .build-chip", section="build", label="Jammy Egg")

    lock_btn = page.locator("#build button").filter(has_text="Lock In My Plate").first
    await tl.click(page, lock_btn, selector="#build button", section="build", label="Lock In My Plate")
    await tl.wait(page, 2000, section="build", label="plate_locked")

    buy_btn = page.locator("#build .build-choice__btn--buy").first
    await tl.click(page, buy_btn, selector="#build .build-choice__btn--buy", section="build", label="Buy This Bowl")
    await tl.wait(page, 3000, section="build", label="added_to_cart")

    # 5. Gift pickers
    gift_nav = page.locator('.site-nav-link[href="#gift"]').first
    await tl.click(page, gift_nav, selector='.site-nav-link[href="#gift"]', section="nav", label="Gift")
    await tl.wait(page, 2000, section="gift", label="gift_scroll")
    await tl.scroll_to(page, "#gift", section="gift", label="gift_section")

    location_toggle = page.locator("#gift-location").first
    await tl.click(page, location_toggle, selector="#gift-location", section="gift", label="location_picker_open")
    await tl.wait(page, 1200, section="gift", label="location_picker_visible")

    location_option = page.locator('ul[aria-labelledby="gift-location-label"] .collect-picker__option').first
    await tl.click(page, location_option, selector="gift-location option", section="gift", label="location_selected")
    await tl.wait(page, 2000, section="gift", label="location_applied")

    preset_toggle = page.locator("#gift-preset").first
    await tl.click(page, preset_toggle, selector="#gift-preset", section="gift", label="preset_picker_open")
    await tl.wait(page, 1200, section="gift", label="preset_picker_visible")

    preset_option = page.locator('ul[aria-labelledby="gift-preset-label"] .collect-picker__option').first
    await tl.click(page, preset_option, selector="gift-preset option", section="gift", label="preset_selected")
    await tl.wait(page, 2500, section="gift", label="preset_applied")

    # 6. Support FAQ + peacock
    support_nav = page.locator('.site-nav-link[href="#support"]').first
    await tl.click(page, support_nav, selector='.site-nav-link[href="#support"]', section="nav", label="Support")
    await tl.wait(page, 2000, section="support", label="support_scroll")
    await tl.scroll_to(page, "#support", section="support", label="support_section")

    faq_btn = page.locator("#support [role='listitem'] button").first
    await tl.click(page, faq_btn, selector="#support FAQ", section="support", label="faq_expand")
    await tl.wait(page, 2500, section="support", label="faq_open")

    support_more = page.locator("#support .section-show-more-btn").first
    if await support_more.is_visible():
        await tl.click(page, support_more, selector="#support .section-show-more-btn", section="support", label="support_peacock")
        await tl.wait(page, 3000, section="support", label="support_expanded")

    # 7. Checkout nav (optional quick peek)
    checkout_nav = page.locator('.site-nav-link[href="#checkout"], .collect-btn--nav').first
    await tl.click(page, checkout_nav, selector="checkout nav", section="nav", label="Checkout")
    await tl.wait(page, 2500, section="checkout", label="checkout_scroll")
    await tl.scroll_to(page, "#checkout", section="checkout", label="checkout_section")
    await tl.wait(page, 2000, section="checkout", label="checkout_hold")


async def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    raw_webm = ASSETS / "interaction-tour-raw.webm"
    tl = Timeline()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport=VIEWPORT,
            device_scale_factor=1,
            record_video_dir=str(ASSETS),
            record_video_size={"width": VIEWPORT["width"], "height": VIEWPORT["height"]},
        )
        page = await context.new_page()
        await run_interaction_tour(page, tl)

        video = page.video
        await page.close()
        await context.close()
        await browser.close()

        if video is None:
            raise RuntimeError("Playwright did not record video")

        recorded = await video.path()
        shutil.move(recorded, raw_webm)

    timeline = tl.to_json()
    TIMELINE_FILE.write_text(json.dumps(timeline, indent=2), encoding="utf-8")
    print(f"Saved interaction timeline: {TIMELINE_FILE} ({len(timeline['events'])} events, {timeline['total_ms']}ms)")
    print(f"Saved raw interaction tour: {raw_webm} ({raw_webm.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    asyncio.run(main())
