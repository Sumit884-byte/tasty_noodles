# Responsivity Voiceover Script

**Target length:** ~75 seconds at a natural read pace  
**Tone:** DEV challenge — technical but friendly, like explaining your build to another frontend dev

---

## Script

SLURP! ships as one HTML file that has to feel like a full noodle shop on every screen. The real split is at **1024 pixels** — Tailwind's `lg` breakpoint — not a separate mobile site.

Below that, the frosted top bar keeps the logo, locale picker, and hamburger drawer. Section navigation moves to a **bottom tab bar**: Dare, Menu, Build, Gift, and Cart — with safe-area padding for notched phones. The floating checkout bar sits **above** that tab bar, never behind it.

At `lg` and up, the hamburger disappears. A **pill-shaped nav track** appears in the header — horizontally scrollable between 1024 and 1280 when labels get tight — with grouped dividers and orange-gradient active states. Checkout moves into the header; the label appears at `xl`.

Content grids follow the same rhythm. Menu cards: one column, two at `md`, three at `lg`. Gift a Bowl stacks on mobile; at `lg`, the form and a **sticky preview card** sit side by side. Store search controls stack until `sm`, then row-align; decorative elephants only show from `md`.

Long lists — menu bowls, stores, reviews, FAQs — use **peacock show-more buttons** that reveal three or four items first, instead of dumping everything at once. Category filter pills and the learn-step strip scroll horizontally on touch.

Motion and input respect preference: `prefers-reduced-motion` disables splash, globe, and steam animations. Chopstick cursors only apply on `pointer: fine` devices. CSS variables for scroll-padding keep anchor links clear of the fixed header and bottom nav.

One page, reshaped by breakpoint — navigation, grids, and chrome all tuned to how you're actually holding the screen.

---

## Recording notes

**Generated:** macOS `say -v Samantha -r 195` → ffmpeg MP3 (~96 seconds).  
Arka `arka_convert_media` does not accept `.aiff` input; convert via ffmpeg first if regenerating from AIFF.

If regenerating audio locally:

```bash
# macOS — generate AIFF then convert to MP3
say -v Samantha -r 175 -o assets/blog/responsivity-voiceover.aiff -f assets/blog/responsivity-voiceover-plain.txt

# Convert with ffmpeg (or Arka arka_convert_media)
ffmpeg -i assets/blog/responsivity-voiceover.aiff -codec:a libmp3lame -qscale:a 2 assets/blog/responsivity-voiceover.mp3
```

Plain-text file for `say -f`: strip markdown formatting from the Script section above.
