"""Batch: Kai Cenat — "Playing every GTA until I beat it" marathon (Twitch VOD 2920505943, 41 h).
Split layout (facecam on top, gameplay below). Clips CLIP8..CLIP13.

usage: gta_batch.py SCRATCHPAD [clip ...]
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from plankit import build, out_times

S = sys.argv[1]; B = f"{S}/gta/batch"
only = set(sys.argv[2:])
E = lambda *cps: "".join(chr(c) for c in cps)
SKULL, CRY, JOY, EYES, SIREN, RAGE, FLUSH, SCREAM, PLEAD, CLOWN, CAP, ROLL, WEARY, STEAM, NEUTRAL, HUNDRED, \
    FIRE, MONEY, TROPHY, GOAT, SHOCK, TIRED = (0x1F480, 0x1F62D, 0x1F602, 0x1F440, 0x1F6A8, 0x1F92C, 0x1F633, 0x1F631,
    0x1F97A, 0x1F921, 0x1F9E2, 0x1F644, 0x1F629, 0x1F624, 0x1F610, 0x1F4AF, 0x1F525, 0x1F4B0, 0x1F3C6, 0x1F410,
    0x1F62E, 0x1F62B)
CAM = [0, 0, 456, 256]
BOT = dict(x=540, y=1730)                       # empty band under the gameplay
L, R = dict(x=290), dict(x=790)                 # beside Kai's face in the facecam band (y ~450-860)
SPLIT = dict(layout="split", cam=CAM, me_pos=(540, 1240),
             laugh_spots=[dict(x=540, y=1730, size=116, rot=-4), dict(x=820, y=520, size=112, rot=5),
                          dict(x=540, y=1740, size=112, rot=3), dict(x=260, y=540, size=112, rot=-5)])
results = {}


def run(name, keep, **kw):
    if only and name not in only:
        return
    def ot(t):
        for d in (0, -0.06, 0.06, -0.2, 0.2):
            r = out_times(t + d, keep)
            if r:
                return round(r[-1] - d, 3)
        raise ValueError(f"{name}: {t} not in kept footage")
    kw = {k: (v(ot) if callable(v) else v) for k, v in kw.items()}
    plan, dur = build(S, B, name, keep, **{**SPLIT, **kw})
    results[name] = dur
    print(f"{name}: {dur:.1f}s, {len(plan['words'])} words, {len(plan['tags'])} tags, {len(plan['sfx'])} sfx")


# CLIP8 — "If I fail, I'm smashing my controller" ... he fails ----------------------------------------
run("controller",
    keep=[[51.6, 57.4], [12.2, 23.4], [44.0, 51.6], [51.6, 57.4], [72.6, 81.0], [87.0, 93.5]],
    header={"lines": ["KAI SWORE HE'D SMASH HIS", "CONTROLLER IF HE FAILED " + E(SKULL)], "color": "#00E5FF"},
    overrides=[(29.0, 51.5, ""), (13.3, 13.6, "FAIL"), (18.7, 19.0, "FAIL"), (20.0, 20.3, "CONTROLLER")],
    tags=lambda ot: [
        {"t": ot(44.2), "e": ot(44.2) + 1.4, "text": "*KAI LOCKS IN*", **R, "y": 520, "size": 112, "rot": 5},
        {"t": ot(52.0), "e": ot(52.0) + 1.3, "text": "*MISSION FAILED*", "box": "#8B0000", **BOT, "size": 124, "rot": -3},
        {"t": ot(87.1), "e": ot(87.1) + 1.5, "text": "*SPIRIT BROKEN*", **L, "y": 560, "size": 118, "rot": -5},
    ],
    stickers=lambda ot: [
        dict(t=0.2, e=5.8, emoji=E(CRY, CRY), size=190, **BOT),
        dict(t=ot(14.8), e=ot(17.8), emoji=E(STEAM), **R, y=760, size=150),
        dict(t=ot(53.6), e=ot(57.3), emoji=E(SKULL, SKULL, SKULL), size=170, **BOT),
        dict(t=ot(73.0), e=ot(80.8), emoji=E(WEARY), size=200, **BOT),
        dict(t=ot(89.0), e=ot(93.4), emoji=E(PLEAD), size=200, **BOT),
    ],
    sfx=lambda ot: [
        {"t": ot(16.0), "id": "vine_boom", "gain_db": -6},
        {"t": ot(22.9), "id": "dun_dun_dun", "gain_db": -10, "dur": 1.6},
        {"t": ot(51.9), "id": "gta_wasted", "gain_db": -6, "dur": 2.6},
        {"t": ot(75.4), "id": "bruh", "gain_db": -7},
        {"t": ot(93.0), "id": "bass_boom", "gain_db": -4},
    ],
    beds=lambda ot: [
        {"id": "mission-impossible-flute", "t": ot(12.2), "e": ot(51.5), "gain_db": -20, "drops": [[ot(51.2), ot(51.6)]]},
        {"id": "sad-hamster-violin-meme", "t": ot(72.6), "e": ot(93.5), "gain_db": -17},
    ],
    zooms=lambda ot: [
        {"t": ot(15.9), "e": ot(16.6), "type": "punch", "amt": 1.2},
        {"t": ot(44.0), "e": ot(51.5), "type": "push", "amt": 1.1},
        {"t": ot(52.2), "e": ot(53.0), "type": "punch", "amt": 1.25},
        {"t": ot(72.6), "e": ot(81.0), "type": "push", "amt": 1.08},
        {"t": ot(92.9), "e": ot(93.5), "type": "punch", "amt": 1.2},
    ],
    flashes=lambda ot: [{"t": ot(52.2), "d": 0.45, "color": "bw"}, {"t": ot(93.0), "d": 0.13, "color": "red"}],
    laugh_label="*KAI LAUGHS*")

# CLIP9 — "There will NOT be another mission I fail, bet?" ... 17 minutes later --------------------------
run("bet",
    keep=[[143.5, 148.9], [12.3, 17.1], [20.8, 21.6], [28.0, 29.95], [46.0, 50.6], [58.9, 64.2], [94.4, 105.6],
          [105.9, 111.0], [143.5, 148.9]],
    header={"lines": ["KAI BET HE'D NEVER FAIL", "A MISSION AGAIN " + E(SKULL)], "color": "#B6FF3B"},
    overrides=[(29.5, 29.95, "MISSION"), (95.4, 95.95, "100 PS5S?"), (147.0, 147.8, "MISSION F*CKING FAILED")],
    fixes={"FIT": "FAILED", "DRIVING": "DRIVER IN"},
    tags=lambda ot: [
        {"t": ot(14.0), "e": ot(15.6), "text": "*CONFIDENCE 100*", **R, "y": 520, "size": 112, "rot": 5},
        {"t": ot(46.0), "e": ot(47.6), "text": "*17 MINUTES LATER*", "box": "#8B0000", "x": 540, "y": 1240, "size": 112},
        {"t": ot(98.7), "e": ot(100.2), "text": "*TIMED MISSION*", **L, "y": 560, "size": 120, "rot": -5},
        {"t": ot(144.3), "e": ot(145.6), "text": "*MISSION FAILED*", "box": "#8B0000", **BOT, "size": 124, "rot": 3},
    ],
    stickers=lambda ot: [
        dict(t=0.2, e=5.4, emoji=E(SKULL, SKULL, SKULL), size=170, **BOT),
        dict(t=ot(16.6), e=ot(21.6), emoji=E(CAP), size=210, **BOT),
        dict(t=ot(47.8), e=ot(50.6), emoji=E(CLOWN), size=200, **BOT),
        dict(t=ot(60.3), e=ot(64.2), emoji=E(EYES), **R, y=760, size=150),
        dict(t=ot(98.6), e=ot(105.5), emoji=E(SIREN, SIREN), size=180, **BOT),
        dict(t=ot(106.0), e=ot(111.0), emoji=E(NEUTRAL), size=200, **BOT),
    ],
    sfx=lambda ot: [
        {"t": ot(16.8), "id": "vine_boom", "gain_db": -6},
        {"t": ot(29.6), "id": "record_scratch", "gain_db": -5},
        {"t": ot(46.0), "id": "dun_dun_dun", "gain_db": -9, "dur": 1.6},
        {"t": ot(48.1), "id": "bruh", "gain_db": -7},
        {"t": ot(98.7), "id": "siren", "gain_db": -14, "dur": 1.2},
        {"t": ot(106.0), "id": "sad_trombone", "gain_db": -9, "dur": 2.0},
        {"t": ot(144.3), "id": "gta_wasted", "gain_db": -6, "dur": 2.6},
    ],
    beds=lambda ot: [
        {"id": "carefree", "t": ot(12.3), "e": ot(29.95), "gain_db": -20},
        {"id": "funny-sad-music", "t": ot(46.0), "e": ot(64.2), "gain_db": -19},
        {"id": "oh-no-no-no-tik-tok-song-sound-effect", "t": ot(94.4), "e": ot(111.0), "gain_db": -19},
    ],
    zooms=lambda ot: [
        {"t": ot(14.0), "e": ot(17.0), "type": "push", "amt": 1.08},
        {"t": ot(47.9), "e": ot(48.7), "type": "punch", "amt": 1.2},
        {"t": ot(98.6), "e": ot(99.3), "type": "punch", "amt": 1.18},
        {"t": ot(144.2), "e": ot(145.0), "type": "punch", "amt": 1.25},
    ],
    flashes=lambda ot: [{"t": ot(46.0), "d": 0.4, "color": "bw"}, {"t": ot(144.3), "d": 0.13, "color": "red"}])

# CLIP10 — Kai vs Rockstar at 1 AM ------------------------------------------------------------------------
run("rockstar",
    keep=[[118.2, 123.2], [59.8, 64.1], [85.8, 91.4], [93.0, 101.6], [118.2, 126.4], [163.4, 172.8], [198.6, 207.0]],
    header={"lines": ["KAI WAS NOT HAVING IT", "WITH ROCKSTAR AT 1 AM " + E(CRY)], "color": "#FF4FD8"},
    overrides=[(89.8, 90.4, "29 HEALTH"), (93.0, 93.95, "LIKE ROCKSTAR")],
    fixes={"ROCK": "ROCK", "W": "W"},
    tags=lambda ot: [
        {"t": ot(89.8), "e": ot(91.3), "text": "*29 HEALTH*", **L, "y": 560, "size": 124, "rot": -5},
        {"t": ot(119.0), "e": ot(120.6), "text": "*MAXIMUM SARCASM*", "box": "#8B0000", **BOT, "size": 116, "rot": 3},
        {"t": ot(164.2), "e": ot(165.8), "text": "*CHAT IS LAUGHING*", **R, "y": 520, "size": 110, "rot": 5},
        {"t": ot(170.4), "e": ot(171.9), "text": "*1 AM RAGE*", "box": "#8B0000", **BOT, "size": 124, "rot": -3},
    ],
    stickers=lambda ot: [
        dict(t=0.2, e=5.0, emoji=E(ROLL), size=200, **BOT),
        dict(t=ot(63.0), e=ot(64.1), emoji=E(SKULL), **R, y=760, size=150),
        dict(t=ot(86.0), e=ot(91.3), emoji=E(WEARY), size=200, **BOT),
        dict(t=ot(94.4), e=ot(101.5), emoji=E(RAGE), size=200, **BOT),
        dict(t=ot(164.2), e=ot(169.0), emoji=E(JOY, JOY), size=150, **L, y=780),
        dict(t=ot(199.0), e=ot(207.0), emoji=E(STEAM), size=200, **BOT),
    ],
    sfx=lambda ot: [
        {"t": ot(63.2), "id": "vine_boom", "gain_db": -6},
        {"t": ot(94.4), "id": "bruh", "gain_db": -7},
        {"t": ot(120.6), "id": "ding", "gain_db": -9, "dur": 1.0},
        {"t": ot(170.5), "id": "dun_dun_dun", "gain_db": -9, "dur": 1.6},
        {"t": ot(206.6), "id": "bass_boom", "gain_db": -4},
    ],
    beds=lambda ot: [
        {"id": "funny-sad-music", "t": ot(59.8), "e": ot(101.6), "gain_db": -20},
        {"id": "carefree", "t": ot(118.2), "e": ot(126.4), "gain_db": -20},
        {"id": "sad-hamster-violin-meme", "t": ot(198.6), "e": ot(207.0), "gain_db": -18},
    ],
    zooms=lambda ot: [
        {"t": ot(63.1), "e": ot(63.8), "type": "punch", "amt": 1.18},
        {"t": ot(93.0), "e": ot(101.6), "type": "push", "amt": 1.08},
        {"t": ot(170.4), "e": ot(171.2), "type": "punch", "amt": 1.22},
        {"t": ot(206.3), "e": ot(207.0), "type": "punch", "amt": 1.22},
    ],
    flashes=lambda ot: [{"t": ot(94.4), "d": 0.13, "color": "red"}, {"t": ot(206.6), "d": 0.13, "color": "red"}])

# CLIP11 — Kai announces 100 PS5 giveaways -----------------------------------------------------------------
run("ps5",
    cam=[0, 312, 398, 224],                    # San Andreas segment: small cam at left, mid-height
    keep=[[30.4, 32.3], [5.9, 10.8], [18.0, 23.4], [25.9, 32.3], [32.9, 41.6], [42.5, 44.5], [48.9, 49.9],
          [53.5, 61.6], [64.0, 66.8]],
    header={"lines": ["KAI JUST ANNOUNCED", "100 PS5 GIVEAWAYS " + E(FLUSH)], "color": "#FFD60A"},
    overrides=[(30.4, 30.85, "100 PS5S")],
    fixes={"PS5,": "PS5", "PS5S,": "PS5S"},
    tags=lambda ot: [
        {"t": ot(18.1), "e": ot(19.6), "text": "*GTA 6 MARATHON*", **R, "y": 520, "size": 112, "rot": 5},
        {"t": ot(26.8), "e": ot(28.2), "text": "*100 PS5s*", "box": "#8B0000", **BOT, "size": 132, "rot": -3},
        {"t": ot(37.4), "e": ot(39.0), "text": "*SUBS GET A BETTER CHANCE*", "x": 540, "y": 1240, "size": 96},
        {"t": ot(53.6), "e": ot(55.2), "text": "*BRAND COLLAB*", **L, "y": 560, "size": 116, "rot": -5},
    ],
    stickers=lambda ot: [
        dict(t=0.2, e=1.9, emoji=E(FLUSH, FLUSH), size=180, **BOT),
        dict(t=ot(7.2), e=ot(10.8), emoji=E(EYES), **R, y=760, size=150),
        dict(t=ot(28.4), e=ot(32.2), emoji=E(SHOCK), size=200, **BOT),
        dict(t=ot(40.0), e=ot(44.4), emoji=E(MONEY, MONEY), size=180, **BOT),
        dict(t=ot(64.2), e=ot(66.8), emoji=E(HUNDRED, FIRE), size=180, **BOT),
    ],
    sfx=lambda ot: [
        {"t": ot(23.2), "id": "vine_boom", "gain_db": -6},
        {"t": ot(26.8), "id": "cash_register", "gain_db": -8, "dur": 1.5},
        {"t": ot(32.1), "id": "anime_wow", "gain_db": -10, "dur": 1.5},
        {"t": ot(64.3), "id": "airhorn", "gain_db": -12, "dur": 1.5},
        {"t": ot(66.5), "id": "bass_boom", "gain_db": -4},
    ],
    beds=lambda ot: [{"id": "carefree", "t": 1.9, "e": ot(66.8), "gain_db": -21, "drops": [[ot(26.4), ot(26.8)]]}],
    zooms=lambda ot: [
        {"t": ot(26.7), "e": ot(27.5), "type": "punch", "amt": 1.2},
        {"t": ot(32.9), "e": ot(41.6), "type": "push", "amt": 1.08},
        {"t": ot(64.2), "e": ot(64.9), "type": "punch", "amt": 1.2},
    ],
    flashes=lambda ot: [{"t": ot(26.8), "d": 0.12, "color": "white"}, {"t": ot(66.5), "d": 0.13, "color": "green"}])

# CLIP12 — rage ... then "tell me that was hard, be honest" --------------------------------------------
run("hard",
    keep=[[83.0, 87.5], [11.5, 14.3], [67.1, 75.3], [76.7, 79.0], [82.4, 91.2], [137.0, 138.4], [159.0, 164.5],
          [172.2, 186.6]],
    header={"lines": ["KAI ALMOST QUIT GTA…", "5 MINUTES LATER " + E(JOY)], "color": "#FF8A00"},
    overrides=[(181.8, 183.5, "Y'ALL TOLD ME THAT WAS HARD")],
    min_laugh=0.55, laugh_label="*KAI LAUGHS*",
    tags=lambda ot: [
        {"t": ot(77.0), "e": ot(78.6), "text": "*WHERE ARE MY TOOLS*", **R, "y": 520, "size": 106, "rot": 5},
        {"t": ot(137.0), "e": ot(138.4), "text": "*5 MINUTES LATER*", "box": "#8B0000", "x": 540, "y": 1240, "size": 112},
        {"t": ot(174.3), "e": ot(175.8), "text": "*MISSION PASSED*", "box": "#1F7A1F", **BOT, "size": 124, "rot": -3},
    ],
    stickers=lambda ot: [
        dict(t=0.2, e=4.5, emoji=E(RAGE), size=200, **BOT),
        dict(t=ot(11.6), e=ot(14.3), emoji=E(SCREAM), **L, y=780, size=150),
        dict(t=ot(68.6), e=ot(75.2), emoji=E(STEAM), size=200, **BOT),
        dict(t=ot(176.0), e=ot(180.9), emoji=E(SKULL, SKULL), size=180, **BOT),
        dict(t=ot(184.6), e=ot(186.6), emoji=E(TROPHY, GOAT), size=180, **BOT),
    ],
    sfx=lambda ot: [
        {"t": ot(69.3), "id": "vine_boom", "gain_db": -6},
        {"t": ot(78.6), "id": "bruh", "gain_db": -7},
        {"t": ot(137.0), "id": "record_scratch", "gain_db": -5},
        {"t": ot(174.3), "id": "correct", "gain_db": -9},
        {"t": ot(184.8), "id": "airhorn", "gain_db": -12, "dur": 1.4},
    ],
    beds=lambda ot: [
        {"id": "oh-no-no-no-tik-tok-song-sound-effect", "t": 4.5, "e": ot(91.2), "gain_db": -20},
        {"id": "drift-phonk", "t": ot(172.2), "e": ot(186.6), "gain_db": -21},
    ],
    zooms=lambda ot: [
        {"t": ot(69.2), "e": ot(69.9), "type": "punch", "amt": 1.2},
        {"t": ot(84.0), "e": ot(84.7), "type": "punch", "amt": 1.2},
        {"t": ot(174.3), "e": ot(186.6), "type": "push", "amt": 1.08},
    ],
    flashes=lambda ot: [{"t": ot(84.0), "d": 0.13, "color": "red"}, {"t": ot(174.3), "d": 0.13, "color": "green"}])

# CLIP13 — "Catalina wants me in JAIL, I'm convinced" -----------------------------------------------------
run("catalina",
    keep=[[5.2, 14.7], [17.5, 19.9], [30.2, 35.5], [47.8, 48.7], [86.4, 94.8], [116.8, 120.3], [122.6, 126.1],
          [134.7, 146.0]],
    cold_open=False,
    header={"lines": ["CATALINA IS TRYING", "TO GET KAI ARRESTED " + E(CRY)], "color": "#00E5FF"},
    overrides=[(5.2, 8.95, "YOU SEE HOW MESSED UP HER MISSIONS ARE FOR ME"),
               (134.7, 138.4, "YO WHAT THE F*CK IS GOING ON WITH THIS GAME"),
               (138.6, 141.95, "YO WHAT IS Y'ALL GAME? WHAT THE F*CK?"),
               (143.1, 146.0, "OH THEY BEEN HAVING TANKS, ALL THESE N*GGAS BEEN HAVING TANKS")],
    tags=lambda ot: [
        {"t": ot(10.4), "e": ot(11.9), "text": "*SET UP*", **R, "y": 520, "size": 130, "rot": 5},
        {"t": ot(18.6), "e": ot(19.9), "text": "*TIMED MISSION*", **L, "y": 560, "size": 116, "rot": -5},
        {"t": ot(119.5), "e": ot(120.3), "text": "*4 STARS*", "box": "#8B0000", **BOT, "size": 130, "rot": 3},
        {"t": ot(145.2), "e": ot(146.0), "text": "*TANKS*", "box": "#8B0000", **BOT, "size": 140, "rot": -3},
    ],
    stickers=lambda ot: [
        dict(t=ot(9.8), e=ot(14.6), emoji=E(SIREN, SIREN), size=180, **BOT),
        dict(t=ot(30.4), e=ot(35.4), emoji=E(SKULL), size=200, **BOT),
        dict(t=ot(88.5), e=ot(94.7), emoji=E(EYES), **R, y=760, size=150),
        dict(t=ot(122.7), e=ot(126.0), emoji=E(SCREAM), size=200, **BOT),
        dict(t=ot(138.6), e=ot(144.9), emoji=E(RAGE), size=200, **BOT),
    ],
    sfx=lambda ot: [
        {"t": ot(11.1), "id": "vine_boom", "gain_db": -6},
        {"t": ot(19.6), "id": "siren", "gain_db": -14, "dur": 1.2},
        {"t": ot(34.7), "id": "dun_dun_dun", "gain_db": -9, "dur": 1.6},
        {"t": ot(48.2), "id": "bruh", "gain_db": -7},
        {"t": ot(119.8), "id": "siren", "gain_db": -13, "dur": 1.4},
        {"t": ot(145.5), "id": "bass_boom", "gain_db": -4},
    ],
    beds=lambda ot: [
        {"id": "investigations", "t": 0.5, "e": ot(35.5), "gain_db": -20},
        {"id": "mission-impossible-flute", "t": ot(86.4), "e": ot(126.1), "gain_db": -20},
        {"id": "oh-no-no-no-tik-tok-song-sound-effect", "t": ot(134.7), "e": ot(145.2), "gain_db": -20},
    ],
    zooms=lambda ot: [
        {"t": ot(10.9), "e": ot(11.7), "type": "punch", "amt": 1.2},
        {"t": ot(30.2), "e": ot(35.5), "type": "push", "amt": 1.08},
        {"t": ot(119.5), "e": ot(120.2), "type": "punch", "amt": 1.2},
        {"t": ot(145.3), "e": ot(146.0), "type": "punch", "amt": 1.25},
    ],
    flashes=lambda ot: [{"t": ot(11.1), "d": 0.13, "color": "red"}, {"t": ot(145.5), "d": 0.13, "color": "red"}])

print({k: round(v, 1) for k, v in results.items()})
