#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""公共工具：定位 ffmpeg、确定工作目录。"""
import os


def get_ffmpeg_exe():
    """优先用 imageio-ffmpeg 提供的静态二进制，否则回退到 PATH 里的 ffmpeg。"""
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def workdir():
    """脚本默认操作当前工作目录；可用 DOUYIN_WORKDIR 环境变量覆盖。"""
    return os.environ.get("DOUYIN_WORKDIR", os.getcwd())
