"""Tag non-speech sound events (SFX, laughter, impacts...) in a media file with an AudioSet model.

usage: tagaudio.py MEDIA [window_s=1.0] [hop_s=0.5] [min_prob=0.25]
Prints one line per window with the top non-speech labels.
"""
import sys, subprocess, numpy as np, sherpa_onnx, os

M = os.environ.get("TAGGER_DIR", "/tmp/claude-0/-home-user-moviepy/85d12e5f-492e-5f24-ac1c-c6bff0419910/"
                   "scratchpad/models/sherpa-onnx-ced-base-audio-tagging-2024-04-19/")
cfg = sherpa_onnx.AudioTaggingConfig(
    model=sherpa_onnx.AudioTaggingModelConfig(ced=M + "model.int8.onnx", num_threads=4),
    labels=M + "class_labels_indices.csv", top_k=8)
tagger = sherpa_onnx.AudioTagging(cfg)

SKIP = {"Speech", "Male speech, man speaking", "Female speech, woman speaking", "Conversation",
        "Narration, monologue", "Inside, small room", "Inside, large room or hall", "Child speech, kid speaking",
        "Speech synthesizer"}
src = sys.argv[1]
win = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
hop = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
pmin = float(sys.argv[4]) if len(sys.argv) > 4 else 0.25
SR = 16000
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                     capture_output=True).stdout
a = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
t = 0.0
while t < len(a) / SR - 0.2:
    x = a[int(t * SR):int((t + win) * SR)]
    s = tagger.create_stream(); s.accept_waveform(SR, x)
    ev = [e for e in tagger.compute(s) if e.name not in SKIP and e.prob >= pmin]
    if ev:
        print(f"{t:5.1f}s  " + ", ".join(f"{e.name}({e.prob:.2f})" for e in ev[:4]))
    t += hop
