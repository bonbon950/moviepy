"""Rank the most clip-worthy moments from scan_vod.py output.

usage: rank_moments.py scan.csv [top=12]
Score/second = 3*laugh + 2*scream + 1*crowd + loudness bonus, minus a penalty when music dominates
(music-only stretches are not content). Smoothed over 8 s; peaks picked with 60 s spacing.
"""
import csv, sys
import numpy as np

rows = list(csv.DictReader(open(sys.argv[1])))
top = int(sys.argv[2]) if len(sys.argv) > 2 else 12
t = np.array([int(r["t"]) for r in rows])
f = {k: np.array([float(r[k]) for r in rows]) for k in ("loud_db", "laugh", "scream", "crowd", "music")}
loud = f["loud_db"]
lz = (loud - np.median(loud)) / (np.std(loud) + 1e-6)
score = 3 * f["laugh"] + 2 * f["scream"] + 1 * f["crowd"] + 0.4 * np.clip(lz, 0, 3) - 1.5 * np.clip(f["music"] - 0.6, 0, 1)
k = np.ones(8) / 8
sm = np.convolve(score, k, "same")
order = np.argsort(-sm)
picked = []
for i in order:
    if all(abs(i - j) > 60 for j in picked):
        picked.append(i)
    if len(picked) >= top:
        break
def hms(s): return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"
print("rank  peak      score  laugh_s scream_s crowd  window(-30s..+25s)")
for r, i in enumerate(picked, 1):
    a, b = max(0, i - 30), min(len(t) - 1, i + 25)
    print(f"{r:>3}  {hms(int(t[i]))}  {sm[i]:5.2f}   {int((f['laugh'][a:b] > 0.3).sum()):>4}   "
          f"{int((f['scream'][a:b] > 0.3).sum()):>4}    {f['crowd'][a:b].mean():.2f}   {hms(a)}-{hms(b)}")
