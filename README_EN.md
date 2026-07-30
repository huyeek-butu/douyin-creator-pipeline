# douyin-creator-pipeline

A Douyin (TikTok China) creator content-collection & subtitle-extraction pipeline — a WorkBuddy user-level skill.

One-shot: bulk-download **all videos** of a given Douyin creator to local disk, then run a local whisper model to transcribe the speech into subtitles, producing structured text material ready to feed an LLM for "distillation" analysis.

## Features

- **M1 Resolve**: paste a creator's profile share-link, automatically extract `sec_uid` (no cookie required).
- **M2 List**: call Douyin's web post-list endpoint with pagination to grab every video ID of that creator (works around yt-dlp not supporting profile URLs).
- **M3 Download**: yt-dlp downloads each video, deduplicated by video ID.
- **M4 Subtitle**: ffmpeg extracts audio + local faster-whisper transcribes, producing `.srt` (with timestamps) + plain `.txt`.

## Requirements

- Python 3.12+ (WorkBuddy's managed isolated Python recommended)
- `yt-dlp`, `imageio-ffmpeg`, `faster-whisper` (install into an isolated venv via `pip install`)
- A valid Douyin login cookie file (`cookies.txt`)

## Install

Copy this whole directory into your WorkBuddy user-level skills folder:

```
C:\Users\<your-username>\.workbuddy\skills\douyin-creator-pipeline\
```

Or unzip the Release package into that folder.

## Usage

1. **Prepare cookie**: install the **Cookie-Editor** extension in Edge / Chrome, open https://www.douyin.com and log in, click Export and choose **Netscape** format, save it as `cookies.txt` in your working directory. See `references/cookies_guide.md`.
2. **Provide the creator profile link**: send me the "Share → Copy link" URL from the creator's profile in the Douyin app (looks like `https://v.douyin.com/xxxx/`).
3. **Run the pipeline**: I will automatically run M1→M4 and output videos, subtitles, post captions, and a merged material file into the working directory.

## Known pitfalls (documented in detail in SKILL.md)

1. Douyin forcibly requires a login cookie — without it you cannot download even a single video.
2. yt-dlp's Douyin extractor only accepts `/video/{id}`, not profile `/user/{sec_uid}` — you must paginate the API to collect IDs.
3. Cloud sandbox is isolated from your local machine; `--cookies-from-browser` is physically impossible — you can only export the cookie file manually.
4. HuggingFace direct access is blocked + the new `huggingface_hub` defaults to the Xet protocol (401) — you must set `HF_ENDPOINT=https://hf-mirror.com` and `HF_HUB_DISABLE_XET=1`.
5. Sandbox recycle bin is unavailable; the `safe-delete` warning is harmless.

## Disclaimer

This tool is for personal backup and study only. Respect Douyin's Terms of Service; do not redistribute or commercialize downloaded content.

## License

MIT
