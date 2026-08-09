# Interaction Tour Voiceover Script

**Target length:** ~59 seconds (synced to `interaction-tour.mp4`)  
**Tone:** DEV challenge walkthrough — narrate each click as it happens on screen  
**Sync approach:** Per-segment TTS clips merged onto video with ffmpeg `adelay` (Option C)

---

## Cue sheet

| Start (s) | Interaction on screen | Narration |
|-----------|----------------------|-----------|
| 0.0 | Page loads on hero | Welcome to SLURP! Every major interaction on this page is wired with Alpine.js — let's click through the highlights. |
| 3.5 | Click **TRY AND CATCH THIS!** | First up: the hero dare. Tap the catch button and Chef Marco throws a full SVG splash at your screen — smears, strands, garnishes, the works. |
| 11.0 | Splash overlay visible | Pure CSS and SVG keyframes, with JavaScript seeding random extra noodle strands on each replay. Close the modal when you're done getting roasted. |
| 15.0 | Splash closes | Back to the hero. Notice the frosted desktop nav — pill-shaped links with orange active states and a scroll-progress bar up top. |
| 19.0 | Click **Menu** nav pill | Click a nav pill and the page scrolls to that section. The active link updates as you move — scroll spy baked into one Alpine component. |
| 24.0 | Menu section, peacock show-more | Long lists use peacock show-more buttons instead of pagination. Three bowls show first — click the peacock to fan out the rest of the vault. |
| 27.0 | Click **Build** nav | Build Your Bowl is CSS-only: broth color, noodle style, and toppings all update a live plate preview via custom properties — no image swaps. |
| 30.0 | Select broth / noodle / topping chips | Pick your broth, noodle style, and toppings. Each chip toggles with aria-pressed so screen readers know what's selected. |
| 33.0 | Click **Lock In My Plate** | Lock in your plate, then choose Buy or Learn. Buy drops a generated bowl name straight into the cart. |
| 36.0 | Click **Buy This Bowl** | Added to cart — the floating checkout bar and header badge bump to match. |
| 39.0 | Scroll to Gift a Bowl | Gift a Bowl uses searchable CollectUI-style pickers for delivery location and preset messages — both wired with scoped click-outside handlers. |
| 42.0 | Open location picker | Open the location picker, search a city or store, and the live gift card preview updates as you type. |
| 45.0 | Open preset message picker | Same pattern for preset messages — pick a note and watch it land on the gift card preview. |
| 50.0 | Support section, FAQ accordion | Slurp Support: contact channel cards plus an FAQ accordion. Click a question and the answer expands in place. |
| 53.0 | Support peacock show-more | Four FAQs show first; the peacock reveals the rest — same progressive-disclosure pattern as menu and reviews. |
| 56.0 | Checkout section | Finally, checkout — your cart summary, qty steppers, and a client-side order flow. Every button click you just saw lives in one index.html file. |

---

## Recording notes

**Video:** `python3 scripts/capture-interaction-tour.py` → `assets/blog/interaction-tour-raw.webm`  
**Audio:** Segment files in `assets/blog/interaction-voiceover-segments/` via macOS `say`  
**Merge:** `python3 scripts/merge-interaction-tour.py` → `interaction-tour.mp4` + `interaction-tour.webm`

Regenerate a single segment:

```bash
say -v Samantha -r 180 -o assets/blog/interaction-voiceover-segments/03-splash.aiff \
  "Pure CSS and SVG keyframes, with JavaScript seeding random extra noodle strands on each replay."
ffmpeg -y -i assets/blog/interaction-voiceover-segments/03-splash.aiff \
  -codec:a libmp3lame -qscale:a 2 assets/blog/interaction-voiceover-segments/03-splash.mp3
```

Plain-text batch file: `interaction-voiceover-plain.txt` (one segment per blank-line-separated block).
