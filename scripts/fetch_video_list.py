#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""翻页抓取抖音博主全部视频 ID 与发布文案（抖音 web 作品列表 API，裸调无需 a_bogus）。

用法:
    python fetch_video_list.py <sec_uid> [workdir]

说明:
    - 从工作目录读取 cookies.txt（Netscape 格式），输出 video_list.json
    - sec_uid 来自博主主页短链 302 跳转后的 /user/MS4wLjAB... 段
"""
import sys, os, json, subprocess, time

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def fetch(sec_uid, workdir=None, out="video_list.json", max_pages=300):
    workdir = workdir or os.environ.get("DOUYIN_WORKDIR", os.getcwd())
    ck = os.path.join(workdir, "cookies.txt")
    if not os.path.exists(ck):
        print("[错误] 工作目录缺少 cookies.txt，请先按 references/cookies_guide.md 导出")
        return
    videos = []
    cursor = 0
    page = 0
    while page < max_pages:
        url = (f"https://www.douyin.com/aweme/v1/web/aweme/post/"
               f"?aid=6383&sec_user_id={sec_uid}&count=20&max_cursor={cursor}")
        cmd = ["curl", "-s", "-A", UA, "-b", ck, "-H", "Referer: https://www.douyin.com/", url]
        r = subprocess.run(cmd, capture_output=True, text=True)
        try:
            data = json.loads(r.stdout)
        except Exception as e:
            print("parse error:", e)
            break
        if data.get("status_code") != 0:
            print("status_code:", data.get("status_code"), "(cookie 可能失效，请重新导出 cookies.txt)")
            break
        lst = data.get("aweme_list") or []
        for a in lst:
            videos.append({"id": a.get("aweme_id"), "desc": a.get("desc", "")})
        page += 1
        print(f"page {page}: +{len(lst)} total {len(videos)} has_more={data.get('has_more')}")
        if not data.get("has_more"):
            break
        cursor = data.get("max_cursor", cursor)
        time.sleep(1.5)
    with open(os.path.join(workdir, out), "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)
    print("TOTAL_VIDEOS:", len(videos))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python fetch_video_list.py <sec_uid> [workdir]")
        sys.exit(1)
    sec = sys.argv[1]
    wd = sys.argv[2] if len(sys.argv) > 2 else None
    fetch(sec, wd)
