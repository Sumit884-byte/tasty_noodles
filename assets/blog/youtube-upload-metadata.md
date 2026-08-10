# YouTube upload — SLURP! interaction tour

**Video file:** `assets/blog/interaction-tour.mp4` (~93s, 5.3 MB, H.264 with synced voiceover)

**Fallback (scroll-only, no voiceover):** `assets/blog-scroll-demo.mp4` (~50s)

---

## Title

```
SLURP! Noodle Shop Landing Page — Full Scroll & Interaction Tour
```

## Description

```
A narrated walkthrough of SLURP! — Tastiest Noodles on the Planet, my submission for the DEV Frontend Challenge (Comfort Food Edition, Perfect Landing).

🍜 Live demo: https://tastynoodles.vercel.app
📦 Source code: https://github.com/Sumit884-byte/tasty_noodles
🏆 Challenge: https://dev.to/challenges/frontend-2026-07-29

What's covered in this ~93s tour:
• Hero splash — SVG/CSS noodle splatter animation
• Desktop nav — frosted pill track with scroll-spy
• Peacock show-more — menu vault expands in place
• Build Your Bowl — live CSS plate preview + cart
• Gift a Bowl — searchable delivery & preset pickers
• Slurp Support — FAQ accordion
• CollectUI checkout flow

Stack: single index.html, Tailwind CSS, Alpine.js, Three.js, vanilla JS. No build step.

#frontend #webdev #landingpage #devchallenge #css #javascript #alpinejs
```

## Tags

```
frontend, landing page, alpine.js, css animation, web development, dev challenge, comfort food, noodle shop, three.js, tailwind css
```

## Category

Science & Technology (or Howto & Style)

## Visibility

Public (unlisted is fine if you prefer to embed only on the blog post)

## Thumbnail suggestion

Use a frame from the hero splash (~2s in) or the existing blog cover:
`assets/blog-cover.jpg`

---

## After upload

1. Copy the video URL (`https://youtube.com/watch?v=VIDEO_ID`)
2. Add to `blog-post.md` under **Interaction tour (with voiceover)**:

```markdown
**YouTube:** https://youtube.com/watch?v=VIDEO_ID

{% embed https://youtube.com/watch?v=VIDEO_ID %}
```

3. Commit and push `blog-post.md`

---

## Manual upload (fastest)

1. Open https://studio.youtube.com/channel/UC/videos?d=ud
2. Click **Create** → **Upload videos**
3. Select `assets/blog/interaction-tour.mp4`
4. Paste title, description, and tags from above
5. Publish (or save as unlisted)
6. Copy the watch URL and update `blog-post.md`

## Automated upload (optional, one-time OAuth setup)

See `scripts/upload-to-youtube.py` — requires Google Cloud OAuth client + `pip install google-api-python-client google-auth-oauthlib google-auth-httplib2`.
