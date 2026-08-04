# SLURP! — Tastiest Noodles on the Planet

A playful comfort-food landing page for an imaginary noodle shop. Built for the [DEV Frontend Challenge: Comfort Food Edition](https://dev.to/challenges/frontend-2026-07-29).

## Live Demo

**https://tastynoodles.vercel.app**

GitHub: **https://github.com/Sumit884-byte/tasty_noodles**

## CodePen

Open the project in the CodePen editor (images load from the live deploy):

**https://tastynoodles.vercel.app/codepen/**

1. Click **Open in CodePen**
2. Log in and click **Save**
3. Set the pen to **Public** and share your pen URL

To regenerate the export after editing `index.html`:

```bash
python3 scripts/build-codepen.py
```

## Features

- Interactive noodle splash hero animation
- Noodle Vault — 6 bowls with CollectUI-style cards and category filters
- Build Your Bowl — live CSS plate preview (thick, thin, or broth-only)
- Pan India store finder — 15 locations across 12 cities with directions
- Slurp Squad — 8 customer testimonials
- Galactic Slurp story section with a Three.js 3D spinning globe
- CollectUI-style cart bar + checkout flow

## Stack

- HTML, Tailwind CSS (CDN), Alpine.js, Three.js, vanilla JavaScript
- All images self-hosted in `/assets` — no external image dependencies

## Run Locally

```bash
# Any static server works, e.g.:
python3 -m http.server 8080
# Open http://localhost:8080
```

Or open `index.html` directly in a browser.

## License

MIT
