"""Checklist review sheet: one frame at every tag, sticker and hook moment of a rendered short.

usage: review.py PLAN.json VIDEO.mp4 OUT.jpg
"""
import json, subprocess, sys, tempfile, os
from PIL import Image, ImageDraw

plan, video, out = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
                           capture_output=True, text=True).stdout)
pts = {0.25: "hook", 1.2: "hook"}
for g in plan.get("tags", []):
    pts[round(g["t"] + 0.35, 2)] = g["text"][:18]
for s in plan.get("stickers", []):
    pts.setdefault(round(s["t"] + 0.45, 2), "sticker")
pts[round(dur - 0.4, 2)] = "end"
pts = dict(sorted((t, l) for t, l in pts.items() if t < dur))
tmp = tempfile.mkdtemp()
ims = []
for i, (t, lab) in enumerate(pts.items()):
    f = os.path.join(tmp, f"{i}.jpg")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t}", "-i", video, "-frames:v", "1", "-vf", "scale=216:384", f])
    im = Image.open(f); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 216, 14], fill="black"); d.text((3, 1), f"{t:.1f}s {lab}", fill="yellow")
    ims.append(im)
cols = 9
sheet = Image.new("RGB", (216 * cols, 384 * ((len(ims) + cols - 1) // cols)))
for i, im in enumerate(ims):
    sheet.paste(im, ((i % cols) * 216, (i // cols) * 384))
sheet.save(out)
print(f"{out}: {len(ims)} frames, video {dur:.1f}s")
