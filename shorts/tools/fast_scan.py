"""Fast loudness pass over a very long Twitch VOD without storing its audio.

usage: fast_scan.py AUDIO_PLAYLIST_URL OUT.csv [workers=8]
Fetches every 10 s audio segment, decodes to 8 kHz mono, writes per-second:
  t, db (RMS loudness), hf (share of energy above ~1.5 kHz: screams/yells are bright), peak
"""
import csv, re, subprocess, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
import numpy as np

url, out = sys.argv[1], sys.argv[2]
workers = int(sys.argv[3]) if len(sys.argv) > 3 else 8
base = url.rsplit("/", 1)[0] + "/"
pl = urllib.request.urlopen(url, timeout=60).read().decode()
segs, t, d = [], 0.0, None
for line in pl.splitlines():
    m = re.match(r"#EXTINF:([\d.]+)", line)
    if m:
        d = float(m.group(1))
    elif line and not line.startswith("#"):
        segs.append((t, d, line)); t += d
SR = 8000


def work(item):
    t0, du, name = item
    for _ in range(4):
        try:
            data = urllib.request.urlopen(base + name, timeout=60).read()
            break
        except Exception:
            data = None
    if not data:
        return t0, []
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", "pipe:0", "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                         input=data, capture_output=True).stdout
    a = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    rows = []
    for k in range(int(len(a) // SR)):
        x = a[k * SR:(k + 1) * SR]
        rms = np.sqrt(np.mean(x ** 2)) + 1e-9
        spec = np.abs(np.fft.rfft(x)) ** 2
        hf = spec[int(1500 * len(spec) / (SR / 2)):].sum() / (spec.sum() + 1e-12)
        rows.append((round(t0 + k, 1), round(20 * np.log10(rms), 2), round(float(hf), 4),
                     round(float(np.abs(x).max()), 3)))
    return t0, rows


with open(out, "w", newline="") as f, ThreadPoolExecutor(workers) as ex:
    w = csv.writer(f); w.writerow(["t", "db", "hf", "peak"])
    for i, (t0, rows) in enumerate(ex.map(work, segs)):
        w.writerows(rows)
        if i % 500 == 0:
            f.flush(); print(f"{i}/{len(segs)} segments", flush=True)
print("done")
