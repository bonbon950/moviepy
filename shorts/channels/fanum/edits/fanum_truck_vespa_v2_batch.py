"""Batch (v2 style): Fanum — "REVEALING MY NEW TRUCK / BUYING A VESPA" (Twitch VOD 2925209386, Nov 10 2026, 10:09:06).
IRL stream (truck reveal at the house, then the Vespa dealership). Sent by Bjorn for this batch (Nov 11).

usage: fanum_truck_vespa_v2_batch.py WORKDIR VODDIR [clip ...]   (WORKDIR = shorts_work with sfx_lib/fonts/emoji;
       VODDIR holds batch/; all times are VOD seconds; batch/<name>_parts.json maps them)
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "tools"))
from plankit import build, out_times

S = sys.argv[1]; B = f"{sys.argv[2]}/batch"
only = set(sys.argv[3:])
E = lambda *cps: "".join(chr(c) for c in cps)
SKULL, CRY, NERD, SHOCK, COOL, MONEYWINGS, FIRE, STEAM, HUNDRED, EYES = (
    0x1F480, 0x1F62D, 0x1F913, 0x1F62E, 0x1F60E, 0x1F4B8, 0x1F525, 0x1F624, 0x1F4AF, 0x1F440)
STORY = dict(layout="story", me_pos=(540, 760),
             laugh_spots=[dict(x=300, y=800, size=108, rot=-5), dict(x=780, y=780, size=108, rot=5),
                          dict(x=540, y=740, size=110, rot=3), dict(x=780, y=820, size=108, rot=-4)])
R, L = dict(x=790, y=770), dict(x=300, y=800)   # eye level beside the faces (story frame)
BAND = 1640                                     # bottom band: emoji + evidence pop-ups
SALES = "#00E5FF"                               # caption color for the Vespa salesman
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


# 1) VESPA — the salesman keeps it real: the 50 won't make the hill ... "especially my size" -------------------------
run("vespa",
    keep_vod=[[3524.8, 3528.25],                # hook (salesman): "especially my size. So neither one of us are, you know"
              [3265.7, 3269.45],                # "Why do you want a Vespa?" "Because it's a motorcycle, right?"
              [3270.1, 3271.75],                # (salesman) "No. It's not. It's a scooter."
              [3406.6, 3408.85],                # "That's a Mickey Mouse Vespa right there, Jack"
              [3508.1, 3509.85],                # (salesman) "this is a fifty, even slower"
              [3513.2, 3516.1],                 # "35 top speed"
              [3516.85, 3522.8],                # "but going up a hill like this ... it ain't gonna go"
              [3524.8, 3528.25],                # "especially my size. So neither one of us are, you know"
              [3654.25, 3660.95],               # "I'm gonna use the Vespa every day, and it's safer, right? I'm trying to be safe"
              [3695.8, 3697.85]],               # "I guess I'll do that one then." -> LOOP
    notes=[("START", None, "THE SALESMAN KEPT IT 100"),
           (3265.7, 3269.45, "WHY DOES FANUM WANT A VESPA?"),
           (3270.1, 3271.75, "CORRECTED."),
           (3406.6, 3408.85, "THE MICKEY MOUSE EDITION"),
           (3508.1, 3516.1, "THE SMALL ONE: 35 MPH MAX"),
           (3516.85, 3522.8, "PROBLEM: HILLS"),
           (3524.8, 3528.25, "AND... THE SIZE"),
           (3654.25, 3660.95, "HIS REASON: SAFETY"),
           (3695.8, "END", "SOLD: $7,424 + TAX")],
    header={"lines": ["THE VESPA SALESMAN WAS", "TOO HONEST WITH FANUM " + E(CRY)], "color": "#7CFFB2", "size": 84},
    speakers=[(3265.7, 3267.1, "sales", SALES), (3270.1, 3271.75, "sales", SALES),
              (3508.1, 3522.8, "sales", SALES), (3524.8, 3528.25, "sales", SALES)],
    overrides=[(3524.8, 3528.25, "ESPECIALLY MY SIZE. SO NEITHER ONE OF US ARE, YOU KNOW..."),
               (3508.1, 3509.85, "THIS IS A FIFTY. EVEN SLOWER."),
               (3513.2, 3516.1, "35 TOP SPEED."),
               (3654.25, 3655.6, "I'M GONNA USE THE VESPA EVERY DAY")],
    tags=lambda ot: [
        {"t": ot(3270.3), "e": ot(3271.7), "text": "*CORRECTED*", "box": "#8B0000", **L, "size": 112, "rot": -4},
        {"t": ot(3407.4), "e": ot(3408.8), "text": "*MICKEY*", **R, "size": 112, "rot": 4},
        {"t": ot(3521.6), "e": ot(3522.8), "text": "*NO HILLS*", **L, "size": 108, "rot": 3},
        {"t": ot(3525.6), "e": ot(3528.2), "text": "*FELT THAT*", "box": "#8B0000", **R, "size": 112, "rot": -4},
        {"t": ot(3658.3), "e": ot(3660.9), "text": "*SAFETY FIRST*", **L, "size": 100, "rot": 4},
        {"t": ot(3696.9), "e": ot(3697.85), "text": "*SOLD*", "box": "#8B0000", **R, "size": 124, "rot": 5},
    ],
    stickers=lambda ot: [
        dict(t=ot(3270.3), e=ot(3271.75), emoji=E(NERD), size=170, x=540, y=BAND),
        dict(t=ot(3513.3), e=ot(3516.1), emoji=E(SHOCK), size=170, x=540, y=BAND),
        dict(t=ot(3525.6), e=ot(3528.25), emoji=E(SKULL, SKULL), size=170, x=540, y=BAND),
        dict(t=ot(3656.0), e=ot(3660.9), emoji=E(COOL), size=160, x=540, y=1830),
    ],
    sfx=lambda ot: [
        {"t": ot(3266.0), "id": "huh", "gain_db": -9},
        {"t": ot(3270.3), "id": "wrong_buzzer", "gain_db": -10, "dur": 0.9},
        {"t": ot(3407.4), "id": "boing", "gain_db": -10},
        {"t": ot(3513.3), "id": "sad_trombone", "gain_db": -12, "dur": 1.2},
        {"t": ot(3518.3), "id": "suspense", "gain_db": -12, "dur": 1.6},
        {"t": ot(3525.6), "id": "vine_boom", "gain_db": -6},
        {"t": ot(3527.6), "id": "emotional_damage", "gain_db": -10},
        {"t": ot(3658.3), "id": "ding", "gain_db": -10, "dur": 1.0},
        {"t": ot(3696.9), "id": "cash_register", "gain_db": -9},
    ],
    zooms=lambda ot: [
        {"t": ot(3265.7), "e": ot(3269.4), "type": "push", "amt": 1.06},
        {"t": ot(3270.3), "e": ot(3271.0), "type": "punch", "amt": 1.18},
        {"t": ot(3516.85), "e": ot(3522.8), "type": "push", "amt": 1.1},
        {"t": ot(3525.6), "e": ot(3526.3), "type": "punch", "amt": 1.2},
        {"t": ot(3696.9), "e": ot(3697.6), "type": "punch", "amt": 1.16},
    ],
    flashes=lambda ot: [{"t": ot(3270.3), "d": 0.12, "color": "red"}, {"t": ot(3525.6), "d": 0.3, "color": "bw"},
                        {"t": ot(3696.9), "d": 0.14, "color": "green"}],
    insets=[{"t": 3695.9, "e": "END", "png": "ev_vespa.png", "crop": [0, 0, 1060, 560], "scale": 0.8, "x": 540, "y": BAND}])


# 2) TRUCK — bought a Ram 3500 dually to carry his other cars; 6'5", "180 lbs lean muscle" -------------------------
run("truck",
    keep_vod=[[993.4, 998.1],                   # hook: "I'm six foot five ... a hundred and eighty pounds lean muscle mass"
              [745.9, 748.45],                  # "y'all know I got more than one car"
              [762.6, 765.35],                  # "So we got the lambo truck Urus, AKA Thanos"
              [789.95, 791.95],                 # "I can only drive one car at a time, bro"
              [796.6, 800.25],                  # "I used to pay for shipping for cars, that shit is expensive"
              [818.0, 822.0],                   # "I got me a brand new Ram 3500 dually"
              [828.9, 831.25],                  # "I might start a tow trucking business with this"
              [1060.9, 1063.45],                # chat: "stop slamming doors" -> "it's a truck"
              [1067.4, 1071.2],                 # "What do you think this is, a Mini Cooper? It's a truck, bro. Have some respect"
              [1859.8, 1864.5]],                # chat: "angle makes Fanum look fat when he is a chiseled man with abs. Thank you." -> LOOP
    notes=[("START", None, "FANUM'S OFFICIAL STATS:"),
           (745.9, 748.45, "PROBLEM: TOO MANY CARS"),
           (762.6, 765.35, "LIKE THIS ONE. \"THANOS\""),
           (789.95, 800.25, "SHIPPING THEM? EXPENSIVE."),
           (818.0, 822.0, "THE SOLUTION:"),
           (828.9, 831.25, "NEW CAREER UNLOCKED"),
           (1060.9, 1071.2, "CHAT HAD NOTES"),
           (1859.8, "END", "CHAT ALSO SAID:")],
    header={"lines": ["FANUM BOUGHT A TRUCK TO", "CARRY HIS OTHER CARS " + E(SKULL)], "color": "#FF2E88", "size": 86},
    overrides=[(993.4, 998.1, "I'M SIX FOOT FIVE, YOU KNOW I'M SAYING, A HUNDRED AND EIGHTY POUNDS LEAN MUSCLE MASS"),
               (762.6, 765.35, "SO WE GOT THE LAMBO TRUCK, URUS, AKA THANOS."),
               (818.0, 822.0, "I GOT ME A BRAND NEW RAM 3500 DUALLY"),
               (1060.9, 1063.45, "STOP SLAMMING DOORS... IT'S A TRUCK, GANG"),
               (1859.8, 1860.5, ""),
               (1860.5, 1864.5, "ANGLE MAKES FANUM LOOK FAT WHEN HE IS A CHISELED MAN WITH ABS. THANK YOU.")],
    tags=lambda ot: [
        {"t": ot(996.5), "e": ot(998.1), "text": "*LEAN MUSCLE*", **R, "size": 104, "rot": 4},
        {"t": ot(764.8), "e": ot(765.35), "text": "*THANOS*", **L, "size": 112, "rot": -4},
        {"t": ot(799.6), "e": ot(800.25), "text": "*$$$*", "box": "#8B0000", **R, "size": 124, "rot": 4},
        {"t": ot(829.8), "e": ot(831.25), "text": "*CEO MODE*", **L, "size": 108, "rot": -3},
        {"t": ot(1067.5), "e": ot(1069.5), "text": "*OFFENDED*", "box": "#8B0000", **R, "size": 112, "rot": 4},
        {"t": ot(1863.0), "e": ot(1864.5), "text": "*AGREES*", **L, "size": 112, "rot": -4},
    ],
    stickers=lambda ot: [
        dict(t=ot(996.5), e=ot(998.1), emoji=E(COOL), size=170, x=540, y=BAND),
        dict(t=ot(799.6), e=ot(800.25), emoji=E(MONEYWINGS), size=170, x=540, y=BAND),
        dict(t=ot(829.8), e=ot(831.25), emoji=E(HUNDRED), size=170, x=540, y=BAND),
        dict(t=ot(1068.6), e=ot(1071.2), emoji=E(STEAM), size=170, x=540, y=BAND),
        dict(t=ot(1863.0), e=ot(1864.5), emoji=E(SKULL), size=170, x=540, y=BAND),
    ],
    sfx=lambda ot: [
        {"t": ot(996.5), "id": "rizz", "gain_db": -10},
        {"t": ot(764.8), "id": "vine_boom", "gain_db": -7},
        {"t": ot(799.6), "id": "cash_register", "gain_db": -10},
        {"t": ot(818.2), "id": "riser", "gain_db": -14, "dur": 1.5},
        {"t": ot(820.4), "id": "bass_drop", "gain_db": -12, "dur": 1.2},
        {"t": ot(829.8), "id": "airhorn", "gain_db": -15, "dur": 1.0},
        {"t": ot(1061.0), "id": "door_knock", "gain_db": -10},
        {"t": ot(1067.5), "id": "huh", "gain_db": -9},
        {"t": ot(1864.1), "id": "bruh", "gain_db": -8},
    ],
    zooms=lambda ot: [
        {"t": ot(993.4), "e": ot(996.4), "type": "push", "amt": 1.06},
        {"t": ot(764.8), "e": ot(765.3), "type": "punch", "amt": 1.16},
        {"t": ot(818.0), "e": ot(822.0), "type": "push", "amt": 1.1},
        {"t": ot(1067.5), "e": ot(1068.2), "type": "punch", "amt": 1.18},
        {"t": ot(1864.1), "e": ot(1864.5), "type": "punch", "amt": 1.16},
    ],
    flashes=lambda ot: [{"t": ot(820.4), "d": 0.12, "color": "white"}, {"t": ot(1067.5), "d": 0.12, "color": "red"}],
    insets=[{"t": 818.3, "e": 822.0, "png": "ev_truck.png", "crop": [0, 0, 1300, 700], "scale": 0.72, "x": 540, "y": BAND}])

print({k: round(val, 1) for k, val in results.items()})
