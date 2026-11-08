"""Batch: Kai Cenat — "Kai Cenat Plays GTA In Real Life..." (YouTube zFgVajSvLac, 19:29). Clips CLIP1..CLIP4.
Kai plays Tommy Vercetti IRL with a GTA HUD overlay (money counter top-right stays $0 all night).

usage: irl_batch.py WORKDIR [clip ...]
All times below are VOD seconds; v() converts them to SOURCE seconds of batch/<name>_src.mp4.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from plankit import build, out_times

S = sys.argv[1]; B = f"{S}/batch"
only = set(sys.argv[2:])
E = lambda *cps: "".join(chr(c) for c in cps)
SKULL, CRY, JOY, EYES, SIREN, FIRE, MONEY, MONEYFACE, SHOCK, STEAM, PLEAD, FLUSH, HUNDRED, NO, THINK, SUNG, \
    WEARY, GRIMACE = (0x1F480, 0x1F62D, 0x1F602, 0x1F440, 0x1F6A8, 0x1F525, 0x1F4B0, 0x1F911, 0x1F62E, 0x1F624,
    0x1F97A, 0x1F633, 0x1F4AF, 0x1F6AB, 0x1F914, 0x1F60E, 0x1F629, 0x1F62C)
BOT = dict(x=540, y=1450)                       # empty bottom band
L, R = dict(x=290, y=840), dict(x=790, y=840)   # eye level
OFF = {"truck": 5, "job": 360, "soda": 715, "bar": 840}
CUST = "#FFE14D"                                # customers / other people
results = {}


def run(name, keep, **kw):
    if only and name not in only:
        return
    o = OFF[name]
    v = lambda t: round(t - o, 3)
    keep = [[v(a), v(b)] for a, b in keep]
    def ot(t):                                  # VOD seconds -> OUTPUT seconds
        t = v(t)
        for d in (0, -0.06, 0.06, -0.2, 0.2):
            r = out_times(t + d, keep)
            if r:
                return round(r[-1] - d, 3)
        raise ValueError(f"{name}: {t + o} not in kept footage")
    kw = {k: (val(ot) if callable(val) else val) for k, val in kw.items()}
    kw["speakers"] = [(v(a), v(b), *rest) for a, b, *rest in kw.get("speakers", [])]
    kw["overrides"] = [(v(a), v(b), txt) for a, b, txt in kw.get("overrides", [])]
    kw["skip_laughs"] = [ot(t) for t in kw.get("skip_laughs", [])]
    plan, dur = build(S, B, name, keep, **kw)
    results[name] = dur
    print(f"{name}: {dur:.1f}s, {len(plan['words'])} words, {len(plan['tags'])} tags, {len(plan['sfx'])} sfx")


# CLIP1 — nobody wants Tommy's ice cream ... then the crowd swarms the truck --------------------------
run("truck",
    keep=[[184.0, 187.4], [9.2, 18.5], [31.5, 33.4], [43.7, 46.5], [51.0, 53.1], [158.6, 170.0],
          [178.2, 187.4], [189.9, 199.2]],
    header={"lines": ["NOBODY WANTED KAI'S", "ICE CREAM UNTIL... " + E(CRY)], "color": "#FF2E88"},
    speakers=[(193.0, 199.2, "crowd", CUST)],
    overrides=[(192.9, 194.45, "OH, ICE CREAM! OVER HERE!")],
    tags=lambda ot: [
        {"t": ot(11.4), "e": ot(11.4) + 1.4, "text": "*ICE CREAM TRUCK SPOTTED*", "x": 540, "y": 820, "size": 96, "rot": 3},
        {"t": ot(32.4), "e": ot(33.4), "text": "*TOMMY VERCETTI*", **L, "size": 112, "rot": -4},
        {"t": ot(158.8), "e": ot(158.8) + 1.6, "text": "*SINGING FOR CUSTOMERS*", **BOT, "size": 104, "rot": -3},
        {"t": ot(184.2), "e": ot(184.2) + 1.3, "text": "*REJECTED*", "box": "#8B0000", **R, "size": 132, "rot": 5},
        {"t": ot(193.0), "e": ot(193.0) + 1.6, "text": "*CROWD RUSHES IN*", **BOT, "size": 130, "rot": 3},
    ],
    stickers=lambda ot: [
        dict(t=ot(12.3), e=ot(15.2), emoji=E(EYES), size=180, **BOT),
        dict(t=ot(168.8), e=ot(170.0), emoji=E(CRY, CRY), size=190, **BOT),
        dict(t=ot(185.5), e=ot(187.4), emoji=E(SKULL, SKULL), size=180, **BOT),
        dict(t=ot(196.2), e=ot(199.2), emoji=E(FIRE, MONEYFACE), size=180, x=820, y=780),
    ],
    sfx=lambda ot: [
        {"t": 1.2, "id": "vine_boom", "gain_db": -6},
        {"t": ot(9.6), "id": "anime_wow", "gain_db": -9},
        {"t": ot(12.1), "id": "airhorn", "gain_db": -12, "dur": 1.0},
        {"t": ot(32.6), "id": "gta_wasted", "gain_db": -12, "dur": 1.4},
        {"t": ot(168.8), "id": "spongebob_fail", "gain_db": -9, "dur": 1.6},
        {"t": ot(184.2), "id": "bruh", "gain_db": -6},
        {"t": ot(186.2), "id": "sad_trombone", "gain_db": -12, "dur": 1.4},
        {"t": ot(193.0), "id": "ohhh_crowd", "gain_db": -10, "dur": 1.6},
        {"t": ot(197.7), "id": "bass_drop", "gain_db": -6},
    ],
    beds=lambda ot: [
        {"id": "sneaky_snitch", "t": ot(9.2), "e": ot(53.1), "gain_db": -21},
        {"id": "sad_violin", "t": ot(158.6), "e": ot(187.4), "gain_db": -20, "drops": [[ot(183.8), ot(184.2)]]},
        {"id": "carefree", "t": ot(189.9), "e": ot(199.2), "gain_db": -20},
    ],
    zooms=lambda ot: [
        {"t": ot(9.6), "e": ot(10.3), "type": "punch", "amt": 1.18},
        {"t": ot(43.7), "e": ot(53.1), "type": "push", "amt": 1.07},
        {"t": ot(168.8), "e": ot(169.6), "type": "punch", "amt": 1.2},
        {"t": ot(184.2), "e": ot(185.0), "type": "punch", "amt": 1.22},
        {"t": ot(193.0), "e": ot(193.7), "type": "punch", "amt": 1.2},
        {"t": ot(197.7), "e": ot(198.5), "type": "punch", "amt": 1.24},
    ],
    flashes=lambda ot: [{"t": ot(168.8), "d": 0.35, "color": "bw"}, {"t": ot(184.2), "d": 0.4, "color": "bw"},
                        {"t": ot(193.0), "d": 0.13, "color": "white"}, {"t": ot(197.7), "d": 0.13, "color": "red"}])


# CLIP2 — Tommy tries to buy the bar like a Vice City property; staff shut it down ----------------------
run("bar",
    keep=[[1003.5, 1005.9], [842.4, 846.3], [860.6, 867.7], [932.6, 939.6], [964.7, 966.9], [986.8, 990.4],
          [999.4, 1005.9], [1009.5, 1018.0], [1019.7, 1022.3], [1027.0, 1031.5]],
    header={"lines": ["KAI TRIED TO BUY A BAR", "LIKE IT'S GTA " + E(CRY)], "color": "#00E5FF"},
    speakers=[(861.5, 862.1, "friend", CUST), (863.4, 867.7, "friend", CUST), (999.4, 1002.5, "staff", CUST), (1009.4, 1010.0, "staff", CUST),
              (1019.6, 1022.3, "staff", CUST), (1026.9, 1029.9, "staff", CUST)],
    overrides=[(988.9, 990.5, "TOMMY VERCETTI LIKES DABBLING"), (964.6, 966.95, "OKAY, HE'S THE MANAGER"),
               (862.4, 862.9, "SIDE MISSION, OKAY."), (936.4, 937.2, "TRYING TO TAKE OVER MY CITY"), (1027.0, 1028.4, "THE OWNERS ARE GONE FOR THE DAY,"),
               (1012.3, 1013.0, "SERIOUS, BRO."), (1013.3, 1016.0, "I'M ON MY SIXTH BUSINESS.")],
    tags=lambda ot: [
        {"t": ot(844.4), "e": ot(846.3), "text": "*NEEDS A CAR*", **R, "size": 110, "rot": 4},
        {"t": ot(860.7), "e": ot(860.7) + 1.4, "text": "*MISSION ACCEPTED*", "box": "#8B0000", **BOT, "size": 120, "rot": -3},
        {"t": ot(936.1), "e": ot(939.6), "text": "*TAKING OVER THE CITY*", "x": 560, "y": 830, "size": 100, "rot": -4},
        {"t": ot(986.9), "e": ot(986.9) + 1.5, "text": "*SPOTS THE SLOTS*", **R, "size": 112, "rot": 5},
        {"t": ot(999.5), "e": ot(999.5) + 1.6, "text": "*SECURITY*", "box": "#8B0000", **R, "size": 136, "rot": 4},
        {"t": ot(1016.4), "e": ot(1018.0), "text": "*LISTS HIS BUSINESSES*", **BOT, "size": 108, "rot": 3},
        {"t": ot(1027.1), "e": ot(1029.9), "text": "*DENIED*", "box": "#8B0000", **L, "size": 140, "rot": -4},
    ],
    stickers=lambda ot: [
        dict(t=ot(864.5), e=ot(867.7), emoji=E(SKULL), size=190, **BOT),
        dict(t=ot(938.0), e=ot(939.6), emoji=E(MONEY, MONEY), size=180, **BOT),
        dict(t=ot(987.0), e=ot(990.4), emoji=E(MONEYFACE), size=170, **BOT),
        dict(t=ot(1004.3), e=ot(1005.9), emoji=E(SUNG), size=170, x=820, y=780),
        dict(t=ot(1029.8), e=ot(1031.5), emoji=E(CRY, CRY), size=190, **BOT),
    ],
    sfx=lambda ot: [
        {"t": 1.0, "id": "vine_boom", "gain_db": -6},
        {"t": ot(845.8), "id": "bruh", "gain_db": -8},
        {"t": ot(860.8), "id": "correct", "gain_db": -11, "dur": 1.2},
        {"t": ot(865.0), "id": "vine_boom", "gain_db": -8},
        {"t": ot(939.3), "id": "cash_register", "gain_db": -9},
        {"t": ot(987.0), "id": "money_counter", "gain_db": -12, "dur": 1.4},
        {"t": ot(999.5), "id": "dun_dun_dun", "gain_db": -11, "dur": 1.6},
        {"t": ot(1004.5), "id": "vine_boom", "gain_db": -6},
        {"t": ot(1017.9), "id": "huh", "gain_db": -9},
        {"t": ot(1027.1), "id": "wrong_buzzer", "gain_db": -10, "dur": 0.9},
        {"t": ot(1030.2), "id": "mission_failed", "gain_db": -8, "dur": 1.3},
    ],
    beds=lambda ot: [
        {"id": "mission_impossible_flute", "t": ot(842.4), "e": ot(966.9), "gain_db": -21},
        {"id": "pink_panther", "t": ot(986.8), "e": ot(990.4), "gain_db": -21},
        {"id": "jeopardy_thinking", "t": ot(999.4), "e": ot(1022.3), "gain_db": -21, "drops": [[ot(1021.9), ot(1022.3)]]},
        {"id": "curb_your_enthusiasm", "t": ot(1030.2), "e": ot(1031.5), "gain_db": -14},
    ],
    zooms=lambda ot: [
        {"t": ot(865.0), "e": ot(865.8), "type": "punch", "amt": 1.18},
        {"t": ot(932.6), "e": ot(939.6), "type": "push", "amt": 1.07},
        {"t": ot(999.5), "e": ot(1000.3), "type": "punch", "amt": 1.18},
        {"t": ot(1004.5), "e": ot(1005.3), "type": "punch", "amt": 1.22},
        {"t": ot(1009.5), "e": ot(1018.0), "type": "push", "amt": 1.07},
        {"t": ot(1027.1), "e": ot(1027.9), "type": "punch", "amt": 1.2},
    ],
    flashes=lambda ot: [{"t": ot(999.5), "d": 0.13, "color": "red"}, {"t": ot(1027.1), "d": 0.45, "color": "bw"}])


# CLIP3 — works the ice cream truck all night, GTA money stays at $0 -----------------------------------
run("job",
    keep=[[391.4, 395.4], [362.0, 366.0], [366.0, 370.6], [384.1, 386.5], [391.4, 395.4], [503.6, 506.8],
          [509.7, 514.0], [517.1, 527.3], [528.3, 538.4], [540.0, 541.2]],
    header={"lines": ["KAI WORKED A WHOLE SHIFT", "AND STILL HAS $0 " + E(CRY)], "color": "#FFE600"},
    speakers=[(363.3, 363.8, "cust", CUST), (366.9, 368.2, "cust", CUST), (521.8, 522.4, "cust", CUST),
              (523.2, 523.5, "cust", CUST), (527.1, 527.3, "cust", CUST), (531.3, 532.8, "cust", CUST)],
    overrides=[(531.8, 532.7, "YOU'RE NOT GONNA GET ICE CREAM?"), (533.0, 534.7, "I'M ON THE JOB, GIRL!"),
               (540.0, 540.8, "I'M TOMMY VERCETTI")],
    tags=lambda ot: [
        {"t": ot(362.3), "e": ot(363.4), "text": "*ON THE CLOCK*", **R, "size": 112, "rot": 4},
        {"t": ot(368.3), "e": ot(369.8), "text": "*TAKING ORDERS*", **BOT, "size": 112, "rot": -3},
        {"t": ot(391.5), "e": ot(393.0), "text": "*CHECKS HIS MONEY*", **L, "size": 114, "rot": -5},
        {"t": ot(394.7), "e": ot(395.4), "text": "*$0*", "box": "#8B0000", **R, "size": 140, "rot": 5},
        {"t": ot(520.9), "e": ot(520.9) + 1.3, "text": "*TOO BUSY FOR PICS*", **BOT, "size": 108, "rot": 3},
        {"t": ot(533.0), "e": ot(534.7), "text": "*WORKING MAN*", **L, "size": 120, "rot": -4},
        {"t": ot(540.0), "e": ot(541.2), "text": "*STILL $0*", "box": "#8B0000", **BOT, "size": 140, "rot": -3},
    ],
    stickers=lambda ot: [
        dict(t=ot(363.5), e=ot(364.8), emoji=E(SUNG), size=170, **BOT),
        dict(t=ot(392.0), e=ot(393.4), emoji=E(EYES), size=170, **BOT),
        dict(t=ot(394.9), e=ot(395.4), emoji=E(CRY, CRY), size=190, **BOT),
        dict(t=ot(510.6), e=ot(513.0), emoji=E(MONEY), size=170, x=820, y=780),
        dict(t=ot(535.0), e=ot(538.4), emoji=E(WEARY), size=180, **BOT),
    ],
    sfx=lambda ot: [
        {"t": 0.0 + 2.6, "id": "wrong_buzzer", "gain_db": -9, "dur": 0.9},
        {"t": ot(362.3), "id": "ding", "gain_db": -10, "dur": 1.0},
        {"t": ot(368.3), "id": "cash_register", "gain_db": -10},
        {"t": ot(391.5), "id": "suspense", "gain_db": -12, "dur": 1.3},
        {"t": ot(394.7), "id": "sad_trombone", "gain_db": -10, "dur": 1.2},
        {"t": ot(504.0), "id": "coins", "gain_db": -11, "dur": 1.0},
        {"t": ot(521.1), "id": "nani", "gain_db": -9},
        {"t": ot(533.0), "id": "vine_boom", "gain_db": -6},
        {"t": ot(540.0), "id": "bass_drop", "gain_db": -6},
    ],
    beds=lambda ot: [
        {"id": "fluffing_a_duck", "t": ot(362.0), "e": ot(386.5), "gain_db": -21, "drops": [[ot(386.1), ot(386.5)]]},
        {"id": "sad_violin", "t": ot(391.4), "e": ot(395.4), "gain_db": -18},
        {"id": "kahoot_lobby", "t": ot(503.6), "e": ot(538.4), "gain_db": -21},
        {"id": "curb_your_enthusiasm", "t": ot(540.0), "e": ot(541.2), "gain_db": -14},
    ],
    zooms=lambda ot: [
        {"t": ot(362.3), "e": ot(363.0), "type": "punch", "amt": 1.16},
        {"t": ot(384.1), "e": ot(386.5), "type": "push", "amt": 1.07},
        {"t": ot(394.7), "e": ot(395.4), "type": "punch", "amt": 1.24},
        {"t": ot(517.1), "e": ot(527.3), "type": "push", "amt": 1.07},
        {"t": ot(533.0), "e": ot(533.7), "type": "punch", "amt": 1.2},
        {"t": ot(540.0), "e": ot(540.8), "type": "punch", "amt": 1.24},
    ],
    flashes=lambda ot: [{"t": ot(394.7), "d": 0.4, "color": "bw"}, {"t": ot(533.0), "d": 0.13, "color": "white"},
                        {"t": ot(540.0), "d": 0.13, "color": "red"}])


# CLIP4 — fans hand Tommy a grass-flavored soda --------------------------------------------------------
run("soda",
    keep=[[768.4, 769.9], [719.5, 730.0], [735.5, 739.0], [755.0, 787.0]],
    laugh_spots=[dict(x=540, y=1440, size=116, rot=-4), dict(x=680, y=820, size=110, rot=5),
                 dict(x=540, y=1450, size=112, rot=3), dict(x=400, y=840, size=110, rot=-5)],
    header={"lines": ["KAI TRIED GRASS", "FLAVORED SODA " + E(SKULL)], "color": "#B6FF00"},
    speakers=[(763.0, 768.0, "fan", "#7FD8FF"), (770.4, 771.1, "fan", "#7FD8FF"), (773.2, 773.9, "fan", "#7FD8FF"),
              (775.3, 776.3, "fan", "#7FD8FF"), (779.0, 780.3, "fan", "#7FD8FF"), (783.6, 784.4, "fan", "#7FD8FF"),
              (786.4, 787.0, "fan", "#7FD8FF")],
    overrides=[(724.0, 730.0, "")],
    tags=lambda ot: [
        {"t": ot(735.6), "e": ot(737.2), "text": "*OPENING IT*", **R, "size": 112, "rot": 4},
        {"t": ot(761.2), "e": ot(761.2) + 1.4, "text": "*READS THE LABEL*", **L, "size": 112, "rot": -5},
        {"t": ot(771.7), "e": ot(772.6), "text": "*CONFUSED*", "box": "#8B0000", **R, "size": 130, "rot": 5},
        {"t": ot(774.9), "e": ot(776.3), "text": "*RADIOACTIVE??*", **BOT, "size": 124, "rot": -3},
        {"t": ot(786.4), "e": ot(787.0), "text": "*VERDICT: NO*", "box": "#8B0000", **L, "size": 136, "rot": -4},
    ],
    stickers=lambda ot: [
        dict(t=ot(722.0), e=ot(725.0), emoji=E(EYES), size=170, **BOT),
        dict(t=ot(761.6), e=ot(763.0), emoji=E(SKULL, SKULL, SKULL), size=170, **BOT),
        dict(t=ot(768.4), e=ot(769.9), emoji=E(GRIMACE), size=180, x=820, y=780),
        dict(t=ot(776.0), e=ot(778.5), emoji=E(SHOCK), size=180, **BOT),
        dict(t=ot(785.4), e=ot(787.0), emoji=E(SKULL, SKULL), size=190, **BOT),
    ],
    sfx=lambda ot: [
        {"t": 0.8, "id": "vine_boom", "gain_db": -6},
        {"t": ot(735.6), "id": "pop", "gain_db": -9},
        {"t": ot(761.2), "id": "dramatic_chipmunk", "gain_db": -10, "dur": 1.2},
        {"t": ot(768.6), "id": "huh", "gain_db": -9},
        {"t": ot(771.7), "id": "confused", "gain_db": -10, "dur": 1.2},
        {"t": ot(775.8), "id": "siren", "gain_db": -15, "dur": 1.2},
        {"t": ot(781.8), "id": "nani", "gain_db": -9},
        {"t": ot(786.4), "id": "bass_drop", "gain_db": -6},
    ],
    beds=lambda ot: [
        {"id": "spongebob_hawaiian", "t": ot(719.5), "e": ot(760.8), "gain_db": -21},
        {"id": "jeopardy_thinking", "t": ot(761.2), "e": ot(786.0), "gain_db": -21, "drops": [[ot(786.0), ot(786.4)]]},
    ],
    zooms=lambda ot: [
        {"t": ot(719.5), "e": ot(730.0), "type": "push", "amt": 1.07},
        {"t": ot(761.2), "e": ot(761.9), "type": "punch", "amt": 1.2},
        {"t": ot(768.4), "e": ot(769.2), "type": "punch", "amt": 1.18},
        {"t": ot(775.8), "e": ot(776.6), "type": "punch", "amt": 1.2},
        {"t": ot(786.4), "e": ot(787.0), "type": "punch", "amt": 1.24},
    ],
    flashes=lambda ot: [{"t": ot(771.7), "d": 0.4, "color": "bw"}, {"t": ot(775.8), "d": 0.13, "color": "green"},
                        {"t": ot(786.4), "d": 0.13, "color": "red"}])

print({k: round(val, 1) for k, val in results.items()})
