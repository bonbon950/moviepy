"""Batch: Kai Cenat — AMP Halloween Party (Twitch VOD 2915383492). Builds 6 plans (+ the nail clip separately).

usage: halloween_batch.py SCRATCHPAD [clip ...]
Times in keep/overrides/speakers are SOURCE seconds of batch/<name>_src.mp4; ot(t) maps to OUTPUT time.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from plankit import build, out_times

S = sys.argv[1]; B = f"{S}/vod/batch"
only = set(sys.argv[2:])
E = lambda *cps: "".join(chr(c) for c in cps)          # emoji helper
SKULL, CRY, JOY, EYES, SIREN, NO, RAGE, FLUSH, MONEY, NAIL, BROKEN, SCREAM, PLEAD, CLOWN, WOLF, CROWN, RAISED, \
    STEAM, CAMERA, BOOM, HUNDRED, FIRE, WEARY = (0x1F480, 0x1F62D, 0x1F602, 0x1F440, 0x1F6A8, 0x1F6AB, 0x1F92C,
    0x1F633, 0x1F4B8, 0x1F485, 0x1F494, 0x1F631, 0x1F97A, 0x1F921, 0x1F43A, 0x1F451, 0x1F928, 0x1F624, 0x1F4F8,
    0x1F92F, 0x1F4AF, 0x1F525, 0x1F629)
BOT = dict(x=540, y=1450)          # empty bottom band
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
    plan, dur = build(S, B, name, keep, **kw)
    results[name] = dur
    print(f"{name}: {dur:.1f}s, {len(plan['words'])} words, {len(plan['tags'])} tags, {len(plan['sfx'])} sfx")


# 1) RAKAI BANNED FROM THE PARTY ------------------------------------------------------------------
run("rakai",
    keep=[[48.6, 51.5], [6.3, 12.2], [13.7, 18.45], [40.3, 41.4], [44.8, 47.95], [48.1, 53.2], [54.0, 60.4],
          [66.8, 71.7], [88.8, 96.6], [120.4, 125.3]],
    header={"lines": ["KAI BANNED RAKAI", "FROM THE PARTY " + E(CRY)], "color": "#00E5FF"},
    speakers=[(40.0, 48.05, "rakai", "#C77DFF")],
    overrides=[(44.8, 47.95, "IT'S OKAY, I JUST WANNA COME ONE LAST TIME AND PARTY, HALLOWEEN STUFF"),
               (58.6, 59.35, "META-GAME")],
    fixes={"RAKKAH": "RAKAI", "MEDIGAME": "META-GAME"},
    tags=lambda ot: [
        {"t": ot(40.3) - 0.1, "e": ot(40.3) + 1.2, "text": "*RAKAI CALLS*", "box": "#8B0000", "x": 760, "y": 840, "size": 124, "rot": 5},
        {"t": ot(51.0), "e": ot(51.0) + 1.0, "text": "*DENIED*", "x": 330, "y": 880, "size": 145, "rot": -6},
        {"t": ot(88.8), "e": ot(88.8) + 1.4, "text": "*KAI ON THE HUNT*", "box": "#8B0000", "x": 540, "y": 790, "size": 118, "rot": 3},
    ],
    stickers=lambda ot: [
        dict(t=0.2, e=2.9, emoji=E(NO, NO), size=180, **BOT),
        dict(t=ot(13.84), e=ot(16.3), emoji=E(SIREN, SIREN), size=180, **BOT),
        dict(t=ot(56.6), e=ot(60.3), emoji=E(SKULL, SKULL), size=175, **BOT),
        dict(t=ot(66.9), e=ot(71.6), emoji=E(CRY), size=200, **BOT),
        dict(t=ot(89.0), e=ot(92.5), emoji=E(EYES), x=200, y=790, size=150),
        dict(t=ot(120.5), e=ot(125.3), emoji=E(EYES, EYES), size=170, **BOT),
    ],
    sfx=lambda ot: [
        {"t": ot(13.84), "id": "dun_dun_dun", "gain_db": -9, "dur": 1.6},
        {"t": ot(15.44), "id": "siren", "gain_db": -14, "dur": 1.2},
        {"t": ot(40.3) - 0.25, "id": "phone_ring", "gain_db": -10, "dur": 1.0},
        {"t": ot(48.96), "id": "vine_boom", "gain_db": -6},
        {"t": ot(51.0), "id": "wrong_buzzer", "gain_db": -7},
        {"t": ot(57.58), "id": "emotional_damage", "gain_db": -8, "dur": 2.2},
        {"t": ot(96.2), "id": "fbi_open_up", "gain_db": -6},
        {"t": ot(125.1), "id": "bass_boom", "gain_db": -4},
    ],
    beds=lambda ot: [
        {"id": "investigations", "t": 2.9, "e": ot(18.4), "gain_db": -19, "drops": [[ot(13.5), ot(13.9)]]},
        {"id": "sneaky-snitch-meme", "t": ot(40.3), "e": ot(53.2), "gain_db": -19, "drops": [[ot(50.7), ot(51.2)]]},
        {"id": "oh-no-no-no-tik-tok-song-sound-effect", "t": ot(54.0), "e": ot(60.4), "gain_db": -19},
        {"id": "sad-hamster-violin-meme", "t": ot(66.8), "e": ot(71.7), "gain_db": -17},
        {"id": "henry-mancini-the-pink-panther", "t": ot(88.8), "e": ot(125.3), "gain_db": -19},
    ],
    zooms=lambda ot: [
        {"t": ot(13.84), "e": ot(14.6), "type": "punch", "amt": 1.22},
        {"t": ot(40.3), "e": ot(47.9), "type": "push", "amt": 1.07},
        {"t": ot(51.0), "e": ot(51.7), "type": "punch", "amt": 1.22},
        {"t": ot(56.62), "e": ot(57.5), "type": "punch", "amt": 1.18},
        {"t": ot(66.8), "e": ot(71.7), "type": "push", "amt": 1.08},
        {"t": ot(96.2), "e": ot(96.6), "type": "punch", "amt": 1.2},
        {"t": ot(124.9), "e": ot(125.3), "type": "punch", "amt": 1.22},
    ],
    flashes=lambda ot: [{"t": ot(17.32), "d": 0.1, "color": "white"}, {"t": ot(51.0), "d": 0.45, "color": "bw"},
                        {"t": ot(125.1), "d": 0.13, "color": "red"}],
    laugh_label="*LAUGHING*")

# 2) EVERYONE THINKS KAI IS LIL NAS X --------------------------------------------------------------
run("lilnas",
    keep=[[75.3, 79.1], [5.9, 12.3], [27.9, 31.25], [46.6, 53.85], [67.2, 75.3], [102.2, 106.2], [110.3, 113.3],
          [128.7, 134.8], [149.5, 156.8]],
    header={"lines": ["EVERYONE THINKS KAI", "IS LIL NAS X " + E(CRY)], "color": "#FF3D7F"},
    speakers=[(46.5, 54.0, "friend", "#FFE14D"), (69.7, 79.2, "friend", "#FFE14D"), (104.5, 111.5, "friend", "#FFE14D"),
              (149.5, 152.0, "fan", "#9DFF5C"), (154.3, 157.0, "fan", "#9DFF5C")],
    overrides=[(7.44, 8.3, "LIL NAS X"), (10.24, 11.1, "LIL NAS X"), (68.2, 68.9, "LIL NAS X?"),
               (78.6, 79.06, "LIL NAS X"), (51.0, 53.85, "YOU WERE LIKE LIL NAS X"), (149.5, 150.1, "TEEN WOLF!")],
    fixes={"TEAM": "TEEN"},
    min_laugh=0.33, laugh_label="*KAI LAUGHS*",
    tags=lambda ot: [
        {"t": ot(5.9), "e": ot(5.9) + 1.2, "text": "*CHAT SPAMMING LIL NAS X*", "x": 540, "y": 790, "size": 96},
        {"t": ot(28.1), "e": ot(29.3), "text": "*DEEPLY OFFENDED*", "box": "#8B0000", "x": 740, "y": 860, "size": 122, "rot": 5},
        {"t": ot(128.7), "e": ot(130.2), "text": "*KAI IS HURT*", "x": 330, "y": 830, "size": 130, "rot": -5},
        {"t": ot(154.4), "e": ot(156.0), "text": "*SOMEONE FINALLY GETS IT*", "box": "#8B0000", "x": 540, "y": 800, "size": 98},
    ],
    stickers=lambda ot: [
        dict(t=0.3, e=3.8, emoji=E(SKULL, SKULL, SKULL), size=170, **BOT),
        dict(t=ot(70.6), e=ot(73.6), emoji=E(RAISED), size=200, **BOT),
        dict(t=ot(110.3), e=ot(113.3), emoji=E(CLOWN), size=200, **BOT),
        dict(t=ot(128.9), e=ot(134.6), emoji=E(PLEAD), size=200, **BOT),
        dict(t=ot(154.5), e=ot(156.8), emoji=E(WOLF, CROWN), size=185, **BOT),
    ],
    sfx=lambda ot: [
        {"t": ot(10.82), "id": "vine_boom", "gain_db": -6},
        {"t": ot(29.18), "id": "dramatic_chipmunk", "gain_db": -9, "dur": 1.4},
        {"t": ot(53.4), "id": "bruh", "gain_db": -6},
        {"t": ot(70.6), "id": "huh", "gain_db": -10, "dur": 1.2},
        {"t": ot(110.34), "id": "wrong_buzzer", "gain_db": -7},
        {"t": ot(154.5), "id": "heavenly", "gain_db": -10, "dur": 2.3},
        {"t": ot(156.3), "id": "bass_boom", "gain_db": -4},
    ],
    beds=lambda ot: [
        {"id": "investigations", "t": 3.8, "e": ot(75.3), "gain_db": -20, "drops": [[ot(10.5), ot(10.9)]]},
        {"id": "jeopardy-final-jeopardy-thinking-music", "t": ot(102.2), "e": ot(113.3), "gain_db": -20},
        {"id": "sad-hamster-violin-meme", "t": ot(128.7), "e": ot(134.8), "gain_db": -17},
        {"id": "drift-phonk", "t": ot(149.5), "e": ot(156.8), "gain_db": -20},
    ],
    zooms=lambda ot: [
        {"t": ot(9.98), "e": ot(10.8), "type": "punch", "amt": 1.2},
        {"t": ot(28.9), "e": ot(29.6), "type": "punch", "amt": 1.18},
        {"t": ot(70.6), "e": ot(71.4), "type": "punch", "amt": 1.18},
        {"t": ot(112.6), "e": ot(113.3), "type": "punch", "amt": 1.2},
        {"t": ot(128.7), "e": ot(134.8), "type": "push", "amt": 1.08},
        {"t": ot(156.2), "e": ot(156.8), "type": "punch", "amt": 1.22},
    ],
    flashes=lambda ot: [{"t": ot(110.34), "d": 0.4, "color": "bw"}, {"t": ot(156.3), "d": 0.13, "color": "white"}])

# 3) KAI FOUND OUT HOW HARD IT IS BEING A GIRL -----------------------------------------------------
run("girl",
    keep=[[129.3, 134.4], [1.7, 4.0], [14.5, 16.1], [26.0, 34.3], [37.8, 43.6], [45.5, 53.1], [70.9, 73.4],
          [107.6, 111.0], [127.2, 135.0], [145.2, 148.0]],
    header={"lines": ["KAI FOUND OUT HOW HARD", "IT IS BEING A GIRL " + E(CRY)], "color": "#FF4FD8"},
    overrides=[(133.4, 134.4, "OH GOD IT HURTS"), (146.8, 148.0, "I TOLD YOU")],
    tags=lambda ot: [
        {"t": ot(2.0), "e": ot(3.2), "text": "*NAILS FALLING OFF*", "x": 760, "y": 850, "size": 110, "rot": 4},
        {"t": ot(26.0), "e": ot(27.2), "text": "*COUNTING HIS NAILS*", **BOT, "size": 108, "rot": -3},
        {"t": ot(28.4), "e": ot(29.8), "text": "*$200 NAILS*", "box": "#8B0000", "x": 330, "y": 860, "size": 130, "rot": -5},
        {"t": ot(48.0), "e": ot(49.6), "text": "*KAI UNDERSTANDS WOMEN NOW*", **BOT, "size": 96, "rot": 2},
        {"t": ot(71.0), "e": ot(72.4), "text": "*MISSING 3 NAILS*", "x": 740, "y": 820, "size": 116, "rot": 6},
        {"t": ot(108.9), "e": ot(110.0), "text": "*WRONG FINGER*", "x": 330, "y": 860, "size": 124, "rot": -6},
        {"t": ot(130.2), "e": ot(131.8), "text": "*SCREAMS IN PAIN*", "box": "#8B0000", "x": 540, "y": 800, "size": 132, "rot": 3},
    ],
    stickers=lambda ot: [
        dict(t=0.3, e=5.1, emoji=E(CRY, CRY), size=190, **BOT),
        dict(t=ot(28.6), e=ot(32.7), emoji=E(MONEY, NAIL), size=180, **BOT),
        dict(t=ot(42.3), e=ot(43.6), emoji=E(BROKEN), size=200, **BOT),
        dict(t=ot(50.0), e=ot(53.0), emoji=E(NAIL, WEARY), size=180, x=540, y=1460),
        dict(t=ot(71.0), e=ot(73.4), emoji=E(FLUSH), x=200, y=790, size=150),
        dict(t=ot(132.0), e=ot(134.9), emoji=E(SCREAM, SCREAM), size=180, **BOT),
    ],
    sfx=lambda ot: [
        {"t": ot(28.6), "id": "cash_register", "gain_db": -7, "dur": 1.5},
        {"t": ot(43.1), "id": "bruh", "gain_db": -6},
        {"t": ot(73.14), "id": "vine_boom", "gain_db": -6},
        {"t": ot(109.2), "id": "wrong_buzzer", "gain_db": -7},
        {"t": ot(130.3), "id": "bass_boom", "gain_db": -4},
        {"t": ot(146.5), "id": "sad_trombone", "gain_db": -9, "dur": 1.5},
    ],
    beds=lambda ot: [
        {"id": "oh-no-no-no-tik-tok-song-sound-effect", "t": 5.1, "e": ot(16.1), "gain_db": -19},
        {"id": "funny-sad-music", "t": ot(26.0), "e": ot(43.6), "gain_db": -19, "drops": [[ot(28.3), ot(28.7)]]},
        {"id": "sad-hamster-violin-meme", "t": ot(45.5), "e": ot(53.1), "gain_db": -17},
        {"id": "mission-impossible-flute", "t": ot(107.6), "e": ot(130.1), "gain_db": -19, "drops": [[ot(129.8), ot(130.1)]]},
    ],
    zooms=lambda ot: [
        {"t": ot(28.5), "e": ot(29.3), "type": "punch", "amt": 1.2},
        {"t": ot(43.0), "e": ot(43.6), "type": "punch", "amt": 1.18},
        {"t": ot(45.5), "e": ot(53.1), "type": "push", "amt": 1.08},
        {"t": ot(73.0), "e": ot(73.4), "type": "punch", "amt": 1.2},
        {"t": ot(130.2), "e": ot(131.0), "type": "punch", "amt": 1.25},
    ],
    flashes=lambda ot: [{"t": ot(109.2), "d": 0.4, "color": "bw"}, {"t": ot(130.3), "d": 0.13, "color": "red"}],
    laugh_label="*EVERYONE LAUGHS*")

# 4) SWAMP A$$ ON STREAM ------------------------------------------------------------------------------
run("swamp",
    keep=[[5.2, 14.0], [21.7, 39.8], [40.4, 42.96], [44.5, 46.3], [47.4, 48.4], [61.4, 68.0], [85.5, 93.0]],
    cold_open=False,
    header={"lines": ["KAI WALKED AROUND", "WITH SWAMP A$$ ALL DAY " + E(SKULL)], "color": "#B6FF3B"},
    overrides=[(5.2, 9.9, "NOW WHY WOULD HE DO THAT CHAT? WAIT, SWAMP A$$?"),
               (31.0, 32.15, "DAVIS AND CHRIS ABOUT TO GO LIVE"), (37.5, 39.1, "PLEASE DON'T SCREENSHOT THAT CHAT"),
               (39.9, 41.8, "CHAT, NOW I'M UNDER CHECK"), (88.8, 93.0, "CHAT WHO'S LAUGHING? OH MY GOD, SWAMP A$$")],
    tags=lambda ot: [
        {"t": ot(10.0), "e": ot(11.3), "text": "*SWAMP A$$ REVEALED*", "box": "#8B0000", "x": 540, "y": 800, "size": 118, "rot": -3},
        {"t": ot(36.5), "e": ot(37.8), "text": "*DAMAGE CONTROL*", "x": 760, "y": 860, "size": 116, "rot": 5},
        {"t": ot(61.5), "e": ot(62.8), "text": "*IN DENIAL*", "x": 330, "y": 840, "size": 132, "rot": -6},
        {"t": ot(87.7), "e": ot(89.0), "text": "*KAI IS LIVID*", **BOT, "size": 120, "rot": 3},
    ],
    stickers=lambda ot: [
        dict(t=ot(9.3), e=ot(13.9), emoji=E(SKULL, SKULL, SKULL), size=170, **BOT),
        dict(t=ot(34.6), e=ot(36.4), emoji=E(FLUSH), x=200, y=790, size=150),
        dict(t=ot(36.9), e=ot(39.6), emoji=E(CAMERA, NO), size=175, **BOT),
        dict(t=ot(44.9), e=ot(48.3), emoji=E(CRY), size=200, **BOT),
        dict(t=ot(62.4), e=ot(67.8), emoji=E(BOOM), size=200, **BOT),
        dict(t=ot(89.0), e=ot(93.0), emoji=E(STEAM), x=860, y=790, size=150),
    ],
    sfx=lambda ot: [
        {"t": ot(9.38), "id": "vine_boom", "gain_db": -5},
        {"t": ot(10.5), "id": "siren", "gain_db": -13, "dur": 1.2},
        {"t": ot(34.86), "id": "emotional_damage", "gain_db": -8, "dur": 2.0},
        {"t": ot(37.04), "id": "camera_shutter", "gain_db": -6},
        {"t": ot(61.5), "id": "record_scratch", "gain_db": -6},
        {"t": ot(92.44), "id": "bass_boom", "gain_db": -4},
    ],
    beds=lambda ot: [
        {"id": "oh-no-no-no-tik-tok-song-sound-effect", "t": ot(21.7), "e": ot(39.8), "gain_db": -20},
        {"id": "funny-sad-music", "t": ot(40.4), "e": ot(68.0), "gain_db": -19},
        {"id": "curb-your-enthusiasm", "t": ot(92.6), "e": ot(93.0) + 0.0, "gain_db": -12},
    ],
    zooms=lambda ot: [
        {"t": ot(9.38), "e": ot(10.2), "type": "punch", "amt": 1.25},
        {"t": ot(21.7), "e": ot(30.0), "type": "push", "amt": 1.08},
        {"t": ot(34.1), "e": ot(34.9), "type": "punch", "amt": 1.18},
        {"t": ot(61.5), "e": ot(62.3), "type": "punch", "amt": 1.18},
        {"t": ot(92.3), "e": ot(93.0), "type": "punch", "amt": 1.22},
    ],
    flashes=lambda ot: [{"t": ot(9.38), "d": 0.13, "color": "red"}, {"t": ot(37.04), "d": 0.1, "color": "white"},
                        {"t": ot(92.44), "d": 0.13, "color": "red"}],
    laugh_label="*EVERYONE LAUGHS*")

# 5) KAI'S HUGS COME WITH A CATCH -----------------------------------------------------------------------
run("food",
    keep=[[48.3, 59.45], [59.45, 64.8], [4.5, 13.6], [17.6, 34.2]],
    cold_open=False,
    header={"lines": ["KAI ONLY WANTED A HUG", "FOR ONE REASON " + E(SKULL)], "color": "#00E5FF"},
    speakers=[(25.4, 26.0, "friend", "#FFE14D"), (28.9, 31.2, "friend", "#FFE14D")],
    overrides=[(48.3, 49.9, "BUT THE PARTY WAS TODAY"), (24.3, 24.9, "GIVE ME A HUG")],
    fixes={"YOUR": "YOU'RE"},
    tags=lambda ot: [
        {"t": ot(50.0), "e": ot(51.3), "text": "*CALLS DAVIS*", "x": 760, "y": 840, "size": 116, "rot": 5},
        {"t": ot(60.0), "e": ot(61.3), "text": "*HUG DEMAND #1*", "box": "#8B0000", **BOT, "size": 118, "rot": -3},
        {"t": ot(19.6), "e": ot(20.9), "text": "*HUG DEMAND #2*", "box": "#8B0000", **BOT, "size": 118, "rot": 3},
        {"t": ot(25.5), "e": ot(26.6), "text": "*REJECTED*", "x": 330, "y": 870, "size": 140, "rot": -6},
        {"t": ot(32.6), "e": ot(34.2), "text": "*THE REAL REASON*", "x": 540, "y": 790, "size": 112},
    ],
    stickers=lambda ot: [
        dict(t=ot(50.9), e=ot(55.4), emoji=E(SKULL), size=200, **BOT),
        dict(t=ot(6.2), e=ot(9.2), emoji=E(STEAM), x=860, y=790, size=150),
        dict(t=ot(25.5), e=ot(28.4), emoji=E(BROKEN), size=200, **BOT),
        dict(t=ot(32.6), e=ot(34.2), emoji=E(SKULL, SKULL, SKULL), size=170, **BOT),
    ],
    sfx=lambda ot: [
        {"t": ot(50.9), "id": "vine_boom", "gain_db": -6},
        {"t": ot(55.3), "id": "gunshot", "gain_db": -9},
        {"t": ot(25.5), "id": "wrong_buzzer", "gain_db": -7},
        {"t": ot(30.7), "id": "bruh", "gain_db": -7},
        {"t": ot(34.0), "id": "bass_boom", "gain_db": -4},
    ],
    beds=lambda ot: [
        {"id": "sneaky-snitch-meme", "t": 0.6, "e": ot(64.8), "gain_db": -20},
        {"id": "thinking-theme-jeopardy", "t": ot(4.5), "e": ot(13.6), "gain_db": -20},
        {"id": "fluffing-a-duck", "t": ot(17.6), "e": ot(33.9), "gain_db": -20, "drops": [[ot(25.2), ot(25.6)]]},
        {"id": "curb-your-enthusiasm", "t": ot(34.2) - 1.6, "e": ot(34.2), "gain_db": -12},
    ] if os.path.exists(f"{S}/beds/fluffing-a-duck.mp3") else [
        {"id": "sneaky-snitch-meme", "t": 0.6, "e": ot(64.8), "gain_db": -20},
        {"id": "thinking-theme-jeopardy", "t": ot(4.5), "e": ot(13.6), "gain_db": -20},
        {"id": "vlc-record-2019-06-12-15h36m37s-fluffing-a-duck", "t": ot(17.6), "e": ot(33.9), "gain_db": -20,
         "drops": [[ot(25.2), ot(25.6)]]},
    ],
    zooms=lambda ot: [
        {"t": ot(50.9), "e": ot(51.7), "type": "punch", "amt": 1.2},
        {"t": ot(55.2), "e": ot(55.9), "type": "punch", "amt": 1.2},
        {"t": ot(25.5), "e": ot(26.2), "type": "punch", "amt": 1.18},
        {"t": ot(32.6), "e": ot(34.2), "type": "push", "amt": 1.1},
    ],
    flashes=lambda ot: [{"t": ot(25.5), "d": 0.4, "color": "bw"}, {"t": ot(34.0), "d": 0.13, "color": "red"}],
    laugh_label="*EVERYONE LAUGHS*")

# 6) AGENT JUDGES THE COSTUME CONTEST --------------------------------------------------------------------
run("judge",
    keep=[[96.4, 100.2], [18.3, 26.5], [62.6, 65.2], [66.2, 69.1], [70.3, 76.0], [81.4, 90.0], [90.6, 100.2],
          [102.3, 106.1], [107.1, 111.0]],
    header={"lines": ["AGENT JUDGED THE", "COSTUME CONTEST " + E(SKULL)], "color": "#FF8A00"},
    speakers=[(18.3, 19.4, "kai", "#FFFFFF"), (20.9, 22.0, "agent", "#7FD8FF"), (22.8, 23.3, "agent", "#7FD8FF"),
              (24.3, 24.6, "agent", "#7FD8FF"), (83.6, 111.2, "her", "#FF9EE5")],
    overrides=[(96.4, 97.1, "THE BACK IS COMPLETELY IRRELEVANT"), (63.2, 64.45, "BAGGY-ASS JEAN SHORTS")],
    fixes={"WEIGH": "RATE", "WESLEY,": "AGENT,", "WESLEY": "AGENT", "DUH": "THE"},
    min_laugh=0.55, laugh_label="*EVERYONE LAUGHS*",
    tags=lambda ot: [
        {"t": ot(18.3), "e": ot(19.6), "text": "*COSTUME CONTEST*", "x": 540, "y": 790, "size": 112},
        {"t": ot(23.2), "e": ot(24.2), "text": "*DODGES QUESTION*", "x": 760, "y": 860, "size": 112, "rot": 5},
        {"t": ot(85.3), "e": ot(86.6), "text": "*JUDGING*", "x": 330, "y": 840, "size": 130, "rot": -5},
        {"t": ot(102.3), "e": ot(103.6), "text": "*NO NOTES TAKEN*", "box": "#8B0000", **BOT, "size": 116, "rot": 3},
    ],
    stickers=lambda ot: [
        dict(t=0.3, e=3.8, emoji=E(SKULL, SKULL), size=180, **BOT),
        dict(t=ot(21.1), e=ot(23.7), emoji=E(EYES), x=200, y=790, size=150),
        dict(t=ot(63.2), e=ot(65.1), emoji=E(SKULL), size=200, **BOT),
        dict(t=ot(88.9), e=ot(90.0), emoji=E(FIRE), x=860, y=790, size=150),
        dict(t=ot(97.0), e=ot(100.2), emoji=E(RAISED, SKULL), size=180, **BOT),
        dict(t=ot(105.0), e=ot(106.1), emoji=E(STEAM), x=860, y=790, size=150),
    ],
    sfx=lambda ot: [
        {"t": ot(23.46), "id": "record_scratch", "gain_db": -7},
        {"t": ot(63.52), "id": "vine_boom", "gain_db": -6},
        {"t": ot(71.4), "id": "ding", "gain_db": -9, "dur": 1.0},
        {"t": ot(97.0), "id": "vine_boom", "gain_db": -5},
        {"t": ot(104.4), "id": "bruh", "gain_db": -7},
        {"t": ot(110.6), "id": "bass_boom", "gain_db": -4},
    ],
    beds=lambda ot: [
        {"id": "carefree", "t": 3.8, "e": ot(26.5), "gain_db": -21},
        {"id": "jeopardy-final-jeopardy-thinking-music", "t": ot(81.4), "e": ot(100.2), "gain_db": -21,
         "drops": [[ot(96.6), ot(97.0)]]},
        {"id": "curb-your-enthusiasm", "t": ot(110.6), "e": ot(111.0) + 0.0, "gain_db": -12},
    ],
    zooms=lambda ot: [
        {"t": ot(23.2), "e": ot(23.9), "type": "punch", "amt": 1.18},
        {"t": ot(63.5), "e": ot(64.3), "type": "punch", "amt": 1.18},
        {"t": ot(81.4), "e": ot(90.0), "type": "push", "amt": 1.07},
        {"t": ot(96.9), "e": ot(97.7), "type": "punch", "amt": 1.22},
        {"t": ot(110.4), "e": ot(111.0), "type": "punch", "amt": 1.2},
    ],
    flashes=lambda ot: [{"t": ot(97.0), "d": 0.13, "color": "red"}, {"t": ot(104.4), "d": 0.35, "color": "bw"}])

print({k: round(v, 1) for k, v in results.items()})
