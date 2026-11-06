"""Build the SFX library from shorts/sfx_manifest.tsv (first Myinstants search hit per id).

usage: fetch_sfx.py OUT_DIR
Needs www.myinstants.com allowed in the environment. Skips files that already exist.
"""
import csv, os, re, subprocess, sys, urllib.parse, urllib.request

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
man = os.path.join(os.path.dirname(__file__), "..", "sfx_manifest.tsv")
UA = {"User-Agent": "Mozilla/5.0"}
ok = fail = 0
for row in csv.DictReader(open(man), delimiter="\t"):
    dst = os.path.join(out, row["id"] + ".mp3")
    if os.path.exists(dst):
        ok += 1; continue
    try:
        q = row["myinstants_search"]
        if q.startswith("/media/"):  # pinned exact file
            m = re.match(r".+", q)
        else:
            html = urllib.request.urlopen(urllib.request.Request(
                f"https://www.myinstants.com/en/search/?name={urllib.parse.quote_plus(q)}", headers=UA),
                timeout=20).read().decode()
            m = re.search(r"/media/sounds/[^'\"]+\.mp3", html)
        if not m:
            raise RuntimeError("no result")
        data = urllib.request.urlopen(urllib.request.Request(
            "https://www.myinstants.com" + m.group(0), headers=UA), timeout=30).read()
        open(dst, "wb").write(data)
        dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", dst],
                             capture_output=True, text=True).stdout.strip()
        print(f"OK   {row['id']:<18} {dur:>8}s  <- {m.group(0)}")
        ok += 1
    except Exception as e:
        print(f"FAIL {row['id']:<18} {e}")
        fail += 1
print(f"\n{ok} ok, {fail} failed -> {out}")
