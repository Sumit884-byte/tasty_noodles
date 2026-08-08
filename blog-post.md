---
title: "I Built a Noodle Shop Landing Page That Throws Food at Your Screen 🍜"
published: false
description: "How I built SLURP! — a playful comfort-food landing page with SVG splash animations, a CSS bowl builder, and a Three.js spinning globe — for the DEV Frontend Challenge."
tags: devchallenge, frontend, webdev, javascript, css, threejs
cover_image: https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/blog-cover.png
canonical_url: https://tastynoodles.vercel.app
---

_This is a submission for [Frontend Challenge - Comfort Food Edition, Perfect Landing](https://dev.to/challenges/frontend-2026-07-29)_

## What I Built

I built **[SLURP! — Tastiest Noodles on the Planet](https://tastynoodles.vercel.app)**, a single-page landing page for an imaginary noodle shop. The comfort food theme is **ramen and noodle bowls** — warm, slurpy, a little chaotic — and I leaned into that with copy, color, and interactions that feel cozy *and* playful.

The hook: Chef Marco is so confident in his noodles that he literally throws a bowl at your screen. The hero CTA is **"TRY AND CATCH THIS! 🍜"** — miss the catch, get roasted, then explore the rest of the shop.

**What's on the page:**

- **Noodle Splash Hero** — full-screen SVG + CSS animation (sauce smears, flying noodle clusters, garnishes, a frosted-glass "SPLAAAT!" modal). Each replay seeds random extra strands in JavaScript so the splatter feels slightly different every time.
- **The Noodle Vault** — six signature bowls in a CollectUI-inspired card grid (Dragon Breath Chili Oil, Midnight Tonkotsu, Garlic Butter Dan Dan, Bombay Street Manchow, Golden Curry Udon, Peanut Crunch Yakisoba) with category filter chips and wavy noodle-strand SVG borders generated at runtime.
- **Build Your Bowl** — live CSS plate preview (broth color, thick/thin/broth-only noodles, six toppings). No image swaps — just custom properties, positioned elements, and steam keyframes. Hit **"That's My Plate"** and it drops into the cart with a generated name.
- **Galactic Slurp** — story section with a Three.js spinning globe, alien rider, and twinkling stars (static fallback for `prefers-reduced-motion` and WebGL failures).
- **Pan India Store Finder** — 15 kitchens across 12 cities, searchable by city, area, or pincode, with Google Maps directions.
- **Slurp Squad** — eight fake testimonials from regulars who also failed to catch the noodles.
- **Social Feed Preview** — Reels/Stories/TikTok-style cards using the same self-hosted bowl photos (platform buttons are visual-only demos).
- **CollectUI Checkout Flow** — Alpine.js cart with sticky bar, mobile bottom sheet, and a full client-side order flow.

**Stack:** one `index.html` file — HTML, Tailwind CSS (CDN), Alpine.js 3.14, Three.js 0.172, vanilla JS, Lucide icons, Chewy font. No build step. All images self-hosted in `/assets`. MIT licensed.

**Source:** [github.com/Sumit884-byte/tasty_noodles](https://github.com/Sumit884-byte/tasty_noodles)

## Demo

**Live site:** [tastynoodles.vercel.app](https://tastynoodles.vercel.app)

Click **TRY AND CATCH THIS!** on the hero — that's the centerpiece interaction. Append `?splash` to the URL if you want to land directly in the splatter overlay.

**Screenshots:**

![SLURP! hero — "Our Noodles Are Tastiest"](https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/blog-cover.png)

![Build Your Bowl — live CSS plate preview](https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/build-your-bowl.png)

**Links:**

- 🍜 Live demo: [tastynoodles.vercel.app](https://tastynoodles.vercel.app)
- 📦 Source: [github.com/Sumit884-byte/tasty_noodles](https://github.com/Sumit884-byte/tasty_noodles)

## Journey

### Why noodles?

The [DEV Frontend Challenge](https://dev.to/challenges/frontend-2026-07-29) prompt was comfort food — not "a nice restaurant site," but something that makes you hungry just thinking about it. Noodles felt right: warm broth, slurping sounds, late-night cravings. I wanted the page to feel like a **brand**, not a template — chunky typography, an amber/orange/stone palette, and interactions that reward curiosity.

### Process

I started with the splash hero because it set the tone. Pure SVG + CSS — no canvas, no video, no Lottie. `stroke-dashoffset` for smears and strands, staggered keyframes for clusters and garnishes, JavaScript to seed random extra strands on each replay.

From there I built outward: menu cards with runtime-generated wavy SVG borders, the CSS-only bowl builder (my favorite section technically — a well-structured DOM + custom properties replaced a lot of image-swap logic), then the Three.js globe with performance guardrails (IntersectionObserver to pause off-screen, `visibilitychange` for hidden tabs, adaptive geometry, `pixelRatio` cap, static fallback for reduced motion).

Alpine.js became the app's brain — one `slurpApp()` component handles cart, custom plate builder, store locator, menu filtering, splash overlay, mobile nav, and checkout. Accessibility was baked in from the start: skip link, splash dialog with focus management, `aria-pressed` on builder chips, `prefers-reduced-motion` disabling splash/globe/steam animations, semantic landmarks, lazy-loaded images with explicit dimensions.

### What I'm proud of

- The splash animation — elaborate, replayable, and still pure SVG/CSS
- The CSS bowl preview — instant, lightweight, infinitely recombinable
- Wavy SVG card borders via `attachNoodleFrame()` — micro-detail that makes the UI feel designed
- Progressive enhancement for motion and WebGL — fun features that don't punish users who prefer reduced motion or lack WebGL
- Shipping everything in one file you can open locally without explaining npm

### What I learned

**Commit to the joke, but ship real craft.** The copy is silly; underneath there's form validation, accessible modals, performance-conscious 3D, and responsive layouts.

**CSS can do more than I thought.** The bowl preview taught me that custom properties + keyframes can replace a lot of asset-heavy UI logic.

**Constraints spark creativity.** "Comfort food" pushed me toward warmth and interactivity instead of a generic SaaS layout.

**Single-file projects are underrated.** For a challenge submission or portfolio piece, one `index.html` felt like a superpower.

### What's next?

This was a challenge submission, not a production restaurant platform — but there's room to grow:

- Extract the splash animation into a reusable Web Component
- Add sound effects (with mute toggle)
- Wire up real social links if SLURP! ever becomes a real brand
- **India wireframe map with store pins** — a sketch-style outline of the country with clickable markers for each kitchen, tied into the existing store finder
- **Peacock feather expansion on show-more** — the peacock buttons already reveal extra cards; next up is a feather-fan unfold animation on click, so expanding a section feels like the bird opening its tail

For now, I'm happy with what I shipped: a page that makes people smile, teaches a few frontend tricks, and proves that comfort food deserves better than a stock photo and an "Order Now" button.

If you're participating in the challenge — or you've built something fun for it already — drop a link in the comments. I want to see your comfort food takes.

And if you try to catch the noodles... good luck. Chef Marco doesn't believe in you. 🍜

---

*Built with too much chili oil and not enough sleep. MIT licensed — see [LICENSE](https://github.com/Sumit884-byte/tasty_noodles/blob/main/LICENSE).*
