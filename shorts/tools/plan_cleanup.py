"""Keep POSTING PLAN clean: remove rows that are done.

Rules (Bjorn): delete a row when
  - APPROVE is YES and its POST TIME (Philippine time) has passed  -> already live on YouTube
  - APPROVE is NO                                                   -> rejected
Blank APPROVE = not reviewed yet -> never deleted. Only sheet rows are removed, never Drive videos.

usage: plan_cleanup.py WEBAPP_URL            (dry run: shows what would be deleted)
       plan_cleanup.py WEBAPP_URL --apply    (deletes, then reads the sheet back)
"""
import datetime as dt, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import upload_drive as u  # noqa: E402

SHEET_ID = "12th0-8z61cYyA0eT0HxaCjsn5Avy0DW5H6PyGTnVtx4"
PH = dt.timezone(dt.timedelta(hours=8))
u.URL = sys.argv[1]
apply = "--apply" in sys.argv


def post_time(s, now):
    m = re.search(r"([A-Z][a-z]{2}) (\d{1,2}) · (\d{1,2}):(\d{2}) (AM|PM)", s)
    if not m:
        return None
    mon = dt.datetime.strptime(m[1], "%b").month
    h = int(m[3]) % 12 + (12 if m[5] == "PM" else 0)
    t = dt.datetime(now.year, mon, int(m[2]), h, int(m[4]), tzinfo=PH)
    if (t - now).days > 180:      # e.g. a "Jan" row read in December belongs to next year... and vice versa
        t = t.replace(year=now.year - 1)
    elif (now - t).days > 180:
        t = t.replace(year=now.year + 1)
    return t


vals = u.call({"action": "sheet_read", "sheetId": SHEET_ID})["values"]
now = dt.datetime.now(PH)
todo = []
for i, row in enumerate(vals[1:], start=2):
    clip, ap = row[0].strip(), (row[6] if len(row) > 6 else "").strip().upper()
    if not clip.startswith("CLIP"):
        continue
    t = post_time(row[4], now) if len(row) > 4 else None
    if ap == "NO":
        todo.append({"row": i, "clip": clip, "approve": "NO", "why": "rejected"})
    elif ap == "YES" and t and t <= now:
        todo.append({"row": i, "clip": clip, "approve": "YES", "why": f"posted {row[4]}"})
    else:
        state = "approved, posts " + row[4] if ap == "YES" else ("not reviewed yet" if not ap else f"APPROVE={ap!r}")
        print(f"keep   row {i} {clip}: {state}")
for x in todo:
    print(f"DELETE row {x['row']} {x['clip']}: {x['why']}")
if not todo:
    print("nothing to clean")
elif apply:
    r = u.call({"action": "sheet_delete_rows", "sheetId": SHEET_ID},
               json.dumps([{k: x[k] for k in ("row", "clip", "approve")} for x in todo]).encode())
    print(r)
    for i, row in enumerate(u.call({"action": "sheet_read", "sheetId": SHEET_ID})["values"], 1):
        print(i, " | ".join(c.replace("\n", " ")[:40] for c in row[:8]))
else:
    print("(dry run - nothing deleted; add --apply)")
