#!/usr/bin/env python3
"""Plan voiceover cue times from an interaction timeline (+ optional vLLM).

Usage:
  python3 scripts/plan-interaction-voiceover.py
  python3 scripts/plan-interaction-voiceover.py --no-llm
  python3 scripts/plan-interaction-voiceover.py --timeline assets/blog/interaction-tour-timeline.json

Reads interaction events (from capture-interaction-tour.py), segment MP3 durations, and
optionally calls vLLM via Arka to assign start_ms so narration aligns with on-screen actions
at 1x pace (no overlap). Writes assets/blog/interaction-voiceover-planned-cues.json for
merge-interaction-tour.py.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARKA_SRC = ROOT.parent / "arka" / "src"
ASSETS = ROOT / "assets" / "blog"
SEG_DIR = ASSETS / "interaction-voiceover-segments"
TIMELINE_FILE = ASSETS / "interaction-tour-timeline.json"
RAW_VIDEO = ASSETS / "interaction-tour-raw.webm"
PLANNED_CUES_FILE = ASSETS / "interaction-voiceover-planned-cues.json"

MIN_GAP_MS = 250

# Default segment texts (first-person DEV walkthrough).
DEFAULT_SEGMENTS = [
    {"id": "01-intro", "text": "Welcome to SLURP! Every major interaction on this page is wired with Alpine.js — let's click through the highlights."},
    {"id": "02-hero-catch", "text": "First up: the hero dare. Tap the catch button and Chef Marco throws a full SVG splash at your screen — smears, strands, garnishes, the works."},
    {"id": "03-splash", "text": "Pure CSS and SVG keyframes, with JavaScript seeding random extra noodle strands on each replay. Close the modal when you're done getting roasted."},
    {"id": "04-nav", "text": "Back to the hero. Notice the frosted desktop nav — pill-shaped links with orange active states and a scroll-progress bar up top."},
    {"id": "05-menu-nav", "text": "Click a nav pill and the page scrolls to that section. The active link updates as you move — scroll spy baked into one Alpine component."},
    {"id": "06-peacock-menu", "text": "Long lists use peacock show-more buttons instead of pagination. Three bowls show first — click the peacock to fan out the rest of the vault."},
    {"id": "07-build-nav", "text": "Build Your Bowl is CSS-only: broth color, noodle style, and toppings all update a live plate preview via custom properties — no image swaps."},
    {"id": "08-build-chips", "text": "Pick your broth, noodle style, and toppings. Each chip toggles with aria-pressed so screen readers know what's selected."},
    {"id": "09-lock-plate", "text": "Lock in your plate, then choose Buy or Learn. Buy drops a generated bowl name straight into the cart."},
    {"id": "10-buy-bowl", "text": "Added to cart — the floating checkout bar and header badge bump to match."},
    {"id": "11-gift-intro", "text": "Gift a Bowl uses searchable CollectUI-style pickers for delivery location and preset messages — both wired with scoped click-outside handlers."},
    {"id": "12-gift-location", "text": "Open the location picker, search a city or store, and the live gift card preview updates as you type."},
    {"id": "13-gift-preset", "text": "Same pattern for preset messages — pick a note and watch it land on the gift card preview."},
    {"id": "14-support-faq", "text": "Slurp Support: contact channel cards plus an FAQ accordion. Click a question and the answer expands in place."},
    {"id": "15-support-more", "text": "Four FAQs show first; the peacock reveals the rest — same progressive-disclosure pattern as menu and reviews."},
    {"id": "16-checkout", "text": "Finally, checkout — your cart summary, qty steppers, and a client-side order flow. Every button click you just saw lives in one index.html file."},
]

# Map segment id → timeline event label(s) to anchor narration.
ANCHOR_LABELS: dict[str, list[str]] = {
    "01-intro": [],  # always 0ms
    "02-hero-catch": ["TRY AND CATCH", "pre_catch"],
    "03-splash": ["splash_playing", "splash_visible"],
    "04-nav": ["dismiss_splash", "post_splash"],
    "05-menu-nav": ["Menu"],
    "06-peacock-menu": ["peacock_show_more"],
    "07-build-nav": ["Build"],
    "08-build-chips": ["Dragon Chili", "broth_selected"],
    "09-lock-plate": ["Lock In My Plate"],
    "10-buy-bowl": ["Buy This Bowl", "added_to_cart"],
    "11-gift-intro": ["gift_section", "Gift"],
    "12-gift-location": ["location_picker_open"],
    "13-gift-preset": ["preset_picker_open"],
    "14-support-faq": ["faq_expand", "support_section"],
    "15-support-more": ["support_peacock", "support_expanded"],
    "16-checkout": ["checkout_section", "Checkout"],
}


def probe_duration(path: Path) -> float | None:
    try:
        out = subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path),
        ], text=True, stderr=subprocess.DEVNULL).strip()
        return float(out)
    except (subprocess.CalledProcessError, ValueError):
        return None


def load_timeline(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Missing timeline: {path}. Run capture-interaction-tour.py first.")
    return json.loads(path.read_text(encoding="utf-8"))


def derive_timeline_from_capture_delays() -> dict:
    """Fallback timeline when capture hasn't been re-run with event logging."""
    # Mirrors wait/click order in capture-interaction-tour.py (ms cumulative).
    delays = [
        ("page_ready", "wait", 2000, "hero"),
        ("intro", "wait", 1500, "hero"),
        ("pre_catch", "wait", 800, "hero"),
        ("TRY AND CATCH", "click", 0, "hero"),
        ("splash_playing", "wait", 7500, "hero"),
        ("splash_visible", "wait", 1500, "hero"),
        ("dismiss_splash", "click", 0, "hero"),
        ("post_splash", "wait", 2000, "hero"),
        ("Menu", "click", 0, "nav"),
        ("menu_scroll", "wait", 2500, "menu"),
        ("menu_section", "scroll", 700, "menu"),
        ("peacock_show_more", "click", 0, "menu"),
        ("menu_expanded", "wait", 3500, "menu"),
        ("Build", "click", 0, "nav"),
        ("build_scroll", "wait", 2000, "build"),
        ("build_section", "scroll", 700, "build"),
        ("Dragon Chili", "click", 0, "build"),
        ("broth_selected", "wait", 1200, "build"),
        ("Hand-Pulled Thick", "click", 0, "build"),
        ("noodle_selected", "wait", 1200, "build"),
        ("Jammy Egg", "click", 0, "build"),
        ("Lock In My Plate", "click", 0, "build"),
        ("plate_locked", "wait", 2000, "build"),
        ("Buy This Bowl", "click", 0, "build"),
        ("added_to_cart", "wait", 3000, "build"),
        ("Gift", "click", 0, "nav"),
        ("gift_scroll", "wait", 2000, "gift"),
        ("gift_section", "scroll", 700, "gift"),
        ("location_picker_open", "click", 0, "gift"),
        ("location_picker_visible", "wait", 1200, "gift"),
        ("location_selected", "click", 0, "gift"),
        ("location_applied", "wait", 2000, "gift"),
        ("preset_picker_open", "click", 0, "gift"),
        ("preset_picker_visible", "wait", 1200, "gift"),
        ("preset_selected", "click", 0, "gift"),
        ("preset_applied", "wait", 2500, "gift"),
        ("Support", "click", 0, "nav"),
        ("support_scroll", "wait", 2000, "support"),
        ("support_section", "scroll", 700, "support"),
        ("faq_expand", "click", 0, "support"),
        ("faq_open", "wait", 2500, "support"),
        ("support_peacock", "click", 0, "support"),
        ("support_expanded", "wait", 3000, "support"),
        ("Checkout", "click", 0, "nav"),
        ("checkout_scroll", "wait", 2500, "checkout"),
        ("checkout_section", "scroll", 700, "checkout"),
        ("checkout_hold", "wait", 2000, "checkout"),
    ]
    events: list[dict] = []
    elapsed = 0
    for label, action, ms, section in delays:
        if action == "click":
            events.append({"elapsed_ms": elapsed, "action": "click", "label": label, "section": section})
        else:
            elapsed += ms
            events.append({"elapsed_ms": elapsed, "action": action, "label": label, "section": section, "wait_ms": ms})
    return {"base_url": "http://127.0.0.1:8080/", "events": events, "total_ms": elapsed, "derived": True}


def find_anchor_ms(timeline: dict, labels: list[str]) -> int | None:
    events = timeline.get("events", [])
    for label in labels:
        for ev in events:
            if ev.get("label") == label:
                return int(ev["elapsed_ms"])
    return None


def segment_durations(segments: list[dict]) -> list[dict]:
    enriched: list[dict] = []
    for seg in segments:
        mp3 = SEG_DIR / f"{seg['id']}.mp3"
        duration_ms = int(d * 1000) if (d := probe_duration(mp3)) else None
        enriched.append({**seg, "duration_ms": duration_ms})
    return enriched


def enforce_sequential(cues: list[dict]) -> list[dict]:
    """Ensure no overlap at 1x: each segment starts after previous ends + MIN_GAP_MS."""
    prev_end = 0
    fixed: list[dict] = []
    for cue in cues:
        start = max(int(cue["start_ms"]), prev_end + (MIN_GAP_MS if fixed else 0))
        dur = int(cue.get("duration_ms") or 0)
        fixed.append({**cue, "start_ms": start, "anchor_ms": cue.get("anchor_ms"), "shift_ms": start - int(cue.get("anchor_ms") or cue["start_ms"])})
        prev_end = start + dur
    return fixed


def plan_heuristic(timeline: dict, segments: list[dict]) -> list[dict]:
    """Anchor each segment to its interaction event, then enforce sequential 1x pacing."""
    cues: list[dict] = []
    for seg in segments:
        if seg["id"] == "01-intro":
            anchor = 0
        else:
            anchor = find_anchor_ms(timeline, ANCHOR_LABELS.get(seg["id"], []))
        start_ms = anchor if anchor is not None else (cues[-1]["start_ms"] + cues[-1].get("duration_ms", 0) + MIN_GAP_MS if cues else 0)
        cues.append({
            "id": seg["id"],
            "text": seg["text"],
            "start_ms": start_ms,
            "anchor_ms": anchor,
            "duration_ms": seg.get("duration_ms"),
        })
    return enforce_sequential(cues)


def _parse_json_array(text: str) -> list[dict]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def _valid_segment_text(original: str, candidate: str | None) -> str:
    """Keep original text if LLM returns empty, placeholder, or too-short output."""
    if not candidate or not isinstance(candidate, str):
        return original
    cleaned = candidate.strip()
    if cleaned in {"...", "…", "TBD", "N/A"} or len(cleaned) < 20:
        return original
    return cleaned


def plan_with_llm(timeline: dict, segments: list[dict], video_duration_ms: int | None) -> list[dict]:
    if ARKA_SRC.exists() and str(ARKA_SRC) not in sys.path:
        sys.path.insert(0, str(ARKA_SRC))
    try:
        from arka.llm.fallback import llm_complete
    except ImportError:
        print("Arka not found — falling back to heuristic planner.", file=sys.stderr)
        return plan_heuristic(timeline, segments)

    events_compact = [
        {"ms": e["elapsed_ms"], "action": e.get("action"), "label": e.get("label"), "section": e.get("section")}
        for e in timeline.get("events", [])
    ]
    seg_payload = [
        {
            "id": s["id"],
            "text": s["text"],
            "duration_ms": s.get("duration_ms"),
            "anchor_labels": ANCHOR_LABELS.get(s["id"], []),
        }
        for s in segments
    ]

    system = (
        "You schedule voiceover cues for a screen-recording tour at 1x speech speed. "
        "Return ONLY a JSON array: "
        '[{"id":"01-intro","start_ms":0,"text":"..."}]. '
        "Rules: "
        "(1) start_ms aligns narration with the matching on-screen action when possible; "
        "(2) segments must not overlap at 1x — if duration_ms would collide, start later; "
        "(3) prefer natural pacing over cramming into video length — video will extend via padding; "
        "(4) first-person DEV tone; keep each segment's provided text verbatim — do not abbreviate or use placeholders; "
        "(5) intro at 0ms, checkout segment near the checkout action."
    )
    user = json.dumps({
        "video_duration_ms": video_duration_ms,
        "timeline_total_ms": timeline.get("total_ms"),
        "min_gap_ms": MIN_GAP_MS,
        "interaction_events": events_compact,
        "segments": seg_payload,
    }, indent=2)

    print("Calling vLLM via Arka llm_complete…")
    text = llm_complete(system, user, temperature=0.2, task="compose_video")
    rows = _parse_json_array(text)
    by_id = {str(r["id"]): r for r in rows if isinstance(r, dict) and r.get("id")}

    cues: list[dict] = []
    for seg in segments:
        row = by_id.get(seg["id"], {})
        cues.append({
            "id": seg["id"],
            "text": _valid_segment_text(seg["text"], row.get("text")),
            "start_ms": int(row.get("start_ms", 0)),
            "anchor_ms": find_anchor_ms(timeline, ANCHOR_LABELS.get(seg["id"], [])),
            "duration_ms": seg.get("duration_ms"),
        })
    return enforce_sequential(cues)


def print_plan_table(cues: list[dict], video_ms: int | None) -> None:
    print(f"\n{'ID':<18} {'start':>7} {'dur':>6} {'anchor':>7} {'shift':>6}")
    print("-" * 50)
    prev_end = 0
    for cue in cues:
        start = cue["start_ms"]
        dur = cue.get("duration_ms") or 0
        end = start + dur
        anchor = cue.get("anchor_ms")
        shift = start - anchor if anchor is not None else None
        print(f"{cue['id']:<18} {start/1000:>6.1f}s {dur/1000:>5.1f}s "
              f"{(anchor/1000 if anchor is not None else 0):>6.1f}s "
              f"{(shift/1000 if shift is not None else 0):>+5.1f}s")
        prev_end = end
    total_s = prev_end / 1000
    print(f"\nPlanned voiceover: {total_s:.1f}s")
    if video_ms:
        pad = total_s - video_ms / 1000
        print(f"Raw video: {video_ms/1000:.1f}s → padding needed: {max(0, pad):.1f}s")


def main() -> None:
    parser = argparse.ArgumentParser(description="Plan interaction tour voiceover cue times.")
    parser.add_argument("--timeline", type=Path, default=TIMELINE_FILE)
    parser.add_argument("--video", type=Path, default=RAW_VIDEO)
    parser.add_argument("--output", type=Path, default=PLANNED_CUES_FILE)
    parser.add_argument("--no-llm", action="store_true", help="Use heuristic anchor planner only")
    args = parser.parse_args()

    if args.timeline.exists():
        timeline = load_timeline(args.timeline)
        print(f"Loaded timeline: {args.timeline} ({len(timeline.get('events', []))} events)")
    else:
        print(f"No timeline at {args.timeline} — using derived delays from capture script.", file=sys.stderr)
        timeline = derive_timeline_from_capture_delays()

    video_ms: int | None = None
    if args.video.exists():
        video_ms = int(probe_duration(args.video) * 1000)
        print(f"Raw video duration: {video_ms/1000:.1f}s")

    segments = segment_durations(DEFAULT_SEGMENTS)
    missing = [s["id"] for s in segments if s.get("duration_ms") is None]
    if missing:
        print(f"Warning: missing MP3 durations for {missing} — run merge-interaction-tour.py to generate TTS first.", file=sys.stderr)

    if args.no_llm:
        cues = plan_heuristic(timeline, segments)
        planner = "heuristic"
    else:
        try:
            cues = plan_with_llm(timeline, segments, video_ms)
            planner = "vllm"
        except Exception as exc:
            print(f"LLM planner failed ({exc}) — falling back to heuristic.", file=sys.stderr)
            cues = plan_heuristic(timeline, segments)
            planner = "heuristic (fallback)"

    print_plan_table(cues, video_ms)

    payload = {
        "planner": planner,
        "video_duration_ms": video_ms,
        "timeline_total_ms": timeline.get("total_ms"),
        "min_gap_ms": MIN_GAP_MS,
        "cues": [{"id": c["id"], "start_ms": c["start_ms"], "text": c["text"]} for c in cues],
    }
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nSaved planned cues: {args.output}")


if __name__ == "__main__":
    main()
