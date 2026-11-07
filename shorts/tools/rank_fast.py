"""Find hot spots in a fast_scan.py CSV (very long streams).

usage: rank_fast.py fast.csv [top=60] [spacing_s=150]
Loudness is normalized against a rolling 10-minute median, so game-volume changes don't dominate;
bright (high-frequency) loud seconds score extra (screams, yelling, hype). Prints peak times.
"""
import csv, sys
import numpy as np

rows = list(csv.DictReader(open(sys.argv[1])))
top = int(sys.argv[2]) if len(sys.argv) > 2 else 60
spacing = int(sys.argv[3]) if len(sys.argv) > 3 else 150
t = np.array([float(r["t"]) for r in rows]); order = np.argsort(t); t = t[order]
db = np.array([float(r["db"]) for r in rows])[order]
hf = np.array([float(r["hf"]) for r in rows])[order]
W = 600
med = np.array([np.median(db[max(0, i - W // 2): i + W // 2]) for i in range(0, len(db), 30)])
med = np.repeat(med, 30)[:len(db)]
med = np.maximum(med, -32.0)                      # silence (sleep/AFK) must not create fake spikes
sil = np.convolve((db < -60).astype(float), np.ones(W) / W, "same")
rel = np.where((sil < 0.3) & (db > -30), db - med, 0)
score = np.clip(rel, 0, 25) * (0.6 + 2.5 * np.clip(hf - 0.15, 0, 0.5))
sm = np.convolve(score, np.ones(6) / 6, "same")
picked = []
for i in np.argsort(-sm):
    if all(abs(t[i] - t[j]) > spacing for j in picked):
        picked.append(i)
    if len(picked) >= top:
        break
def hms(s): s = int(s); return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"
for r, i in enumerate(picked, 1):
    print(f"{r:>3} {hms(t[i])} t={int(t[i])} score={sm[i]:.1f} rel={rel[i]:+.1f}dB hf={hf[i]:.2f}")
