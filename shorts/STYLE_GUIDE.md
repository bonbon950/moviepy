# Bjorn's Shorts Style Guide

Built from a scan of 14 of my own edits (Drive folder "MY STYLE (for claude)") plus my SFX pack.
This file is the rulebook for every clip. Version 0.3 — Bjorn's decisions + reference style (see bottom).

## Hard rules (never break)

| Rule | Value |
|---|---|
| Aspect / resolution | 9:16, **1080×1920**, 30 fps |
| Length | **40–50 s** target |
| Header | **Always** a header text in the top band, visible the whole video |
| Captions | **Always animated** (word-by-word highlight / pop). Never static. |
| SFX | Heavy — **especially the first 3–5 s** — and always matched to the scene |
| Creators | Kai Cenat, TJR, Duke Dennis, Rakai, Fanum |
| Audio | Original audio + SFX + **a quiet background beat** (decided v0.3) |
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

### 7. Audio (updated v0.3)
- Original audio + SFX + a quiet background beat, like the references.

### 8. Reference
- No "best performer" data available — the 14-video folder is the baseline.

### 9. Zooms — subtle but noticeable
- Add zoom-ins/outs on beats so long shots don't go stale.
- Pick the intensity per clip:
  - **Punch zoom (aggressive, ~115–125%, 2–4 frames)** on reactions, roasts, SFX hits.
  - **Slow push (gentle, 100→108% over 2–4 s)** on talking/explaining stretches.
- Viewers should notice the movement, but it must never feel shaky or nauseating.

---

# v0.3 — Reference style ("IDEAL EDIT SHORTS (FOR CLAUDE)")

Scanned 3 reference shorts frame-by-frame (2 fps), with audio tagging (AudioSet model),
transcripts, cut detection and spectrograms, plus 2 screenshots Bjorn marked as important.
**This is the edit style Bjorn wants.** Take the ideas, be different, keep the same vibe.

## ⭐ RULE: Action tags + SFX (most important)
Every time something happens that isn't speech, show it on screen as a tag between asterisks
and hit it with a matching sound effect.

- **Laughing is mandatory:** whenever someone laughs → `*KAI LAUGHS*` / `*FANUM LAUGHING*`
  (name of the person when known) + a laugh-type SFX or bass hit. Detected automatically
  with the audio tagger (Laughter / Giggle / Chuckle / Belly laugh / Snicker), checked by eye.
- Other actions seen in the references: `*CALLS SPEED*`, `*RAT NOISES*`, `*CONFUSED*`,
  `*AGENT COSTUME*`, `*HYPED*`, `*PIZZA IN THE OVEN*`, `*CORRECT*`, `*TELL TOTA*`, `*$300*`.
- Look: **tall condensed bold font (Bebas Neue / Anton style), ALL CAPS, white with a thick
  black outline**, centered, same spot as the captions (it replaces the caption while it's on).
  Variant: white text on a **dark red box** (screenshot 2).
- Duration: hold for the whole action (0.5–2 s), pop in with a slight scale bounce.
- Pair with a visual: punch zoom and/or a quick color flash (pink/red on laughs, see below).

## Captions (reference style)
- **One word at a time**, centered on the subject's chest/face area, condensed bold font
  (same family as the action tags), white with black outline.
- **Color per speaker** — each person gets a caption color (white / lime-yellow / light blue /
  yellow) so viewers know who is talking. Keep the same color for that person all video.
- **Special-voice color:** a different color/box for phone voices, voicemail, chat TTS, etc.
  (ref 1 used a purple box for the voicemail voice).
- **Keyword color:** money and numbers in green (`$300`).
- Censor curse words with an asterisk in the caption (`F*CKING`, `B*TCH`) — never uncensored.

## Visual effects
- **Fast cuts:** ref 2 cuts roughly every 0.5–1 s in hype parts; refs 1/3 every 1–3 s.
  Remove every pause; jump cut between sentences.
- **Punch zooms** on the face on reactions (ref 1 at 8 s, ref 3 at 14 s).
- **Color flashes:** 2–4 frame color wash on hits — black & white flash (ref 2 at 3.5 s),
  green flash (ref 2 at 21 s), pink/red flash on laughs (ref 3 at 12 s and 17.5 s).
- **Motion-blur whip transitions** between shots (ref 2).
- **Color grade:** punchy — extra saturation and contrast, slight glow (ref 2).
- **Meme / B-roll cutaway:** a 1–2 s visual joke that matches what was said (ref 1: man pouring
  money into the ocean with `*$300*` while he says "you wasted $300").
- **Layout switches mid-clip:** full-screen face crop for reactions, blur sandwich for wide
  shots (ref 1 switches to the wide shot for `*CALLS SPEED*`; ref 3 mixes both).
- Stream timers and chat overlays stay visible.
- End on a punch: echo effect on the last word (ref 3 "OWVEN?") or a final meme hit.

## Sound design (measured)
- Bass **booms / beat drops land on the punchlines**, exactly synced with flashes and tags
  (ref 3: 12.3 s on *KAI LAUGHS*, 17.6 s on the red flash; ref 1: drop at 13.3 s after the
  voicemail, boom at 23.2 s on "ARE YOU SERIOUS?!").
- Meme sounds used: FAHHH-style scream on the cutaway (ref 1 16.5 s), siren (ref 2 2.5 s and
  21.5 s), quack/silly end hit (ref 2 25.5 s), bell (ref 3 0 s), echo tail (ref 3 21.5 s).
- ⚠️ **All 3 references have a background music bed under the whole clip** (detected in
  almost every second). **Decided: use a music bed (option B).**

## Kept from Bjorn's rules even though the references don't do it
- The references have **no header** — Bjorn's rule says always have one → keep the header.
- The references are 22–28 s — Bjorn's target is 40–50 s → keep 40–50 s.
- The references crop tight on faces — Bjorn said minimal crop → tight crop only for
  reaction punch-ins, otherwise minimal.

## SFX library
- `shorts/sfx_manifest.tsv` lists 67 sounds by category with when to use each.
  `python3 shorts/tools/fetch_sfx.py OUT_DIR` rebuilds the library from Myinstants in about a minute.
- Plus Bjorn's own 12-sound pack (gunshot, NANI, bell, DING...).
- `shorts/tools/tagaudio.py` finds laughs and other sound events in any clip.

## Music bed (decided: option B)
- A beat runs under the whole clip, **quiet**: about 18–22 dB below the dialogue, and it
  automatically dips further while people talk, so speech is never buried.
- Energy matches the clip: phonk / drill / trap for hype or chaos, a lighter beat for flex or
  chill clips. The beat changes from clip to clip.
- **Beat drop / bass hit on the punchline**, synced with the action tag + flash (the reference
  trick). Before a big moment, the music can cut to silence for 0.3–0.5 s, then slam back in.
- Music never covers a laugh, a key line, or an SFX hit.
- Source: beats Bjorn puts in a Drive folder "BEATS (FOR CLAUDE)". For TikTok/IG, adding a
  trending sound in the app at low volume at upload also helps reach. A baked-in bed stays
  for YouTube Shorts.

## Background music — VIRAL ONLY (Bjorn, v0.4)
- **Only use viral, commonly used shorts sounds.** No new/unknown tracks — familiar sounds
  keep retention because viewers instantly recognize the vibe.
- **The music must match the scene.** If no viral track fits, use no music rather than the wrong one.
- Library: `shorts/beds_manifest.tsv` (Sneaky Snitch, Fluffing a Duck, Investigations,
  SpongeBob investigation, Pink Panther, Mission Impossible flute, Jeopardy thinking, elevator,
  Curb Your Enthusiasm outro, sad violin, Chopin Nocturne for flex, Oh No No No...) and
  `shorts/beats_manifest.tsv` (Brazilian phonk / montagem for hype).
- Vibe reference: CapCut Commercial library picks Bjorn screenshotted (Laugh Meme So Laugh,
  Laughter in the Investigated, Sneaky Comedy, Comedy Scenes, Quirky Comedy, Plot humor sneaky,
  FICO PRESO Ultra Slowed, Aggressive Game Surge, Trap Epic, Ho no no no) → comedic/sneaky/
  investigation beds for funny clips, slowed phonk/trap for hype.
- Bjorn will send more track names later; add them here.

## v0.5 — Bjorn's notes on test edit v1 ("NEED IMPROVEMENT (FOR CLAUDE)")

### Action tags: move around, change size
- **Never all in one spot.** Every tag gets its own position, chosen for the scene:
  - **Eye level** inside the video band (y ≈ 780–1000 of 1920), left / center / right,
    next to the person or action it describes.
  - **Sometimes** in the empty bottom blur band (y ≈ 1350–1560, centered) — the area Bjorn
    circled. Not every time; mix it up.
- **Size varies** per tag (≈ 92–145 px): noticeably bigger on big moments, never covering the screen.
- Slight tilt (±2–7°), pop-in with overshoot, then a slow "breathing" grow while on screen.
- Captions keep running when a tag is placed away from the caption spot.

### Emoji stickers
- Add emoji on memorable moments (laughs, shock, cringe, roasts) — **sometimes**, not every beat.
- **Always matched to the scene**, e.g. catching something weird → 💀💀💀, crying/loss → 😭😭,
  laughing → 😂😂, rage → 🤬, searching → 👀, wisdom → 💯, nail/beauty → 💅💔.
- Placement: usually the empty bottom band; sometimes a corner at eye level.
- 1–3 emoji in a row, each slightly tilted, pop in, gentle bob.

### Emoji quality
- **High-res glossy 3D emoji** (Microsoft Fluent Emoji 3D, 256 px, MIT license) — the iPhone-style
  look. Apple's own emoji artwork is Apple property and can't be bundled.
  `python3 shorts/tools/fetch_emoji.py OUT_DIR` downloads the set (58 emoji).
