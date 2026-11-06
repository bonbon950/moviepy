"""Find occurrences of each SFX (from the SFX pack) inside each video via normalized cross-correlation."""
import subprocess, numpy as np, glob, os
from scipy.signal import fftconvolve

SR = 8000
S = "/tmp/claude-0/-home-user-moviepy/85d12e5f-492e-5f24-ac1c-c6bff0419910/scratchpad/"
def load(p, ss=None, to=None):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", str(ss), "-to", str(to)] if ss is not None else []) + \
          ["-i", p, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.int16).astype(np.float32) / 32768

SFX = {"gunshot": (0, 0.9), "gun_fire": (2.0, 4.7), "dramatic_hit": (5.4, 6.3), "nani": (7.3, 8.8),
       "bell_ring": (9.1, 10.2), "dramatic_sting": (11.2, 12.9), "squeak": (14.0, 14.8),
       "music_sting": (16.0, 16.5), "bell_toll": (17.3, 19.2), "ding": (22.0, 23.3),
       "blip1": (24.9, 25.1), "blip2": (25.6, 25.9)}
os.makedirs(S + "sfx_lib", exist_ok=True)
tmpl = {}
for k, (a, b) in SFX.items():
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-to", str(b), "-i", S + "media/sfx.mov",
                    "-vn", "-c:a", "pcm_s16le", S + f"sfx_lib/{k}.wav"])
    t = load(S + "media/sfx.mov", a, b); tmpl[k] = (t - t.mean())

for v in sorted(glob.glob(S + "media/v*.mov")):
    x = load(v); hits = []
    x2 = np.concatenate([[0], np.cumsum(x ** 2)])
    for k, t in tmpl.items():
        n = len(t)
        if n < 400: continue
        c = fftconvolve(x, t[::-1], "valid")
        e2 = fftconvolve(x ** 2, np.ones(n), "valid")[:len(c)]
        ok = e2 > 1e-3 * n * 1e-2
        ncc = np.where(ok, c / (np.sqrt(np.maximum(e2, 1e-12)) * np.linalg.norm(t)), 0)
        idx = np.where(ncc > 0.45)[0]
        last = -1e9
        for i in idx[np.argsort(-ncc[idx])]:
            if all(abs(i - j) > SR for j, _ in [(h[1] * SR, 0) for h in hits if h[0] == k]):
                hits.append((k, i / SR, float(ncc[i])))
    hits.sort(key=lambda h: h[1])
    print(os.path.basename(v), " | ".join(f"{h[1]:.1f}s {h[0]}({h[2]:.2f})" for h in hits) or "-")
