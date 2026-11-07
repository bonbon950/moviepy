"""Deep pass on hot spots of a long VOD: fetch a low-res window around each, transcribe, tag laughs/screams.

usage: deep_pass.py PLAYLIST_360P_URL hot.txt OUT_DIR [before=70] [after=50]
hot.txt = output of rank_fast.py (uses the t= values). Writes OUT_DIR/h<rank>.mp4, .txt (transcript with
VOD timestamps), .tags (laugh/scream seconds) and a summary.txt to read through.
"""
import json, os, re, subprocess, sys

T = os.path.dirname(os.path.abspath(__file__))
url, hot, out = sys.argv[1], sys.argv[2], sys.argv[3]
before = float(sys.argv[4]) if len(sys.argv) > 4 else 70
after = float(sys.argv[5]) if len(sys.argv) > 5 else 50
os.makedirs(out, exist_ok=True)
spots = [(int(m[1]), int(m[2])) for m in (re.match(r"\s*(\d+) \S+ t=(\d+)", l) for l in open(hot)) if m]

from faster_whisper import WhisperModel
import numpy as np
model = WhisperModel("base.en", device="cpu", compute_type="int8", cpu_threads=4)


def hms(s): s = int(s); return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


summary = open(os.path.join(out, "summary.txt"), "w")
for rank, t in spots:
    a, b = max(0, t - before), t + after
    mp4 = os.path.join(out, f"h{rank:02d}.mp4")
    if not os.path.exists(mp4):
        subprocess.run(["python3", f"{T}/twitch_section.py", url, str(a), str(b), mp4], capture_output=True)
    if not os.path.exists(mp4):
        continue
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", mp4, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    segs, _ = model.transcribe(audio, vad_filter=True, beam_size=1, condition_on_previous_text=False)
    lines = [f"{hms(a + s.start)} {s.text.strip()}" for s in segs]
    open(mp4[:-4] + ".txt", "w").write("\n".join(lines))
    tags = subprocess.run(["python3", f"{T}/tagaudio.py", mp4, "1.0", "1.0", "0.3"], capture_output=True, text=True).stdout
    keep = [l for l in tags.splitlines() if re.search(r"Laugh|Giggle|Chuckle|Snicker|Scream|Shout|Yell", l)]
    open(mp4[:-4] + ".tags", "w").write("\n".join(keep))
    laughs = sum(1 for l in keep if re.search(r"Laugh|Giggle|Chuckle|Snicker", l))
    screams = sum(1 for l in keep if re.search(r"Scream|Shout|Yell", l))
    summary.write(f"\n##### h{rank:02d}  VOD {hms(a)}-{hms(b)}  laughs={laughs} screams={screams}\n")
    summary.write(" ".join(x.split(" ", 1)[1] for x in lines if " " in x)[:900] + "\n")
    summary.flush()
    print(f"h{rank:02d} done (laughs={laughs} screams={screams})", flush=True)
print("ALL DONE")
