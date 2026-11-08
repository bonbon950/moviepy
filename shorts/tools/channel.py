"""Multi-channel settings: every streamer/YouTube channel has its own folder in shorts/channels/<id>/.

    from channel import load
    ch = load("kai_cenat")
    ch["uploader_url"]            # read from the PRIVATE local file (never stored in the repo)
    ch["output_folder"]("November 11, 2026")   # -> "OUTPUT (November 11, 2026)"
    ch["posting_plan_sheet_id"], ch["dir"], ch["edits"], ch["rulebook_path"], ch["local_dir"]

CLI: channel.py                 -> list channels
     channel.py kai_cenat       -> show that channel's settings (URL hidden)
"""
import glob, json, os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "channels")
DEFAULT = "kai_cenat"


def channels():
    return sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(ROOT, "*", "*_channel.json")))


def load(cid=None):
    cid = cid or os.environ.get("SHORTS_CHANNEL") or DEFAULT
    d = os.path.join(ROOT, cid)
    files = glob.glob(os.path.join(d, "*_channel.json"))
    if not files:
        sys.exit(f"unknown channel '{cid}'. Known: {', '.join(channels())}")
    ch = json.load(open(files[0], encoding="utf-8"))
    ch["dir"] = os.path.abspath(d)
    ch["edits"] = os.path.join(ch["dir"], ch.get("edits_dir", "edits"))
    ch["rulebook_path"] = os.path.join(ch["dir"], ch["rulebook"])
    ch["local_dir"] = os.path.expanduser(ch["local_dir"])
    url_file = os.path.expanduser(ch["uploader_url_file"])
    ch["uploader_url"] = open(url_file).read().strip() if os.path.exists(url_file) else ""
    ch["output_folder"] = lambda date: ch["drive_output_folder"].format(date=date)
    return ch


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("channels:", ", ".join(channels()))
    else:
        c = load(sys.argv[1])
        for k, val in c.items():
            if k == "uploader_url":
                val = "(set)" if val else "(missing - paste it into uploader_url_file)"
            if not callable(val) and not k.startswith("_"):
                print(f"{k}: {val}")
