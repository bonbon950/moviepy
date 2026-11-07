"""Render a finished 9:16 1080x1920 short from an edit-plan JSON.

usage: make_short.py PLAN.json OUT.mp4

Plan (times are in the OUTPUT timeline unless noted):
{
  "source": "segment.mp4",                 # 16:9 stream footage
  "keep": [[s, e], ...],                   # ranges of the SOURCE to keep (jump cuts), in order
  "layout": "sandwich" | "full",           # blur sandwich (default) or minimal-crop full frame
  "fonts_dir": "...",
  "header": {"lines": ["LINE 1", "LINE 2"], "color": "#FF2E88", "size": 96},
  "words": [{"t": 0.0, "e": 0.3, "w": "OH", "color": "#FFFFFF"}],   # one-word captions
  "tags": [{"t": 1.0, "e": 2.0, "text": "*KAI LAUGHS*", "box": "#8B0000"}],
  "zooms": [{"t": 1.0, "e": 1.6, "type": "punch", "amt": 1.22},
            {"t": 3.0, "e": 7.0, "type": "push", "amt": 1.08}],
  "flashes": [{"t": 1.0, "d": 0.13, "color": "pink" | "red" | "green" | "white" | "bw"}],
  "sfx": [{"t": 0.0, "file": "vine_boom.mp3", "gain_db": -3}],
  "bed": {"file": "sneaky.mp3", "gain_db": -21, "drops": [[t0, t1]]},  # drops = silence the bed
  "grade": {"saturation": 1.22, "contrast": 1.07}
}
"""
import json, os, subprocess, sys, tempfile

W, H, FPS = 1080, 1920, 30


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.stderr.write(r.stderr[-4000:]); raise SystemExit(f"ffmpeg failed: {' '.join(cmd[:6])}...")
    return r


def ass_color(hexstr, alpha="00"):
    h = hexstr.lstrip("#")
    return f"&H{alpha}{h[4:6]}{h[2:4]}{h[0:2]}&".upper()


def ts(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def build_ass(p, dur, path, cap_y, head_y):
    hd = p.get("header", {})
    hsize = hd.get("size", 96)
    lines = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 2",
        "ScaledBorderAndShadow: yes", "", "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, "
        "Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, "
        "MarginL, MarginR, MarginV, Encoding",
        f"Style: Header,Anton,{hsize},{ass_color(hd.get('color', '#FFFFFF'))},&H000000FF&,&H00000000&,&H90000000&,"
        "0,0,0,0,100,100,1,0,1,7,4,5,40,40,0,1",
        "Style: Cap,Anton,132,&H00FFFFFF&,&H000000FF&,&H00000000&,&H90000000&,0,0,0,0,100,100,1,0,1,8,3,5,40,40,0,1",
        "Style: Tag,Anton,110,&H00FFFFFF&,&H000000FF&,&H00000000&,&H90000000&,0,0,0,0,100,100,1,0,1,8,3,5,40,40,0,1",
        "Style: TagBox,Anton,110,&H00FFFFFF&,&H000000FF&,&H000000AA&,&H000000AA&,0,0,0,0,100,100,1,0,3,14,0,5,40,40,0,1",
        "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    if hd.get("lines") and not hd.get("png"):
        txt = "\\N".join(hd["lines"])
        # slam in: scale from 160% -> 92% -> 100% over 300 ms, stays the whole video
        anim = "{\\fscx160\\fscy160\\t(0,140,\\fscx92\\fscy92)\\t(140,300,\\fscx100\\fscy100)}"
        lines.append(f"Dialogue: 5,{ts(0)},{ts(dur)},Header,,0,0,0,,{{\\pos({W//2},{head_y})}}{anim}{txt}")
    tag_spans = [(g["t"], g["e"]) for g in p.get("tags", [])
                 if abs(g.get("y", cap_y) - cap_y) < 160]
    for wd in p.get("words", []):
        if any(a <= wd["t"] < b for a, b in tag_spans):
            continue  # tag replaces the caption while it's on screen
        col = ass_color(wd.get("color", "#FFFFFF"))
        pop = "{\\fscx65\\fscy65\\t(0,70,\\fscx115\\fscy115)\\t(70,140,\\fscx100\\fscy100)}"
        lines.append(f"Dialogue: 3,{ts(wd['t'])},{ts(wd['e'])},Cap,,0,0,0,,"
                     f"{{\\pos({W//2},{cap_y})\\1c{col}}}{pop}{wd['w'].upper()}")
    for g in p.get("tags", []):
        style = "TagBox" if g.get("box") else "Tag"
        extra = f"\\3c{ass_color(g['box'])}\\4c{ass_color(g['box'])}" if g.get("box") else ""
        x, y = g.get("x", W // 2), g.get("y", cap_y)
        fs = f"\\fs{g['size']}" if g.get("size") else ""
        rot = f"\\frz{g['rot']}" if g.get("rot") else ""
        # pop with overshoot, then a slow 'breathing' grow so it never sits dead still
        dur_ms = int((g["e"] - g["t"]) * 1000)
        pop = ("{\\fscx40\\fscy40\\t(0,90,\\fscx125\\fscy125)\\t(90,180,\\fscx100\\fscy100)"
               f"\\t(180,{max(200, dur_ms)},\\fscx108\\fscy108)}}")
        lines.append(f"Dialogue: 4,{ts(g['t'])},{ts(g['e'])},{style},,0,0,0,,"
                     f"{{\\pos({x},{y}){fs}{rot}{extra}}}{pop}{g['text'].upper()}")
    open(path, "w").write("\n".join(lines) + "\n")


EMOJI_DIR = os.environ.get("EMOJI_DIR", "")


def render_header_png(hd, fonts_dir, path, max_w=W - 80):
    """Header as a PNG (Anton, colored fill, thick black stroke, shadow, real color emoji)."""
    from PIL import Image, ImageDraw, ImageFont
    size = hd.get("size", 118)
    font = ImageFont.truetype(os.path.join(fonts_dir, "Anton-Regular.ttf"), size)
    fill = hd.get("color", "#FFFFFF")
    stroke = max(6, size // 13)
    rows = []
    for line in hd["lines"]:
        parts, buf = [], ""
        for ch in line:
            cp = f"{ord(ch):x}"
            if ord(ch) > 0x2600 and EMOJI_DIR and os.path.exists(os.path.join(EMOJI_DIR, cp + ".png")):
                if buf: parts.append(("t", buf)); buf = ""
                parts.append(("e", cp))
            elif ord(ch) in (0xFE0F, 0x200D):
                continue
            else:
                buf += ch
        if buf.strip(): parts.append(("t", buf.rstrip()))
        rows.append(parts)
    d0 = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    def width(parts):
        w = 0
        for k, v in parts:
            w += (d0.textbbox((0, 0), v.upper(), font=font, stroke_width=stroke)[2] if k == "t" else int(size * 1.05))
        return w
    lh = int(size * 1.18)
    cw = max(width(r) for r in rows) + 40
    img = Image.new("RGBA", (cw, lh * len(rows) + 40), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    for i, parts in enumerate(rows):
        x = (cw - width(parts)) // 2; y = 20 + i * lh
        for k, v in parts:
            if k == "t":
                dr.text((x + 6, y + 8), v.upper(), font=font, fill=(0, 0, 0, 150), stroke_width=stroke,
                        stroke_fill=(0, 0, 0, 150))
                dr.text((x, y), v.upper(), font=font, fill=fill, stroke_width=stroke, stroke_fill="black")
                x += d0.textbbox((0, 0), v.upper(), font=font, stroke_width=stroke)[2]
            else:
                em = Image.open(os.path.join(EMOJI_DIR, v + ".png")).convert("RGBA")
                es = int(size * 0.95); em = em.resize((es, es), Image.LANCZOS)
                img.alpha_composite(em, (x + int(size * 0.08), y + int(size * 0.18)))
                x += int(size * 1.05)
    if img.width > max_w:
        img = img.resize((max_w, int(img.height * max_w / img.width)), Image.LANCZOS)
    img.save(path)
    return img.size


def render_sticker_png(text, path, size=170):
    """Row of glossy 3D emoji (each slightly tilted) as one transparent PNG."""
    from PIL import Image
    import random
    cps = [f"{ord(c):x}" for c in text if ord(c) > 0x2000 and ord(c) not in (0xFE0F, 0x200D)]
    rnd = random.Random(text + str(size))
    tiles = []
    for cp in cps:
        f = os.path.join(EMOJI_DIR, cp + ".png")
        if not os.path.exists(f):
            continue
        em = Image.open(f).convert("RGBA").resize((size, size), Image.LANCZOS)
        tiles.append(em.rotate(rnd.uniform(-14, 14), resample=Image.BICUBIC, expand=True))
    if not tiles:
        return None
    gap = int(size * -0.12)
    w = sum(t.width for t in tiles) + gap * (len(tiles) - 1)
    h = max(t.height for t in tiles) + 20
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0)); x = 0
    for t in tiles:
        img.alpha_composite(t, (x, (h - t.height) // 2 + rnd.randint(-10, 10))); x += t.width + gap
    img.save(path)
    return img.size


def zoom_expr(zooms):
    """Per-frame zoom factor z(t) for scale eval=frame."""
    expr = "1"
    for z in zooms:
        a, b, amt = z["t"], z["e"], z.get("amt", 1.2)
        if z.get("type", "punch") == "punch":
            r = 0.08  # snap in/out over ~2-3 frames
            f = (f"if(lt(t,{a}+{r}),1+({amt}-1)*(t-{a})/{r},"
                 f"if(gt(t,{b}-{r}),1+({amt}-1)*({b}-t)/{r},{amt}))")
        else:  # slow push
            f = f"1+({amt}-1)*(t-{a})/({b}-{a})"
        expr = f"if(between(t,{a},{b}),{f},{expr})"
    return expr


def main(plan_path, out):
    p = json.load(open(plan_path))
    tmp = tempfile.mkdtemp(prefix="short_")
    src = p["source"]

    # 1) jump cuts: cut each kept range separately (low memory), then concat
    keep = p["keep"]
    parts = []
    for i, (s0, e0) in enumerate(keep):
        part = os.path.join(tmp, f"p{i:02d}.mov")
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{s0:.3f}", "-i", src, "-t", f"{e0 - s0:.3f}",
             "-vf", f"fps={FPS}", "-af", f"afade=t=in:d=0.01,afade=t=out:st={e0 - s0 - 0.01:.3f}:d=0.01",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-c:a", "pcm_s16le", "-ar", "48000", part])
        parts.append(part)
    lst = os.path.join(tmp, "parts.txt")
    open(lst, "w").write("".join(f"file '{x}'\n" for x in parts))
    base = os.path.join(tmp, "base.mov")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", base])
    dur = sum(e - s for s, e in keep)

    # 2) video: layout + zooms + grade + flashes + text
    layout = p.get("layout", "sandwich")
    g = p.get("grade", {"saturation": 1.2, "contrast": 1.06})
    z = zoom_expr(p.get("zooms", []))
    if layout == "sandwich":
        fg_h = 608
        top = (H - fg_h) // 2
        v = (f"[0:v]split[a][b];"
             f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=28:2,eq=brightness=-0.08[bg];"
             f"[b]scale=w='trunc({W}*({z})/2)*2':h=-2:eval=frame,crop={W}:{fg_h}[fg];"
             f"[bg][fg]overlay=0:{top}")
        cap_y, head_y = top + fg_h - 120, top // 2 + 10
    elif layout == "split":  # gameplay streams: facecam (enlarged, zoomable) on top, full gameplay below
        cx, cy, cw, ch = p["cam"]
        cam_h = int(round(W * ch / cw / 2)) * 2
        top = p.get("split_top", 330)
        game_h = 608
        v = (f"[0:v]split=3[a][b][c];"
             f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=28:2,eq=brightness=-0.1[bg];"
             f"[b]crop={cw}:{ch}:{cx}:{cy},scale=w='trunc({W}*({z})/2)*2':h=-2:eval=frame:flags=lanczos,"
             f"crop={W}:{cam_h}[cam];"
             f"[c]scale={W}:{game_h}[game];"
             f"[bg][cam]overlay=0:{top}[t1];[t1][game]overlay=0:{top + cam_h}")
        cap_y, head_y = top + cam_h, top // 2 + 5
    else:  # minimal crop: fill height, crop sides
        v = (f"[0:v]scale=w=-2:h='trunc({H}*({z})/2)*2':eval=frame,crop={W}:{H}")
        cap_y, head_y = int(H * 0.62), 300
    v += f",eq=saturation={g['saturation']}:contrast={g['contrast']}"
    cmap = {"pink": "0xFF4FA3@0.38", "red": "0xFF1E1E@0.38", "green": "0x39FF14@0.35", "white": "white@0.6"}
    for f in p.get("flashes", []):
        a, b = f["t"], f["t"] + f.get("d", 0.13)
        if f["color"] == "bw":
            v += f",hue=s=0:enable='between(t,{a},{b})'"
        else:
            v += f",drawbox=x=0:y=0:w=iw:h=ih:c={cmap[f['color']]}:t=fill:enable='between(t,{a},{b})'"
    ass = os.path.join(tmp, "t.ass")
    hd = p.get("header", {})
    if hd.get("lines"):
        hd["png"] = os.path.join(tmp, "header.png")
        render_header_png(hd, p["fonts_dir"], hd["png"], max_w=int((W - 60) / 1.18))
    build_ass(p, dur, ass, cap_y, head_y)
    v += f",ass={ass}:fontsdir={p['fonts_dir']}"
    if hd.get("png"):
        # slam-in: 160% -> 92% -> 100% over 0.3 s, then holds
        sc = "if(lt(t,0.14),1.18-0.26*t/0.14,if(lt(t,0.3),0.92+0.08*(t-0.14)/0.16,1))"
        v += (f"[pre];movie={hd['png']},loop=-1:1:0,setpts=N/{FPS}/TB,"
              f"scale=w='trunc(iw*({sc})/2)*2':h=-2:eval=frame[hdr];"
              f"[pre][hdr]overlay=x='(W-w)/2':y='{head_y}-h/2':eval=frame:shortest=1")
    for k, st in enumerate(p.get("stickers", [])):
        png = os.path.join(tmp, f"st{k}.png")
        if not render_sticker_png(st["emoji"], png, st.get("size", 170)):
            continue
        t0, t1 = st["t"], st["e"]
        # pop in (40% -> 120% -> 100%) then a gentle bob; only visible between t0 and t1
        sc = (f"if(lt(t,{t0}),0.4,if(lt(t-{t0},0.1),0.4+0.8*(t-{t0})/0.1,if(lt(t-{t0},0.2),"
              f"1.2-0.2*(t-{t0}-0.1)/0.1,1+0.04*sin(2*PI*(t-{t0})*1.6))))")
        v += (f"[m{k}];movie={png},loop=-1:1:0,setpts=N/{FPS}/TB,"
              f"scale=w='max(2,trunc(iw*({sc})/2)*2)':h='max(2,trunc(ih*({sc})/2)*2)':eval=frame[s{k}];"
              f"[m{k}][s{k}]overlay=x='{st.get('x', W // 2)}-w/2':y='{st.get('y', 1450)}-h/2':eval=frame:"
              f"enable='between(t,{t0},{t1})'")
    v += ",format=yuv420p[vout]"

    # 3) audio: original + SFX + music bed (ducked under voice) -> loudness normalize
    a_in = ["-i", base]
    af, mix = [], ["[orig]"]
    af.append("[0:a]aformat=channel_layouts=stereo,asplit=2[orig][key]")
    idx = 1
    for s in p.get("sfx", []):
        a_in += ["-i", s["file"]]
        d = int(s["t"] * 1000)
        trim = f"atrim=0:{s['dur']},afade=t=out:st={max(0, s['dur'] - 0.15)}:d=0.15," if s.get("dur") else ""
        af.append(f"[{idx}:a]aformat=channel_layouts=stereo,{trim}volume={s.get('gain_db', -3)}dB,adelay={d}|{d}[s{idx}]")
        mix.append(f"[s{idx}]"); idx += 1
    beds = p.get("beds") or ([dict(p["bed"], t=0, e=dur)] if p.get("bed") else [])
    if beds:
        parts = []
        for j, b in enumerate(beds):
            a_in += ["-stream_loop", "-1", "-i", b["file"]]
            ln = b["e"] - b["t"]; d = int(b["t"] * 1000)
            mute = "+".join(f"between(t,{x - b['t']},{y - b['t']})" for x, y in b.get("drops", [])) or "0"
            af.append(f"[{idx}:a]aformat=channel_layouts=stereo,atrim=0:{ln},afade=t=in:d=0.08,"
                      f"afade=t=out:st={max(0, ln - 0.25)}:d=0.25,volume={b.get('gain_db', -20)}dB,"
                      f"volume='if({mute},0,1)':eval=frame,adelay={d}|{d},apad=whole_dur={dur}[b{j}]")
            parts.append(f"[b{j}]"); idx += 1
        af.append(f"{''.join(parts)}amix=inputs={len(parts)}:normalize=0:duration=longest[bedr]")
        af.append("[bedr][key]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[bed]")
        mix.append("[bed]")
    else:
        af.append("[key]anullsink")
    af.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=first,"
              f"loudnorm=I=-10:TP=-1:LRA=9,aresample=48000[aout]")
    fc = v.replace("[0:v]", "[0:v]") + ";" + ";".join(a.replace("[0:a]", "[0:a]") for a in af)
    run(["ffmpeg", "-y", "-v", "error"] + a_in + ["-filter_complex", fc, "-map", "[vout]", "-map", "[aout]",
         "-c:v", "libx264", "-preset", "medium", "-b:v", "12M", "-minrate", "12M", "-maxrate", "12M", "-bufsize", "12M", "-x264-params", "nal-hrd=cbr",
         "-r", str(FPS), "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
         "-t", f"{dur:.3f}", out])
    print(f"rendered {out} ({dur:.1f}s)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
