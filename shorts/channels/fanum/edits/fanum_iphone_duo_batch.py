"""Fanum Daily — iPhone Duo food race batch (Twitch VOD 2921632869, "TACO TRUCK @ THE AMP HOUSE 🌮 iPHONE DUO FOOD
CHALLENGE", Nov 2026). Editing style v2 (rulebook §15): 25–35 s, story layout, narrator lines, evidence insets,
loop ending, no copyrighted music.

usage: fanum_iphone_duo_batch.py WORKDIR [name ...]
WORKDIR holds sfx_lib/, emoji3d/, fonts/ and batch/<name>_src.mp4 (+ _words.json, _laughs.txt from prep_clip.py).
Source times below are seconds in <name>_src.mp4; VOD start of each source is in batch/ranges.txt.
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "tools"))
from plankit import build, out_times  # noqa: E402

S = sys.argv[1]; B = f"{S}/batch"
only = set(sys.argv[2:])
E = lambda *cps: "".join(chr(c) for c in cps)
SKULL, CRY, JOY, ROFL, FIRE, EYES, COLD, FRIES, BURGER, PHONE = (0x1F480, 0x1F62D, 0x1F602, 0x1F923, 0x1F525,
                                                                 0x1F440, 0x1F976, 0x1F35F, 0x1F354, 0x1F4F1)
FLAG, CAR, GLOVE, MIC, SHOCK, STEAM, MONEY, TROPHY, EXPLODE, WEARY, QUESTION, CLOWN = (
    0x1F3C1, 0x1F697, 0x1F94A, 0x1F3A4, 0x1F631, 0x1F624, 0x1F4B8, 0x1F3C6, 0x1F92F, 0x1F629, 0x2753, 0x1F921)

CAM = [0, 494, 476, 268]          # Fanum's facecam while the iPhone Duo screen fills the stream (1920x1080 source)
NOTE_Y = 440
L, C, R = dict(x=290), dict(x=540), dict(x=790)
V2 = dict(layout="story", me_pos=(540, 760),
          laugh_spots=[dict(x=300, y=800, size=108, rot=-5), dict(x=780, y=780, size=108, rot=5),
                       dict(x=540, y=740, size=110, rot=3), dict(x=780, y=820, size=108, rot=-4)])
PHONE_RUNS = {"announce": [(0, 105)], "comment": [(0, 250)], "turn": [(0, 48)],
              # code/race: on the checkout & home screens the facecam sits elsewhere (crop showed app UI) -> no cam inset
              "code": [], "race": [], "fries": []}
results = {}


def cam_insets(name, keep):
    """Reaction cam: Fanum's face, big, in the bottom band whenever the stream shows only the phone screens."""
    out, t = [], 0.0
    for a, b in keep:
        for x, y in PHONE_RUNS[name]:
            lo, hi = max(a, x), min(b, y)
            if hi - lo > 0.3:
                out.append({"t": round(t + lo - a, 3), "e": round(t + hi - a, 3), "crop": CAM, "scale": 1.95,
                            "x": 540, "y": 1640})
        t += b - a
    # merge touching spans so the cam doesn't re-pop on every jump cut
    merged = []
    for i in out:
        if merged and i["t"] - merged[-1]["e"] < 0.05:
            merged[-1]["e"] = i["e"]
        else:
            merged.append(i)
    return merged


def run(name, keep, header, notes, insets=(), **kw):
    if only and name not in only:
        return
    def ot(t):
        for d in (0, -0.06, 0.06, -0.2, 0.2):
            r = out_times(t + d, keep)
            if r:
                return round(r[-1] - d, 3)
        raise ValueError(f"{name}: {t} not in kept footage")
    kw = {k: (v(ot) if callable(v) else v) for k, v in kw.items()}
    plan, dur = build(S, B, name, keep, header, beds=[], **V2, **kw)
    plan["notes"] = [dict(n, y=NOTE_Y) for n in (notes(ot, dur) if callable(notes) else notes)]
    plan["insets"] = cam_insets(name, keep) + list(insets(ot) if callable(insets) else insets)
    plan["story_top"], plan["head_y"] = 540, 200
    json.dump(plan, open(f"{B}/{name}_plan.json", "w"), indent=1)
    results[name] = dur
    print(f"{name}: {dur:.1f}s, {len(plan['words'])} words, {len(plan['tags'])} tags, {len(plan['notes'])} notes, "
          f"{len(plan['insets'])} insets")


# CLIP1 — the ring announcer ------------------------------------------------------------------------------------
run("announce",
    keep=[[76.85, 78.9],                                   # cold open: "We want to see blood. We want to see war."
          [20.65, 22.75], [24.45, 26.6], [27.5, 29.9],     # "we are live in the first ever food competition delivery service, live on Fanum's streaming platform"
          [30.75, 32.95], [33.1, 34.7], [34.85, 37.6], [39.9, 41.1],   # red side, six foot five, 220 pounds ... DOORDASH
          [48.95, 50.05], [50.9, 52.9], [53.7, 55.7], [58.3, 61.3], [61.8, 64.1],   # green side ... UBER EATS
          [68.3, 70.05], [71.0, 72.4], [73.3, 76.0]],      # clean fight, respectable fight, no grabbing no tussling -> LOOP
    header={"lines": ["FANUM TURNED FOOD DELIVERY", "INTO A BOXING MATCH " + E(GLOVE)], "color": "#FF4D4D", "size": 88},
    overrides=[(27.5, 29.9, "LIVE ON FANUM'S STREAMING PLATFORM"), (61.8, 64.1, "WE HAVE UBER EATS!"),
               (39.9, 41.1, "DOORDASH!")],
    notes=lambda ot, dur: [
        {"t": 0.1, "e": 2.0, "text": "TONIGHT'S MAIN EVENT"},
        {"t": ot(20.65) + 0.95, "e": ot(29.9), "text": "FANUM IS THE ANNOUNCER NOW"},
        {"t": ot(30.75), "e": ot(41.1), "text": "RED CORNER: DOORDASH"},
        {"t": ot(48.95), "e": ot(64.1), "text": "GREEN CORNER: UBER EATS"},
        {"t": ot(68.3), "e": dur, "text": "THE REF HAS RULES"},
    ],
    tags=lambda ot: [
        {"t": ot(34.9), "e": ot(37.6), "text": "*220 LBS*", "box": "#8B0000", **L, "y": 780, "size": 120, "rot": -5},
        {"t": ot(58.4), "e": ot(61.3), "text": "*216 LBS*", "box": "#0B6E2A", **R, "y": 780, "size": 120, "rot": 5},
        {"t": ot(33.2), "e": ot(34.7), "text": "*HE'S NOT 6'5*", **R, "y": 820, "size": 100, "rot": 4},
        {"t": ot(73.4), "e": ot(76.0), "text": "*NO TUSSLING*", **C, "y": 760, "size": 118, "rot": -3},
    ],
    stickers=lambda ot: [
        dict(t=0.15, e=2.0, emoji=E(GLOVE, GLOVE), size=170, x=820, y=760),
        dict(t=ot(39.9), e=ot(41.1), emoji=E(FIRE), size=170, **L, y=760),
        dict(t=ot(61.8), e=ot(64.1), emoji=E(FIRE), size=170, **R, y=760),
        dict(t=ot(73.3), e=ot(76.0), emoji=E(SKULL), size=160, x=860, y=900),
    ],
    sfx=lambda ot: [
        {"t": ot(20.7), "id": "bell_ring", "gain_db": -8, "dur": 1.6},
        {"t": ot(39.9), "id": "airhorn", "gain_db": -12, "dur": 1.2},
        {"t": ot(34.9), "id": "deep_boom", "gain_db": -8},
        {"t": ot(58.4), "id": "deep_boom", "gain_db": -8},
        {"t": ot(61.9), "id": "airhorn", "gain_db": -12, "dur": 1.2},
        {"t": ot(68.4), "id": "bell_ring", "gain_db": -10, "dur": 1.2},
        {"t": ot(73.4), "id": "vine_boom", "gain_db": -7},
        {"t": ot(33.3), "id": "huh", "gain_db": -10},
    ],
    zooms=lambda ot: [
        {"t": ot(39.9), "e": ot(41.1), "type": "punch", "amt": 1.18},
        {"t": ot(61.8), "e": ot(62.6), "type": "punch", "amt": 1.18},
        {"t": ot(68.3), "e": ot(76.0), "type": "push", "amt": 1.08},
    ],
    flashes=lambda ot: [{"t": ot(39.9), "d": 0.12, "color": "red"}, {"t": ot(61.9), "d": 0.12, "color": "green"},
                        {"t": ot(73.4), "d": 0.12, "color": "white"}])

# CLIP2 — "if he makes this turn he's cooked" -> the DoorDash driver arrives -----------------------------------
JACOB = "#7CFC00"
run("turn",
    keep=[[30.4, 32.9],                                    # cold open: "Oh my god, he went straight."
          [12.5, 16.6], [16.85, 23.4],                     # "for some reason the DoorDash GPS... if he makes this turn he's cooked" x3
          [33.1, 36.4],                                    # "He said he knows where the f*ck he's going"
          [63.0, 66.0], [72.4, 74.1],                      # runs outside: "this is crazy, go go" / "there's journalism right here"
          [131.2, 133.0], [136.9, 138.4],                  # "he's coming up" / "I don't have my glasses"
          [146.1, 148.3], [151.4, 154.6], [156.5, 158.5],  # "is that food delivery?" / "Jacob, nice to meet you" / tip
          [166.7, 168.45]],                                # Jacob: "I tried to do the best job that I can" -> LOOP
    header={"lines": ["THE DRIVER IGNORED THE GPS", "AND STILL WON " + E(FLAG)], "color": "#39FF14", "size": 88},
    speakers=[(153.75, 154.6, "jacob", JACOB), (166.7, 168.45, "jacob", JACOB)],
    overrides=[(15.0, 16.6, "THE DOORDASH GPS"), (72.4, 74.1, "THERE'S JOURNALISM RIGHT HERE")],
    notes=lambda ot, dur: [
        {"t": 0.1, "e": 2.4, "text": "THE DOORDASH DRIVER"},
        {"t": ot(12.5) + 0.9, "e": ot(16.6), "text": "THE GPS SAYS TURN"},
        {"t": ot(16.85), "e": ot(23.4), "text": "IF HE TURNS, IT'S OVER"},
        {"t": ot(33.1), "e": ot(36.4), "text": "HE WENT STRAIGHT"},
        {"t": ot(63.0), "e": ot(74.1), "text": "FANUM RUNS OUTSIDE"},
        {"t": ot(131.2), "e": ot(148.3), "text": "WHO'S FIRST?"},
        {"t": ot(151.4), "e": dur, "text": "DOORDASH WINS"},
    ],
    tags=lambda ot: [
        {"t": ot(17.4), "e": ot(19.0), "text": "*HE'S COOKED*", "box": "#8B0000", **L, "y": 780, "size": 118, "rot": -5},
        {"t": ot(33.2), "e": ot(35.0), "text": "*IGNORES GPS*", **R, "y": 780, "size": 112, "rot": 5},
        {"t": ot(63.1), "e": ot(65.5), "text": "*RUNS OUTSIDE*", **C, "y": 760, "size": 120, "rot": -3},
        {"t": ot(156.6), "e": ot(158.5), "text": "*$20 TIP*", "box": "#0B6E2A", **R, "y": 800, "size": 124, "rot": 4},
    ],
    stickers=lambda ot: [
        dict(t=ot(30.5), e=ot(32.9), emoji=E(CAR, FLAG), size=170, x=820, y=760),
        dict(t=ot(22.3), e=ot(23.4), emoji=E(SKULL, SKULL), size=160, x=300, y=760),
        dict(t=ot(137.0), e=ot(138.4), emoji=E(EYES), size=170, x=820, y=780),
        dict(t=ot(156.6), e=ot(158.5), emoji=E(MONEY, MONEY), size=170, x=300, y=780),
    ],
    sfx=lambda ot: [
        {"t": ot(15.9), "id": "suspense", "gain_db": -11, "dur": 2.0},
        {"t": ot(18.2), "id": "dun_dun_dun", "gain_db": -10, "dur": 1.6},
        {"t": ot(32.4), "id": "dramatic_hit", "gain_db": -7},
        {"t": ot(63.1), "id": "whoosh", "gain_db": -8},
        {"t": ot(72.5), "id": "anime_wow", "gain_db": -11, "dur": 1.2},
        {"t": ot(137.4), "id": "bruh", "gain_db": -9},
        {"t": ot(146.2), "id": "door_knock", "gain_db": -10},
        {"t": ot(156.6), "id": "cash_register", "gain_db": -9},
        {"t": ot(166.8), "id": "heavenly", "gain_db": -13, "dur": 1.6},
    ],
    zooms=lambda ot: [
        {"t": ot(16.85), "e": ot(23.4), "type": "push", "amt": 1.10},
        {"t": ot(33.1), "e": ot(33.8), "type": "punch", "amt": 1.2},
        {"t": ot(156.6), "e": ot(157.3), "type": "punch", "amt": 1.18},
    ],
    flashes=lambda ot: [{"t": ot(33.1), "d": 0.12, "color": "white"}, {"t": ot(156.6), "d": 0.12, "color": "green"}])

# CLIP3 — Fanum the delivery commentator ----------------------------------------------------------------------
run("comment",
    keep=[[222.5, 226.9],                                  # cold open: "Do you think he's taking a sip out of my medium coke?"
          [0.0, 2.65], [4.7, 6.4], [7.8, 12.95],           # "Jose approaching the McDonald's... team Uber Eats... team DoorDash in a bit of a blunder"
          [14.1, 17.6], [48.3, 51.45],                     # "some sort of argument" / "ask for an update? nah let them work"
          [90.0, 93.45], [97.3, 101.1],                    # "he went to the side, what's going on" / "they grabbed him from his car, popped his trunk"
          [163.3, 166.65], [217.9, 221.45]],               # "about to go cook that himself" / "Jose might be in a scuffle... Jacob got the food, he ain't moving" -> LOOP
    header={"lines": ["FANUM IS THE BEST DELIVERY", "COMMENTATOR ALIVE " + E(MIC)], "color": "#00E5FF", "size": 88},
    overrides=[(163.3, 166.65, "HE MIGHT GO IN THE BACK AND COOK IT HIMSELF"), (7.8, 12.95,
               "IT SEEMS LIKE TEAM DOORDASH IS IN A BIT OF A BLUNDER, STUCK AT THE RESTAURANT")],
    notes=lambda ot, dur: [
        {"t": 0.1, "e": 4.3, "text": "HIS ONLY CONCERN:"},
        {"t": ot(0.0) + 0.9, "e": ot(6.4), "text": "LIVE: DOORDASH VS UBER EATS"},
        {"t": ot(7.8), "e": ot(17.6), "text": "DOORDASH IS STUCK"},
        {"t": ot(48.3), "e": ot(51.45), "text": "CHAT WANTS AN UPDATE"},
        {"t": ot(90.0), "e": ot(101.1), "text": "SOMETHING'S WRONG AT McDONALD'S"},
        {"t": ot(163.3), "e": dur, "text": "JACOB HAS THE FOOD..."},
    ],
    tags=lambda ot: [
        {"t": ot(8.4), "e": ot(10.4), "text": "*BLUNDER*", "box": "#8B0000", **L, "y": 780, "size": 120, "rot": -5},
        {"t": ot(49.8), "e": ot(51.4), "text": "*LET THEM WORK*", **R, "y": 780, "size": 108, "rot": 4},
        {"t": ot(100.0), "e": ot(101.1), "text": "*TRUNK POPPED*", **C, "y": 760, "size": 118, "rot": -3},
        {"t": ot(218.4), "e": ot(219.6), "text": "*SCUFFLE?!*", "box": "#8B0000", **R, "y": 800, "size": 124, "rot": 5},
    ],
    stickers=lambda ot: [
        dict(t=0.2, e=4.3, emoji=E(EYES, BURGER), size=170, x=820, y=760),
        dict(t=ot(90.0), e=ot(93.45), emoji=E(QUESTION, QUESTION), size=160, x=300, y=760),
        dict(t=ot(164.0), e=ot(166.65), emoji=E(SKULL), size=170, x=820, y=780),
    ],
    sfx=lambda ot: [
        {"t": ot(0.1), "id": "music_sting", "gain_db": -14, "dur": 1.5},
        {"t": ot(8.4), "id": "sad_trombone", "gain_db": -13, "dur": 1.6},
        {"t": ot(49.8), "id": "huh", "gain_db": -10},
        {"t": ot(91.2), "id": "suspense", "gain_db": -12, "dur": 1.8},
        {"t": ot(100.2), "id": "vine_boom", "gain_db": -7},
        {"t": ot(164.0), "id": "bruh", "gain_db": -10},
        {"t": ot(218.4), "id": "dramatic_hit", "gain_db": -8},
    ],
    zooms=lambda ot: [
        {"t": ot(0.0), "e": ot(6.4), "type": "push", "amt": 1.06},
        {"t": ot(100.2), "e": ot(100.9), "type": "punch", "amt": 1.18},
        {"t": ot(218.4), "e": ot(219.1), "type": "punch", "amt": 1.18},
    ],
    flashes=lambda ot: [{"t": ot(100.2), "d": 0.12, "color": "white"}, {"t": ot(218.4), "d": 0.12, "color": "red"}])

# CLIP4 — Agent gets Fanum's leftovers, cold -----------------------------------------------------------------
run("fries",
    keep=[[65.2, 68.3],                                    # cold open: "Fanum gives Agent cold fries"
          [3.3, 8.6], [9.4, 10.3],                         # "It's cold though... it's really cold." "Fanum tax returns"
          [12.9, 14.3], [16.4, 17.9], [18.1, 19.8],        # "one Big Mac, one fry, one coke" / "I don't eat the fries"
          [40.0, 48.4],                                    # "he never got taxed... it's not a return, he never even submitted one"
          [69.9, 74.0], [82.3, 86.4]],                     # "I can't make this up" / "we should've ate this ourselves" -> LOOP
    header={"lines": ["AGENT GOT FANUM'S", "LEFTOVERS... COLD " + E(COLD)], "color": "#7DF9FF", "size": 88},
    overrides=[(65.2, 68.3, "FANUM GIVES AGENT COLD FRIES"), (9.4, 10.3, "FANUM TAX RETURNS"),
               (40.0, 43.4, "HE NEVER GOT TAXED"), (12.9, 14.3, "THEY SAY ONE BIG MAC"),
               (69.9, 71.5, "OH MY GOD, BRO")],
    notes=lambda ot, dur: [
        {"t": 0.1, "e": 3.0, "text": "FANUM ORDERED TWO MEALS"},
        {"t": ot(3.3) + 0.9, "e": ot(10.3), "text": "AGENT GOT THE SECOND ONE"},
        {"t": ot(12.9), "e": ot(19.8), "text": "HOURS LATER..."},
        {"t": ot(40.0), "e": ot(48.4), "text": "CHAT: \"FANUM TAX RETURN\""},
        {"t": ot(69.9), "e": dur, "text": "AGENT HAS SEEN ENOUGH"},
    ],
    tags=lambda ot: [
        {"t": ot(4.0), "e": ot(5.4), "text": "*COLD*", "box": "#1E5AA8", **R, "y": 780, "size": 130, "rot": 5},
        {"t": ot(18.4), "e": ot(19.8), "text": "*DOESN'T EAT FRIES*", **L, "y": 800, "size": 100, "rot": -4},
        {"t": ot(46.3), "e": ot(48.4), "text": "*NEVER FILED*", "box": "#8B0000", **R, "y": 780, "size": 116, "rot": 4},
    ],
    stickers=lambda ot: [
        dict(t=0.15, e=3.0, emoji=E(FRIES, COLD), size=180, x=540, y=1640),
        dict(t=ot(13.0), e=ot(17.9), emoji=E(BURGER, FRIES), size=170, x=540, y=1640),
        dict(t=ot(40.2), e=ot(44.0), emoji=E(MONEY), size=170, x=540, y=1640),
        dict(t=ot(70.0), e=ot(74.0), emoji=E(SKULL, SKULL, SKULL), size=170, x=540, y=1640),
        dict(t=ot(82.4), e=ot(86.4), emoji=E(CRY, CRY), size=170, x=540, y=1640),
    ],
    sfx=lambda ot: [
        {"t": ot(4.0), "id": "squeak", "gain_db": -12},
        {"t": ot(9.4), "id": "cash_register", "gain_db": -10},
        {"t": ot(18.4), "id": "huh", "gain_db": -10},
        {"t": ot(46.3), "id": "wrong_buzzer", "gain_db": -11, "dur": 0.9},
        {"t": ot(70.0), "id": "sitcom_laugh", "gain_db": -13, "dur": 1.6},
        {"t": ot(82.4), "id": "sad_violin", "gain_db": -16, "dur": 3.8},
    ],
    zooms=lambda ot: [
        {"t": ot(3.3), "e": ot(8.6), "type": "push", "amt": 1.08},
        {"t": ot(9.4), "e": ot(10.1), "type": "punch", "amt": 1.2},
        {"t": ot(46.3), "e": ot(47.0), "type": "punch", "amt": 1.18},
    ],
    flashes=lambda ot: [{"t": ot(9.4), "d": 0.12, "color": "green"}, {"t": ot(70.0), "d": 0.12, "color": "pink"}])

# CLIP5 — the borrowed iPhone Duo wants a code ---------------------------------------------------------------
run("code",
    keep=[[245.1, 247.35],                                 # cold open: "His phone is dead. Damn son."
          [44.0, 47.3],                                    # countdown "...one"
          [64.0, 66.8], [79.0, 82.3],                      # "Yo, I need that code" / "there's a code for DoorDash"
          [131.9, 136.6],                                  # "where is Poji?" + voicemail "please leave your..."
          [155.3, 159.3], [182.3, 184.0],                  # "he's not picking up at all" / "why is he on DND?"
          [220.2, 224.4],                                  # "and go on the joyride with the Maybach. I'm dead"
          [227.6, 230.0], [235.0, 236.6],                  # "you can't give me that code?" / "three minutes behind for DoorDash"
          [271.7, 274.2], [277.4, 279.6]],                 # "should I cancel the orders, try again?" / "it's not fair" -> LOOP
    header={"lines": ["HE BORROWED AN IPHONE DUO...", "BIG MISTAKE " + E(PHONE)], "color": "#FFD60A", "size": 88},
    overrides=[(44.0, 46.95, ""), (64.0, 66.8, "YO, I NEED THAT CODE"),   # countdown was misheard as "money money" (79.0, 82.3, "THERE'S A CODE FOR DOORDASH"),
               (131.9, 136.6, "WHERE IS POJI? PLEASE LEAVE YOUR MESSAGE"), (182.3, 184.0, "WHY IS HE ON DND, BRO?"),
               (227.6, 230.0, "YOU CAN'T GIVE ME THAT CODE?"), (235.0, 236.6, "THREE MINUTES BEHIND FOR DOORDASH"),
               (271.7, 274.2, "SHOULD I CANCEL THE ORDERS, TRY AGAIN?"), (220.2, 222.0, "AND GO ON THE JOYRIDE")],
    notes=lambda ot, dur: [
        {"t": 0.1, "e": 2.2, "text": "THE PHONE ISN'T EVEN HIS"},
        {"t": ot(44.0) + 0.9, "e": ot(47.3), "text": "BOTH ORDERS AT ONCE..."},
        {"t": ot(64.0), "e": ot(82.3), "text": "DOORDASH WANTS A CODE"},
        {"t": ot(131.9), "e": ot(136.6), "text": "THE CODE GOES TO POJI"},
        {"t": ot(155.3), "e": ot(184.0), "text": "POJI ISN'T ANSWERING"},
        {"t": ot(220.2), "e": ot(224.4), "text": "POJI TOOK THE MAYBACH"},
        {"t": ot(227.6), "e": ot(236.6), "text": "DOORDASH: 3 MIN BEHIND"},
        {"t": ot(271.7), "e": dur, "text": "START OVER?"},
    ],
    tags=lambda ot: [
        {"t": ot(45.5), "e": ot(47.3), "text": "*ORDERS PLACED*", **C, "y": 760, "size": 112, "rot": -3},
        {"t": ot(64.9), "e": ot(66.8), "text": "*NEEDS THE CODE*", "box": "#8B0000", **L, "y": 780, "size": 112, "rot": -5},
        {"t": ot(135.4), "e": ot(136.6), "text": "*VOICEMAIL*", **R, "y": 800, "size": 120, "rot": 4},
        {"t": ot(182.4), "e": ot(184.0), "text": "*DO NOT DISTURB*", "box": "#8B0000", **C, "y": 760, "size": 110, "rot": 3},
        {"t": ot(277.5), "e": ot(279.6), "text": "*NOT FAIR*", **R, "y": 780, "size": 124, "rot": 5},
    ],
    stickers=lambda ot: [
        dict(t=0.15, e=2.2, emoji=E(PHONE, SKULL), size=170, x=820, y=760),
        dict(t=ot(155.5), e=ot(159.3), emoji=E(WEARY), size=170, x=820, y=780),
        dict(t=ot(220.3), e=ot(224.4), emoji=E(CAR, SKULL), size=170, x=300, y=780),
    ],
    sfx=lambda ot: [
        {"t": ot(46.6), "id": "ding", "gain_db": -10},
        {"t": ot(64.2), "id": "wrong_buzzer", "gain_db": -11, "dur": 0.9},
        {"t": ot(132.0), "id": "phone_ring", "gain_db": -14, "dur": 1.8},
        {"t": ot(135.4), "id": "voicemail_beep", "gain_db": -12},
        {"t": ot(182.4), "id": "bruh", "gain_db": -10},
        {"t": ot(222.0), "id": "vine_boom", "gain_db": -7},
        {"t": ot(235.1), "id": "suspense", "gain_db": -12, "dur": 1.5},
        {"t": ot(277.5), "id": "sad_trombone", "gain_db": -12, "dur": 2.0},
    ],
    zooms=lambda ot: [
        {"t": ot(64.0), "e": ot(64.7), "type": "punch", "amt": 1.18},
        {"t": ot(155.3), "e": ot(159.3), "type": "push", "amt": 1.08},
        {"t": ot(222.0), "e": ot(222.7), "type": "punch", "amt": 1.2},
    ],
    flashes=lambda ot: [{"t": ot(64.2), "d": 0.12, "color": "red"}, {"t": ot(222.0), "d": 0.12, "color": "white"},
                        {"t": ot(277.5), "d": 0.3, "color": "bw"}])

# CLIP6 — the full experiment: same order, same time, who's faster? -----------------------------------------
run("race",
    keep=[[109.6, 111.55],                                 # cold open: "This is amazing, I've never seen nothing like it"
          [8.2, 10.95],                                    # "today we got an iPhone Duo challenge"
          [48.3, 51.75],                                   # "this is not my iPhone Duo, I borrowed it from somebody else"
          [65.4, 69.35], [70.3, 76.9],                     # "Uber Eats... DoorDash... same place... who gets to the AMP house faster"
          [105.7, 109.35],                                 # "now we get to scroll on both apps at the same time"
          [135.4, 136.3], [137.8, 138.5], [139.8, 140.8],  # "three... two... wait, hold on"
          [163.8, 168.75], [171.6, 176.2]],                # verdict: DoorDash faster; "late start by a minute, got here a minute earlier" -> LOOP
    header={"lines": ["DOORDASH IS FASTER THAN", "UBER EATS. PROVEN " + E(FLAG)], "color": "#FF8C00", "size": 88},
    overrides=[(48.3, 51.75, "THIS IS NOT MY IPHONE DUO, I BORROWED IT FROM SOMEBODY ELSE"),
               (65.4, 69.35, "WE'RE GONNA GO UBER EATS, WE'RE GONNA GO DOORDASH"),
               (70.3, 76.9, "WE'RE GONNA ORDER FOOD FROM THE SAME PLACE AND SEE WHO GETS TO THE AMP HOUSE FASTER")],
    notes=lambda ot, dur: [
        {"t": 0.1, "e": 1.9, "text": "TWO APPS. ONE PHONE."},
        {"t": ot(8.2) + 0.9, "e": ot(10.95), "text": "THE IPHONE DUO CHALLENGE"},
        {"t": ot(48.3), "e": ot(51.75), "text": "IT'S NOT EVEN HIS"},
        {"t": ot(65.4), "e": ot(76.9), "text": "SAME ORDER. SAME TIME."},
        {"t": ot(105.7), "e": ot(140.8), "text": "WHO DELIVERS FIRST?"},
        {"t": ot(163.8), "e": dur, "text": "THE RESULTS ARE IN"},
    ],
    tags=lambda ot: [
        {"t": ot(48.4), "e": ot(51.0), "text": "*BORROWED*", "box": "#8B0000", **R, "y": 780, "size": 120, "rot": 5},
        {"t": ot(139.9), "e": ot(140.8), "text": "*WAIT*", **C, "y": 760, "size": 130, "rot": -4},
        {"t": ot(165.6), "e": ot(168.75), "text": "*DOORDASH WINS*", "box": "#0B6E2A", **L, "y": 780, "size": 116, "rot": -4},
    ],
    stickers=lambda ot: [
        dict(t=0.15, e=1.9, emoji=E(PHONE, PHONE), size=170, x=820, y=760),
        dict(t=ot(70.4), e=ot(76.9), emoji=E(BURGER), size=170, x=540, y=1640),
        dict(t=ot(165.7), e=ot(168.75), emoji=E(TROPHY), size=170, x=820, y=780),
    ],
    sfx=lambda ot: [
        {"t": ot(8.3), "id": "ding", "gain_db": -10},
        {"t": ot(48.4), "id": "huh", "gain_db": -10},
        {"t": ot(65.5), "id": "swoosh", "gain_db": -11},
        {"t": ot(135.4), "id": "blip1", "gain_db": -10},
        {"t": ot(137.8), "id": "blip1", "gain_db": -10},
        {"t": ot(139.9), "id": "record_scratch", "gain_db": -9},
        {"t": ot(165.6), "id": "correct", "gain_db": -9},
        {"t": ot(171.7), "id": "crowd_laugh", "gain_db": -16, "dur": 1.4},
    ],
    zooms=lambda ot: [
        {"t": ot(65.4), "e": ot(76.9), "type": "push", "amt": 1.08},
        {"t": ot(139.8), "e": ot(140.5), "type": "punch", "amt": 1.2},
        {"t": ot(165.6), "e": ot(166.3), "type": "punch", "amt": 1.18},
    ],
    flashes=lambda ot: [{"t": ot(139.9), "d": 0.12, "color": "white"}, {"t": ot(165.6), "d": 0.12, "color": "green"}])

print(results)
