"""List or restore (un-trash) files in one of a channel's output Drive folders via its helper web app.

usage: drive_restore.py CHANNEL "November 7, 2026"            -> list folder (incl. trashed items)
       drive_restore.py CHANNEL "November 7, 2026" FILE_ID ... -> restore those files from trash
       (CHANNEL = id like kai_cenat, or the web-app URL + full folder name = old way)
Restoring is refused for files outside OUTPUT folders. There is no delete function.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import upload_drive as u  # noqa: E402

if sys.argv[1].startswith("http"):
    u.URL, folder = sys.argv[1], sys.argv[2]
else:
    from channel import load
    ch = load(sys.argv[1])
    u.URL = ch["uploader_url"]
    folder = sys.argv[2] if "(" in sys.argv[2] else ch["output_folder"](sys.argv[2])
f = u.call({"action": "folder", "name": folder})
for fid in sys.argv[3:]:
    print(fid, u.call({"action": "restore", "fileId": fid}))
lst = u.call({"action": "list", "folderId": f["id"]})
if "error" in lst:
    sys.exit(f"list failed: {lst['error']} (is the helper updated to v2?)")
for x in sorted(lst["files"], key=lambda x: x["name"]):
    print(f"{'TRASHED ' if x['trashed'] else '        '}{x['name']}  {x['size'] / 1e6:.1f} MB  id={x['id']}")
