"""Upload finished shorts into a channel's Drive output folder via that channel's Apps Script web app.

usage: upload_drive.py CHANNEL "November 11, 2026" video1.mp4 [...]       (CHANNEL = id like kai_cenat;
                                                                         folder name from its settings)
       upload_drive.py WEBAPP_URL "OUTPUT (November 6, 2026)" video1.mp4   (old way)
(The web-app URL is private: it is read from the channel's local uploader_url_file, never from the repo.)
Uploads in 6 MB chunks (resumable), prints the folder link at the end.
"""
import base64, json, os, sys, urllib.parse, urllib.request

URL = sys.argv[1] if len(sys.argv) > 1 else ""
CHUNK = 6 * 1024 * 1024  # multiple of 256 KiB, as Drive requires


def call(params, body=b"", tries=5):
    import time
    for k in range(tries):
        try:
            return _call(params, body)
        except Exception as e:  # network hiccup: back off and retry the same request
            if k == tries - 1:
                raise
            print(f"  retry {k + 1} after {type(e).__name__}", flush=True)
            time.sleep(2 ** (k + 1))


def _call(params, body=b""):
    q = URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(q, data=body or b" ", method="POST",
                                 headers={"Content-Type": "text/plain"})
    with urllib.request.urlopen(req, timeout=300) as r:  # follows the Apps Script redirect
        return json.loads(r.read().decode())


def main(FOLDER, files):
    f = call({"action": "folder", "name": FOLDER})
    if "error" in f:
        sys.exit(f"folder error: {f['error']}")
    # CHECK FIRST: never upload something that is already in the folder (same name) -> no duplicates/mess
    lst = call({"action": "list", "folderId": f["id"]})
    existing = {x["name"]: x for x in lst.get("files", []) if not x["trashed"]} if "files" in lst else None
    if existing is None:
        print("note: helper is v1 (no list) - duplicate check is done server-side only")
        existing = {}
    for path in files:
        if os.path.basename(path) in existing:
            print(f"SKIPPED {os.path.basename(path)}: already in {FOLDER} (no duplicate uploaded)")
            continue
        size = os.path.getsize(path)
        s = call({"action": "start", "folderId": f["id"], "name": os.path.basename(path),
                  "mime": "video/mp4", "size": size})
        if not s.get("session"):
            sys.exit(f"start failed for {path}: {s}")
        with open(path, "rb") as fh:
            start, fid = 0, None
            while start < size:
                data = fh.read(CHUNK)
                r = call({"action": "chunk", "session": s["session"], "start": start, "size": size},
                         base64.b64encode(data))
                if r.get("code") not in (200, 201, 308):
                    sys.exit(f"chunk failed for {path} at {start}: {r}")
                fid = r.get("id") or fid
                start += len(data)
        print(f"uploaded {os.path.basename(path)} ({size / 1e6:.1f} MB) id={fid}")
    print("folder:", f["url"])


if __name__ == "__main__":
    if URL and not URL.startswith("http"):            # channel id -> its own uploader + folder naming
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from channel import load
        ch = load(URL)
        URL = ch["uploader_url"] or sys.exit(f"no uploader URL saved for {ch['id']}: {ch['uploader_url_file']}")
        folder = sys.argv[2] if "(" in sys.argv[2] else ch["output_folder"](sys.argv[2])
    else:
        folder = sys.argv[2]
    main(folder, sys.argv[3:])
