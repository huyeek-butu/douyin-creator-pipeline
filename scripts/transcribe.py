#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用本地 faster-whisper 转写工作目录下的所有 mp4，输出同名 .srt(时间轴)+.txt(纯文本)。

用法:
    python transcribe.py [model_size] [file1.mp4 file2.mp4 ...]

参数:
    model_size  默认 base；可选 tiny/base/small/medium（越大越准越慢）
    文件列表    缺省则处理工作目录全部 *.mp4

环境变量(沙箱/国内网络必需):
    HF_ENDPOINT=https://hf-mirror.com
    HF_HUB_DISABLE_XET=1
    HF_HUB_ENABLE_HF_TRANSFER=0
"""
import os, sys, glob
from common import workdir


def fmt(sec):
    h = int(sec // 3600); m = int((sec % 3600) // 60); s = sec % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


def transcribe_one(mp4, model):
    base = os.path.splitext(mp4)[0]
    srt_path = base + ".srt"
    txt_path = base + ".txt"
    if os.path.exists(srt_path) and os.path.getsize(srt_path) > 0:
        print(f"  [SKIP] 已有字幕: {os.path.basename(srt_path)}")
        return "skip"
    segments, info = model.transcribe(mp4, language="zh", beam_size=5, vad_filter=True)
    srt, txt = [], []
    for i, seg in enumerate(segments, 1):
        srt.append(f"{i}\n{fmt(seg.start)} --> {fmt(seg.end)}\n{seg.text.strip()}\n")
        txt.append(seg.text.strip())
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(srt))
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(txt))
    print(f"  [OK] {os.path.basename(mp4)} -> {len(txt)} 句 | 语种:{info.language} 置信:{info.language_probability:.2f}")
    return "ok"


def main():
    wd = workdir()
    model_size = sys.argv[1] if len(sys.argv) > 1 else "base"
    targets = sys.argv[2:] if len(sys.argv) > 2 else None
    from faster_whisper import WhisperModel
    print(f">>> 加载模型 whisper-{model_size} (cpu, int8) ...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    if targets:
        files = [t for t in targets if t.endswith(".mp4")]
    else:
        files = sorted(glob.glob(os.path.join(wd, "*.mp4")))
    print(f">>> 待处理 {len(files)} 个视频")
    ok = skip = fail = 0
    for fp in files:
        try:
            r = transcribe_one(fp, model)
            if r == "ok":
                ok += 1
            elif r == "skip":
                skip += 1
        except Exception as e:
            fail += 1
            print(f"  [FAIL] {os.path.basename(fp)}: {e}")
    print(f"\nDONE ok={ok} skip={skip} fail={fail}")


if __name__ == "__main__":
    main()
