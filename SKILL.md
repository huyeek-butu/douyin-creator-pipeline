---
name: douyin-creator-pipeline
description: 批量下载抖音博主全部视频并提取字幕，产出可直接喂 LLM 蒸馏的结构化文本素材（发布文案 + 字幕 .srt/.txt + 合并素材）。This skill should be used when users want to download all videos from a specific Douyin creator, extract subtitles/transcripts via local Whisper, or build text corpora for content distillation. 触发词：抖音下载、抖音博主视频、抖音字幕提取、抖音蒸馏、douyin download、douyin subtitle.
agent_created: true
---

# 抖音创作者内容采集与字幕提取流水线

批量下载指定抖音博主的全部视频，并用本地 Whisper 提取语音字幕，产出可直接喂 LLM 蒸馏的结构化文本素材（发布文案 + 字幕 .srt/.txt + 合并素材）。

## 适用场景

- 用户给出抖音博主主页或单条视频链接，要求"下载该博主所有视频"
- 用户需要抖音视频的文案或字幕，作为内容分析、竞品研究、知识库素材
- 触发词：抖音下载、抖音博主视频、抖音字幕提取、抖音蒸馏、douyin download、douyin subtitle

## 前置条件

### 1. Python 环境与依赖

脚本用 `sys.executable -m yt_dlp` 调用 yt-dlp，依赖当前 Python 已安装以下包：

- `yt-dlp`（视频下载）
- `faster-whisper`（字幕转写）
- `imageio-ffmpeg`（自动定位 ffmpeg，无需系统安装）

在 WorkBuddy managed venv 安装（示例路径，以实际 managed python 为准）：

```
C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe -m pip install -q yt-dlp faster-whisper imageio-ffmpeg
```

### 2. 抖音 cookies.txt（必需）

抖音强制要求登录态 cookie，无 cookie 单条都下不了。获取方式见 `references/cookies_guide.md`。
将导出的 `cookies.txt`（Netscape 格式）放到**工作目录**（运行脚本的目录）。

### 3. 解析 sec_uid

从博主主页短链（如 `https://v.douyin.com/xxxx/`）用 curl 解析 302 跳转即可拿到 sec_uid，**无需 cookie**：

```
curl -sI -L "https://v.douyin.com/xxxx/" | grep -i "^location:"
# 跳转目标含 /user/MS4wLjAB... 或 iesdouyin/share/user/MS4wLjAB...，取 MS4wLjAB 开头那段
```

## 核心流程

所有脚本默认操作**当前工作目录**（或环境变量 `DOUYIN_WORKDIR` 指定的目录），`cookies.txt` / `video_list.json` / `*.mp4` 均在该目录。

### M1 抓取视频 ID 列表

```
python scripts/fetch_video_list.py <sec_uid>
```

调用抖音 web 作品列表 API 翻页，输出 `video_list.json`（含每条视频的 id 与发布文案 desc）。

> 注意：抖音 web 接口裸调（带 cookie + UA + Referer）通常无需 a_bogus 签名即可返回；cookie 失效后会报 `status_code` 非 0，需重新导出 cookies.txt。

### M2 逐条下载视频

```
python scripts/download_videos.py
```

读取 `video_list.json`，对每条用 `yt-dlp` 下载，按 19 位视频 ID 去重（已下的跳过）。

> 注意：yt-dlp 的 Douyin extractor **只支持单条 `/video/{id}` URL**，不支持主页 `/user/{sec_uid}`，所以必须先有 M1 的 ID 列表。

### M3 字幕转写（本地 Whisper）

```
set HF_ENDPOINT=https://hf-mirror.com
set HF_HUB_DISABLE_XET=1
set HF_HUB_ENABLE_HF_TRANSFER=0
python scripts/transcribe.py base
```

逐一对工作目录的 `*.mp4` 转写，输出同名 `.srt`（时间轴）+ `.txt`（纯文本）。支持 model 参数（base/small/...）和指定文件列表。

> 关键环境变量见下方"坑 4"。

### M4 合并素材（可选）

将发布文案（`video_list.json` 的 desc）与字幕（`*.txt`）按视频对应，生成一份 `全部字幕_合并素材.txt`，可直接整份喂 LLM 蒸馏。逻辑简单：遍历 video_list，用 id 匹配同名 .txt 拼接即可，可在工作目录用一段简短脚本实现。

## 关键坑（必读）

1. **抖音强制 cookie**：沙箱/无 cookie 环境完全无法下载，任何方案都先确保 cookies.txt 就绪。
2. **yt-dlp 不支持主页 URL**：必须用 M1 的 API 翻页拿 ID 列表，再逐条下。
3. **云端沙箱读不到本机浏览器**：`yt-dlp --cookies-from-browser edge/chrome` 在云端 WorkBuddy 沙箱里会报 "Could not copy Chrome cookie database"——因为沙箱是独立机器。务必走"手动导出 cookies.txt"方案（本项目已验证唯一可行）。
4. **HuggingFace 模型下载**：沙箱直连 huggingface.co 被墙，且新版 `huggingface_hub` 默认走 Xet 协议（连 `cas-server.xethub.hf.co` 返回 401）。必须设置：
   `HF_ENDPOINT=https://hf-mirror.com` + `HF_HUB_DISABLE_XET=1` + `HF_HUB_ENABLE_HF_TRANSFER=0`
   走国内镜像的普通 HTTP 下载。
5. **沙箱回收站不可用**：转写时可能刷 `safe-delete` 警告，无害，不影响结果。

## 合规提醒

下载内容仅限个人备份/学习/研究，勿二次分发或商用；cookies.txt 含登录凭证，用完建议失效。
