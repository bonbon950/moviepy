# Setting up a new streamer's channel

Replace `<id>` with a short lowercase id for the streamer (e.g. `ishowspeed`) and `<STREAMER>` with the name.

## 1. Repo (Claude does this)
1. Copy this folder to `channels/<id>/`.
2. Rename `channel.json.template` → `<id>_channel.json` and fill it in (streamer, YouTube channel name, niche).
3. Create `<STREAMER>_RULEBOOK.md` from `RULEBOOK_TEMPLATE.md`: copy the shared editing rules from
   `channels/kai_cenat/KAI_CENAT_RULEBOOK.md` and replace only the channel-specific parts listed there.
4. Edit plans go in `channels/<id>/edits/<id>_*.py` (copy the import line from a Kai Cenat plan).
5. Add the channel to the table in `shorts/CHANNELS.md`.

## 2. Google account (Bjorn does this, Claude guides step by step)
1. Use the new channel's Google account (one account = one channel).
2. In its Drive, create a Google Sheet named exactly as `posting_plan_sheet_name` (default `POSTING PLAN`).
   Claude fills in the header row and HOW TO USE row.
3. script.google.com → New project → paste `tools/drive_uploader.gs` (v6+) and `tools/appsscript.json`
   (Project Settings → show manifest). Change only the CHANNEL SETTINGS block if the names differ.
4. Run `installHourlyTrigger` once and allow the permissions (YouTube access must say **View** only).
5. Deploy → New deployment → Web app → copy its URL → give it to Claude.

## 3. PC (Claude does this)
1. Save the URL to `~/Documents/shorts_work/channels/<id>/uploader_url.txt` (never in the repo).
2. Test read-only: `python tools/channel.py <id>`, `python tools/posting_plan.py <id> read`.

## Never
- Post the same clip or the same moment on two channels.
- Use a new channel to get around a restriction on another channel (YouTube spam policy).
