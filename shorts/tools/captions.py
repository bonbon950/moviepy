"""Turn a words.json (from words.py, SOURCE timeline) into one-word caption entries in the OUTPUT timeline.

Applies the style rules: censor curse words, money/numbers in green, keep punctuation like ?! ,
map through jump cuts (keep ranges), and clamp each word to >= 0.12 s on screen.

usage (as module): to_captions(words, keep, default_color="#FFFFFF", speaker_colors=None)
"""
import re

CENSOR = {
    "fuck": "F*CK", "fucking": "F*CKING", "fucked": "F*CKED", "motherfucker": "MOTHERF*CKER",
    "shit": "SH*T", "bitch": "B*TCH", "bitches": "B*TCHES", "nigga": "N*GGA", "niggas": "N*GGAS",
    "nigger": "N*GGA", "ass": "A*S", "damn": "DAMN", "dick": "D*CK", "pussy": "P*SSY", "hoe": "H*E",
}
MONEY = re.compile(r"^\$?\d[\d,.]*(k|m)?$|^\$", re.I)


def clean(w):
    core = re.sub(r"[^\w$'*]", "", w).lower()
    punct = "".join(c for c in w if c in "?!")
    txt = CENSOR.get(core, re.sub(r"[^\w$'*.,]", "", w).strip(".,")).upper()
    return txt + punct[:2], core


def map_time(t, keep):
    """SOURCE time -> OUTPUT time through jump cuts (first match); None if cut away."""
    r = map_all(t, keep)
    return r[0][0] if r else None


def map_all(t, keep):
    """All (out_time, range_start_out, range_end_out) for every kept range containing SOURCE time t
    (ranges may repeat footage, e.g. a cold open)."""
    out, off = [], 0.0
    for s, e in keep:
        if s <= t < e:
            out.append((off + (t - s), off, off + (e - s)))
        off += e - s
    return out


def to_captions(words, keep, default_color="#FFFFFF", speaker_of=None, speaker_colors=None,
                money_color="#39FF14"):
    out = []
    for w in words:
        txt, core = clean(w["w"])
        if not txt:
            continue
        col = default_color
        if speaker_of and speaker_colors:
            col = speaker_colors.get(speaker_of(w["t"]), default_color)
        if MONEY.match(core) or core.startswith("$"):
            col = money_color
        for a, r0, r1 in map_all(w["t"], keep):
            b = a + max(0.12, min(w["e"], w["t"] + 1.2) - w["t"])
            b = min(b, r1)                       # never spill past the end of its own section
            out.append({"t": round(a, 3), "e": round(b, 3), "w": txt, "color": col})
    out.sort(key=lambda c: c["t"])
    # no overlaps: each word ends when the next starts (if sooner)
    for i in range(len(out) - 1):
        out[i]["e"] = min(out[i]["e"], out[i + 1]["t"]) if out[i + 1]["t"] > out[i]["t"] else out[i]["e"]
    return out
