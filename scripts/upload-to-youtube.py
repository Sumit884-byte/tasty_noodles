#!/usr/bin/env python3
"""Upload interaction-tour.mp4 to YouTube via Data API v3 (OAuth desktop flow).

One-time setup:
  1. Google Cloud Console → create project → enable "YouTube Data API v3"
  2. Credentials → Create OAuth client ID → Desktop app → download JSON
  3. Save as client_secret.json in repo root (gitignored) OR set GOOGLE_OAUTH_CLIENT_JSON
  4. pip install google-api-python-client google-auth-oauthlib google-auth-httplib2

Usage:
  python3 scripts/upload-to-youtube.py
  python3 scripts/upload-to-youtube.py --video assets/blog-scroll-demo.mp4

On first run, a browser opens for Google sign-in. Token saved to token.json (gitignored).
Prints the watch URL on success.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_VIDEO = REPO / "assets/blog/interaction-tour.mp4"
CLIENT_SECRET = Path(
    __import__("os").environ.get("GOOGLE_OAUTH_CLIENT_JSON", REPO / "client_secret.json")
)
TOKEN_FILE = REPO / "token.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

TITLE = "SLURP! Noodle Shop Landing Page — Full Scroll & Interaction Tour"
DESCRIPTION = """A narrated walkthrough of SLURP! — Tastiest Noodles on the Planet, my submission for the DEV Frontend Challenge (Comfort Food Edition, Perfect Landing).

🍜 Live demo: https://tastynoodles.vercel.app
📦 Source code: https://github.com/Sumit884-byte/tasty_noodles
🏆 Challenge: https://dev.to/challenges/frontend-2026-07-29

What's covered in this ~59s tour:
• Hero splash — SVG/CSS noodle splatter animation
• Desktop nav — frosted pill track with scroll-spy
• Peacock show-more — menu vault expands in place
• Build Your Bowl — live CSS plate preview + cart
• Gift a Bowl — searchable delivery & preset pickers
• Slurp Support — FAQ accordion
• CollectUI checkout flow

Stack: single index.html, Tailwind CSS, Alpine.js, Three.js, vanilla JS. No build step.

#frontend #webdev #landingpage #devchallenge #css #javascript #alpinejs
"""
TAGS = [
    "frontend",
    "landing page",
    "alpine.js",
    "css animation",
    "web development",
    "dev challenge",
    "comfort food",
    "noodle shop",
    "three.js",
    "tailwind css",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Upload SLURP! tour video to YouTube")
    parser.add_argument("--video", type=Path, default=DEFAULT_VIDEO)
    parser.add_argument("--privacy", choices=("public", "unlisted", "private"), default="public")
    args = parser.parse_args()

    if not args.video.is_file():
        print(f"Video not found: {args.video}", file=sys.stderr)
        return 1
    if not CLIENT_SECRET.is_file():
        print(
            f"Missing OAuth client JSON at {CLIENT_SECRET}\n"
            "See script docstring for Google Cloud setup.",
            file=sys.stderr,
        )
        return 1

    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError:
        print(
            "Install deps: pip install google-api-python-client google-auth-oauthlib google-auth-httplib2",
            file=sys.stderr,
        )
        return 1

    creds = None
    if TOKEN_FILE.is_file():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json())

    youtube = build("youtube", "v3", credentials=creds)
    body = {
        "snippet": {
            "title": TITLE,
            "description": DESCRIPTION,
            "tags": TAGS,
            "categoryId": "28",  # Science & Technology
        },
        "status": {"privacyStatus": args.privacy},
    }
    media = MediaFileUpload(str(args.video), mimetype="video/mp4", resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    print(f"Uploading {args.video.name}…")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"  {int(status.progress() * 100)}%")

    video_id = response["id"]
    url = f"https://youtube.com/watch?v={video_id}"
    print(f"\nUploaded: {url}")
    print(f"\nAdd to blog-post.md:\n  **YouTube:** {url}\n  {{% embed {url} %}}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
