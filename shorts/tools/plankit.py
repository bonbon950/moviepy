"""Build make_short.py plans with the rulebook defaults applied automatically.

Per clip you give: keep ranges (SOURCE seconds; the first range is the cold open), header, and the
creative beats (tags, stickers, sfx, beds, zooms, flashes). The kit adds:
  - hook: header-slam bass boom + red flash + punch zoom at 0, record scratch + whoosh +
    *MOMENTS EARLIER* at the end of the cold open (if cold_open=True)
  - every detected laugh in the kept footage -> laugh tag + pink flash + laugh SFX (rule: laughs mandatory),
    positions alternating between eye level and the bottom band
  - captions (one word, speaker colors, censoring, money green) with manual overrides for misheard words
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from captions import to_captions, map_all  # noqa: E402

LAUGH_SPOTS = [dict(x=540, y=1440, size=116, rot=-4), dict(x=760, y=820, size=118, rot=5),
               dict(x=540, y=1450, size=112, rot=3), dict(x=320, y=840, size=120, rot=-5)]
LAUGH_SFX = ["sitcom_laugh", "crowd_laugh", "sitcom_laugh", "hyena_laugh"]


def out_times(t, keep):
    return [a for a, _, _ in map_all(t, keep)]


def build(S, batch, name, keep, header, *, tags=(), stickers=(), sfx=(), beds=(), zooms=(), flashes=(),
          speakers=(), overrides=(), fixes=None, laugh_label="*EVERYONE LAUGHS*", laugh_names=(),
          cold_open=True, min_laugh=0.45, skip_laughs=()):
    words = json.load(open(f"{batch}/{name}_words.json"))
    # manual caption overrides: (src_t0, src_t1, "WORDS ...") replace whatever was heard there
    for t0, t1, text in overrides:
        words = [w for w in words if not (t0 <= w["t"] < t1)]
        toks = text.split(); step = (t1 - t0) / len(toks)
        words += [{"t": t0 + i * step, "e": t0 + (i + 1) * step, "w": tok} for i, tok in enumerate(toks)]
    words.sort(key=lambda w: w["t"])

    def spk(t):
        for a, b, who in speakers:
            if a <= t < b:
                return who
        return "default"
    colors = {"default": "#FFFFFF"}
    colors.update({who: c for _, _, who, c in [(0, 0, k, v) for k, v in dict(
        (s[2], s[3]) for s in speakers if len(s) > 3).items()]})
    speakers = [(s[0], s[1], s[2]) for s in speakers]
    caps = to_captions(words, keep, speaker_of=spk, speaker_colors=colors)
    for c in caps:
        c["w"] = (fixes or {}).get(c["w"], c["w"])

    dur = sum(e - s for s, e in keep)
    tags, stickers, sfx, zooms, flashes = list(tags), list(stickers), list(sfx), list(zooms), list(flashes)
    # hook
    sfx.insert(0, {"t": 0.0, "id": "bass_boom", "gain_db": -3})
    flashes.insert(0, {"t": 0.0, "d": 0.13, "color": "red"})
    zooms.insert(0, {"t": 0.0, "e": 0.55, "type": "punch", "amt": 1.25})
    if cold_open:
        c_end = keep[0][1] - keep[0][0]
        sfx += [{"t": c_end - 0.15, "id": "record_scratch", "gain_db": -4},
                {"t": c_end, "id": "whoosh", "gain_db": -6}]
        # nothing else may share the screen with *MOMENTS EARLIER*: push colliding tags just after it
        for g in tags:
            if c_end - 0.2 <= g["t"] < c_end + 0.95:
                ln = g["e"] - g["t"]; g["t"] = round(c_end + 0.95, 3); g["e"] = round(g["t"] + ln, 3)
        tags.append({"t": c_end, "e": c_end + 0.9, "text": "*MOMENTS EARLIER*", "x": 540, "y": 770, "size": 96})
    # laughs (mandatory)
    busy = [(g["t"] - 0.3, g["e"] + 0.3) for g in tags]
    li = 0
    for line in open(f"{batch}/{name}_laughs.txt").read().splitlines():
        m = re.match(r"\s*([\d.]+)s\s+(.*)", line)
        if not m or not re.search(r"Laugh|Giggle|Chuckle|Snicker", m[2]):
            continue
        p = max(float(x) for x in re.findall(r"(?:Laughter|Giggle|Chuckle, chortle|Snicker|Belly laugh)\(([\d.]+)\)", m[2]) or [0])
        if p < min_laugh:
            continue
        for a in out_times(float(m[1]) + 0.3, keep):
            if any(x <= a <= y for x, y in busy) or any(abs(a - s) < 1.5 for s in skip_laughs):
                continue
            label = laugh_names[li % len(laugh_names)] if laugh_names else laugh_label
            def free(sp):  # no sticker/tag already in that zone at that time
                zone_bottom = sp["y"] > 1300
                for o in list(stickers) + tags:
                    if o["t"] - 0.2 < a + 1.1 and a < o["e"] + 0.2:
                        oy = o.get("y", 1450 if "emoji" in o else 1144)
                        if (oy > 1300) == zone_bottom and abs(o.get("x", 540) - sp["x"]) < 420:
                            return False
                return True
            cands = [LAUGH_SPOTS[(li + k) % len(LAUGH_SPOTS)] for k in range(len(LAUGH_SPOTS))]
            spot = next((sp for sp in cands if free(sp)), None)
            if spot is None:
                continue
            tags.append(dict({"t": a, "e": min(a + 1.1, dur), "text": label, "box": "#8B0000"}, **spot))
            flashes.append({"t": a, "d": 0.12, "color": "pink"})
            sfx.append({"t": a, "id": LAUGH_SFX[li % len(LAUGH_SFX)], "gain_db": -13, "dur": 1.1})
            busy.append((a - 1.5, a + 1.6)); li += 1
    # resolve sound ids
    def res(i):
        for d in ("sfx_lib", "beds", "beats"):
            for ext in (".mp3", ".wav"):
                f = f"{S}/{d}/{i}{ext}"
                if os.path.exists(f):
                    return f
        raise FileNotFoundError(i)
    for s in sfx:
        s["file"] = res(s.pop("id"))
    beds = [dict(b, file=res(b.pop("id"))) for b in beds]
    plan = {"source": f"{batch}/{name}_src.mp4", "keep": keep, "layout": "sandwich", "fonts_dir": f"{S}/fonts",
            "header": header, "words": caps, "tags": sorted(tags, key=lambda g: g["t"]), "stickers": list(stickers),
            "zooms": zooms, "flashes": flashes, "sfx": sorted(sfx, key=lambda s: s["t"]), "beds": beds}
    json.dump(plan, open(f"{batch}/{name}_plan.json", "w"), indent=1)
    return plan, dur
