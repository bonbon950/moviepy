"""Download a time window of a Twitch VOD by fetching its 10 s HLS segments directly.

usage: twitch_section.py PLAYLIST_URL START_S END_S OUT.mp4
(PLAYLIST_URL from: yt-dlp -g -f 1080p60 <vod url>)
Output is cut to exactly [START_S, END_S] relative to the VOD.
"""
import os, re, shutil, subprocess, sys, tempfile, urllib.request
from concurrent.futures import ThreadPoolExecutor

url, start, end, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
base = url.rsplit("/", 1)[0] + "/"
pl = urllib.request.urlopen(url, timeout=30).read().decode()
segs, t = [], 0.0
dur = None
for line in pl.splitlines():
    m = re.match(r"#EXTINF:([\d.]+)", line)
    if m:
        dur = float(m.group(1))
    elif line and not line.startswith("#"):
        segs.append((t, dur, line)); t += dur
need = [(i, s) for i, s in enumerate(segs) if s[0] + s[1] > start and s[0] < end]
tmp = tempfile.mkdtemp(prefix="tw_")
def get(item):
    i, (t0, d, name) = item
    p = os.path.join(tmp, f"{i:06d}.ts")
    for cand in (name, name.replace("-unmuted", "-muted"), name.replace("-muted", "")):
        try:
            open(p, "wb").write(urllib.request.urlopen(base + cand, timeout=60).read()); return name
        except Exception:
            continue
    raise RuntimeError("failed " + name)
with ThreadPoolExecutor(8) as ex:
    names = list(ex.map(get, need))
muted = sum("muted" in n for n in names)
# Twitch-muted segments carry broken (or no) audio: decoding drops those samples, so everything after
# them drifts out of sync. They are silent anyway -> replace their audio with real silence of equal length.
def fix_audio(item):
    (i, (t0, d, name)), got = item
    p = os.path.join(tmp, f"{i:06d}.ts")
    has = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index",
                          "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip()
    if has and "muted" not in got:
        return 0
    q = p[:-3] + "_s.ts"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", p, "-f", "lavfi", "-i",
                    # audio FIRST, like Twitch's own segments: the concat demuxer pairs streams by index
                    "anullsrc=channel_layout=stereo:sample_rate=48000", "-map", "1:a", "-map", "0:v",
                    "-c:v", "copy", "-c:a", "aac", "-t", f"{d:.3f}", q], check=True)
    os.replace(q, p)
    return 1
with ThreadPoolExecutor(8) as ex:
    silent = sum(ex.map(fix_audio, zip(need, names)))
lst = os.path.join(tmp, "l.txt")
open(lst, "w").write("".join(f"file '{os.path.join(tmp, f'{i:06d}.ts')}'\n" for i, _ in need))
first = need[0][1][0]
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-ss", f"{start - first:.3f}",
                "-t", f"{end - start:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-af", "aresample=async=1:first_pts=0", "-c:a", "aac",
                "-b:a", "192k", out], check=True)
shutil.rmtree(tmp, ignore_errors=True)   # raw segments are big: never leave them behind (disk filled up once)
print(f"{out}: {len(need)} segments ({muted} muted by Twitch, {silent} given clean silence)")
