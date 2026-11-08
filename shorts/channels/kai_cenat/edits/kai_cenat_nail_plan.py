"""Edit plan: Kai Cenat — AMP Halloween Party (VOD 2915383492), broken-nail moment (VOD 1:17:50-1:19:50).

Builds plan.json for make_short.py. Source = nail_src.mp4 (VOD 4670-4790 s).
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "tools"))
from captions import to_captions

S = sys.argv[1]            # scratchpad dir
V = f"{S}/vod"
SFX, BEDS = f"{S}/sfx_lib", f"{S}/beds"

keep = [[35.9, 37.9],      # cold open: "YOU BROKE MY F*CKING NAIL!"
        [21.0, 38.3],      # Power Ranger arrives -> dap -> nail breaks -> scream/laughs -> floor search -> yelling
        [41.9, 45.0],      # "say sorry bro, say sorry" -> no apology
        [93.0, 119.2]]     # nails lost -> "that's just life" -> "you like my CONTACTS? rest is wack"
# output = src - offset per range: cold 0-2.0 | A 2.0-19.3 (src-19.0) | B 19.3-22.4 (src-22.6) | C 22.4-48.6 (src-70.6)

KAI, AGENT = "#FFFFFF", "#7FD8FF"
def speaker(t):
    if 42.9 <= t < 44.6: return "agent"                    # "say sorry bro"
    if 99.8 <= t < 104.5 or 106.4 <= t < 112.0: return "agent"   # life advice + "I like your contacts"
    return "kai"

words = json.load(open(f"{V}/nail_words.json"))
caps = to_captions(words, keep, speaker_of=speaker, speaker_colors={"kai": KAI, "agent": AGENT})
FIX = {"PUT": "BROKE", "WAGS": "WACK"}   # speech-to-text mistakes checked by ear/transcript
for c in caps:
    c["w"] = FIX.get(c["w"], c["w"])

plan = {
    "source": f"{V}/nail_src.mp4", "keep": keep, "layout": "sandwich", "fonts_dir": f"{S}/fonts",
    "header": {"lines": ["A POWER RANGER", "BROKE KAI'S NAIL \U0001F62D"], "color": "#FF2E88"},
    "words": caps,
    # Positions: video band is y 656-1264 (eye level ~780-1000); empty bottom band zone ~y 1350-1560.
    "tags": [
        {"t": 2.0, "e": 2.9, "text": "*MOMENTS EARLIER*", "x": 540, "y": 770, "size": 96},
        {"t": 3.0, "e": 4.5, "text": "*EVERYONE LAUGHS*", "box": "#8B0000", "x": 540, "y": 1440, "size": 118, "rot": -4},
        {"t": 5.9, "e": 6.7, "text": "*NAIL BREAKS*", "box": "#8B0000", "x": 380, "y": 900, "size": 132, "rot": 5},
        {"t": 12.4, "e": 13.0, "text": "*KAI SCREAMS*", "x": 700, "y": 820, "size": 128, "rot": -6},
        {"t": 12.9, "e": 13.9, "text": "*EVERYONE LAUGHS*", "box": "#8B0000", "x": 540, "y": 1450, "size": 112, "rot": 3},
        {"t": 13.3, "e": 14.5, "text": "*SEARCHING FOR HIS NAIL*", "x": 540, "y": 960, "size": 92, "rot": 2},
        {"t": 21.9, "e": 22.4, "text": "*NO SORRY*", "x": 760, "y": 860, "size": 142, "rot": -7},
        {"t": 24.3, "e": 25.2, "text": "*THEY LAUGH*", "box": "#8B0000", "x": 540, "y": 1440, "size": 116, "rot": 4},
    ],
    # glossy 3D emoji, picked per scene (not on every beat)
    "stickers": [
        {"t": 0.9, "e": 2.0, "emoji": "\U0001F62D\U0001F62D", "x": 540, "y": 1450, "size": 190},   # Kai screaming over the nail
        {"t": 3.0, "e": 4.5, "emoji": "\U0001F602\U0001F602", "x": 860, "y": 770, "size": 135},   # laughing at the Ranger
        {"t": 6.7, "e": 8.4, "emoji": "\U0001F485\U0001F494", "x": 540, "y": 1460, "size": 185},   # nail polish + broken heart
        {"t": 13.3, "e": 14.5, "emoji": "\U0001F440", "x": 190, "y": 790, "size": 150},             # searching the floor
        {"t": 17.8, "e": 19.3, "emoji": "\U0001F92C", "x": 540, "y": 1450, "size": 200},            # "MY F*CKING NAIL!"
        {"t": 30.0, "e": 33.2, "emoji": "\U0001FAE1", "x": 540, "y": 1450, "size": 180},            # "that's just life"
        {"t": 38.3, "e": 40.6, "emoji": "\U0001F4AF", "x": 540, "y": 1450, "size": 200},  # words of wisdom
        {"t": 45.0, "e": 46.5, "emoji": "\U0001F480\U0001F480\U0001F480", "x": 540, "y": 1450, "size": 170},  # "you like my CONTACTS?"
        {"t": 46.5, "e": 48.6, "emoji": "\U0001F62D\U0001F62D", "x": 540, "y": 1450, "size": 190},  # "the rest is wack"
    ],
    "zooms": [
        {"t": 0.0, "e": 0.55, "type": "punch", "amt": 1.25},
        {"t": 5.9, "e": 6.8, "type": "punch", "amt": 1.25},
        {"t": 12.4, "e": 13.1, "type": "punch", "amt": 1.18},
        {"t": 17.7, "e": 18.6, "type": "punch", "amt": 1.22},
        {"t": 25.3, "e": 37.5, "type": "push", "amt": 1.08},
        {"t": 45.6, "e": 46.6, "type": "punch", "amt": 1.22},
    ],
    "flashes": [
        {"t": 0.0, "d": 0.13, "color": "red"}, {"t": 3.0, "d": 0.12, "color": "pink"},
        {"t": 5.95, "d": 0.13, "color": "red"}, {"t": 13.0, "d": 0.12, "color": "pink"},
        {"t": 17.8, "d": 0.1, "color": "white"}, {"t": 21.9, "d": 0.5, "color": "bw"},
        {"t": 24.3, "d": 0.12, "color": "pink"}, {"t": 46.5, "d": 0.13, "color": "red"},
    ],
    "sfx": [
        # hook (first 3-5 s): stacked, all tied to the action
        {"t": 0.0, "file": f"{SFX}/bass_boom.mp3", "gain_db": -3},          # header slam
        {"t": 0.9, "file": f"{SFX}/vine_boom.mp3", "gain_db": -5},          # on "NAIL!"
        {"t": 1.85, "file": f"{SFX}/record_scratch.mp3", "gain_db": -4},    # rewind
        {"t": 2.0, "file": f"{SFX}/whoosh.mp3", "gain_db": -6},             # *MOMENTS EARLIER*
        {"t": 3.0, "file": f"{SFX}/sitcom_laugh.mp3", "gain_db": -12, "dur": 1.5},
        # story beats
        {"t": 5.9, "file": f"{SFX}/punch.mp3", "gain_db": -3},              # the dap that breaks it
        {"t": 6.0, "file": f"{SFX}/bass_drop.mp3", "gain_db": -6, "dur": 1.5},
        {"t": 12.2, "file": f"{SFX}/vine_boom.mp3", "gain_db": -6},         # "...as f*ck"
        {"t": 12.9, "file": f"{SFX}/sitcom_laugh.mp3", "gain_db": -12, "dur": 1.1},
        {"t": 13.3, "file": f"{SFX}/suspense.mp3", "gain_db": -9, "dur": 1.3},  # searching the floor
        {"t": 17.8, "file": f"{SFX}/bass_boom.mp3", "gain_db": -4},         # "MY F*CKING NAIL!"
        {"t": 21.9, "file": f"{SFX}/bruh.mp3", "gain_db": -4},              # no apology
        {"t": 24.3, "file": f"{SFX}/sitcom_laugh.mp3", "gain_db": -13, "dur": 1.0},
        {"t": 38.2, "file": f"{SFX}/heavenly.mp3", "gain_db": -10, "dur": 2.4},  # words of wisdom
        {"t": 45.0, "file": f"{SFX}/vine_boom.mp3", "gain_db": -5},         # "...my CONTACTS"
        {"t": 46.5, "file": f"{SFX}/bass_boom.mp3", "gain_db": -4},         # "THE REST IS WACK"
    ],
    "beds": [
        {"file": f"{BEDS}/oh-no-no-no-tik-tok-song-sound-effect.mp3", "t": 2.0, "e": 22.4, "gain_db": -19,
         "drops": [[5.7, 6.4], [17.5, 18.3]]},                                  # silence before the hits
        {"file": f"{BEDS}/sad-hamster-violin-meme.mp3", "t": 22.4, "e": 40.6, "gain_db": -17},
        {"file": f"{BEDS}/curb-your-enthusiasm.mp3", "t": 46.6, "e": 48.6, "gain_db": -12},
    ],
}
json.dump(plan, open(f"{V}/nail_plan.json", "w"), indent=1)
print(f"{len(caps)} caption words, {sum(e - s for s, e in keep):.1f}s")
