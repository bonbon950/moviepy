"""Word-level transcript with timestamps (faster-whisper).

usage: words.py MEDIA OUT.json [model=small.en]
Writes [{"t": start, "e": end, "w": word, "p": prob}, ...]
"""
import json, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

model = WhisperModel(sys.argv[3] if len(sys.argv) > 3 else "small.en", device="cpu", compute_type="int8",
                     cpu_threads=4)
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", sys.argv[1], "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                     capture_output=True).stdout
audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
segs, _ = model.transcribe(audio, word_timestamps=True, vad_filter=False, beam_size=5,
                           condition_on_previous_text=False)
out = []
for s in segs:
    for w in s.words or []:
        out.append({"t": round(w.start, 2), "e": round(w.end, 2), "w": w.word.strip(), "p": round(w.probability, 2)})
json.dump(out, open(sys.argv[2], "w"), indent=0)
print(len(out), "words")
