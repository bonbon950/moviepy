"""Download high-res glossy 3D emoji (Microsoft Fluent Emoji 3D, MIT license, 256x256 PNG).

usage: fetch_emoji.py OUT_DIR
Saves <codepoint>.png (e.g. 1f480.png for 💀) — the renderer looks emoji up by codepoint.
"""
import os, sys, urllib.parse, urllib.request

BASE = "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/"
# codepoint -> Fluent asset folder name (no skin-tone variants)
EMOJI = {
    "1f62d": "Loudly crying face", "1f480": "Skull", "1f602": "Face with tears of joy",
    "1f923": "Rolling on the floor laughing", "1f525": "Fire", "1f633": "Flushed face",
    "1f92f": "Exploding head", "1f4b0": "Money bag", "1f4b8": "Money with wings", "1f911": "Money-mouth face",
    "1f631": "Face screaming in fear", "1f440": "Eyes", "2757": "Red exclamation mark",
    "2753": "Red question mark", "1f6a8": "Police car light", "1f60e": "Smiling face with sunglasses",
    "1f97a": "Pleading face", "1f62e": "Face with open mouth", "1f92c": "Face with symbols on mouth",
    "1f47b": "Ghost", "1f383": "Jack-o-lantern", "1f624": "Face with steam from nose",
    "1f62c": "Grimacing face", "1fae1": "Saluting face", "1f928": "Face with raised eyebrow",
    "1f610": "Neutral face", "1f494": "Broken heart", "1f921": "Clown face", "1f644": "Face with rolling eyes",
    "1f629": "Weary face", "1f976": "Cold face", "1f608": "Smiling face with horns", "1f451": "Crown",
    "1f410": "Goat", "1f4af": "Hundred points", "26a0": "Warning", "1f9e2": "Billed cap",
    "1f5e3": "Speaking head", "1f62b": "Tired face", "1f972": "Smiling face with tear",
    "1f635": "Knocked-out face", "1f92b": "Shushing face", "1f914": "Thinking face",
    "1f913": "Nerd face", "1f979": "Face holding back tears", "1f60f": "Smirking face",
    "1f480_": "Skull", "1f43a": "Wolf", "1f9db": "Person vampire", "1f485": "Nail polish",
    "1f494_": "Broken heart", "1f3c6": "Trophy", "1f4f8": "Camera with flash", "1f3a4": "Microphone",
    "1f923_": "Rolling on the floor laughing", "1f62f": "Hushed face", "1fae2": "Face with open eyes and hand over mouth",
    "1fae3": "Face with peeking eye", "1f9cd": "Person standing", "1f6ab": "Prohibited",
    "1f94a": "Boxing glove", "1f35f": "French fries", "1f354": "Hamburger", "1f4f1": "Mobile phone",
    "1f3c1": "Chequered flag", "1f697": "Automobile", "1f37a": "Beer mug", "1f6f5": "Motor scooter",
    "2615": "Hot beverage", "1f32f": "Burrito", "1f45f": "Running shoe", "1f64f": "Folded hands",
    "1f620": "Angry face",
}
SKIN = {"1f485", "1f9db", "1f9cd", "1f64f"}  # these live under Default/3D

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
ok = fail = 0
for cp, name in EMOJI.items():
    cp = cp.rstrip("_")
    dst = os.path.join(out, cp + ".png")
    if os.path.exists(dst) and os.path.getsize(dst) > 5000:
        ok += 1; continue
    paths = []
    for fn in (name.lower().replace(" ", "_").replace("-", "_"), name.lower().replace(" ", "_")):
        paths += [f"{name}/3D/{fn}_3d.png", f"{name}/Default/3D/{fn}_3d_default.png"]
    if cp in SKIN:
        paths.reverse()
    for p in paths:
        try:
            data = urllib.request.urlopen(BASE + urllib.parse.quote(p), timeout=30).read()
            if data[:4] == b"\x89PNG":
                open(dst, "wb").write(data); ok += 1; break
        except Exception:
            continue
    else:
        print("FAIL", cp, name); fail += 1
print(f"{ok} ok, {fail} failed -> {out}")
