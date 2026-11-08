"""Batch (v2 style): Kai Cenat — "I Played GTA 3 For The First Time..." (YouTube V2dHvaSfGZ0, 3:28:16).
Exception to the Kai/AMP IRL-only rule approved by Bjorn for this video; moments already used in CLIP8–13
(controller, never-fail bet, 15 health, PS5s, rage/"that was hard", Catalina/tanks) are skipped.
Gameplay clips use the split frame (enlarged facecam + gameplay); the Loch Ness clip is full-screen camera (story frame).

usage: gta3_v2_batch.py WORKDIR [clip ...]       (all times are VOD seconds; batch/<name>_parts.json maps them)
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from plankit import build, out_times

S = sys.argv[1]; B = f"{S}/batch"
only = set(sys.argv[2:])
E = lambda *cps: "".join(chr(c) for c in cps)
SKULL, CRY, FLUSH, EYES, SHOCK, HUNDRED, THINK, CLOWN, NERD, STEAM, TROPHY, GOAT, PLEAD, SMIRK, FIRE = (
    0x1F480, 0x1F62D, 0x1F633, 0x1F440, 0x1F62E, 0x1F4AF, 0x1F914, 0x1F921, 0x1F913, 0x1F624, 0x1F3C6, 0x1F410,
    0x1F97A, 0x1F60F, 0x1F525)
CAM = [0, 0, 458, 256]
TTS = "#7FD8FF"                                 # TTS / donation voice
# split frame: header (y~230) / narrator (y~385) / facecam 1080x606 at y=450 / gameplay 1080x608 / bottom band
SPLIT = dict(layout="split", cam=CAM, me_pos=(780, 700),
             laugh_spots=[dict(x=790, y=700, size=104, rot=5), dict(x=300, y=760, size=100, rot=-5),
                          dict(x=780, y=740, size=104, rot=-3), dict(x=310, y=720, size=100, rot=4)])
STORY = dict(layout="story", me_pos=(540, 760),
             laugh_spots=[dict(x=300, y=800, size=108, rot=-5), dict(x=780, y=780, size=108, rot=5),
                          dict(x=540, y=740, size=110, rot=3), dict(x=780, y=820, size=108, rot=-4)])
R, L = dict(x=790, y=700), dict(x=300, y=760)   # eye level beside Kai's face (split frame)
BAND = 1790                                     # bottom band centre (split frame): emoji + evidence pop-ups
results = {}


def run(name, keep_vod, notes, frame, insets=(), **kw):
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
    plan, dur = build(S, B, name, keep, beds=[], **{**frame, **kw})
    first_len = keep[0][1] - keep[0][0]
    note_y = 385 if frame["layout"] == "split" else 440
    plan["notes"] = [{"t": 0.1 if a == "START" else ot(a) + (0.9 if i == 1 else 0),
                      "e": first_len if a == "START" else (dur if b == "END" else ot(b)),
                      "text": txt, "y": note_y} for i, (a, b, txt) in enumerate(notes)]
    plan["insets"] = [dict(ins, t=ot(ins["t"]), e=(first_len if ins.get("hook") else ot(ins["e"])))
                      for ins in insets]
    if frame["layout"] == "split":
        plan["split_top"] = 450
    else:
        plan["story_top"], plan["head_y"] = 540, 200
    json.dump(plan, open(f"{B}/{name}_plan.json", "w"), indent=1)
    results[name] = dur
    print(f"{name}: {dur:.1f}s, {len(plan['words'])} words, {len(plan['notes'])} narrator lines, {len(plan['tags'])} tags")


# 1) DEATH — "everybody's so angry, I'm kinda scared" -> one-shot -> "everybody just forget about that" ------
run("death", frame=SPLIT,
    keep_vod=[[1610.15, 1614.25], [1536.05, 1538.4], [1543.4, 1544.4], [1586.9, 1589.0], [1593.4, 1598.0],
              [1604.2, 1607.0], [1610.15, 1621.5], [1624.3, 1628.1]],
    notes=[("START", None, "HIS FIRST DEATH IN GTA 3"),
           (1536.05, 1538.4, "LIBERTY CITY IS ANGRY..."),
           (1543.4, 1544.4, "...AND HE'S SCARED"),
           (1586.9, 1589.0, "TIME TO BE BRAVE"),
           (1593.4, 1598.0, "ONE SHOT."),
           (1604.2, 1607.0, "BACK TO THE START"),
           (1610.15, 1621.5, "DAMAGE CONTROL MODE"),
           (1624.3, "END", "WE SAW IT, KAI")],
    header={"lines": ["KAI BEGGED CHAT TO FORGET", "HIS FIRST DEATH " + E(CRY)], "color": "#FF2E88", "size": 84},
    laugh_label="*KAI LAUGHS*",
    overrides=[(1610.15, 1611.65, "JUST GOT MY FIRST TIME DYING IN GTA."), (1593.4, 1596.1, "BRO, HE ONE-SHOTTED ME WITH A SHOTGUN")],
    tags=lambda ot: [
        {"t": ot(1543.5), "e": ot(1544.4), "text": "*SCARED*", **L, "size": 108, "rot": -5},
        {"t": ot(1595.0), "e": ot(1595.0) + 1.2, "text": "*SHOTGUN*", "box": "#8B0000", **R, "size": 120, "rot": 5},
        {"t": ot(1616.1), "e": ot(1616.1) + 1.4, "text": "*BEGGING CHAT*", **R, "size": 104, "rot": -4},
    ],
    stickers=lambda ot: [
        dict(t=ot(1543.6), e=ot(1544.4), emoji=E(FLUSH), size=160, x=540, y=BAND),
        dict(t=ot(1612.4), e=ot(1614.0), emoji=E(CRY, CRY), size=160, x=540, y=BAND),
        dict(t=ot(1619.0), e=ot(1621.5), emoji=E(PLEAD), size=160, x=540, y=BAND),
    ],
    sfx=lambda ot: [
        {"t": ot(1543.5), "id": "dun_dun_dun", "gain_db": -12, "dur": 1.0},
        {"t": ot(1595.0), "id": "punch", "gain_db": -6},
        {"t": ot(1596.1), "id": "gta_wasted", "gain_db": -9, "dur": 1.6},
        {"t": ot(1605.9), "id": "sad_trombone", "gain_db": -12, "dur": 1.1},
        {"t": ot(1616.1), "id": "bruh", "gain_db": -8},
        {"t": ot(1626.0), "id": "huh", "gain_db": -9},
    ],
    zooms=lambda ot: [
        {"t": ot(1595.0), "e": ot(1595.7), "type": "punch", "amt": 1.2},
        {"t": ot(1610.15), "e": ot(1614.0), "type": "push", "amt": 1.08},
        {"t": ot(1616.1), "e": ot(1616.8), "type": "punch", "amt": 1.16},
    ],
    flashes=lambda ot: [{"t": ot(1595.0), "d": 0.13, "color": "red"}, {"t": ot(1596.1), "d": 0.4, "color": "bw"}],
    insets=[{"t": 1596.0, "e": 1598.0, "crop": [600, 330, 720, 170], "scale": 1.2, "x": 540, "y": BAND}])


# 2) NESSIE — "GTA 6 is going to have a Loch Ness Monster ... I'm gonna be the first to discover it" ----------
run("nessie", frame=STORY,
    keep_vod=[[3326.7, 3331.4], [3319.55, 3323.7], [3326.7, 3343.45]],   # full-screen camera only
    notes=[("START", None, "KAI'S WILDEST GTA 6 PREDICTION"),
           (3319.55, 3323.7, "HE'S CALLING IT NOW"),
           (3326.7, 3333.0, "THE PREDICTION:"),
           (3333.0, 3339.6, "A REAL SEA MONSTER"),
           (3339.6, 3341.6, "AND HE'LL FIND IT FIRST"),
           (3341.6, "END", "SCREENSHOT THIS")],
    header={"lines": ["KAI SAYS GTA 6 HAS", "A LOCH NESS MONSTER " + E(EYES)], "color": "#00E5FF", "size": 88},
    overrides=[(3320.35, 3320.75, "AND I'M GONNA BE")],
    tags=lambda ot: [
        {"t": ot(3320.1), "e": ot(3320.1) + 1.2, "text": "*CALLS IT*", "x": 300, "y": 800, "size": 112, "rot": -4},
        {"t": ot(3330.1), "e": ot(3330.1) + 1.2, "text": "*LOCH NESS*", "box": "#8B0000", "x": 780, "y": 760, "size": 120, "rot": 5},
        {"t": ot(3341.8), "e": ot(3343.45), "text": "*CALLED IT*", "box": "#8B0000", "x": 780, "y": 780, "size": 116, "rot": -3},
    ],
    stickers=lambda ot: [
        dict(t=ot(3322.0), e=ot(3323.6), emoji=E(HUNDRED), size=170, x=540, y=1640),
        dict(t=ot(3333.1), e=ot(3335.2), emoji=E(SHOCK), size=170, x=540, y=1640),
        dict(t=ot(3337.6), e=ot(3339.4), emoji=E(EYES, EYES), size=170, x=540, y=1640),
    ],
    sfx=lambda ot: [
        {"t": ot(3320.1), "id": "riser", "gain_db": -14, "dur": 1.5},
        {"t": ot(3322.2), "id": "heavenly", "gain_db": -14, "dur": 1.4},
        {"t": ot(3330.1), "id": "dun_dun_dun", "gain_db": -10, "dur": 1.6},
        {"t": ot(3333.1), "id": "thunder", "gain_db": -14, "dur": 1.5},
        {"t": ot(3338.0), "id": "suspense", "gain_db": -13, "dur": 1.5},
        {"t": ot(3342.4), "id": "vine_boom", "gain_db": -6},
    ],
    zooms=lambda ot: [
        {"t": ot(3326.7), "e": ot(3342.3), "type": "push", "amt": 1.12},
        {"t": ot(3342.4), "e": ot(3343.1), "type": "punch", "amt": 1.18},
    ],
    flashes=lambda ot: [{"t": ot(3333.1), "d": 0.13, "color": "white"}])


# 3) DRIVER — chat roasts his driving -> "I'm the best driver, bro" -> blames 2001 controllers -------------
run("driver", frame=SPLIT,
    keep_vod=[[5383.7, 5388.1], [4763.6, 4766.5], [4770.3, 4774.2], [4778.1, 4779.5], [4785.95, 4787.8],
              [5362.0, 5366.0], [5368.45, 5369.7], [5377.4, 5391.5]],
    notes=[("START", None, "HIS EXCUSE FOR BAD DRIVING"),
           (4763.6, 4766.5, "CHAT ROASTED HIS DRIVING"),
           (4770.3, 4774.2, "HE DISAGREES"),
           (4778.1, 4787.8, "THE BEST DRIVER, APPARENTLY"),
           (5362.0, 5369.7, "AN HOUR LATER..."),
           (5377.4, 5383.7, "THE EXCUSE:"),
           (5383.7, 5388.1, "FACT CHECK: THEY EXISTED (1997)"),
           (5388.1, "END", "BLAME THE GAME")],
    header={"lines": ["KAI BLAMED HIS DRIVING", "ON 2001 CONTROLLERS " + E(SKULL)], "color": "#FFD60A", "size": 84},
    overrides=[(4763.6, 4766.6, "YOU'RE GENUINELY THE WORST I'VE SEEN ANYBODY DRIVE"),
               (5380.05, 5380.35, "Y'ALL")],
    speakers=[(4763.5, 4766.6, "chat", TTS)],
    tags=lambda ot: [
        {"t": ot(4764.0), "e": ot(4764.0) + 1.3, "text": "*CHAT ROASTS HIM*", **R, "size": 100, "rot": 4},
        {"t": ot(4778.3), "e": ot(4779.5), "text": "*CONFIDENT*", **L, "size": 108, "rot": -5},
        {"t": ot(5385.3), "e": ot(5385.3) + 1.2, "text": "*THE EXCUSE*", "box": "#8B0000", **R, "size": 116, "rot": 5},
    ],
    stickers=lambda ot: [
        dict(t=ot(4765.0), e=ot(4766.5), emoji=E(SKULL), size=160, x=540, y=BAND),
        dict(t=ot(4786.4), e=ot(4787.8), emoji=E(SMIRK), size=160, x=540, y=BAND),
        dict(t=ot(5386.0), e=ot(5388.1), emoji=E(CLOWN), size=160, x=540, y=BAND),
    ],
    sfx=lambda ot: [
        {"t": ot(4764.0), "id": "oof", "gain_db": -8},
        {"t": ot(4778.3), "id": "anime_wow", "gain_db": -10},
        {"t": ot(4786.4), "id": "rizz", "gain_db": -11},
        {"t": ot(5363.0), "id": "bruh", "gain_db": -8},
        {"t": ot(5385.3), "id": "record_scratch", "gain_db": -8},
        {"t": ot(5388.0), "id": "wrong_buzzer", "gain_db": -9, "dur": 0.9},
    ],
    zooms=lambda ot: [
        {"t": ot(4778.3), "e": ot(4779.0), "type": "punch", "amt": 1.16},
        {"t": ot(5377.4), "e": ot(5385.3), "type": "push", "amt": 1.08},
        {"t": ot(5385.3), "e": ot(5386.0), "type": "punch", "amt": 1.2},
    ],
    flashes=lambda ot: [{"t": ot(5385.3), "d": 0.35, "color": "bw"}])


# 4) ESCORT — "you were supposed to protect the truck, but instead you destroyed it" -> "I DO know what escort means" ---
run("escort", frame=SPLIT,
    keep_vod=[[9927.4, 9932.0], [9878.0, 9883.3], [9919.9, 9921.0], [9927.4, 9941.0], [9942.6, 9948.2]],
    notes=[("START", None, "HE KNOWS WHAT ESCORT MEANS..."),
           (9878.0, 9883.3, "THE ROAST:"),
           (9919.9, 9921.0, "MISSION: ESCORT THE TRUCK"),
           (9927.4, 9932.6, "THE DEFENSE:"),
           (9932.6, 9941.0, "DICTIONARY MODE ACTIVATED"),
           (9942.6, "END", "CASE CLOSED?")],
    header={"lines": ["KAI DESTROYED THE TRUCK", "HE WAS ESCORTING " + E(CRY)], "color": "#B6FF3B", "size": 84},
    laugh_label="*KAI LAUGHS*",
    speakers=[(9877.9, 9883.3, "tts", TTS)],
    overrides=[(9938.6, 9940.7, "STOP MAKING ME ACT LIKE I'M STUPID"), (9942.6, 9945.6, "\"I DON'T KNOW WHAT ESCORT MEANS\"?")],
    tags=lambda ot: [
        {"t": ot(9880.2), "e": ot(9880.2) + 1.3, "text": "*ROASTED*", "box": "#8B0000", **R, "size": 120, "rot": 5},
        {"t": ot(9927.6), "e": ot(9927.6) + 1.3, "text": "*DEFENDS HIMSELF*", **R, "size": 100, "rot": -4},
        {"t": ot(9946.8), "e": ot(9948.2), "text": "*SPELLING IT OUT*", **L, "size": 96, "rot": 4},
    ],
    stickers=lambda ot: [
        dict(t=ot(9882.5), e=ot(9883.3), emoji=E(SKULL, SKULL), size=160, x=540, y=BAND),
        dict(t=ot(9933.0), e=ot(9936.6), emoji=E(NERD), size=160, x=540, y=BAND),
        dict(t=ot(9939.0), e=ot(9941.0), emoji=E(STEAM), size=160, x=540, y=BAND),
    ],
    sfx=lambda ot: [
        {"t": ot(9878.2), "id": "oh_hell_nah", "gain_db": -10},
        {"t": ot(9882.5), "id": "emotional_damage", "gain_db": -9, "dur": 1.4},
        {"t": ot(9927.6), "id": "huh", "gain_db": -9},
        {"t": ot(9936.2), "id": "correct", "gain_db": -11, "dur": 1.0},
        {"t": ot(9940.6), "id": "bruh", "gain_db": -8},
        {"t": ot(9947.6), "id": "vine_boom", "gain_db": -6},
    ],
    zooms=lambda ot: [
        {"t": ot(9882.5), "e": ot(9883.2), "type": "punch", "amt": 1.18},
        {"t": ot(9932.6), "e": ot(9941.0), "type": "push", "amt": 1.08},
        {"t": ot(9947.6), "e": ot(9948.2), "type": "punch", "amt": 1.18},
    ],
    flashes=lambda ot: [{"t": ot(9882.5), "d": 0.13, "color": "red"}])


# 5) BEAT IT — "a lot of people do not think I can beat the game" -> credits: "GTA 3 is officially complete" --------
run("beatit", frame=STORY,   # stream switches layouts here: full-screen cam + credits -> story frame
    keep_vod=[[12329.25, 12332.6], [108.0, 111.3], [117.0, 122.4], [12326.4, 12332.6],
              [12398.4, 12405.3], [12489.15, 12494.3]],
    notes=[("START", None, "THE CREDITS ARE ROLLING"),
           (108.0, 111.3, "THE DOUBTERS"),
           (117.0, 122.4, "HIS PREDICTION: BY THE 12TH"),
           (12326.4, 12332.6, "THE FINAL MISSION: DONE"),
           (12398.4, 12405.3, "IT WAS NOT EASY"),
           (12489.15, "END", "NEXT STOP: VICE CITY")],
    header={"lines": ["THEY SAID KAI COULDN'T", "BEAT GTA 3 " + E(EYES)], "color": "#FFD60A", "size": 84},
    overrides=[(12329.25, 12330.7, "GTA 3 IS"), (12402.3, 12402.9, "CHAT? CHAT?"), (12489.2, 12494.4, "FINALLY, BRO. FINALLY. THANK GOD")],
    tags=lambda ot: [
        {"t": ot(108.1), "e": ot(108.1) + 1.3, "text": "*THE DOUBTERS*", "x": 780, "y": 840, "size": 104, "rot": 4},
        {"t": ot(12400.0), "e": ot(12401.4), "text": "*RELIEVED*", "x": 780, "y": 840, "size": 108, "rot": 5},
    ],
    stickers=lambda ot: [
        dict(t=ot(12330.6), e=ot(12332.6), emoji=E(TROPHY), size=170, x=860, y=BAND),
        dict(t=ot(12490.5), e=ot(12494.3), emoji=E(TROPHY), size=170, x=540, y=BAND),
    ],
    sfx=lambda ot: [
        {"t": ot(12329.4), "id": "heavenly", "gain_db": -12, "dur": 1.6},
        {"t": ot(108.1), "id": "dun_dun_dun", "gain_db": -11, "dur": 1.4},
        {"t": ot(12331.7), "id": "bass_boom", "gain_db": -6},
        {"t": ot(12400.0), "id": "huh", "gain_db": -10},
        {"t": ot(12490.5), "id": "correct", "gain_db": -11, "dur": 1.0},
    ],
    zooms=lambda ot: [
        {"t": ot(12331.7), "e": ot(12332.4), "type": "punch", "amt": 1.2},
        {"t": ot(117.0), "e": ot(122.4), "type": "push", "amt": 1.08},
    ],
    flashes=lambda ot: [{"t": ot(12331.7), "d": 0.13, "color": "white"}])


# 6) MISTY — Kai keeps talking to Misty (an NPC who never answers) --------------------------------------------
run("misty", frame=SPLIT,
    keep_vod=[[815.5, 818.3], [790.05, 791.2], [806.8, 815.5], [815.5, 818.3], [829.7, 834.1], [904.4, 912.5],
              [935.0, 939.0]],
    notes=[("START", None, "SHE NEVER SAID A WORD"),
           (790.05, 791.2, "HIS FIRST PASSENGER: MISTY"),
           (806.8, 815.5, "HE TRIED EVERYTHING"),
           (815.5, 818.3, "STILL NOTHING"),
           (829.7, 834.1, "GIVING UP... FOR NOW"),
           (904.4, 912.5, "NEXT MISSION: MISTY AGAIN"),
           (935.0, "END", "HE'S IN TOO DEEP")],
    header={"lines": ["KAI TRIED TO RIZZ", "A GTA 3 NPC " + E(CRY)], "color": "#FF2E88", "size": 88},
    laugh_label="*KAI LAUGHS*",
    fixes={"MISSY": "MISTY", "MISSY,": "MISTY,", "MISSY.": "MISTY."},
    overrides=[(814.6, 815.4, "MISTY VIBES"), (790.05, 791.2, "HOLD ON MISTY, HOLD ON MISTY"), (806.85, 809.3, "WHAT'S UP MISTY,"),
               (935.05, 939.0, "I WON'T... WATCH, MISTY GONNA F*CK UP, CHAT")],
    tags=lambda ot: [
        {"t": ot(809.2), "e": ot(809.2) + 1.3, "text": "*RIZZ ATTEMPT*", **R, "size": 104, "rot": 4},
        {"t": ot(818.0), "e": ot(818.3), "text": "*SILENCE*", "box": "#8B0000", **L, "size": 112, "rot": -4},
        {"t": ot(909.5), "e": ot(909.5) + 1.2, "text": "*MAIN CHARACTER*", **R, "size": 100, "rot": -3},
    ],
    stickers=lambda ot: [
        dict(t=ot(810.0), e=ot(812.2), emoji=E(SMIRK), size=160, x=540, y=BAND),
        dict(t=ot(816.0), e=ot(818.3), emoji=E(PLEAD), size=160, x=540, y=BAND),
        dict(t=ot(937.0), e=ot(939.0), emoji=E(SKULL), size=160, x=540, y=BAND),
    ],
    sfx=lambda ot: [
        {"t": ot(809.2), "id": "rizz", "gain_db": -10},
        {"t": ot(818.0), "id": "confused", "gain_db": -10, "dur": 1.0},
        {"t": ot(831.0), "id": "sad_violin", "gain_db": -16, "dur": 1.6},
        {"t": ot(909.5), "id": "vine_boom", "gain_db": -6},
        {"t": ot(937.5), "id": "oh_hell_nah", "gain_db": -10},
    ],
    zooms=lambda ot: [
        {"t": ot(806.8), "e": ot(815.5), "type": "push", "amt": 1.08},
        {"t": ot(818.0), "e": ot(818.3), "type": "punch", "amt": 1.16},
        {"t": ot(909.5), "e": ot(910.2), "type": "punch", "amt": 1.18},
    ],
    flashes=lambda ot: [{"t": ot(818.0), "d": 0.3, "color": "bw"}])

print({k: round(val, 1) for k, val in results.items()})
