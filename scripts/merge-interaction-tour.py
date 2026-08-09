#!/usr/bin/env python3
"""Generate TTS segments and merge interaction tour video + synced voiceover."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "blog"
SEG_DIR = ASSETS / "interaction-voiceover-segments"
RAW_VIDEO = ASSETS / "interaction-tour-raw.webm"
OUT_MP4 = ASSETS / "interaction-tour.mp4"
OUT_WEBM = ASSETS / "interaction-tour.webm"
OUT_MP3 = ASSETS / "interaction-voiceover.mp3"
CUES_FILE = ASSETS / "interaction-voiceover-cues.json"

# Timestamps (ms) aligned to ~59s capture-interaction-tour.py pacing.
CUES = [
    {"id": "01-intro", "start_ms": 0, "text": "Welcome to SLURP! Every major interaction on this page is wired with Alpine.js — let's click through the highlights."},
    {"id": "02-hero-catch", "start_ms": 3500, "text": "First up: the hero dare. Tap the catch button and Chef Marco throws a full SVG splash at your screen — smears, strands, garnishes, the works."},
    {"id": "03-splash", "start_ms": 11000, "text": "Pure CSS and SVG keyframes, with JavaScript seeding random extra noodle strands on each replay. Close the modal when you're done getting roasted."},
    {"id": "04-nav", "start_ms": 15000, "text": "Back to the hero. Notice the frosted desktop nav — pill-shaped links with orange active states and a scroll-progress bar up top."},
    {"id": "05-menu-nav", "start_ms": 19000, "text": "Click a nav pill and the page scrolls to that section. The active link updates as you move — scroll spy baked into one Alpine component."},
    {"id": "06-peacock-menu", "start_ms": 24000, "text": "Long lists use peacock show-more buttons instead of pagination. Three bowls show first — click the peacock to fan out the rest of the vault."},
    {"id": "07-build-nav", "start_ms": 27000, "text": "Build Your Bowl is CSS-only: broth color, noodle style, and toppings all update a live plate preview via custom properties — no image swaps."},
    {"id": "08-build-chips", "start_ms": 30000, "text": "Pick your broth, noodle style, and toppings. Each chip toggles with aria-pressed so screen readers know what's selected."},
    {"id": "09-lock-plate", "start_ms": 33000, "text": "Lock in your plate, then choose Buy or Learn. Buy drops a generated bowl name straight into the cart."},
    {"id": "10-buy-bowl", "start_ms": 36000, "text": "Added to cart — the floating checkout bar and header badge bump to match."},
    {"id": "11-gift-intro", "start_ms": 39000, "text": "Gift a Bowl uses searchable CollectUI-style pickers for delivery location and preset messages — both wired with scoped click-outside handlers."},
    {"id": "12-gift-location", "start_ms": 42000, "text": "Open the location picker, search a city or store, and the live gift card preview updates as you type."},
    {"id": "13-gift-preset", "start_ms": 45000, "text": "Same pattern for preset messages — pick a note and watch it land on the gift card preview."},
    {"id": "14-support-faq", "start_ms": 50000, "text": "Slurp Support: contact channel cards plus an FAQ accordion. Click a question and the answer expands in place."},
    {"id": "15-support-more", "start_ms": 53000, "text": "Four FAQs show first; the peacock reveals the rest — same progressive-disclosure pattern as menu and reviews."},
    {"id": "16-checkout", "start_ms": 56000, "text": "Finally, checkout — your cart summary, qty steppers, and a client-side order flow. Every button click you just saw lives in one index.html file."},
]


def run(cmd: list[str]) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True)


def generate_segments() -> list[dict]:
    SEG_DIR.mkdir(parents=True, exist_ok=True)
    segments: list[dict] = []

    for cue in CUES:
        aiff = SEG_DIR / f"{cue['id']}.aiff"
        mp3 = SEG_DIR / f"{cue['id']}.mp3"
        txt = SEG_DIR / f"{cue['id']}.txt"
        txt.write_text(cue["text"], encoding="utf-8")

        if not mp3.exists() or mp3.stat().st_mtime < txt.stat().st_mtime:
            run(["say", "-v", "Samantha", "-r", "180", "-o", str(aiff), "-f", str(txt)])
            run([
                "ffmpeg", "-y", "-i", str(aiff),
                "-codec:a", "libmp3lame", "-qscale:a", "2",
                str(mp3),
            ])
            if aiff.exists():
                aiff.unlink()

        segments.append({"id": cue["id"], "start_ms": cue["start_ms"], "path": str(mp3)})
        print(f"  {cue['id']}: {mp3.name}")

    return segments


def probe_duration(path: Path) -> float:
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path),
    ], text=True).strip()
    return float(out)


MIN_GAP_MS = 200  # silence between voiceover segments


def schedule_segments(cues: list[dict], segments: list[dict], video_duration: float) -> list[dict]:
    """Place clips on cue times; speed up (atempo) if a clip would overlap the next."""
    scheduled: list[dict] = []
    prev_end_ms = 0
    video_end_ms = int(video_duration * 1000)

    for i, (cue, seg) in enumerate(zip(cues, segments)):
        path = Path(seg["path"])
        raw_duration_ms = int(probe_duration(path) * 1000)
        start_ms = max(cue["start_ms"], prev_end_ms + (MIN_GAP_MS if scheduled else 0))

        next_boundary_ms = cues[i + 1]["start_ms"] if i + 1 < len(cues) else video_end_ms
        max_duration_ms = max(next_boundary_ms - MIN_GAP_MS - start_ms, 400)

        if raw_duration_ms > max_duration_ms:
            atempo = min(raw_duration_ms / max_duration_ms, 1.8)
            duration_ms = int(raw_duration_ms / atempo)
        else:
            atempo = 1.0
            duration_ms = raw_duration_ms

        scheduled.append(
            {
                **seg,
                "start_ms": start_ms,
                "cue_start_ms": cue["start_ms"],
                "duration_ms": duration_ms,
                "raw_duration_ms": raw_duration_ms,
                "atempo": round(atempo, 3),
            }
        )
        prev_end_ms = start_ms + duration_ms

    return scheduled


def extend_video_to_duration(src: Path, dst: Path, target_duration: float) -> None:
    """Pad the last frame if voiceover runs slightly past the captured tour."""
    current = probe_duration(src)
    if target_duration <= current + 0.05:
        if src != dst:
            shutil.copy2(src, dst)
        return

    pad = target_duration - current
    run([
        "ffmpeg", "-y",
        "-i", str(src),
        "-vf", f"tpad=stop_mode=clone:stop_duration={pad:.3f}",
        "-c:v", "libvpx-vp9", "-crf", "32", "-b:v", "0",
        "-an",
        str(dst),
    ])


def merge_audio(segments: list[dict], video_duration: float) -> tuple[Path, float]:
    scheduled = schedule_segments(CUES, segments, video_duration)
    total_ms = scheduled[-1]["start_ms"] + scheduled[-1]["duration_ms"]
    audio_duration = max(video_duration, total_ms / 1000 + 0.15)

    mixed = ASSETS / "interaction-voiceover-mixed.wav"

    inputs: list[str] = []
    filter_parts: list[str] = []
    mix_inputs: list[str] = []

    for i, seg in enumerate(scheduled):
        inputs.extend(["-i", seg["path"]])
        delay = seg["start_ms"]
        label = f"a{i}"
        tempo = seg["atempo"]
        if tempo > 1.001:
            filter_parts.append(
                f"[{i}:a]atempo={tempo},adelay={delay}|{delay},"
                f"apad=pad_dur={audio_duration}[{label}]"
            )
        else:
            filter_parts.append(
                f"[{i}:a]adelay={delay}|{delay},apad=pad_dur={audio_duration}[{label}]"
            )
        mix_inputs.append(f"[{label}]")

    n = len(scheduled)
    filter_parts.append(
        f"{''.join(mix_inputs)}amix=inputs={n}:duration=longest:dropout_transition=0,"
        f"apad=pad_dur={audio_duration},atrim=0:{audio_duration}[outa]"
    )
    filter_complex = ";".join(filter_parts)

    cmd = ["ffmpeg", "-y", *inputs, "-filter_complex", filter_complex, "-map", "[outa]", str(mixed)]
    run(cmd)

    run([
        "ffmpeg", "-y", "-i", str(mixed),
        "-codec:a", "libmp3lame", "-qscale:a", "2",
        str(OUT_MP3),
    ])
    mixed.unlink(missing_ok=True)

    CUES_FILE.write_text(
        json.dumps(
            [
                {
                    "id": seg["id"],
                    "start_ms": seg["start_ms"],
                    "cue_start_ms": seg["cue_start_ms"],
                    "duration_ms": seg["duration_ms"],
                    "raw_duration_ms": seg["raw_duration_ms"],
                    "atempo": seg["atempo"],
                    "path": seg["path"],
                }
                for seg in scheduled
            ],
            indent=2,
        ),
        encoding="utf-8",
    )
    return OUT_MP3, audio_duration


def merge_video_audio() -> None:
    if not RAW_VIDEO.exists():
        raise FileNotFoundError(f"Missing raw video: {RAW_VIDEO}. Run capture-interaction-tour.py first.")

    duration = probe_duration(RAW_VIDEO)
    print(f"Raw video duration: {duration:.1f}s")

    segments = generate_segments()
    _, audio_duration = merge_audio(segments, duration)

    padded_video = ASSETS / "interaction-tour-padded.webm"
    extend_video_to_duration(RAW_VIDEO, padded_video, audio_duration)
    print(f"Voiceover duration: {audio_duration:.1f}s")

    run([
        "ffmpeg", "-y",
        "-i", str(padded_video),
        "-i", str(OUT_MP3),
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(OUT_MP4),
    ])
    padded_video.unlink(missing_ok=True)

    run([
        "ffmpeg", "-y",
        "-i", str(OUT_MP4),
        "-c:v", "libvpx-vp9", "-crf", "32", "-b:v", "0",
        "-c:a", "libopus",
        str(OUT_WEBM),
    ])

    print(f"\nSaved composite video:")
    print(f"  {OUT_MP4} ({OUT_MP4.stat().st_size // 1024} KB)")
    print(f"  {OUT_WEBM} ({OUT_WEBM.stat().st_size // 1024} KB)")
    print(f"  {OUT_MP3} ({OUT_MP3.stat().st_size // 1024} KB)")


def write_plain_text() -> None:
    blocks = [c["text"] for c in CUES]
    (ASSETS / "interaction-voiceover-plain.txt").write_text("\n\n".join(blocks) + "\n", encoding="utf-8")


if __name__ == "__main__":
    write_plain_text()
    try:
        merge_video_audio()
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
