# Bjorn's Shorts Style Guide

Built from a scan of 14 of my own edits (Drive folder "MY STYLE (for claude)") plus my SFX pack.
This file is the rulebook for every clip. Version 0.2 — Bjorn's decisions locked in (see "Editing decisions").

## Hard rules (never break)

| Rule | Value |
|---|---|
| Aspect / resolution | 9:16, **1080×1920**, 30 fps |
| Length | **40–50 s** target |
| Header | **Always** a header text in the top band, visible the whole video |
| Captions | **Always animated** (word-by-word highlight / pop). Never static. |
| SFX | Heavy — **especially the first 3–5 s** — and always matched to the scene |
| Creators | Kai Cenat, TJR, Duke Dennis, Rakai, Fanum |
| Audio | **Original audio + SFX only. No background music.** |
| Export | H.264/HEVC ≥ 10 Mbps, loudness normalized (see Audio) |
| Never | CapCut end card / watermark, unrelated emojis, garbled captions |

## What the scan measured (14 videos)

### Format
- 14/14 are 1080×1920, 30 fps, HEVC. Bitrate 3.7–11.2 Mbps (v01 is low at 3.7).
- Length: 30–109 s, median ≈ 51 s. Only **4/14** land in the 40–50 s target;
  7 run long (52–63 s, one 109 s), 3 run short (30–37 s).
- Creators: TJR ×7, Kai Cenat ×7.

### Layout — "blur sandwich" (my signature)
- 12/14: the 16:9 stream/vlog shot is scaled to full width in the **middle band**;
  a zoomed, heavily blurred copy of the same footage fills the top and bottom.
- Header sits in the top blur band; captions sit on the lower edge of the video band
  or in the bottom blur band.
- v02: full-screen vertical footage with the header over the video.
- v05: split screen reaction (content top, streamer facecam bottom).
- Twitch chat/overlays are left visible on Kai stream clips.

### Header
- Present in 13/14 (**v14 had none** — rule break).
- Static for the whole video, 1–3 lines, bold heavy sans (one serif: "TJR's LIFESTYLEEE").
- Colors rotate per video: white w/ black stroke, yellow (often w/ glow), red,
  green, pink/magenta. Black outline/drop shadow on all.
- Emojis in 6/14 (🔥 💀 😭 💵 🤑 💸), placed at line end.
- Optional **second text** in the bottom band in 4/14 ("FOR THAT FOOD REVIEW",
  "GIFT From IShowSpeed!!!", "3 MILLION$ CAR 🤑🔥", 🔥💵).
- Only v05 animated the header (yellow-box "KAI" logo sliding in).
- Wording is mostly a **label** ("KAI RECEIVED", "KAI'S IPHONE DUO", "TJR's LIFESTYLEEE")
  rather than a curiosity hook.

### Captions (all animated; 5 styles seen)
1. **Highlight box** (6/14): 2–4 words, ALL CAPS, white w/ black stroke, active word
   in a colored box (purple, teal/blue, black).
2. **Keyword color** (2/14): ALL CAPS white, active word yellow.
3. **Big single word pop** (2/14): one word at a time, large, center of video.
4. **Condensed lowercase bounce** (2/14): active word bigger + yellow.
5. Single small yellow word (1/14).
- Some captions were wrong (v12 auto-captioned Japanese speech into nonsense;
  "cotta/cotton").

### Pacing
- Very few hard cuts: 0–9 per video, median ~2. Average shot 4.6–63 s.
  Most clips are one continuous moment with overlays on top.
- Almost no dead air (0% in 10/14).

### Audio
- Integrated loudness ranges from −7.4 to −15.4 LUFS — an **8 dB spread** between videos.
- **The SFX pack was not found in any of the 14 videos** (audio fingerprint search;
  one weak match in v10 at 10.5 s).

## SFX pack (from "SOUND EFFECTS MOSTLY I USE")
| id | sound | use for |
|---|---|---|
| gunshot / gun_fire | gunshot, gun firing | roast lands, "he's dead", savage line |
| dramatic_hit / dramatic_sting | dramatic music hit | reveal, shock, price drop |
| nani | "NANI?!" | confusion, disbelief |
| bell_ring / bell_toll | bell, boxing bell | round start, argument, "ding ding" |
| ding | DING | correct / idea / price reveal |
| squeak, music_sting, blip1, blip2 | short accents | caption pops, transitions |

## Improvements (ranked by expected view impact)
1. **Hook in the first 1.5 s** — open on the peak/reaction, header as a curiosity hook
   ("KAI DIDN'T EXPECT THIS 😭") instead of a label.
2. **Hit 40–50 s** — 10/14 missed the range; trim setup, end right after the payoff.
3. **Actually use SFX** — 3–8 per clip, synced to reactions and caption pops.
4. **Punch-in zooms / jump cuts every 2–4 s** on long single shots.
5. **One house caption style + one header template** for brand recognition.
6. **Consistent loudness** (−10 LUFS integrated, −1 dBTP), duck original under SFX.
7. Fix captions by hand on non-English or slang; never auto-caption foreign speech.
8. Remove CapCut outro (v12); always include a header (v14); bitrate ≥ 10 Mbps.
9. End on a loopable beat so replays count.

## Editing decisions (from Bjorn, v0.2)

### 1. SFX — retention first
- **Go heavy in the first 3–5 s.** The opening must stop the scroll: stack 2–4 SFX on the
  hook (impact on the first frame, accent on the header pop, hit on the first reaction).
- After the hook, keep using SFX on every real beat (reaction, roast, reveal, punchline).
- **Every SFX must fit the scene and the vibe.** Test for each one: *does it make the moment
  funnier/hit harder, or is it just noise?* If it's noise, cut it.
  - Roast/savage line → gunshot · Shock/reveal → dramatic hit/sting · Confusion → NANI?! ·
    Argument/round start → boxing bell · Price/idea/"correct" → DING · Caption pops → blips.
- Duck original audio ~4–6 dB under each SFX, never bury the dialogue.

### 2. Captions — mix per video
- Choose the caption style per clip from the 5 styles in my catalog (highlight box,
  keyword color, big single-word pop, condensed bounce, single word) — whichever fits the energy:
  - Fast/chaotic/hype (Kai IRL, arguments) → big single-word pop or bounce.
  - Talking/flex/explaining (TJR watches, cars) → 2–4 word highlight box or keyword color.
- One style per video (no mixing inside a clip). Always animated. Hand-check every word.

### 3. Color — attention over habit
- No fixed palette. Pick whatever pops hardest **against that clip's footage**
  (contrast first: e.g. hot pink/cyan on warm footage, orange/red on blue footage).
- Not limited to yellow/green. Can change every video.
- Always a black stroke/shadow so it reads on any background.

### 4. Header — curiosity hook
- The header's job is to stop the scroll and make them watch to the end.
- Use a bold claim, an open loop, or a tension line — never a plain label.
  - ❌ "KAI RECEIVED" → ✅ "IShowSpeed Sent Kai Something He Didn't Expect 😭"
  - ❌ "TJR's LIFESTYLEEE" → ✅ "This Is What $1M/Month Actually Looks Like"
  - ❌ "KAI'S IPHONE DUO" → ✅ "Kai Found A Phone Apple Hasn't Released Yet"
- Must stay true to the clip — no fake claims that the video doesn't pay off.
- 1–2 lines, max ~8 words, 0–1 emoji. I'll write 3 options per clip and pick the strongest.

### 5. Layout — minimal crop
- Default: blur sandwich (16:9 in the middle, blurred fill top/bottom).
- Crop only a little if needed. Never crop so hard it disturbs the viewer.

### 6. Twitch chat / stream overlays
- Keep them visible.

### 7. Audio
- Original audio only. No music beds.

### 8. Reference
- No "best performer" data available — the 14-video folder is the baseline.

### 9. Zooms — subtle but noticeable
- Add zoom-ins/outs on beats so long shots don't go stale.
- Pick the intensity per clip:
  - **Punch zoom (aggressive, ~115–125%, 2–4 frames)** on reactions, roasts, SFX hits.
  - **Slow push (gentle, 100→108% over 2–4 s)** on talking/explaining stretches.
- Viewers should notice the movement, but it must never feel shaky or nauseating.
