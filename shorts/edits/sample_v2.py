"""SAMPLE of the proposed v2 style ("original story cut"), for Bjorn to approve before the rulebook changes.
Same moment as CLIP3 (Nov 8, "$0 shift"), recut: ~27 s, story layout, narrator commentary, evidence inset,
loop ending, no copyrighted music.

usage: sample_v2.py WORKDIR      (times below are VOD seconds of YouTube zFgVajSvLac; job_src starts at 360)
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from plankit import build, out_times

S = sys.argv[1]; B = f"{S}/batch"; O = 360
v = lambda t: round(t - O, 3)
E = lambda *cps: "".join(chr(c) for c in cps)
MONEY, SKULL, STEAM, CRY = 0x1F4B0, 0x1F480, 0x1F624, 0x1F62D
CUST = "#FFE14D"
HUD_0 = [1703, 57, 100, 60]                    # the "$0" money counter in the GTA HUD (1920x1080 source)

# story order: hook (the payoff line) -> rewind -> the "job" -> checks the money ... loops back to the hook
keep_vod = [[391.4, 395.4],                    # hook: "my money should be going up... I still got zero dollars"
            [362.0, 366.0], [366.0, 369.8],    # on the job / takes an order
            [503.6, 506.8],                    # making sales
            [520.8, 523.6],                    # "wait, I'm on the clock" (no pics)
            [531.3, 535.4], [540.0, 541.2],    # "I'm on the job, girl!" / "I'm Tommy Vercetti"
            [384.1, 388.15]]                   # "I'm gonna enter it right now... my money should be going up" -> LOOP
keep = [[v(a), v(b)] for a, b in keep_vod]


def ot(t):
    t = v(t)
    for d in (0, -0.06, 0.06, -0.2, 0.2):
        r = out_times(t + d, keep)
        if r:
            return round(r[-1] - d, 3)
    raise ValueError(t + O)


dur = sum(b - a for a, b in keep)
NOTE_Y = 440
plan, _ = build(
    S, B, "job", keep,
    header={"lines": ["GTA MONEY DOESN'T WORK", "IN REAL LIFE " + E(SKULL)], "color": "#00E5FF", "size": 88},
    layout="story", me_pos=(540, 760),
    laugh_spots=[dict(x=300, y=800, size=108, rot=-5), dict(x=780, y=780, size=108, rot=5),
                 dict(x=540, y=740, size=110, rot=3), dict(x=780, y=820, size=108, rot=-4)],   # eye level only
    speakers=[(v(363.3), v(363.8), "cust", CUST), (v(366.9), v(368.2), "cust", CUST), (v(521.8), v(522.4), "cust", CUST),
              (v(523.2), v(523.5), "cust", CUST), (v(531.3), v(532.8), "cust", CUST)],
    overrides=[(v(531.8), v(532.7), "YOU'RE NOT GONNA GET ICE CREAM?"), (v(533.0), v(534.7), "I'M ON THE JOB, GIRL!"),
               (v(540.0), v(540.8), "I'M TOMMY VERCETTI")],
    tags=[
        {"t": ot(394.7), "e": ot(395.4), "text": "*$0*", "box": "#8B0000", "x": 800, "y": 760, "size": 130, "rot": 5},
        {"t": ot(386.6), "e": ot(388.15), "text": "*CHECKS THE MONEY*", "x": 320, "y": 800, "size": 104, "rot": -4},
    ],
    stickers=[
        dict(t=ot(504.0), e=ot(506.8), emoji=E(MONEY, MONEY), size=170, x=540, y=1640),
        dict(t=ot(533.0), e=ot(535.4), emoji=E(STEAM), size=170, x=820, y=780),
        dict(t=ot(394.9), e=ot(395.4), emoji=E(CRY, CRY), size=170, x=540, y=1830),
    ],
    sfx=[
        {"t": ot(394.7), "id": "wrong_buzzer", "gain_db": -9, "dur": 0.9},
        {"t": ot(362.3), "id": "ding", "gain_db": -10, "dur": 1.0},
        {"t": ot(368.3), "id": "cash_register", "gain_db": -10},
        {"t": ot(504.0), "id": "coins", "gain_db": -11, "dur": 1.0},
        {"t": ot(521.1), "id": "nani", "gain_db": -9},
        {"t": ot(533.0), "id": "vine_boom", "gain_db": -6},
        {"t": ot(540.0), "id": "money_counter", "gain_db": -12, "dur": 1.2},
        {"t": ot(386.6), "id": "suspense", "gain_db": -11, "dur": 1.6},
    ],
    beds=[],                                   # v2: no copyrighted music
    zooms=[
        {"t": ot(394.7), "e": ot(395.4), "type": "punch", "amt": 1.22},
        {"t": ot(362.0), "e": ot(369.8), "type": "push", "amt": 1.06},
        {"t": ot(533.0), "e": ot(533.7), "type": "punch", "amt": 1.18},
        {"t": ot(384.1), "e": ot(388.15), "type": "push", "amt": 1.14},   # tension builds into the loop
    ],
    flashes=[{"t": ot(394.7), "d": 0.35, "color": "bw"}, {"t": ot(533.0), "d": 0.12, "color": "white"}],
)

# v2 additions: narrator commentary (our own story voice) + evidence insets
plan["notes"] = [
    {"t": 0.1, "e": ot(393.4), "text": "HE WORKED ALL NIGHT FOR THIS", "y": NOTE_Y},
    {"t": ot(362.0) + 0.9, "e": ot(366.0), "text": "TOMMY VERCETTI GOT A REAL JOB", "y": NOTE_Y},
    {"t": ot(366.0), "e": ot(369.8), "text": "GTA RULE: EVERY SALE = MONEY", "y": NOTE_Y},
    {"t": ot(503.6), "e": ot(506.8), "text": "SALE AFTER SALE...", "y": NOTE_Y},
    {"t": ot(520.8), "e": ot(523.6), "text": "NO PICS. HE'S ON THE CLOCK", "y": NOTE_Y},
    {"t": ot(531.3), "e": ot(541.2), "text": "EMPLOYEE OF THE MONTH", "y": NOTE_Y},
    {"t": ot(384.1), "e": dur, "text": "MOMENT OF TRUTH...", "y": NOTE_Y},
]
plan["insets"] = [
    {"t": ot(393.4), "e": ot(395.4), "crop": HUD_0, "scale": 4.0, "x": 540, "y": 1620},   # proof: the HUD says $0
]
plan["story_top"], plan["head_y"] = 540, 200
json.dump(plan, open(f"{B}/job_v2_plan.json", "w"), indent=1)
print(f"sample: {dur:.1f}s, {len(plan['words'])} words, {len(plan['notes'])} narrator lines")
