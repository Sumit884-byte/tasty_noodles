---
title: "I Built a Noodle Shop Landing Page That Throws Food at Your Screen 🍜"
published: false
description: "How I built SLURP! — a playful comfort-food landing page with SVG splash animations, a CSS bowl builder, and a Three.js spinning globe — for the DEV Frontend Challenge."
tags: devchallenge, frontend, webdev, javascript
cover_image: https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/blog-cover.jpg
canonical_url: https://tastynoodles.vercel.app
---

_This is a submission for [Frontend Challenge - Comfort Food Edition, Perfect Landing](https://dev.to/challenges/frontend-2026-07-29)_

## What I Built

I built **[SLURP! — Tastiest Noodles on the Planet](https://tastynoodles.vercel.app)**, a single-page landing page for an imaginary noodle shop. The comfort food theme is **ramen and noodle bowls** — warm, slurpy, a little chaotic — and I leaned into that with copy, color, and interactions that feel cozy *and* playful.

The hook: Chef Marco is so confident in his noodles that he literally throws a bowl at your screen. The hero CTA is **"TRY AND CATCH THIS! 🍜"** — miss the catch, get roasted, then explore the rest of the shop.

![Hero splash overlay — SVG/CSS noodle splatter](https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/blog-sections/hero-splash.png)

**What's on the page:**

- **Noodle Splash Hero** — full-screen SVG + CSS animation (sauce smears, flying noodle clusters, garnishes, a frosted-glass "SPLAAAT!" modal). Each replay seeds random extra strands in JavaScript so the splatter feels slightly different every time.
- **The Noodle Vault** — six signature bowls in a CollectUI-inspired card grid (Dragon Breath Chili Oil, Midnight Tonkotsu, Garlic Butter Dan Dan, Bombay Street Manchow, Golden Curry Udon, Peanut Crunch Yakisoba) with category filter chips and wavy noodle-strand SVG borders generated at runtime.
- **Build Your Bowl** — live CSS plate preview (broth color, thick/thin/broth-only noodles, six toppings). No image swaps — just custom properties, positioned elements, and steam keyframes. Hit **"Lock In My Plate"**, then **"Buy This Bowl"** — it drops into the cart with a generated name.
- **Galactic Slurp** — story section with a Three.js spinning globe, alien rider, and twinkling stars (static fallback for `prefers-reduced-motion` and WebGL failures).
- **Pan India Store Finder** — 15 kitchens across 12 cities, searchable by city, area, or pincode, with Google Maps directions.
- **Slurp Squad** — eight fake testimonials from regulars who also failed to catch the noodles.
- **Social Feed Preview** — Reels/Stories/TikTok-style cards using the same self-hosted bowl photos (platform buttons are visual-only demos).
- **Gift a Bowl** — send-a-bowl flow with searchable delivery-location and preset-message pickers, live gift card preview.
- **Slurp Support** — contact channel cards (phone, WhatsApp, email, order help), seven-item FAQ accordion with peacock show-more, quick links to stores/gift/checkout, wired into desktop nav.
- **Desktop section nav** — frosted-glass bar, pill-shaped link track with grouped dividers, orange-gradient active states, and a scroll-progress indicator.
- **CollectUI Checkout Flow** — Alpine.js cart with sticky bar, mobile bottom sheet, and a full client-side order flow.

**Stack:** one `index.html` file — HTML, Tailwind CSS (CDN), Alpine.js 3.14, Three.js 0.172, vanilla JS, Lucide icons, Chewy font. No build step. All images self-hosted in `/assets`. MIT licensed.

**Source:** [github.com/Sumit884-byte/tasty_noodles](https://github.com/Sumit884-byte/tasty_noodles)

## Demo

**Live site:** [tastynoodles.vercel.app](https://tastynoodles.vercel.app)

Click **TRY AND CATCH THIS!** on the hero — that's the centerpiece interaction. Append `?splash` to the URL if you want to land directly in the splatter overlay.

![Desktop nav — frosted pill track with scroll-spy](https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/blog-sections/desktop-nav.png)

**Scroll demo** — full page top to bottom, every section (~57s):

<video controls width="100%" src="https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/blog-scroll-demo.mp4">
  <a href="https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/blog-scroll-demo.mp4">Watch scroll demo (MP4)</a>
</video>

### Interaction tour (with voiceover)

I recorded a **~111s desktop walkthrough** (111.1s) — narrated clicks through the main Alpine.js interactions: hero splash, nav scroll-spy, peacock show-more, bowl builder, gift pickers, FAQ accordion, and checkout.

<video controls width="100%" src="https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/blog/interaction-tour.mp4">
  <a href="https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/blog/interaction-tour.mp4">Watch interaction tour (MP4)</a>
</video>

I synced narration to on-screen actions with a three-step pipeline: Playwright captures the click tour and writes an interaction timeline JSON; Arka/vLLM reads that timeline plus segment MP3 lengths and assigns cue start times at **1× pace** with no overlap; sixteen TTS segments get muxed onto the raw webm, extending the last frame if voice runs past the capture. Voice is baked into the MP4 above — segments never overlap and are never sped up.

**Interactions demonstrated:**

1. **Hero splash** — `TRY AND CATCH THIS!` triggers the SVG/CSS splatter overlay; dismiss with *Wipe Screen & Place Order*
2. **Desktop nav pills** — frosted pill track with scroll-spy active states
3. **Peacock show-more** — menu vault expands from 3 → 6 bowls in place
4. **Build Your Bowl** — broth/noodle/topping chips → Lock In My Plate → Buy This Bowl (cart bump)
5. **Gift pickers** — searchable delivery-location and preset-message dropdowns with live card preview
6. **Support FAQ** — accordion expand + peacock show-more for hidden questions
7. **Checkout** — cart summary after items are added

Voiceover script and cue timestamps: [`assets/blog/interaction-voiceover-script.md`](https://github.com/Sumit884-byte/tasty_noodles/blob/main/assets/blog/interaction-voiceover-script.md) · vLLM-planned cues in [`assets/blog/interaction-voiceover-planned-cues.json`](https://github.com/Sumit884-byte/tasty_noodles/blob/main/assets/blog/interaction-voiceover-planned-cues.json) · merged segment sheet in [`assets/blog/interaction-voiceover-cues.json`](https://github.com/Sumit884-byte/tasty_noodles/blob/main/assets/blog/interaction-voiceover-cues.json)

**Screenshots** (hero through checkout — current layout):

![Hero — noodle splash landing](https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/blog-sections/hero.jpg)

![The Noodle Vault — menu cards](https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/blog-sections/menu.jpg)

![Build Your Bowl — live CSS plate preview](https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/blog-sections/build.png)

![Galactic Slurp — Three.js globe story](https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/blog-sections/story.png)

![Pan India Store Finder](https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/blog-sections/stores.png)

![Slurp Squad — testimonials](https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/blog-sections/reviews.png)

![Social Feed Preview](https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/blog-sections/social.png)

![Gift a Bowl](https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/blog-sections/gift.png)

![Slurp Support — contact and FAQ](https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/blog-sections/support.png)

![CollectUI Checkout Flow](https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/blog-sections/checkout.png)

**Links:**

- 🍜 Live demo: [tastynoodles.vercel.app](https://tastynoodles.vercel.app)
- 📦 Source: [github.com/Sumit884-byte/tasty_noodles](https://github.com/Sumit884-byte/tasty_noodles)

## Journey

### Why noodles?

The [DEV Frontend Challenge](https://dev.to/challenges/frontend-2026-07-29) prompt was comfort food — not "a nice restaurant site," but something that makes you hungry just thinking about it. Noodles felt right: warm broth, slurping sounds, late-night cravings. I wanted the page to feel like a **brand**, not a template — chunky typography, an amber/orange/stone palette, and interactions that reward curiosity.

### Process

I started with the splash hero because it set the tone. Pure SVG + CSS — no canvas, no video, no Lottie. `stroke-dashoffset` for smears and strands, staggered keyframes for clusters and garnishes, JavaScript to seed random extra strands on each replay.

![Build Your Bowl — broth, noodles, toppings, and live plate preview](https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/blog-sections/build-plate.png)

From there I built outward: menu cards with runtime-generated wavy SVG borders, the CSS-only bowl builder (my favorite section technically — a well-structured DOM + custom properties replaced a lot of image-swap logic), then the Three.js globe with performance guardrails (IntersectionObserver to pause off-screen, `visibilitychange` for hidden tabs, adaptive geometry, `pixelRatio` cap, static fallback for reduced motion).

Alpine.js became the app's brain — one `slurpApp()` component handles cart, custom plate builder, store locator, menu filtering, splash overlay, mobile nav, gift flow, support FAQ, and checkout. I baked accessibility in from the start: skip link, splash dialog with focus management, `aria-pressed` on builder chips, `prefers-reduced-motion` disabling splash/globe/steam animations, semantic landmarks, lazy-loaded images with explicit dimensions.

Later passes added **Slurp Support** — contact cards, accordion FAQ, peacock show-more, quick links — and tightened the **Gift a Bowl** pickers. Nested `@click.outside` handlers were closing delivery-location and preset-message dropdowns before you could pick an option; scoping each picker (and `@click.stop` on the search inputs) fixed it, and a clearer `giftPresetItem` getter made the preset dropdown label behave.

The desktop upper nav got a full polish pass: frosted-glass bar, pill-shaped link track with grouped dividers, orange-gradient active states, and a scroll-progress bar. That redesign surfaced an Alpine gotcha — `x-for` with multiple root nodes (divider span + link) only rendered the dividers. Wrapping each iteration in a single `.site-nav__item` fixed it, along with contrast, hover, and overflow tweaks at the 1024px breakpoint.

For the blog demos I built a reproducible voiceover pipeline in-repo:

1. **Capture** — `scripts/capture-interaction-tour.py` records the desktop click tour and writes interaction timeline JSON
2. **Plan** — `scripts/plan-interaction-voiceover.py` sends the timeline plus segment MP3 lengths to Arka/vLLM, which assigns cue start times so narration lands on each on-screen action at 1× pace with no overlap
3. **Merge** — `scripts/merge-interaction-tour.py` muxes sixteen TTS segments onto the raw webm, extending the last frame if voice runs past the capture

Scroll demo and section screenshots come from `scripts/capture-blog-assets.py`. The whole thing stays reproducible without re-recording by hand.

### How responsivity is designed

Responsivity on SLURP! is not a bolted-on `@media` pass at the end — I designed it into navigation, layout grids, scroll behavior, and motion from the start. The page uses Tailwind's default breakpoints (`sm` 640px, `md` 768px, `lg` 1024px, `xl` 1280px), but the **primary split is `lg` (1024px)**: below that you're in touch-first mode; above it you're in desktop mode.

![Mobile layout — bottom tab bar and frosted header (390×844)](https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/blog-sections/mobile-nav.png)

**Listen:** [Responsivity walkthrough (~96s)](https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/blog/responsivity-voiceover.mp3)

<audio controls src="https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/blog/responsivity-voiceover.mp3">
  Your browser does not support the audio element. <a href="https://raw.githubusercontent.com/Sumit884-byte/tasty_noodles/main/assets/blog/responsivity-voiceover.mp3">Download the voiceover</a>.
</audio>

Responsivity script: [`assets/blog/responsivity-voiceover-script.md`](https://github.com/Sumit884-byte/tasty_noodles/blob/main/assets/blog/responsivity-voiceover-script.md)

#### Navigation: bottom tabs vs pill track

On **mobile and tablet** (`max-width: 1023px`):

- The frosted top bar keeps logo, locale picker, and a hamburger drawer (full section list + locale chips).
- Section navigation moves to a **fixed bottom tab bar** — five icons: Dare, Menu, Build, Gift, Cart — with a wavy noodle SVG divider and `env(safe-area-inset-bottom)` padding for notched phones.
- The floating checkout bar sits **above** the tab bar (`bottom: calc(4.875rem + safe-area)`), never behind it.
- `body` gets bottom padding so content isn't hidden under the chrome; when the cart bar is visible, padding doubles.

On **desktop** (`lg:` / `min-width: 1024px`):

- Hamburger and bottom tab bar hide (`lg:hidden`).
- A **pill-shaped nav track** appears in the header (`hidden lg:block`) — frosted inner track, grouped dividers between section clusters, orange-gradient active link states, and a scroll-progress bar.
- The track **scrolls horizontally** when the viewport is tight (1024–1279px): link font-size and padding compress, checkout button becomes icon-only, and locale picker label hides until `xl`.
- Checkout moves into the header; the "Checkout" label appears at `xl`.

Scroll offsets are wired through CSS variables on `:root`:

```css
--site-header-offset: 3.5rem;   /* mobile */
--site-bottom-offset: 4.875rem; /* mobile tab bar */
/* at 1024px+: header 5rem, bottom 0 */
```

`scroll-padding-top` and `.section-scroll-target { scroll-margin-top }` keep anchor jumps from landing under fixed chrome.

#### Layout grids and section patterns

| Section | Mobile | `md` (768px) | `lg` (1024px) |
|---------|--------|--------------|---------------|
| Menu cards | 1 col | 2 col | 3 col |
| Gift a Bowl | stacked | — | 2-col grid + sticky preview |
| Store results | 1 col | 2 col | — |
| Social share cards | 1 col | 2 col (`sm`) | 4 col |
| Build Your Bowl | stacked | 2 col | — |
| Learn section | horizontal step strip | — | sticky step list |

**Gift layout:** `.gift-layout` is a single-column grid on mobile; at `lg` it becomes `grid-template-columns: 1.05fr 0.95fr` with `.gift-preview-wrap { position: sticky; top: 6rem }`. Form fields use `sm:grid-cols-2` for To/From name pairs.

**Store finder:** search row stacks vertically until `sm`, then row-aligns; decorative elephant SVGs are `display: none` until `md`. Store decor animations scale down or hide on small screens to reduce visual noise.

**Menu cards:** CollectUI-style grid with horizontal-scrolling category filter pills (`menu-cat-scroll`, scrollbar hidden). Cards use runtime wavy SVG borders via `attachNoodleFrame()`.

#### Overflow and progressive disclosure

Instead of infinite scroll, long lists use **peacock show-more buttons** (`section-show-more-btn`) with Alpine `visibleSlice()` — initial limits of 3–4 items per section (menu, stores, reviews, spread, slurp-code, checkout, support FAQ). Tap expands in place; no route change, no pagination component.

Other intentional overflow:

- Desktop nav track: `overflow-x: auto` with edge fade masks.
- Learn step strip on tablet: horizontal scroll + `scroll-snap-type: x mandatory`.
- Category pills: `overflow-x-auto` with hidden scrollbars.

#### Motion, cursors, and locale

**`prefers-reduced-motion: reduce`** disables splash animations, globe spin, steam keyframes, store decoration animations, nav hover transforms, and chopstick card ornaments. JavaScript checks `matchMedia('(prefers-reduced-motion: reduce)')` before confetti, splash replay, and Three.js init — static fallback for the globe.

**Chopstick theme** (`body.chopstick-theme`): custom noodle cursors apply only under `@media (pointer: fine)` — touch users keep the system cursor. Section-scoped accent colors via `body[data-section="…"] { --chopstick-accent }`. Active nav states show crossed-chopstick icons (inline on drawer links, overlay on desktop pills, above icon on mobile bottom nav).

**Locale picker:** compact toggle in the header; full locale chip row in the mobile drawer. A floating locale-suggestion banner uses `max-width: calc(100vw - 1.5rem)` and repositions at `md`. Between 1024–1279px the picker label hides to save header space.

#### Checkout UX across breakpoints

The CollectUI-style flow uses a **floating checkout bar** when items are in cart — centered, max-width 24rem, with optional inline qty stepper for single-item carts. On mobile it floats above the bottom nav; on desktop it sits at `bottom: 1rem` with no body padding conflict. The checkout section itself is a centered `max-w-2xl` card with peacock show-more for long cart lists.

### What I'm proud of

- The splash animation — elaborate, replayable, and still pure SVG/CSS
- The CSS bowl preview — instant, lightweight, infinitely recombinable
- Wavy SVG card borders via `attachNoodleFrame()` — micro-detail that makes the UI feel designed
- Progressive enhancement for motion and WebGL — fun features that don't punish users who prefer reduced motion or lack WebGL
- **Slurp Support** — contact cards and FAQ that feel on-brand, not a generic help-desk widget pasted onto a landing page
- The desktop nav — frosted glass, pill track, scroll progress, and a real Alpine `x-for` debugging story
- The voiceover pipeline — reproducible capture → vLLM cue planning → merge, all at 1× with no overlapping narration
- Shipping everything in one file you can open locally without explaining npm

### What I learned

**Commit to the joke, but ship real craft.** The copy is silly; underneath there's form validation, accessible modals, performance-conscious 3D, and responsive layouts.

**CSS can do more than I thought.** The bowl preview taught me that custom properties + keyframes can replace a lot of asset-heavy UI logic.

**Constraints spark creativity.** "Comfort food" pushed me toward warmth and interactivity instead of a generic SaaS layout.

**Single-file projects are underrated.** For a challenge submission or portfolio piece, one `index.html` felt like a superpower.

**Timing narration to UI is a pipeline problem.** Splitting capture, cue planning, and merge into separate scripts made the ~111s tour reproducible — and vLLM cue assignment beat hand-editing timestamps.

### What's next?

This was a challenge submission, not a production restaurant platform — but there's room to grow:

- Extract the splash animation into a reusable Web Component
- Add sound effects (with mute toggle)
- Wire up real social links if SLURP! ever becomes a real brand
- **India wireframe map with store pins** — a sketch-style outline of the country with clickable markers for each kitchen, tied into the existing store finder
- **Peacock feather expansion on show-more** — peacock buttons already reveal extra menu cards, testimonials, and support FAQs; next up is a feather-fan unfold animation on click, so expanding a section feels like the bird opening its tail

For now, I'm happy with what I shipped: a page that makes people smile, teaches a few frontend tricks, and proves that comfort food deserves better than a stock photo and an "Order Now" button.

If you're participating in the challenge — or you've built something fun for it already — drop a link in the comments. I want to see your comfort food takes.

And if you try to catch the noodles... good luck. Chef Marco doesn't believe in you. 🍜

---

*Built with too much chili oil and not enough sleep. MIT licensed — see [LICENSE](https://github.com/Sumit884-byte/tasty_noodles/blob/main/LICENSE).*
