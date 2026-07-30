#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""逐条下载 video_list.json 里的视频（yt-dlp 单视频模式 + 抖音 API 列表）。

用法:
    python download_videos.py

说明:
    - 读取工作目录的 video_list.json 与 cookies.txt
    - 按 19 位视频 ID 去重，已下载的跳过
    - ffmpeg 由 common.get_ffmpeg_exe() 自动定位（imageio-ffmpeg）
"""
import sys, os, json, subprocess, re, glob
from common import get_ffmpeg_exe, workdir


def main():
    wd = workdir()
    ck = os.path.join(wd, "cookies.txt")
    ff = get_ffmpeg_exe()
    out = os.path.join(wd, "%(title).60s_%(id)s.%(ext)s")

    if not os.path.exists(ck):
        print("[错误] 工作目录缺少 cookies.txt")
        return
    vl = os.path.join(wd, "video_list.json")
    if not os.path.exists(vl):
        print("[错误] 缺少 video_list.json，请先运行 fetch_video_list.py <sec_uid>")
        return

    videos = json.load(open(vl, encoding="utf-8"))

    # 按 id 去重，避免重复下载
    existing = set()
    for p in glob.glob(os.path.join(wd, "*.mp4")):
        for m in re.findall(r'\d{15,20}', os.path.basename(p)):
            existing.add(m)

    ok = skip = fail = 0
    for i, v in enumerate(videos):
        vid = v.get("id")
        if not vid:
            continue
        if vid in existing:
            print(f"[{i+1}/{len(videos)}] skip (exists) {vid}")
            skip += 1
            continue
        url = f"https://www.douyin.com/video/{vid}"
        cmd = [sys.executable, "-m", "yt_dlp", "--cookies", ck,
               "--ffmpeg-location", ff, "--no-warnings", "-o", out, url]
        print(f"[{i+1}/{len(videos)}] dl {vid}")
        rc = subprocess.run(cmd, check=False).returncode
        if rc == 0:
            ok += 1
        else:
            fail += 1

    print(f"DONE ok={ok} skip={skip} fail={fail} total={len(videos)}")


if __name__ == "__main__":
    main()
