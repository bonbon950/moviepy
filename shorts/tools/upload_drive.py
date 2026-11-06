"""Upload finished shorts into Bjorn's Drive folder "OUTPUT (<date>)" via the Apps Script web app.

usage: upload_drive.py WEBAPP_URL "OUTPUT (November 6, 2026)" video1.mp4 [video2.mp4 ...]
(WEBAPP_URL = the deployed drive_uploader.gs URL; keep it private.)
Uploads in 6 MB chunks (resumable), prints the folder link at the end.
"""
import base64, json, os, sys, urllib.parse, urllib.request

URL, FOLDER, files = sys.argv[1], sys.argv[2], sys.argv[3:]
CHUNK = 6 * 1024 * 1024  # multiple of 256 KiB, as Drive requires


def call(params, body=b""):
    q = URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(q, data=body or b" ", method="POST",
                                 headers={"Content-Type": "text/plain"})
    with urllib.request.urlopen(req, timeout=300) as r:  # follows the Apps Script redirect
        return json.loads(r.read().decode())


f = call({"action": "folder", "name": FOLDER})
if "error" in f:
    sys.exit(f"folder error: {f['error']}")
for path in files:
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
