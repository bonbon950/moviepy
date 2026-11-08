"""Two more SAMPLES of the proposed v2 style ("original story cut") — see sample_v2.py for the first one.
Sample 2 = ice cream truck (truck_src, VOD offset 5); Sample 3 = bar (bar_src, VOD offset 840).

usage: samples_v2_more.py WORKDIR [truck] [bar]     (times are VOD seconds of YouTube zFgVajSvLac)
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "tools"))
from plankit import build, out_times

S = sys.argv[1]; B = f"{S}/batch"
only = set(sys.argv[2:])
E = lambda *cps: "".join(chr(c) for c in cps)
SKULL, CRY, FIRE, EYES, MONEY, MONEYFACE, SUNG, SHOCK = (0x1F480, 0x1F62D, 0x1F525, 0x1F440, 0x1F4B0, 0x1F911,
                                                        0x1F60E, 0x1F62E)
CUST = "#FFE14D"
NOTE_Y = 440
SPOTS = [dict(x=300, y=800, size=108, rot=-5), dict(x=780, y=780, size=108, rot=5),      # eye level only
         dict(x=540, y=740, size=110, rot=3), dict(x=780, y=820, size=108, rot=-4)]


def make(name, src, off, keep_vod, notes, insets=(), **kw):
    if only and name not in only:
        return
    v = lambda t: round(t - off, 3)
    keep = [[v(a), v(b)] for a, b in keep_vod]
    def ot(t):
        t = v(t)
        for d in (0, -0.06, 0.06, -0.2, 0.2):
            r = out_times(t + d, keep)
            if r:
                return round(r[-1] - d, 3)
        raise ValueError(f"{name}: {t + off}")
    kw = {k: (val(ot) if callable(val) else val) for k, val in kw.items()}
    kw["speakers"] = [(v(a), v(b), *r) for a, b, *r in kw.get("speakers", [])]
    kw["overrides"] = [(v(a), v(b), t) for a, b, t in kw.get("overrides", [])]
    plan, dur = build(S, B, src, keep, layout="story", me_pos=(540, 760), laugh_spots=SPOTS, beds=[], **kw)
    first_len = keep[0][1] - keep[0][0]          # the hook is the first kept range
    end = lambda t: dur if t == "END" else ot(t)
    plan["notes"] = [{"t": (0.1 if a == "START" else ot(a) + (0.9 if i == 1 else 0)), "e": (first_len if a == "START" else end(b)), "text": txt,
                      "y": NOTE_Y} for i, (a, b, txt) in enumerate(notes)]
    plan["insets"] = [dict(ins, t=ot(ins["t"]), e=end(ins["e"])) for ins in insets]
    plan["story_top"], plan["head_y"] = 540, 200
    json.dump(plan, open(f"{B}/{name}_plan.json", "w"), indent=1)
    print(f"{name}: {dur:.1f}s, {len(plan['words'])} words, {len(plan['notes'])} narrator lines")


# SAMPLE 2 — the ice cream truck: rejected by the diners ... then the street shows up ------------------
make("truck_v2", "truck", 5,
     keep_vod=[[184.0, 187.4],                 # hook: "No? Okay, thank you... nobody wants some more"
               [9.2, 13.0],                    # "It's an ice cream truck!"
               [43.7, 46.5],                   # "we got to sell some ice cream"
               [164.9, 170.0],                 # singing ... "nobody wants ice cream"
               [178.2, 185.2],                 # asks the diners -> "No? Okay, thank you"
               [189.9, 199.2]],                # "Everybody want some ice cream?" -> crowd: "OVER HERE! YES YES YES"
     notes=[("START", 187.4, "HE ASKED A WHOLE TABLE..."),
            (9.2, 13.0, "TOMMY VERCETTI FOUND A NEW BUSINESS"),
            (43.7, 46.5, "THE PLAN: SELL ICE CREAM. GET RICH."),
            (164.9, 170.0, "CUSTOMERS SO FAR: 0"),
            (178.2, 185.2, "ONE LAST TRY..."),
            (189.9, "END", "...THEN THE WHOLE STREET SHOWED UP")],
     header={"lines": ["THEY TURNED DOWN", "KAI'S ICE CREAM " + E(CRY)], "color": "#FF2E88", "size": 92},
     speakers=[(192.9, 199.2, "crowd", CUST)],
     overrides=[(192.9, 194.45, "OH, ICE CREAM! OVER HERE!")],
     tags=lambda ot: [
         {"t": ot(184.2), "e": ot(184.2) + 1.1, "text": "*REJECTED*", "box": "#8B0000", "x": 790, "y": 760, "size": 128, "rot": 5},
         {"t": ot(10.0), "e": ot(10.0) + 1.3, "text": "*NEW RIDE*", "x": 320, "y": 800, "size": 112, "rot": -4},
         {"t": ot(193.0), "e": ot(193.0) + 1.5, "text": "*CROWD RUSHES IN*", "x": 560, "y": 760, "size": 116, "rot": 3},
     ],
     stickers=lambda ot: [
         dict(t=ot(168.8), e=ot(170.0), emoji=E(CRY, CRY), size=170, x=540, y=1830),
         dict(t=ot(184.4), e=ot(185.2), emoji=E(SKULL), size=170, x=540, y=1640),
         dict(t=ot(196.2), e=ot(199.2), emoji=E(FIRE, MONEYFACE), size=170, x=540, y=1830),
     ],
     sfx=lambda ot: [
         {"t": ot(184.2), "id": "bruh", "gain_db": -6},
         {"t": ot(9.6), "id": "anime_wow", "gain_db": -9},
         {"t": ot(44.5), "id": "cash_register", "gain_db": -11},
         {"t": ot(168.8), "id": "spongebob_fail", "gain_db": -9, "dur": 1.6},
         {"t": ot(184.4), "id": "sad_trombone", "gain_db": -12, "dur": 1.2},
         {"t": ot(193.0), "id": "ohhh_crowd", "gain_db": -10, "dur": 1.6},
         {"t": ot(197.7), "id": "bass_drop", "gain_db": -6},
     ],
     zooms=lambda ot: [
         {"t": ot(184.2), "e": ot(184.9), "type": "punch", "amt": 1.2},
         {"t": ot(9.6), "e": ot(10.3), "type": "punch", "amt": 1.16},
         {"t": ot(178.2), "e": ot(184.0), "type": "push", "amt": 1.1},
         {"t": ot(193.0), "e": ot(193.7), "type": "punch", "amt": 1.18},
         {"t": ot(197.7), "e": ot(198.5), "type": "punch", "amt": 1.22},
     ],
     flashes=lambda ot: [{"t": ot(168.8), "d": 0.3, "color": "bw"}, {"t": ot(184.2), "d": 0.35, "color": "bw"},
                         {"t": ot(193.0), "d": 0.12, "color": "white"}],
     insets=[{"t": 168.6, "e": 170.0, "crop": [1632, 64, 88, 52], "scale": 4.4, "x": 540, "y": 1640}])


# SAMPLE 3 — Tommy tries to buy a bar ("GTA property") with his GTA budget ----------------------------
HUD_CASH = [1648, 57, 150, 60]                 # the "$5000" HUD money counter
make("bar_v2", "bar", 840,
     keep_vod=[[1003.5, 1005.9],               # hook: "Yeah, I just wanted to buy this place"
               [842.4, 846.3],                 # "I'm tired of walking, I need a car"
               [860.6, 862.9],                 # "You got a mission for me?" "Side mission"
               [935.4, 939.6],                 # "trying to take over my city ... is this profitable?"
               [986.8, 990.4],                 # slot machines: "Tommy Vercetti likes dabbling"
               [999.4, 1005.9],                # staff: no footage / "I just wanted to buy this place"
               [1013.3, 1018.0],               # "I'm on my sixth business ... boat shop"
               [1027.0, 1031.5]],              # "come back during the day" "Okay, thank you"
     notes=[("START", 1005.9, "HE WALKED IN TO BUY A REAL BAR"),
            (842.4, 846.3, "TOMMY VERCETTI MODE: ON"),
            (860.6, 862.9, "NEW MISSION UNLOCKED"),
            (935.4, 939.6, "GTA RULE: BUY PROPERTY = PROFIT"),
            (986.8, 990.4, "...MAYBE A CASINO TOO"),
            (999.4, 1005.9, "REALITY CHECK"),
            (1013.3, 1018.0, "HIS GTA RESUME"),
            (1027.0, "END", "MISSION FAILED")],
     header={"lines": ["KAI TRIED TO BUY A BAR", "WITH GTA MONEY " + E(SKULL)], "color": "#00E5FF", "size": 88},
     speakers=[(999.4, 1002.5, "staff", CUST), (1019.6, 1022.3, "staff", CUST), (1026.9, 1029.9, "staff", CUST)],
     overrides=[(988.9, 990.5, "TOMMY VERCETTI LIKES DABBLING"), (862.4, 862.9, "SIDE MISSION, OKAY."),
                (936.4, 937.2, "TRYING TO TAKE OVER MY CITY"), (1027.0, 1028.4, "THE OWNERS ARE GONE FOR THE DAY,"),
                (1013.3, 1016.0, "I'M ON MY SIXTH BUSINESS.")],
     tags=lambda ot: [
         {"t": ot(999.5), "e": ot(999.5) + 1.4, "text": "*SECURITY*", "box": "#8B0000", "x": 790, "y": 760, "size": 128, "rot": 4},
         {"t": ot(1027.1), "e": ot(1029.9), "text": "*DENIED*", "box": "#8B0000", "x": 300, "y": 780, "size": 136, "rot": -4},
     ],
     stickers=lambda ot: [
         dict(t=ot(938.0), e=ot(939.6), emoji=E(MONEY, MONEY), size=170, x=540, y=1640),
         dict(t=ot(987.0), e=ot(990.4), emoji=E(MONEYFACE), size=170, x=540, y=1640),
         dict(t=ot(1029.8), e=ot(1031.5), emoji=E(CRY, CRY), size=180, x=540, y=1640),
     ],
     sfx=lambda ot: [
         {"t": ot(845.8), "id": "bruh", "gain_db": -8},
         {"t": ot(860.8), "id": "correct", "gain_db": -11, "dur": 1.2},
         {"t": ot(939.3), "id": "cash_register", "gain_db": -9},
         {"t": ot(987.0), "id": "money_counter", "gain_db": -12, "dur": 1.4},
         {"t": ot(999.5), "id": "dun_dun_dun", "gain_db": -11, "dur": 1.6},
         {"t": ot(1004.5), "id": "vine_boom", "gain_db": -6},
         {"t": ot(1017.9), "id": "huh", "gain_db": -9},
         {"t": ot(1027.1), "id": "wrong_buzzer", "gain_db": -10, "dur": 0.9},
         {"t": ot(1030.2), "id": "mission_failed", "gain_db": -8, "dur": 1.3},
     ],
     zooms=lambda ot: [
         {"t": ot(935.4), "e": ot(939.6), "type": "push", "amt": 1.08},
         {"t": ot(999.5), "e": ot(1000.3), "type": "punch", "amt": 1.18},
         {"t": ot(1004.5), "e": ot(1005.3), "type": "punch", "amt": 1.22},
         {"t": ot(1027.1), "e": ot(1027.9), "type": "punch", "amt": 1.2},
     ],
     flashes=lambda ot: [{"t": ot(999.5), "d": 0.13, "color": "red"}, {"t": ot(1027.1), "d": 0.45, "color": "bw"}],
     insets=[{"t": 1004.0, "e": 1005.9, "crop": HUD_CASH, "scale": 3.2, "x": 540, "y": 1640}])
