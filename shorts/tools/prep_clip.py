"""Prepare one clip's source: concat its downloaded VOD sections, transcribe words, find laughs, frame sheet.

usage: prep_clip.py BATCH_DIR NAME
Expects BATCH_DIR/NAME_1.mp4, NAME_2.mp4 ... (in story order) and BATCH_DIR/ranges.txt.
Writes NAME_src.mp4, NAME_words.json, NAME_laughs.txt, NAME_sheet.jpg, NAME_parts.json
(parts.json = list of [src_start, src_end, vod_start] so times can be traced back to the VOD).
"""
import glob, json, os, subprocess, sys

d, name = sys.argv[1], sys.argv[2]
T = os.path.dirname(os.path.abspath(__file__))
parts = sorted(glob.glob(f"{d}/{name}_[0-9].mp4"), key=lambda p: int(p.rsplit("_", 1)[1][:-4]))
vod = {f"{r.split()[0]}_{r.split()[1]}": float(r.split()[2]) for r in open(f"{d}/ranges.txt") if r.strip()}
src = f"{d}/{name}_src.mp4"
lst = f"{d}/{name}_list.txt"
open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", src], check=True)
pm, t = [], 0.0
for p in parts:
    du = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                              capture_output=True, text=True).stdout)
    pm.append([round(t, 2), round(t + du, 2), vod[os.path.basename(p)[:-4]]]); t += du
json.dump(pm, open(f"{d}/{name}_parts.json", "w"))
subprocess.run([sys.executable, f"{T}/words.py", src, f"{d}/{name}_words.json"], check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
lg = subprocess.run([sys.executable, f"{T}/tagaudio.py", src, "1.0", "0.5", "0.25"], capture_output=True, text=True).stdout
open(f"{d}/{name}_laughs.txt", "w").write("\n".join(l for l in lg.splitlines()
    if any(k in l for k in ("Laugh", "Giggle", "Chuckle", "Snicker", "Scream", "Shout", "Yell"))))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vf",
                "fps=1,scale=240:135,drawtext=text='%{pts\\:hms}':x=2:y=2:fontsize=14:fontcolor=yellow:box=1:boxcolor=black,"
                "tile=10x12", "-frames:v", "1", f"{d}/{name}_sheet.jpg"], check=True)
print(f"{name}: {t:.1f}s from {len(parts)} parts")
