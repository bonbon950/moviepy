"""List or restore (un-trash) files in one of Bjorn's "OUTPUT (...)" Drive folders via the helper web app.

usage: drive_restore.py WEBAPP_URL "OUTPUT (November 7, 2026)"            -> list folder (incl. trashed items)
       drive_restore.py WEBAPP_URL "OUTPUT (November 7, 2026)" FILE_ID ... -> restore those files from trash
Restoring is refused for files outside OUTPUT folders. There is no delete function.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import upload_drive as u  # noqa: E402

u.URL = sys.argv[1]
f = u.call({"action": "folder", "name": sys.argv[2]})
for fid in sys.argv[3:]:
    print(fid, u.call({"action": "restore", "fileId": fid}))
lst = u.call({"action": "list", "folderId": f["id"]})
if "error" in lst:
    sys.exit(f"list failed: {lst['error']} (is the helper updated to v2?)")
for x in sorted(lst["files"], key=lambda x: x["name"]):
    print(f"{'TRASHED ' if x['trashed'] else '        '}{x['name']}  {x['size'] / 1e6:.1f} MB  id={x['id']}")
