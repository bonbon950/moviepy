"""Read / update / extend the POSTING PLAN Google Sheet through the Drive helper (v3).

usage:   (CHANNEL = channel id like kai_cenat, or the web-app URL = old way, Kai Cenat channel)
  posting_plan.py CHANNEL read
  posting_plan.py CHANNEL set ROW COL "value"          (1-based; e.g. STATUS column = 8)
  posting_plan.py CHANNEL append rows.json            (list of 8-column rows)
  posting_plan.py CHANNEL style
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import upload_drive as u  # noqa: E402
from channel import load  # noqa: E402

ch = load(None if sys.argv[1].startswith("http") else sys.argv[1])
SHEET_ID = ch["posting_plan_sheet_id"]
u.URL = sys.argv[1] if sys.argv[1].startswith("http") else ch["uploader_url"]
cmd = sys.argv[2]
if cmd == "read":
    r = u.call({"action": "sheet_read", "sheetId": SHEET_ID})
    if "error" in r:
        sys.exit(r["error"])
    for i, row in enumerate(r["values"], 1):
        print(i, " | ".join(c.replace("\n", " ")[:60] for c in row))
elif cmd == "set":
    # the web app decodes URL parameters as Latin-1 -> emoji/symbols get garbled. Only plain ASCII here.
    # (append is safe: rows go in the body as JSON with \uXXXX escapes)
    if not sys.argv[5].isascii():
        sys.exit("refusing: 'set' only supports plain text (no emoji/symbols)")
    print(u.call({"action": "sheet_set", "sheetId": SHEET_ID, "row": sys.argv[3], "col": sys.argv[4],
                  "value": sys.argv[5]}))
elif cmd == "append":
    rows = json.load(open(sys.argv[3]))
    print(u.call({"action": "sheet_append", "sheetId": SHEET_ID}, json.dumps(rows).encode()))
elif cmd == "style":
    print(u.call({"action": "sheet_style", "sheetId": SHEET_ID}))
