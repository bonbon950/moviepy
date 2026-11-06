"""Scan a long stream's audio and score every second for "clip-worthiness".

usage: scan_vod.py AUDIO_16K_MONO.wav OUT.csv
Columns: t, loud_db, laugh, scream, crowd, music  (AudioSet probabilities, 1 s windows)
"""
import sys, wave, numpy as np, sherpa_onnx, os

M = os.environ.get("TAGGER_DIR", "/tmp/claude-0/-home-user-moviepy/85d12e5f-492e-5f24-ac1c-c6bff0419910/"
                   "scratchpad/models/sherpa-onnx-ced-base-audio-tagging-2024-04-19/")
tagger = sherpa_onnx.AudioTagging(sherpa_onnx.AudioTaggingConfig(
    model=sherpa_onnx.AudioTaggingModelConfig(ced=M + "model.int8.onnx", num_threads=8),
    labels=M + "class_labels_indices.csv", top_k=40))
GROUPS = {
    "laugh": {"Laughter", "Giggle", "Belly laugh", "Chuckle, chortle", "Snicker", "Baby laughter"},
    "scream": {"Screaming", "Shout", "Yell", "Children shouting", "Battle cry", "Whoop"},
    "crowd": {"Crowd", "Cheering", "Applause", "Hubbub, speech noise, speech babble", "Chatter"},
    "music": {"Music"},
}
w = wave.open(sys.argv[1]); SR = w.getframerate()
a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
out = open(sys.argv[2], "w"); out.write("t,loud_db,laugh,scream,crowd,music\n")
n = len(a) // SR
for i in range(n):
    x = a[i * SR:(i + 1) * SR]
    db = 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
    s = tagger.create_stream(); s.accept_waveform(SR, x)
    ev = tagger.compute(s)
    g = {k: max([e.prob for e in ev if e.name in v] or [0]) for k, v in GROUPS.items()}
    out.write(f"{i},{db:.1f},{g['laugh']:.3f},{g['scream']:.3f},{g['crowd']:.3f},{g['music']:.3f}\n")
    if i % 600 == 0:
        out.flush(); print(f"{i}/{n}", flush=True)
out.close()
