"""Batch (v2 style): Kai Cenat — "PLAYING EVERY GTA UNTIL I BEAT IT: Grand Theft Auto 4" (Twitch VOD 2924282282,
Nov 9-11 2026, 35:07:00; the last day of the 130-hour GTA 3 -> GTA 5 marathon).
Gameplay stream: only the full-camera talking moments are used (story frame). Sent by Bjorn for this batch (Nov 11).

usage: kai_cenat_gta_marathon_finale_v2.py WORKDIR VODDIR [clip ...]   (WORKDIR = shorts_work with sfx_lib/fonts/emoji;
       VODDIR holds batch/; all times are VOD seconds; batch/<name>_parts.json maps them)
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "tools"))
from plankit import build, out_times

S = sys.argv[1]; B = f"{sys.argv[2]}/batch"
only = set(sys.argv[3:])
E = lambda *cps: "".join(chr(c) for c in cps)
SKULL, FIRE, HUNDRED, TROPHY, MIC, GRIMACE, MINDBLOWN, TEARS, CROWN, SHOCK = (
    0x1F480, 0x1F525, 0x1F4AF, 0x1F3C6, 0x1F3A4, 0x1F62C, 0x1F92F, 0x1F979, 0x1F451, 0x1F62E)
STORY = dict(layout="story", me_pos=(540, 760),
             laugh_spots=[dict(x=300, y=800, size=108, rot=-5), dict(x=780, y=780, size=108, rot=5),
                          dict(x=540, y=740, size=110, rot=3), dict(x=780, y=820, size=108, rot=-4)])
R, L = dict(x=800, y=770), dict(x=290, y=800)   # eye level beside Kai's face (story frame)
BAND = 1640                                     # bottom band: emoji + evidence pop-ups
results = {}


def run(name, keep_vod, notes, insets=(), **kw):
    if only and name not in only:
        return
    parts = json.load(open(f"{B}/{name}_parts.json"))
    def v(t):                                   # VOD seconds -> SOURCE seconds
        for a, b, vs in parts:
            if vs - 0.01 <= t <= vs + (b - a) + 0.01:
                return round(a + t - vs, 3)
        raise ValueError(f"{name}: VOD {t} not in source")
    keep = [[v(a), v(b)] for a, b in keep_vod]
    def ot(t):                                  # VOD seconds -> OUTPUT seconds
        s = v(t)
        for d in (0, -0.06, 0.06, -0.2, 0.2):
            r = out_times(s + d, keep)
            if r:
                return round(r[-1] - d, 3)
        raise ValueError(f"{name}: VOD {t} not in kept footage")
    kw = {k: (val(ot) if callable(val) else val) for k, val in kw.items()}
    kw["speakers"] = [(v(a), v(b), *r) for a, b, *r in kw.get("speakers", [])]
    kw["overrides"] = [(v(a), v(b), t) for a, b, t in kw.get("overrides", [])]
    plan, dur = build(S, B, name, keep, beds=[], laugh_label="*KAI LAUGHS*", **{**STORY, **kw})
    first_len = keep[0][1] - keep[0][0]
    plan["notes"] = [{"t": 0.1 if a == "START" else ot(a) + (0.9 if i == 1 else 0),
                      "e": first_len if a == "START" else (dur if b == "END" else ot(b)),
                      "text": txt, "y": 440} for i, (a, b, txt) in enumerate(notes)]
    plan["insets"] = [dict(ins, t=ot(ins["t"]), e=(dur if ins["e"] == "END" else ot(ins["e"])),
                           **({"png": f"{B}/{ins['png']}"} if ins.get("png") else {}))
                      for ins in insets]
    plan["story_top"], plan["head_y"] = 540, 200
    json.dump(plan, open(f"{B}/{name}_plan.json", "w"), indent=1)
    results[name] = dur
    print(f"{name}: {dur:.1f}s, {len(plan['words'])} words, {len(plan['notes'])} narrator lines, {len(plan['tags'])} tags")


# 1) FINALE — 130 hours, every GTA beaten, checks his phone: +128K subscribers, next stop Vice City ---------------
run("finale",
    keep_vod=[[126030.5, 126035.4],             # hook: "We went up a hundred and twenty eight thousand subscribers, bro"
              [126013.9, 126017.0],             # "just look at this phone, look at this, bro"
              [126019.3, 126020.8],             # "Holy crap, bro."
              [126021.0, 126024.7],             # "You guys are incredible, bro. 130 hours"
              [126028.4, 126035.6],             # "Check on YouTube for subscribers. We went up 128 thousand subscribers"
              [126039.6, 126042.9],             # "Insane. I look rough now chat, I'm not gonna lie"
              [126128.1, 126131.4],             # "The next time you guys see me will be GTA 6."
              [126132.4, 126136.7],             # "I don't know how I'm going to do it, but chat, we're going to pull it off"
              [126161.5, 126164.6]],            # "I will see you guys in Vice City." -> LOOP
    notes=[("START", None, "THE RESULT OF 130 HOURS:"),
           (126013.9, 126020.8, "HE CHECKS HIS PHONE..."),
           (126021.0, 126024.7, "EVERY GTA. 130 HOURS."),
           (126028.4, 126035.6, "THE NUMBER:"),
           (126039.6, 126042.9, "WORTH IT."),
           (126128.1, 126136.7, "NEXT MISSION: GTA 6"),
           (126161.5, "END", "SEE YOU IN VICE CITY")],
    header={"lines": ["130 HOURS OF GTA", "WAS WORTH IT " + E(HUNDRED)], "color": "#39FF14", "size": 96},
    overrides=[(126030.5, 126035.4, "WE WENT UP A HUNDRED AND TWENTY EIGHT THOUSAND SUBSCRIBERS, BRO"),
               (126028.4, 126030.4, "CHECK ON YOUTUBE FOR SUBSCRIBERS."),
               (126039.6, 126040.0, "INSANE.")],
    tags=lambda ot: [
        {"t": ot(126014.2), "e": ot(126016.8), "text": "*CHECKS PHONE*", **R, "size": 104, "rot": 4},
        {"t": ot(126019.4), "e": ot(126020.8), "text": "*SPEECHLESS*", "box": "#8B0000", **L, "size": 112, "rot": -4},
        {"t": ot(126040.3), "e": ot(126042.9), "text": "*130 HOURS LATER*", **R, "size": 96, "rot": -3},
    ],
    stickers=lambda ot: [
        dict(t=ot(126019.4), e=ot(126020.8), emoji=E(MINDBLOWN), size=170, x=540, y=BAND),
        dict(t=ot(126031.2), e=ot(126035.6), emoji=E(TROPHY), size=170, x=540, y=BAND),
        dict(t=ot(126040.3), e=ot(126042.9), emoji=E(SKULL), size=150, x=540, y=BAND),
        dict(t=ot(126133.0), e=ot(126136.7), emoji=E(FIRE), size=170, x=540, y=BAND),
    ],
    sfx=lambda ot: [
        {"t": ot(126014.2), "id": "suspense", "gain_db": -12, "dur": 1.6},
        {"t": ot(126019.4), "id": "anime_wow", "gain_db": -10},
        {"t": ot(126023.2), "id": "ding", "gain_db": -10, "dur": 1.0},
        {"t": ot(126028.6), "id": "riser", "gain_db": -14, "dur": 1.5},
        {"t": ot(126031.6), "id": "cash_register", "gain_db": -10},
        {"t": ot(126033.0), "id": "airhorn", "gain_db": -15, "dur": 1.0},
        {"t": ot(126040.4), "id": "bruh", "gain_db": -9},
        {"t": ot(126130.8), "id": "bass_drop", "gain_db": -12, "dur": 1.2},
        {"t": ot(126161.6), "id": "heavenly", "gain_db": -14, "dur": 1.4},
    ],
    zooms=lambda ot: [
        {"t": ot(126013.9), "e": ot(126017.0), "type": "push", "amt": 1.06},
        {"t": ot(126019.4), "e": ot(126020.1), "type": "punch", "amt": 1.2},
        {"t": ot(126028.4), "e": ot(126035.6), "type": "push", "amt": 1.1},
        {"t": ot(126130.8), "e": ot(126131.4), "type": "punch", "amt": 1.16},
        {"t": ot(126161.5), "e": ot(126164.6), "type": "push", "amt": 1.08},
    ],
    flashes=lambda ot: [{"t": ot(126019.4), "d": 0.12, "color": "white"}, {"t": ot(126031.6), "d": 0.14, "color": "green"}],
    insets=[{"t": 126021.3, "e": 126024.7, "crop": [0, 330, 600, 230], "scale": 1.3, "x": 540, "y": BAND}])


# 2) INTRO — 33 hours into the stream he films the YouTube intro: take 1 fumbles, take 2 hits ----------------------
run("intro",
    keep_vod=[[119908.2, 119911.1],             # hook: "that was good, that one hit, that hit"
              [119848.3, 119851.95],            # "This is the intro to the major YouTube video, chat. You ready?"
              [119865.9, 119869.9],             # take 1: "What's going on YouTube, is your boy Kai Cenat and today for the-"
              [119869.95, 119880.75],           # take 2: "...in one sitting I will be playing every GTA ... preparing for GTA 6"
              [119892.5, 119896.6],             # "and I cannot get off unless I beat every single one"
              [119900.0, 119901.95],            # "I'll see you guys on the other side"
              [119907.6, 119913.2]],            # "that was good, that one hit, that hit, that hit..." -> LOOP
    notes=[("START", None, "HE KNOWS IT HIT"),
           (119848.3, 119851.95, "33 HOURS INTO THE STREAM..."),
           (119865.9, 119869.9, "TAKE 1"),
           (119869.95, 119880.75, "TAKE 2"),
           (119892.5, 119896.6, "THE RULE: BEAT EVERY GTA"),
           (119900.0, 119901.95, "AND..."),
           (119907.6, "END", "HE KNEW.")],
    header={"lines": ["33 HOURS IN... KAI NAILED", "HIS YOUTUBE INTRO " + E(HUNDRED)], "color": "#FFE14D", "size": 84},
    overrides=[(119866.0, 119869.9, "WHAT'S GOING ON YOUTUBE, IS YOUR BOY KAI CENAT AND TODAY FOR THE-"),
               (119870.2, 119872.45, "WHAT'S GOING ON YOUTUBE, IS YOUR BOY KAI CENAT AND")],
    tags=lambda ot: [
        {"t": ot(119849.4), "e": ot(119851.9), "text": "*LOCKS IN*", **R, "size": 108, "rot": 4},
        {"t": ot(119868.9), "e": ot(119869.9), "text": "*FUMBLES*", "box": "#8B0000", **L, "size": 116, "rot": -5},
        {"t": ot(119893.0), "e": ot(119895.0), "text": "*SERIOUS*", **R, "size": 104, "rot": -3},
        {"t": ot(119909.0), "e": ot(119911.5), "text": "*HYPED*", "box": "#8B0000", **L, "size": 120, "rot": 4},
    ],
    stickers=lambda ot: [
        dict(t=ot(119849.4), e=ot(119851.9), emoji=E(MIC), size=170, x=540, y=1830),
        dict(t=ot(119894.2), e=ot(119896.6), emoji=E(TROPHY), size=170, x=540, y=BAND),
        dict(t=ot(119909.0), e=ot(119913.2), emoji=E(FIRE, FIRE), size=170, x=540, y=BAND),
    ],
    sfx=lambda ot: [
        {"t": ot(119849.4), "id": "riser", "gain_db": -14, "dur": 1.5},
        {"t": ot(119868.9), "id": "wrong_buzzer", "gain_db": -10, "dur": 0.9},
        {"t": ot(119870.1), "id": "camera_shutter", "gain_db": -9},
        {"t": ot(119874.3), "id": "swoosh", "gain_db": -10},
        {"t": ot(119894.2), "id": "vine_boom", "gain_db": -6},
        {"t": ot(119901.4), "id": "ding", "gain_db": -10, "dur": 1.0},
        {"t": ot(119909.0), "id": "ohhh_crowd", "gain_db": -12, "dur": 1.5},
        {"t": ot(119911.4), "id": "airhorn", "gain_db": -15, "dur": 1.0},
    ],
    zooms=lambda ot: [
        {"t": ot(119868.9), "e": ot(119869.6), "type": "punch", "amt": 1.18},
        {"t": ot(119870.0), "e": ot(119880.7), "type": "push", "amt": 1.06},
        {"t": ot(119892.5), "e": ot(119896.5), "type": "push", "amt": 1.1},
        {"t": ot(119909.0), "e": ot(119909.7), "type": "punch", "amt": 1.18},
    ],
    flashes=lambda ot: [{"t": ot(119868.9), "d": 0.3, "color": "bw"}, {"t": ot(119894.2), "d": 0.12, "color": "white"}],
    insets=[{"t": 119866.0, "e": 119869.9, "png": "chat_intro.png", "crop": [0, 0, 360, 270], "scale": 1.9,
             "x": 540, "y": BAND}])

print({k: round(val, 1) for k, val in results.items()})
