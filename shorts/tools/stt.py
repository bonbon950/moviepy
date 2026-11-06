"""Transcribe audio in segments. usage: stt.py media [seg_list 'start-end,...' | auto]"""
import sys, subprocess, numpy as np, sherpa_onnx, re

M = "/tmp/claude-0/-home-user-moviepy/85d12e5f-492e-5f24-ac1c-c6bff0419910/scratchpad/models/sherpa-onnx-whisper-small.en/"
rec = sherpa_onnx.OfflineRecognizer.from_whisper(
    encoder=M + "small.en-encoder.int8.onnx", decoder=M + "small.en-decoder.int8.onnx",
    tokens=M + "small.en-tokens.txt", num_threads=4, language="en", task="transcribe")

src = sys.argv[1]
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                     capture_output=True).stdout
a = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
SR = 16000

def segs_auto():
    # split on quiet gaps, cap at ~8s per segment for finer timestamps
    win = int(0.05 * SR)
    e = np.sqrt(np.convolve(a ** 2, np.ones(win) / win, "same"))
    thr = max(np.percentile(e, 20) * 1.5, 0.005)
    out, s, i, n = [], 0, 0, len(a)
    while s < n:
        end = min(s + 8 * SR, n)
        if end < n:
            lo = s + 3 * SR
            cut = lo + int(np.argmin(e[lo:end])) if end > lo else end
            end = cut
        out.append((s / SR, end / SR)); s = end
    return out

segs = segs_auto() if len(sys.argv) < 3 or sys.argv[2] == "auto" else \
    [tuple(map(float, p.split("-"))) for p in sys.argv[2].split(",")]
for st, en in segs:
    x = a[int(st * SR):int(en * SR)]
    if len(x) < SR * 0.2: continue
    s = rec.create_stream(); s.accept_waveform(SR, x); rec.decode_stream(s)
    t = s.result.text.strip()
    print(f"[{st:6.1f}-{en:6.1f}] {t}")
