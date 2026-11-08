"""Batch (v2 style): Fanum — "50 CENT BLOOD ON THE SAND MARATHON" (Twitch VOD 2922748515, Nov 8 2026, 4:54:55).
Gameplay stream: exception to the IRL-first rule approved by Bjorn for this VOD. Only full-camera talking moments
are used (story frame); the Xbox 360 dashboard moment was dropped (tiny facecam on menus -> low-res, boring).

usage: fanum_50cent_v2_batch.py WORKDIR VODDIR [clip ...]   (WORKDIR = shorts_work with sfx_lib/fonts/emoji;
       VODDIR holds batch/; all times are VOD seconds; batch/<name>_parts.json maps them)
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "tools"))
from plankit import build, out_times

S = sys.argv[1]; B = f"{sys.argv[2]}/batch"
only = set(sys.argv[3:])
E = lambda *cps: "".join(chr(c) for c in cps)
SKULL, CRY, FLUSH, EYES, SHOCK, HUNDRED, STEAM, FIRE, ANGRY, COFFEE, BURRITO, SHOE, MONEYWINGS, PRAY, NERD, CROWN = (
    0x1F480, 0x1F62D, 0x1F633, 0x1F440, 0x1F62E, 0x1F4AF, 0x1F624, 0x1F525, 0x1F620, 0x2615, 0x1F32F, 0x1F45F,
    0x1F4B8, 0x1F64F, 0x1F913, 0x1F451)
STORY = dict(layout="story", me_pos=(540, 760),
             laugh_spots=[dict(x=300, y=800, size=108, rot=-5), dict(x=780, y=780, size=108, rot=5),
                          dict(x=540, y=740, size=110, rot=3), dict(x=780, y=820, size=108, rot=-4)])
R, L = dict(x=790, y=770), dict(x=300, y=800)   # eye level beside Fanum's face (story frame)
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
    plan, dur = build(S, B, name, keep, beds=[], laugh_label="*FANUM LAUGHS*", **{**STORY, **kw})
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


# 1) SNACK WRAP — pauses the final boss to eat ... someone already took a bite ---------------------------------
run("snack",
    keep_vod=[[10570.2, 10572.4],               # hook: "Now somebody bit my snack wrap"
              [10362.0, 10367.55],              # "Should we eat now or after we kill him? Now or after?"
              [10372.6, 10373.6],               # "NOW."
              [10535.0, 10541.4],               # "just now... I almost died"
              [10563.7, 10566.6],               # "I'ma take a bite out of my snack wrap already"
              [10567.8, 10583.0]],              # "nah... somebody bit my snack wrap ... violated" -> LOOP
    notes=[("START", None, "SOMEONE TOUCHED HIS FOOD"),
           (10362.0, 10367.55, "FINAL BOSS ON THE SCREEN..."),
           (10372.6, 10373.6, "FOOD WINS"),
           (10535.0, 10541.4, "HE ALMOST DIED FOR THIS MEAL"),
           (10563.7, 10566.6, "FINALLY. FIRST BITE..."),
           (10567.8, 10576.3, "WAIT."),
           (10576.3, "END", "CRIME SCENE")],
    header={"lines": ["NEVER TOUCH FANUM'S", "SNACK WRAP " + E(STEAM)], "color": "#FF2E88", "size": 92},
    overrides=[(10535.0, 10541.4, "JUST NOW... I ALMOST DIED."),
               (10563.7, 10566.6, "I'MA TAKE A BITE OUT MY SNACK WRAP ALREADY"),
               (10576.3, 10579.5, "LOOK, LOOK, SOMEBODY BIT MY SHIT. LOOK")],
    tags=lambda ot: [
        {"t": ot(10372.7), "e": ot(10373.6), "text": "*PAUSES THE BOSS*", **R, "size": 100, "rot": 4},
        {"t": ot(10568.0), "e": ot(10569.5), "text": "*NOTICES*", "box": "#8B0000", **L, "size": 120, "rot": -5},
        {"t": ot(10580.5), "e": ot(10583.0), "text": "*VIOLATED*", "box": "#8B0000", **R, "size": 116, "rot": 4},
    ],
    stickers=lambda ot: [
        dict(t=ot(10372.7), e=ot(10373.6), emoji=E(BURRITO), size=170, x=540, y=BAND),
        dict(t=ot(10537.0), e=ot(10541.4), emoji=E(SKULL), size=170, x=540, y=BAND),
        dict(t=ot(10568.0), e=ot(10570.0), emoji=E(EYES, EYES), size=170, x=540, y=BAND),
    ],
    sfx=lambda ot: [
        {"t": ot(10362.3), "id": "suspense", "gain_db": -12, "dur": 1.6},
        {"t": ot(10372.7), "id": "ding", "gain_db": -9, "dur": 1.0},
        {"t": ot(10537.0), "id": "oof", "gain_db": -9},
        {"t": ot(10565.3), "id": "pop", "gain_db": -8},
        {"t": ot(10568.0), "id": "record_scratch", "gain_db": -6},
        {"t": ot(10571.0), "id": "dun_dun_dun", "gain_db": -11, "dur": 1.4},
        {"t": ot(10577.0), "id": "fbi_open_up", "gain_db": -10, "dur": 1.5},
        {"t": ot(10581.0), "id": "oh_hell_nah", "gain_db": -9},
    ],
    zooms=lambda ot: [
        {"t": ot(10362.0), "e": ot(10367.5), "type": "push", "amt": 1.06},
        {"t": ot(10372.7), "e": ot(10373.4), "type": "punch", "amt": 1.2},
        {"t": ot(10568.0), "e": ot(10568.7), "type": "punch", "amt": 1.18},
        {"t": ot(10571.0), "e": ot(10576.0), "type": "push", "amt": 1.1},
        {"t": ot(10581.0), "e": ot(10581.7), "type": "punch", "amt": 1.18},
    ],
    flashes=lambda ot: [{"t": ot(10372.7), "d": 0.12, "color": "white"}, {"t": ot(10568.0), "d": 0.35, "color": "bw"}],
    insets=[{"t": 10574.0, "e": 10580.0, "crop": [800, 300, 440, 440], "scale": 1.15, "x": 540, "y": BAND}])


# 2) MOCHA DICTATORSHIP — someone mentions the sugar -> everyone gets timed out ----------------------------------
run("mocha",
    keep_vod=[[6959.2, 6961.3],                 # hook: "This is a dictatorship"
              [6821.4, 6826.2],                 # "I'm gonna do the mocha... medium mocha frappe"
              [6842.0, 6848.6],                 # "That shit got mad sugar?! ... you think I don't know what I'm ordering"
              [6868.1, 6871.6],                 # "Time out. Don't try to mess up my vibe"
              [6879.4, 6882.8],                 # "Time out, time out, and time out Zeba"
              [6936.6, 6941.2],                 # "You mad bro? I'm not mad. I'm not mad. YouTube chat chill"
              [6954.1, 6961.3]],                # "I'm hangry... anybody that say ban me, time 'em out. This is a dictatorship" -> LOOP
    notes=[("START", None, "HE ONLY WANTED A COFFEE"),
           (6821.4, 6826.2, "THE ORDER: MEDIUM MOCHA FRAPPE"),
           (6842.0, 6848.6, "SOMEONE MENTIONED THE SUGAR..."),
           (6868.1, 6871.6, "WRONG MOVE"),
           (6879.4, 6882.8, "NOBODY IS SAFE. NOT EVEN ZEBA"),
           (6936.6, 6941.2, "HE'S NOT MAD (HE'S MAD)"),
           (6954.1, "END", "HUNGRY FANUM = NEW LAWS")],
    header={"lines": ["NEVER TELL FANUM HIS COFFEE", "HAS TOO MUCH SUGAR " + E(COFFEE)], "color": "#00E5FF", "size": 80},
    overrides=[(6821.4, 6826.2, "I'M GONNA DO THE MOCHA. MEDIUM MOCHA FRAPPE."),
               (6879.4, 6882.8, "YO, TIME OUT, TIME OUT, AND TIME OUT ZEBA."),
               (6956.7, 6959.25, "ANYBODY THAT SAY BAN ME, TIME 'EM OUT.")],
    tags=lambda ot: [
        {"t": ot(6843.3), "e": ot(6844.6), "text": "*TRIGGERED*", "box": "#8B0000", **R, "size": 116, "rot": 4},
        {"t": ot(6868.2), "e": ot(6869.6), "text": "*TIMEOUT*", "box": "#8B0000", **L, "size": 120, "rot": -4},
        {"t": ot(6882.0), "e": ot(6882.8), "text": "*ZEBA DOWN*", **R, "size": 104, "rot": -3},
        {"t": ot(6937.2), "e": ot(6938.2), "text": "*NOT MAD*", **L, "size": 108, "rot": 4},
    ],
    stickers=lambda ot: [
        dict(t=ot(6822.4), e=ot(6826.2), emoji=E(COFFEE), size=170, x=540, y=BAND),
        dict(t=ot(6843.3), e=ot(6845.5), emoji=E(ANGRY), size=170, x=540, y=BAND),
        dict(t=ot(6958.5), e=ot(6961.3), emoji=E(CROWN), size=170, x=540, y=1830),
    ],
    sfx=lambda ot: [
        {"t": ot(6822.4), "id": "cash_register", "gain_db": -12},
        {"t": ot(6842.4), "id": "record_scratch", "gain_db": -6},
        {"t": ot(6843.3), "id": "vine_boom", "gain_db": -6},
        {"t": ot(6868.2), "id": "wrong_buzzer", "gain_db": -10, "dur": 0.9},
        {"t": ot(6882.0), "id": "punch", "gain_db": -7},
        {"t": ot(6937.2), "id": "huh", "gain_db": -9},
        {"t": ot(6960.2), "id": "chinese_gong", "gain_db": -11, "dur": 1.4},
    ],
    zooms=lambda ot: [
        {"t": ot(6843.3), "e": ot(6844.0), "type": "punch", "amt": 1.2},
        {"t": ot(6868.2), "e": ot(6868.9), "type": "punch", "amt": 1.16},
        {"t": ot(6879.4), "e": ot(6882.8), "type": "push", "amt": 1.08},
        {"t": ot(6954.1), "e": ot(6959.0), "type": "push", "amt": 1.1},
        {"t": ot(6960.2), "e": ot(6960.9), "type": "punch", "amt": 1.2},
    ],
    flashes=lambda ot: [{"t": ot(6843.3), "d": 0.12, "color": "red"}, {"t": ot(6960.2), "d": 0.3, "color": "bw"}],
    insets=[{"t": 6880.2, "e": 6882.8, "png": "chat_ziba.png", "crop": [0, 0, 500, 230], "scale": 1.8, "x": 540, "y": BAND},
            {"t": 6937.0, "e": 6941.2, "png": "chat_madbro.png", "crop": [0, 0, 330, 36], "scale": 2.4, "x": 540, "y": BAND}])


# 3) PARLAY — every leg hits ... except the one that needed 10 points -------------------------------------------
run("parlay",
    keep_vod=[[6548.1, 6552.2],                 # hook: "10 points. He could get 10 points. He got 7 points"
              [6511.3, 6514.5],                 # "I put a ticket bro. Listen to the ticket"
              [6522.5, 6525.9],                 # "I had Mitchell for 23 points... scored 37"
              [6526.7, 6529.8],                 # "I had Kat for 15. He got 29"
              [6534.7, 6536.3],                 # "Jalen for 25. He scored 31"
              [6537.4, 6539.1],                 # "Kat for 10 rebounds. He got 13 boards"
              [6541.7, 6546.9],                 # "The only leg was James Harden. And it was 10 points."
              [6548.1, 6552.2],                 # "...He got 7 points"
              [6564.0, 6566.4],                 # "but damn son, give me 10"
              [6608.4, 6613.1]],                # "I feel like it's bad energy on the streams bro" -> LOOP
    notes=[("START", None, "ONE LEG AWAY..."),
           (6511.3, 6514.5, "FANUM'S PARLAY:"),
           (6522.5, 6525.9, "HIT."),
           (6526.7, 6529.8, "HIT."),
           (6534.7, 6536.3, "HIT."),
           (6537.4, 6539.1, "HIT."),
           (6541.7, 6546.9, "LAST LEG: 10 POINTS"),
           (6548.1, 6552.2, "HE NEEDED 3 MORE"),
           (6564.0, 6566.4, "PAIN."),
           (6608.4, "END", "THE EXCUSE:")],
    header={"lines": ["ONE PLAYER RUINED", "FANUM'S WHOLE PARLAY " + E(SKULL)], "color": "#FFE14D", "size": 84},
    overrides=[(6522.5, 6524.2, "I HAD MITCHELL FOR 23 POINTS."), (6526.7, 6529.8, "I HAD KAT FOR 15. HE GOT 29."),
               (6537.4, 6539.1, "KAT FOR 10 REBOUNDS. HE GOT 13 BOARDS.")],
    tags=lambda ot: [
        {"t": ot(6551.3), "e": ot(6552.2), "text": "*7 POINTS*", "box": "#8B0000", **R, "size": 124, "rot": 5},
        {"t": ot(6564.2), "e": ot(6565.6), "text": "*BEGGING*", **L, "size": 110, "rot": -4},
        {"t": ot(6610.9), "e": ot(6612.6), "text": "*BLAMES THE STREAM*", **R, "size": 96, "rot": -3},
    ],
    stickers=lambda ot: [
        dict(t=ot(6525.2), e=ot(6525.9), emoji=E(MONEYWINGS), size=160, x=540, y=1830),
        dict(t=ot(6535.6), e=ot(6539.1), emoji=E(FIRE), size=160, x=540, y=1830),
        dict(t=ot(6551.3), e=ot(6552.2), emoji=E(CRY, CRY), size=170, x=540, y=1830),
        dict(t=ot(6564.2), e=ot(6566.4), emoji=E(PRAY), size=170, x=540, y=BAND),
    ],
    sfx=lambda ot: [
        {"t": ot(6511.6), "id": "riser", "gain_db": -14, "dur": 1.5},
        {"t": ot(6525.3), "id": "correct", "gain_db": -10},
        {"t": ot(6529.2), "id": "correct", "gain_db": -10},
        {"t": ot(6535.8), "id": "correct", "gain_db": -10},
        {"t": ot(6538.6), "id": "correct", "gain_db": -10},
        {"t": ot(6544.4), "id": "suspense", "gain_db": -11, "dur": 1.6},
        {"t": ot(6551.3), "id": "wrong_buzzer", "gain_db": -8, "dur": 0.9},
        {"t": ot(6551.8), "id": "sad_trombone", "gain_db": -12, "dur": 1.2},
        {"t": ot(6611.0), "id": "bruh", "gain_db": -8},
    ],
    zooms=lambda ot: [
        {"t": ot(6522.5), "e": ot(6539.1), "type": "push", "amt": 1.08},
        {"t": ot(6541.7), "e": ot(6546.9), "type": "push", "amt": 1.12},
        {"t": ot(6551.3), "e": ot(6552.0), "type": "punch", "amt": 1.22},
        {"t": ot(6611.0), "e": ot(6611.7), "type": "punch", "amt": 1.16},
    ],
    flashes=lambda ot: [{"t": ot(6551.3), "d": 0.35, "color": "bw"}],
    insets=[{"t": 6550.0, "e": 6552.2, "crop": [800, 260, 360, 340], "scale": 1.4, "x": 540, "y": BAND}])


# 4) BIG BONED — beats the game, blames Kai, then defends the vest ----------------------------------------------
run("boned",
    keep_vod=[[17302.1, 17307.5],               # hook: "I mean under four... but then Kai dumbass bro" (on camera)
              [17289.7, 17294.2],               # "Don't even that bad though. We beat it under five hours low-key"
              [17312.4, 17317.5],               # "I blame Duke cause Duke let him stream near him. I blame Duke"
              [17320.7, 17325.9],               # "that vest hella tiny, or maybe I'm just hella big"
              [17332.6, 17335.8],               # "Fun fact, this is a real vest"
              [17343.7, 17348.1],               # "Yo look bro, this is good vest game"
              [17356.3, 17358.0]],              # "I'm not big, I'm just big boned" (off camera -> vest still pop-up)
    notes=[("START", None, "HE HAS AN EXPLANATION"),
           (17289.7, 17294.2, "GAME BEATEN IN UNDER 5 HOURS"),
           (17312.4, 17317.5, "AND IT'S DUKE'S FAULT TOO"),
           (17320.7, 17325.9, "NOW ABOUT THAT VEST"),
           (17332.6, 17335.8, "IT'S A REAL ONE"),
           (17343.7, 17348.1, "AND IT FITS. PERFECTLY."),
           (17356.3, "END", "CASE CLOSED")],
    header={"lines": ["FANUM BEAT THE GAME...", "AND BLAMED KAI " + E(CRY)], "color": "#FF2E88", "size": 90},
    overrides=[(17289.7, 17294.2, "NOT EVEN THAT BAD THOUGH. WE BEAT IT UNDER FIVE HOURS, LOW-KEY."),
               (17305.64, 17306.26, "KAI"),
               (17320.7, 17325.9, "THAT VEST HELLA TINY, OR MAYBE I'M JUST HELLA BIG. Y'ALL EVER THOUGHT ABOUT THAT?"),
               (17356.3, 17358.0, "Y'ALL, I'M NOT BIG. I'M JUST BIG BONED.")],
    tags=lambda ot: [
        {"t": ot(17305.7), "e": ot(17307.3), "text": "*BLAMES KAI*", "box": "#8B0000", **R, "size": 116, "rot": 4},
        {"t": ot(17313.0), "e": ot(17314.5), "text": "*BLAMES DUKE*", **L, "size": 108, "rot": -4},
        {"t": ot(17344.5), "e": ot(17346.5), "text": "*MODELING*", **R, "size": 108, "rot": -3},
    ],
    stickers=lambda ot: [
        dict(t=ot(17291.5), e=ot(17294.2), emoji=E(CROWN), size=170, x=540, y=BAND),
        dict(t=ot(17323.8), e=ot(17325.9), emoji=E(FLUSH), size=170, x=540, y=BAND),
        dict(t=ot(17356.4), e=ot(17358.0), emoji=E(SKULL), size=150, x=930, y=1450),
    ],
    sfx=lambda ot: [
        {"t": ot(17291.5), "id": "heavenly", "gain_db": -14, "dur": 1.4},
        {"t": ot(17305.7), "id": "vine_boom", "gain_db": -6},
        {"t": ot(17313.0), "id": "huh", "gain_db": -9},
        {"t": ot(17323.8), "id": "boing", "gain_db": -10},
        {"t": ot(17333.4), "id": "anime_wow", "gain_db": -10},
        {"t": ot(17344.5), "id": "rizz", "gain_db": -10},
        {"t": ot(17357.3), "id": "bruh", "gain_db": -8},
    ],
    zooms=lambda ot: [
        {"t": ot(17302.1), "e": ot(17305.6), "type": "push", "amt": 1.08},
        {"t": ot(17305.7), "e": ot(17306.4), "type": "punch", "amt": 1.2},
        {"t": ot(17320.7), "e": ot(17325.9), "type": "push", "amt": 1.1},
        {"t": ot(17357.3), "e": ot(17358.0), "type": "punch", "amt": 1.18},
    ],
    flashes=lambda ot: [{"t": ot(17305.7), "d": 0.12, "color": "red"}, {"t": ot(17344.5), "d": 0.12, "color": "white"}],
    insets=[{"t": 17344.0, "e": 17348.1, "crop": [420, 80, 640, 560], "scale": 0.85, "x": 540, "y": BAND},
            {"t": 17356.3, "e": "END", "png": "vest_still.png", "crop": [0, 0, 640, 560], "scale": 0.85, "x": 540, "y": BAND}])


# 5) G-UNIT DRIP — dressed as 50 Cent to play 50 Cent's game ----------------------------------------------------
run("gunit",
    keep_vod=[[322.4, 326.8],                   # hook: "just to show you, look, look, hold on, just to show you I came correct"
              [296.3, 304.35],                  # "We got 50 Cent Blood on the Sand... can't get off until we beat it"
              [331.2, 337.7],                   # "If you know you know, I got the G-Unit Reeboks"
              [357.3, 362.2],                   # "look and look, I'm really not fooling around"
              [374.1, 378.4]],                  # "vitamin water, vitamin water" -> LOOP
    notes=[("START", None, "HE CAME PREPARED"),
           (296.3, 304.35, "TODAY: 50 CENT'S OWN VIDEO GAME"),
           (331.2, 337.7, "STEP 1: G-UNIT REEBOKS"),
           (357.3, 362.2, "STEP 2: THE VEST"),
           (374.1, "END", "STEP 3: 50'S FAMOUS DRINK")],
    header={"lines": ["FANUM SHOWED UP", "DRESSED AS 50 CENT " + E(HUNDRED)], "color": "#FFE14D", "size": 90},
    overrides=[(299.24, 301.94, "BLOOD ON THE SAND."), (374.12, 374.94, "I KNOW")],
    tags=lambda ot: [
        {"t": ot(325.6), "e": ot(326.8), "text": "*CAME CORRECT*", **R, "size": 104, "rot": 4},
        {"t": ot(332.6), "e": ot(334.4), "text": "*G-UNIT*", "box": "#8B0000", **L, "size": 124, "rot": -5},
        {"t": ot(375.0), "e": ot(377.0), "text": "*SIPS*", **R, "size": 116, "rot": -4},
    ],
    stickers=lambda ot: [
        dict(t=ot(298.0), e=ot(301.9), emoji=E(FIRE), size=170, x=540, y=1830),
        dict(t=ot(358.5), e=ot(362.2), emoji=E(HUNDRED), size=170, x=540, y=BAND),
        dict(t=ot(376.3), e=ot(378.4), emoji=E(CROWN), size=170, x=540, y=1830),
    ],
    sfx=lambda ot: [
        {"t": ot(297.0), "id": "airhorn", "gain_db": -14, "dur": 1.0},
        {"t": ot(332.6), "id": "vine_boom", "gain_db": -6},
        {"t": ot(335.0), "id": "anime_wow", "gain_db": -10},
        {"t": ot(357.6), "id": "rizz", "gain_db": -10},
        {"t": ot(375.0), "id": "ding", "gain_db": -10, "dur": 1.0},
    ],
    zooms=lambda ot: [
        {"t": ot(296.3), "e": ot(304.3), "type": "push", "amt": 1.06},
        {"t": ot(332.6), "e": ot(333.3), "type": "punch", "amt": 1.18},
        {"t": ot(357.3), "e": ot(362.2), "type": "push", "amt": 1.1},
        {"t": ot(375.0), "e": ot(375.7), "type": "punch", "amt": 1.16},
    ],
    flashes=lambda ot: [{"t": ot(332.6), "d": 0.12, "color": "white"}],
    insets=[{"t": 333.0, "e": 337.7, "crop": [840, 360, 760, 380], "scale": 0.9, "x": 540, "y": BAND}])

print({k: round(val, 1) for k, val in results.items()})
