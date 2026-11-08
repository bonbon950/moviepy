# Bjorn's Shorts system — channels

One **shared engine** (`tools/`, sound manifests) serves several YouTube channels. Each streamer/channel has
**its own folder** in `channels/`, named after the streamer, and its own Google account, Drive, uploader script
copy, POSTING PLAN sheet and YouTube (read-only) access. Channels never share clips, folders or sheets.

| Channel id | Streamer | YouTube channel | Folder |
|---|---|---|---|
| `kai_cenat` | Kai Cenat | **KaiCentralClip** (formerly The13Clips) | `channels/kai_cenat/` |
| `fanum` | Fanum | **Fanum Daily** (@FanumDaily) — setting up | `channels/fanum/` |

## What is where
```
shorts/
├── CHANNELS.md                ← this index
├── tools/                     ← shared engine: scan, transcribe, captions, render, upload, posting plan, analytics
├── *_manifest.tsv             ← shared SFX / music libraries
└── channels/
    ├── fanum/                         ← Fanum Daily: FANUM_RULEBOOK.md, fanum_channel.json, edits/fanum_*.py
    ├── kai_cenat/
    │   ├── KAI_CENAT_RULEBOOK.md     ← rules for this channel (editing style v2 = section 15)
    │   ├── kai_cenat_channel.json    ← settings: YouTube channel, Drive folder naming, sheet, local paths
    │   └── edits/kai_cenat_*.py      ← every edit plan made for this channel
    └── _template/                     ← copy this to start a new streamer's channel
```

## Using a channel
Every tool takes the **channel id** where it used to take the uploader link:
```
python tools/channel.py                                   # list channels
python tools/channel.py kai_cenat                         # show its settings (link hidden)
python tools/upload_drive.py kai_cenat "November 11, 2026" CLIP1.mp4 ...
python tools/posting_plan.py kai_cenat read
python tools/plan_cleanup.py kai_cenat                    # dry run
python tools/drive_restore.py kai_cenat "November 8, 2026"
```
The uploader link is **private**: it is read from the PC file named in the channel settings
(`~/Documents/shorts_work/channels/<id>/uploader_url.txt`), never stored in this repo. In a cloud/phone
session, paste it once and save it to that path for the session.

## Rules that apply to every channel
- Drive: never delete or trash anything; list the folder before and after every upload; no duplicates.
- Never post the same clip or the same streamer moment on two channels (reused/repetitive content risk).
  Streamers appear on each other's streams (Fanum is often on Kai's): before editing a moment for one channel,
  check the other channel's edit plans and POSTING PLAN so the same moment never goes up twice.
- Editing style v2 (see each rulebook, section 15) and the growth plan (section 14) apply to every channel.

## Adding a new streamer
See `channels/_template/NEW_CHANNEL_SETUP.md`.
