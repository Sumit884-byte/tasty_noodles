#!/usr/bin/env python3
"""Generate bowl-aware learn instructions and modular Chef Marco audio via Arka edge TTS."""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIO_DIR = ROOT / "assets" / "audio" / "learn" / "en"
RECIPES_PATH = ROOT / "assets" / "learn" / "recipes-en.json"
MANIFEST_PATH = AUDIO_DIR / "manifest.json"

VOICE = "en-IN-PrabhatNeural"
STEP_TOTAL = 7

BROTHS = ["tonkotsu", "chili", "sesame"]
NOODLES = ["thick", "thin"]
TOPPINGS = ["scallion", "egg", "chashu", "chili", "sesame", "peanut"]

NOODLE_STYLE = {"thick": "hand-pulled", "thin": "ramen"}

BROTH_LABELS = {
    "tonkotsu": "tonkotsu",
    "chili": "dragon chili",
    "sesame": "sesame dan dan",
}

NOODLE_LABELS = {
    "thick": "hand-pulled thick noodles",
    "thin": "silk-thin noodles",
}

NOODLE_STEPS: dict[str, list[dict[str, str]]] = {
    "hand-pulled": [
        {
            "title": "Mix the dough",
            "body": "Combine 300g bread flour, 150ml warm water, and ½ tsp salt. Stir until shaggy, then knead 8–10 minutes until smooth and springy.",
            "tip": "Dough should feel like a soft earlobe — firm but forgiving.",
            "time": "10 min",
        },
        {
            "title": "Rest & knead again",
            "body": "Wrap in plastic and rest 30 minutes. Knead 2 more minutes — the gluten relaxes and the pull gets easier.",
            "tip": "Skip the rest and the noodles snap instead of stretch.",
            "time": "30 min rest",
        },
        {
            "title": "Oil & coil",
            "body": "Brush the dough with neutral oil. Roll into a long snake and coil it into a tight spiral on an oiled tray.",
            "tip": "Oil is your insurance policy against sticking.",
            "time": "5 min",
        },
        {
            "title": "Pull the strands",
            "body": "Hold both ends, bounce gently, fold in half, and repeat. Each fold doubles the strands — aim for pencil-thin noodles.",
            "tip": "Pull over the pot so they drop straight into boiling water.",
            "time": "5 min",
        },
        {
            "title": "Boil & slurp",
            "body": "Boil in salted rolling water 2–3 minutes until they float and taste chewy. Rinse briefly if serving cold, or ladle straight into the hot {brothLabel} broth you started in step one.",
            "tip": "Fresh noodles cook fast — taste at 90 seconds.",
            "time": "3 min",
        },
    ],
    "ramen": [
        {
            "title": "Make alkaline dough",
            "body": "Mix 300g high-protein flour with 120ml water plus 1 tsp baked baking soda dissolved in warm water (kansui substitute). Knead until tight.",
            "tip": "Alkaline water gives ramen its signature yellow color and chew.",
            "time": "12 min",
        },
        {
            "title": "Rest the dough",
            "body": "Wrap tightly and rest 1 hour at room temperature — or overnight in the fridge for extra chew.",
            "tip": "Cold rest makes rolling much easier.",
            "time": "1 hr rest",
        },
        {
            "title": "Roll thin sheets",
            "body": "Divide dough, flatten with a rolling pin or pasta machine to about 1.5mm thick. Dust lightly with cornstarch between folds.",
            "tip": "Cornstarch, not flour — it keeps strands separate.",
            "time": "15 min",
        },
        {
            "title": "Cut the noodles",
            "body": "Fold the sheet accordion-style and slice into 2mm strips with a sharp knife. Shake loose and dust again.",
            "tip": "Uneven cuts cook unevenly — slow down on the last fold.",
            "time": "5 min",
        },
        {
            "title": "Par-boil & finish",
            "body": "Boil 60–90 seconds, drain, and rinse once. Reheat in your {brothLabel} broth for 30 seconds before serving — never overcook twice.",
            "tip": "Par-cooking lets you prep ahead for ramen night.",
            "time": "2 min",
        },
    ],
    "udon": [
        {
            "title": "Salt-water dough",
            "body": "Dissolve 2 tbsp salt in 240ml water. Mix into 300g all-purpose flour until a shaggy, wet dough forms — udon is intentionally soft.",
            "tip": "It will feel too wet. That is correct.",
            "time": "5 min",
        },
        {
            "title": "Knead with weight",
            "body": "Knead 5 minutes, then stomp the dough with your feet (in a bag) or press with a heavy pan for 5 more. The gluten needs abuse.",
            "tip": "Traditional udon shops literally foot-knead — you can too.",
            "time": "10 min",
        },
        {
            "title": "Long rest",
            "body": "Wrap and rest at least 4 hours — overnight is best. The dough will relax and become smooth.",
            "tip": "Plan udon a day ahead; it rewards patience.",
            "time": "4+ hr rest",
        },
        {
            "title": "Roll & cut thick",
            "body": "Roll to 4–5mm thick. Cut into 4mm-wide strips — udon should be fat, square, and proud.",
            "tip": "Thicker noodles = longer boil. Do not rush the cut.",
            "time": "10 min",
        },
        {
            "title": "Boil until buoyant",
            "body": "Boil in plenty of water 10–12 minutes until noodles float and the center is translucent. Rinse in cold water for chewy texture, or serve hot in the {brothLabel} broth from step one.",
            "tip": "Cold rinse stops carryover cooking — essential for salad udon.",
            "time": "12 min",
        },
    ],
}

BROTH_STEPS: dict[str, dict[str, str]] = {
    "tonkotsu": {
        "title": "Start the tonkotsu",
        "body": "Blanch 1 kg pork bones, then simmer with water, ginger, and garlic for at least 4 hours. Skim foam, strain, and season with a splash of soy. Let it bubble away while you make the noodles.",
        "tip": "Milky white color means you did it right — emulsified fat is the goal.",
        "time": "4+ hr simmer",
    },
    "chili": {
        "title": "Build the chili broth base",
        "body": "Heat half a cup of neutral oil until shimmering. Pour over chili flakes, minced garlic, and Sichuan peppercorn. Stir in soy and a pinch of sugar. This is your dragon chili broth — not the chili crisp topping later.",
        "tip": "Pour the hot oil from high — the sizzle is the whole point.",
        "time": "10 min",
    },
    "sesame": {
        "title": "Whisk the sesame broth base",
        "body": "Combine 3 tbsp sesame paste, 2 tbsp soy sauce, 1 tbsp rice vinegar, and half a cup of warm stock until silky smooth. This is your sesame dan dan broth — separate from any sesame seed topping.",
        "tip": "Thin with hot stock, not water — it keeps the nutty flavor.",
        "time": "5 min",
    },
}

TOPPING_PREP: dict[str, str] = {
    "scallion": "Finish with sliced scallions on top.",
    "egg": "Halve a jammy soft-boiled egg and place yolk-side up.",
    "chashu": "Lay warm chashu slices over the noodles.",
    "chili": "Spoon chili crisp on top as a finishing heat — this is separate from your dragon chili broth base.",
    "sesame": "Scatter toasted sesame seeds for crunch — separate from your sesame dan dan broth base.",
    "peanut": "Crush roasted peanuts and sprinkle generously.",
}

ASSEMBLY = {
    "title": "Top your bowl",
    "bodyIntro": "Ladle your {noodleLabel} into the steaming {brothLabel} broth from step one.",
    "noToppings": "Serve straight — pure noodle confidence today.",
    "tip": "Eat while the noodles still have bounce — timing is everything.",
    "time": "2 min",
}

ALL_DONE = "All seven steps complete. Time to slurp your bowl!"


def fill(template: str, ctx: dict[str, str]) -> str:
    out = template
    for key, value in ctx.items():
        out = out.replace("{" + key + "}", value)
    return out


def bowl_key(broth: str, noodles: str, toppings: list[str]) -> str:
    tops = "-".join(sorted(toppings)) if toppings else "none"
    return f"{broth}-{noodles}-{tops}"


def build_recipe(broth: str, noodles: str, toppings: list[str]) -> dict[str, object]:
    style = NOODLE_STYLE[noodles]
    ctx = {
        "brothLabel": BROTH_LABELS[broth],
        "noodleLabel": NOODLE_LABELS[noodles],
    }
    steps: list[dict[str, object]] = []

    broth_step = BROTH_STEPS[broth]
    steps.append(
        {
            "index": 0,
            "phase": "broth",
            "title": broth_step["title"],
            "body": broth_step["body"],
            "tip": broth_step["tip"],
            "time": broth_step["time"],
        }
    )

    for noodle_index, step in enumerate(NOODLE_STEPS[style]):
        steps.append(
            {
                "index": noodle_index + 1,
                "phase": "noodle",
                "title": step["title"],
                "body": fill(step["body"], ctx),
                "tip": step["tip"],
                "time": step["time"],
            }
        )

    topping_lines = " ".join(TOPPING_PREP[t] for t in sorted(toppings)) if toppings else ASSEMBLY["noToppings"]
    assembly_body = f"{fill(ASSEMBLY['bodyIntro'], ctx)} {topping_lines}"
    steps.append(
        {
            "index": 6,
            "phase": "assembly",
            "title": ASSEMBLY["title"],
            "body": assembly_body,
            "tip": ASSEMBLY["tip"],
            "time": ASSEMBLY["time"],
        }
    )

    return {
        "key": bowl_key(broth, noodles, toppings),
        "style": style,
        "broth": broth,
        "noodles": noodles,
        "toppings": sorted(toppings),
        "steps": steps,
    }


def build_speech(step: dict[str, str], index: int) -> str:
    intro = f"Step {index + 1} of {STEP_TOTAL}. {step['title']}."
    tip = f"Chef Marco tip: {step['tip']}"
    return f"{intro} {step['body']} {tip}"


def all_recipes() -> dict[str, dict[str, object]]:
    recipes: dict[str, dict[str, object]] = {}
    for broth, noodles in itertools.product(BROTHS, NOODLES):
        for r in range(len(TOPPINGS) + 1):
            for combo in itertools.combinations(TOPPINGS, r):
                recipe = build_recipe(broth, noodles, list(combo))
                recipes[str(recipe["key"])] = recipe
    return recipes


def main() -> int:
    try:
        from arka.voice.edge_speak import synthesize_to_file
    except ImportError as exc:
        print("arka package not found — install arka or run from its venv", file=sys.stderr)
        raise SystemExit(1) from exc

    recipes = all_recipes()
    RECIPES_PATH.parent.mkdir(parents=True, exist_ok=True)
    RECIPES_PATH.write_text(
        json.dumps(
            {
                "stepTotal": STEP_TOTAL,
                "permutationCount": len(recipes),
                "templates": {
                    "broths": BROTHS,
                    "noodles": NOODLES,
                    "toppings": TOPPINGS,
                },
                "recipes": recipes,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(recipes)} bowl recipes to {RECIPES_PATH}")

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, object] = {
        "voice": VOICE,
        "locale": "en",
        "stepTotal": STEP_TOTAL,
        "broth": {},
        "steps": {},
        "stepBoilBroth": {"hand-pulled": {}, "ramen": {}},
        "assemblyLadle": {},
        "topping": {},
        "assemblyTip": "assembly-tip.mp3",
        "allDone": "all-done.mp3",
    }

    jobs: list[tuple[str, str]] = []

    for broth, step in BROTH_STEPS.items():
        filename = f"broth-{broth}.mp3"
        jobs.append((filename, build_speech(step, 0)))
        manifest["broth"][broth] = filename

    for style, steps in NOODLE_STEPS.items():
        manifest_steps: list[str] = []
        for noodle_index, step in enumerate(steps):
            learn_index = noodle_index + 1
            if noodle_index < 4:
                filename = f"{style}-{noodle_index}.mp3"
                jobs.append((filename, build_speech(step, learn_index)))
                manifest_steps.append(filename)
            elif style in ("hand-pulled", "ramen"):
                for broth in BROTHS:
                    ctx = {"brothLabel": BROTH_LABELS[broth], "noodleLabel": ""}
                    filled = {**step, "body": fill(step["body"], ctx)}
                    filename = f"{style}-4-{broth}.mp3"
                    jobs.append((filename, build_speech(filled, learn_index)))
                    manifest["stepBoilBroth"][style][broth] = filename
                manifest_steps.append(f"{style}-4-{{broth}}.mp3")
            else:
                filename = f"{style}-4.mp3"
                ctx = {"brothLabel": "prepared", "noodleLabel": ""}
                filled = {**step, "body": fill(step["body"], ctx)}
                jobs.append((filename, build_speech(filled, learn_index)))
                manifest_steps.append(filename)
        manifest["steps"][style] = manifest_steps

    for noodles, broth in itertools.product(NOODLES, BROTHS):
        ctx = {"brothLabel": BROTH_LABELS[broth], "noodleLabel": NOODLE_LABELS[noodles]}
        ladle_line = fill(ASSEMBLY["bodyIntro"], ctx)
        filename = f"assembly-ladle-{noodles}-{broth}.mp3"
        jobs.append(
            (
                filename,
                f"Step 7 of {STEP_TOTAL}. {ASSEMBLY['title']}. {ladle_line}",
            )
        )
        manifest["assemblyLadle"][f"{noodles}-{broth}"] = filename

    jobs.append(("assembly-tip.mp3", f"Chef Marco tip: {ASSEMBLY['tip']}"))

    for topping, prep in TOPPING_PREP.items():
        filename = f"topping-{topping}.mp3"
        jobs.append((filename, prep))
        manifest["topping"][topping] = filename

    jobs.append(("topping-none.mp3", ASSEMBLY["noToppings"]))
    manifest["topping"]["none"] = "topping-none.mp3"

    jobs.append(("all-done.mp3", ALL_DONE))

    for index, (filename, text) in enumerate(jobs, start=1):
        print(f"[{index}/{len(jobs)}] {filename}")
        synthesize_to_file(text, AUDIO_DIR / filename, voice=VOICE)

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"\nWrote {len(jobs)} audio clips to {AUDIO_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
