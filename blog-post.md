---
title: "I Built a Noodle Shop Landing Page That Throws Food at Your Screen 🍜"
published: false
description: "How I built SLURP! — a playful comfort-food landing page with SVG splash animations, a CSS bowl builder, and a Three.js spinning globe — for the DEV Frontend Challenge."
tags: devchallenge, frontend, webdev, javascript, css, threejs
cover_image: https://tastynoodles.vercel.app/assets/noodle-splash.png
canonical_url: https://tastynoodles.vercel.app
---

**TL;DR:** I built [SLURP! — Tastiest Noodles on the Planet](https://tastynoodles.vercel.app) for the [DEV Frontend Challenge: Comfort Food Edition](https://dev.to/challenges/frontend-2026-07-29). It's a single-page imaginary noodle shop with a full-screen SVG splash animation, a 6-bowl CollectUI-style menu, a live CSS bowl builder, pan-India store finder, 8 Slurp Squad reviews, a Three.js globe, and a CollectUI cart/checkout flow — all in one `index.html` file. Source: [github.com/Sumit884-byte/tasty_noodles](https://github.com/Sumit884-byte/tasty_noodles).

---

## The hook that started it all

The brief was comfort food. Not "a nice restaurant site." Not "a recipe blog." **Comfort food** — the kind that makes you hungry just thinking about it.

So I leaned into the bit: what if a noodle shop was so confident in its product that Chef Marco literally *throws* a bowl at your screen and dares you to catch it?

That's **SLURP!** — an imaginary noodle shop where the hero CTA is "TRY AND CATCH THIS! 🍜" and missing the catch is part of the experience.

> *"Our Noodles Are Tastiest. You Don't Believe Me?"*

If you haven't tried it yet, [open the live demo](https://tastynoodles.vercel.app) and click the red button. I'll wait.

---

## Why this challenge was fun

The [DEV Frontend Challenge: Comfort Food Edition](https://dev.to/challenges/frontend-2026-07-29) is one of those prompts where the constraint actually helps creativity. "Comfort food" gives you warmth, nostalgia, and permission to be playful — but you still need real frontend craft to pull it off.

I wanted the page to feel like a **brand**, not a template:

- Bold, chunky typography with a hand-drawn energy
- A coherent warm palette (amber, orange, stone)
- Interactions that reward curiosity
- Enough polish that it could plausibly ship as a real landing page

No framework. No build step. Just HTML, Tailwind, Alpine.js, Three.js, and a lot of CSS keyframes.

---

## Feature walkthrough

Here's what you'll find scrolling through the page — and what I had the most fun building.

### 1. The Noodle Splash Hero

The centerpiece interaction: click **"TRY AND CATCH THIS!"** and noodles splatter across your entire viewport.

This is pure **SVG + CSS animation** — no canvas, no video, no Lottie files:

- Sauce smears draw in with `stroke-dashoffset` animations
- Noodle clusters slam in from opposite corners (`cluster-slam`, `cluster-fly`)
- Individual strands pop with staggered delays
- Garnishes burst in with a springy scale animation
- A frosted-glass modal appears: *"SPLAAAT! Oh... you couldn't catch that? Too slow!"*

Each replay also **seeds random extra strands** via JavaScript, so the splatter feels slightly different every time. Chef Marco's speech bubble even updates to roast you.

**Screenshots in repo:** `splash-check/website-pc.png`, `assets/splat-modal.png`, `assets/noodle-splash.png`

![Noodle splash hero on desktop](https://tastynoodles.vercel.app/assets/noodle-splash.png)

### 2. The Noodle Vault (Menu)

Six signature bowls in a **CollectUI-inspired card grid** — each with its own self-hosted photo, rating, prep time, and category badge:

| Bowl | Vibe | Price |
|------|------|-------|
| **Dragon Breath Chili Oil** | 🌶️ Spicy AF | $14.99 |
| **Midnight Tonkotsu** | ⭐ Best Seller | $16.50 |
| **Garlic Butter Dan Dan** | 🌱 Umami Bomb | $15.20 |
| **Bombay Street Manchow** | 🇮🇳 Desi Hit | $13.99 |
| **Golden Curry Udon** | 🍛 Cozy | $15.99 |
| **Peanut Crunch Yakisoba** | 🔥 Wok Tossed | $14.50 |

Horizontal **category filter chips** (All Bowls, Spicy, Best Sellers, Comfort, Indo-Chinese, Wok Tossed) let you browse without leaving the page. Each card has a floating **+** add button in classic food-delivery UI style.

Every menu card gets a **wavy noodle-strand border** — SVG paths generated at runtime by a vanilla JS helper that draws sinusoidal edges around each card. It's a small detail, but it ties the whole visual language together.

Images live in `/assets` — six unique bowl photos plus logo, chef, and globe texture. No external image CDN dependencies.

**Screenshots in repo:** `page-screenshot.png/website-pc.png`, `build-check/website-tablet.png`

### 3. Build Your Bowl — Live CSS Plate Preview

This might be my favorite section technically.

Instead of swapping images when you customize your bowl, the preview is **100% CSS**:

- Broth color changes via CSS custom properties (`--broth-color`)
- Noodle thickness toggles between thick, thin, or **Broth Only** (no noodles)
- Visible **white ceramic rim** and broth pool around the noodle cluster — the bowl reads clearly even before toppings land
- Toppings (scallion, jammy egg, chashu, chili crisp, sesame, peanuts) are individual positioned elements that show/hide with Alpine.js
- Rising steam wisps animate in the background

Pick your combo, hit **"That's My Plate"**, and it drops into the cart with a generated name like *"Dragon Breath Custom"* and a description of your exact configuration.

No image assets needed for the preview — which means it's instant, lightweight, and infinitely recombinable.

**Screenshots in repo:** `build-check/website-pc.png`, `build-check/website-mobile.png`

### 4. Galactic Slurp — Three.js Spinning Globe

Because Earth's love of noodles became *too powerful for one planet*, obviously.

The story section features:

- A **Three.js WebGL globe** with an earth texture, Phong shading, and a subtle atmosphere shell
- A CSS-only **alien rider** blasting off with a bowl in hand
- Twinkling stars, a dashed noodle trail, and copy that commits fully to the bit

The globe respects `prefers-reduced-motion` — when enabled, it falls back to a static `earth-map.jpg` image instead of spinning. WebGL failures degrade gracefully the same way.

**Screenshot reference:** scroll to `#story` on the live demo, or see `splash-check/website-pc.png` for the full-page context.

### 5. Pan India Store Finder

SLURP! isn't just delivery — **15 physical kitchens across 12 Indian cities**, searchable from the page:

- City filter tabs (Mumbai, Delhi, Bengaluru, Hyderabad, Chennai, and more)
- Search by city, area, or pincode
- Full address, hours, phone, and **Get Directions** (Google Maps) per store
- Alpine.js-powered filtering with live result count

Scroll to **Find Stores** (`#stores`) on the live demo.

### 6. Slurp Squad Reviews

Eight fake testimonials from people who "failed to catch the noodles" — including Mumbai, Bengaluru, Delhi, and Hyderabad regulars. Star ratings, avatar initials, and the same wavy card borders as the menu.

### 7. Social Feed Preview

A **social feed preview** with Reels, Stories, and TikTok-style cards — all using the same self-hosted bowl photos.

The platform buttons (Instagram, X, YouTube, TikTok) are visual-only demos marked with `aria-disabled="true"`. Honest about being a landing page, not a real social presence.

### 8. CollectUI Checkout Flow

Alpine.js powers a real (client-side) cart with **CollectUI-style buttons**:

- Dark pill cart icon in the nav with live item count
- **Sticky cart bar** — white floating shell, dark rounded button showing `3 items · View Cart · $45.00 →`
- Full-width mobile bottom sheet with safe-area padding
- Orange gradient **Place Order** pill on the checkout form
- Instant jump to `#checkout` (no long smooth scroll from top of page)
- Add menu items or custom bowls, see running total, remove items
- Submit with name + address → *"Your noodles are sprinting to your door."*

It's not a real payment processor — but the flow feels complete enough that you can demo the full user journey in one sitting.

---

## Technical highlights

### Stack (intentionally simple)

```
HTML + Tailwind CSS (CDN)
Alpine.js 3.14       → state management
Three.js 0.172       → 3D globe (ES module import)
Vanilla JavaScript   → SVG frame generation, splash seeding
Lucide               → icons
Chewy (Google Fonts) → brand wordmark styling
```

One file. Deploy anywhere static files go. I used [Vercel](https://tastynoodles.vercel.app).

### Alpine.js as the app's brain

All interactive state lives in a single `slurpApp()` component:

- Cart management (`addToCart`, `removeFromCart`, `cartTotal`)
- Custom plate builder (`customPlate`, `toggleTopping`, `brothColor` getter)
- Store locator (`storeLocations`, `filteredStores`, `directionsUrl`)
- Menu filtering (`menuItems`, `filteredMenuItems`, `selectedMenuCategory`)
- Instant checkout navigation (`goToCheckout` — bypasses global smooth scroll)
- Splash overlay toggle (`throwNoodles`, `dismissSplash`)
- Mobile nav, checkout validation, order confirmation

Alpine's `x-cloak`, `x-show`, and `@keydown.escape` made modal behavior and accessibility straightforward without reaching for a heavier framework.

### Three.js with performance guardrails

The globe isn't just "drop Three.js on the page and hope." I added:

- **IntersectionObserver** — stops rendering when the globe scrolls out of view
- **`visibilitychange` listener** — pauses when the tab is hidden
- **Adaptive geometry** — 32 segments on mobile, 48 on desktop
- **`pixelRatio` cap** at 2
- **`pagehide` cleanup** — disposes geometry, materials, and renderer
- **Static fallback** for reduced motion and WebGL failures

These are small lines of code that make a big difference on lower-end devices and battery life.

### Accessibility baked in, not bolted on

- Skip link to main content
- Splash dialog with `role="dialog"`, `aria-modal`, focus management on open
- `aria-pressed` on bowl builder chips
- `aria-label` on cart/checkout buttons with dynamic item counts
- `prefers-reduced-motion` media query that disables splash, globe, alien, and steam animations
- Semantic landmarks (`header`, `main`, `footer`, `nav`)
- Lazy-loaded images with explicit `width`/`height` to reduce layout shift

### Self-hosted assets

Every image ships from `/assets`:

- `slurp-logo.png`
- `chef-marco.jpg`
- Bowl photos (chili, tonkotsu, dan dan, manchow, curry udon, yakisoba)
- `earth-map.jpg` (globe texture + fallback)
- `noodle-splash.png`, `splat-modal.png` (marketing/preview)

No hotlinked Unsplash URLs. The page loads the same way in six months as it does today.

### Wavy SVG borders (the detail I'm weirdly proud of)

Cards get noodle-shaped frames via `attachNoodleFrame()` — functions that compute wavy SVG paths using quadratic Bézier curves, then attach them with `ResizeObserver` so they scale with the element. Checkout uses separate **CollectUI-style** rounded pills with soft elevation shadows instead.

It's the kind of micro-interaction that doesn't show up in a feature list but makes the UI feel *designed*.

---

## Lessons learned

**1. Commit to the joke, but ship real craft.**

The copy is silly. The animations are elaborate. But underneath, there's proper form validation, accessible modals, performance-conscious 3D, and responsive layouts. Playfulness and professionalism aren't opposites.

**2. CSS can do more than you think.**

The bowl preview taught me that a well-structured DOM + custom properties + a handful of keyframes can replace a lot of image-swap logic. Faster, lighter, more flexible.

**3. Progressive enhancement for motion.**

The splash is fun. The globe is cool. Neither should punish users who prefer reduced motion or lack WebGL. Fallbacks aren't afterthoughts — they're part of the feature.

**4. Single-file projects are underrated.**

For a challenge submission or portfolio piece, one `index.html` that you can open locally, deploy to Vercel in 30 seconds, and hand to someone without explaining npm is a superpower.

**5. Constraints spark creativity.**

"Comfort food" pushed me toward warmth and interactivity instead of a generic SaaS layout. The DEV challenge format is great precisely because it gives you a starting direction without prescribing the destination.

---

## Try it yourself

🍜 **Live demo:** [tastynoodles.vercel.app](https://tastynoodles.vercel.app)

✏️ **CodePen:** [Deploy on CodePen](https://tastynoodles.vercel.app/codepen/) — open the link, click **Open in CodePen**, log in, **Save**, set **Public**, share your pen URL.

📦 **Source code:** [github.com/Sumit884-byte/tasty_noodles](https://github.com/Sumit884-byte/tasty_noodles)

Clone it, run any static server, and poke around:

```bash
git clone https://github.com/Sumit884-byte/tasty_noodles.git
cd tasty_noodles
python3 -m http.server 8080
# Open http://localhost:8080
```

**Pro tip:** Append `?splash` to the URL to land directly in the noodle splatter overlay — useful for demos and screenshots.

---

## What's next?

This was a challenge submission, not a production restaurant platform — but there's room to grow:

- Extract the splash animation into a reusable Web Component
- Add sound effects (with mute toggle, obviously)
- Wire up real social links if SLURP! ever becomes a real brand
- Globe tour of store cities with lat/lon markers
- Split into a proper build pipeline if the project outgrows single-file territory

For now, I'm happy with what shipped: a page that makes people smile, teaches a few frontend tricks, and proves that comfort food deserves better than a stock photo and a "Order Now" button.

---

## Your turn

If you're participating in the [DEV Frontend Challenge](https://dev.to/challenges/frontend-2026-07-29) — or you've built something fun for it already — drop a link in the comments. I want to see your comfort food takes.

And if you try to catch the noodles... good luck. Chef Marco doesn't believe in you. 🍜

---

*Built with too much chili oil and not enough sleep. MIT licensed.*
