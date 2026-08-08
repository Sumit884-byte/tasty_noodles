#!/usr/bin/env python3
"""Record gift form dropdown demo video via Playwright."""

from __future__ import annotations

import asyncio
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "assets" / "screenshots"
URL = "http://127.0.0.1:8766/index.html"
VIDEO_PATH = OUTPUT_DIR / "gift-dropdowns-demo.webm"
MP4_PATH = OUTPUT_DIR / "gift-dropdowns-demo.mp4"
FRAME_PATH = OUTPUT_DIR / "gift-dropdowns-final-frame.png"

DEMO_SCRIPT = """
async () => {
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const app = Alpine.$data(document.body);
  if (!app?.toggleGiftLocationMenu) throw new Error('Gift form not ready');

  document.querySelector('#gift')?.scrollIntoView({ block: 'start' });
  location.hash = '#gift';
  await sleep(1200);

  app.giftTo = 'Priya';
  app.giftFrom = 'Arjun';
  await sleep(700);

  app.closeGiftPickers('location');
  app.giftLocationMenuOpen = true;
  await sleep(900);

  app.giftLocationSearch = 'bandra';
  await sleep(900);

  app.selectGiftLocation('mum-1');
  await sleep(1200);

  app.closeGiftPickers('preset');
  app.giftPresetMenuOpen = true;
  await sleep(900);

  app.giftPresetSearch = 'birthday';
  await sleep(900);

  app.selectGiftPreset(4);
  await sleep(1200);

  app.closeGiftPickers('bowl');
  app.giftBowlMenuOpen = true;
  await sleep(900);

  app.selectGiftBowl('dragon-breath');
  await sleep(2000);
}
"""


async def main() -> None:
    from playwright.async_api import async_playwright

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 900},
            record_video_dir=str(OUTPUT_DIR),
            record_video_size={"width": 1280, "height": 900},
        )
        page = await context.new_page()
        await page.goto(URL, wait_until="load", timeout=60_000)
        await page.wait_for_function(
            "() => window.Alpine && typeof Alpine.$data(document.body)?.toggleGiftLocationMenu === 'function'",
            timeout=30_000,
        )
        await page.wait_for_timeout(1500)
        await page.evaluate(DEMO_SCRIPT)
        await page.screenshot(path=str(FRAME_PATH), full_page=False)
        video = page.video
        await page.close()
        await context.close()
        await browser.close()

        if video:
            raw = await video.path()
            if raw and Path(raw).exists():
                if VIDEO_PATH.exists():
                    VIDEO_PATH.unlink()
                Path(raw).rename(VIDEO_PATH)

    print(f"webm: {VIDEO_PATH}")
    print(f"frame: {FRAME_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
