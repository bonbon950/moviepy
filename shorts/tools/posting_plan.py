"""Read / update / extend the POSTING PLAN Google Sheet through the Drive helper (v3).

usage:
  posting_plan.py URL read
  posting_plan.py URL set ROW COL "value"          (1-based; e.g. STATUS column = 8)
  posting_plan.py URL append rows.json            (list of 8-column rows)
  posting_plan.py URL style
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import upload_drive as u  # noqa: E402

SHEET_ID = "12th0-8z61cYyA0eT0HxaCjsn5Avy0DW5H6PyGTnVtx4"
u.URL, cmd = sys.argv[1], sys.argv[2]
if cmd == "read":
    r = u.call({"action": "sheet_read", "sheetId": SHEET_ID})
    if "error" in r:
        sys.exit(r["error"])
    for i, row in enumerate(r["values"], 1):
        print(i, " | ".join(c.replace("\n", " ")[:60] for c in row))
elif cmd == "set":
    print(u.call({"action": "sheet_set", "sheetId": SHEET_ID, "row": sys.argv[3], "col": sys.argv[4],
                  "value": sys.argv[5]}))
elif cmd == "append":
    rows = json.load(open(sys.argv[3]))
    print(u.call({"action": "sheet_append", "sheetId": SHEET_ID}, json.dumps(rows).encode()))
elif cmd == "style":
    print(u.call({"action": "sheet_style", "sheetId": SHEET_ID}))
