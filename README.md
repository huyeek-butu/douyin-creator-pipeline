# douyin-creator-pipeline

抖音创作者内容采集与字幕提取流水线（WorkBuddy 用户级技能）

一键式把指定抖音博主的**全部视频**批量下载到本地，并用本地 whisper 模型提取语音字幕，产出可直接喂给 LLM 做蒸馏分析的结构化文本素材。

## 功能

- **M1 解析**：输入博主主页分享短链，自动提取 `sec_uid`（无需 cookie）
- **M2 列表**：调用抖音 web 作品列表接口翻页，抓取该博主全部视频 ID（绕过 yt-dlp 不支持主页 URL 的限制）
- **M3 下载**：yt-dlp 逐条下载，按视频 ID 去重
- **M4 字幕**：ffmpeg 抽音 + 本地 faster-whisper 转写，生成 `.srt`（带时间轴）+ 纯文本 `.txt`

## 环境依赖

- Python 3.12+（推荐用 WorkBuddy 托管的隔离 Python）
- `yt-dlp`、`imageio-ffmpeg`、`faster-whisper`（用 `pip install` 装进隔离 venv）
- 一个有效的抖音登录 Cookie（`cookies.txt`）

## 安装

将本目录整体复制到 WorkBuddy 用户级技能目录：

```
C:\Users\<你的用户名>\.workbuddy\skills\douyin-creator-pipeline\
```

或直接用 Release 里的 zip 解压到该目录。

## 使用流程

1. **准备 Cookie**：用 Edge / Chrome 安装扩展 **Cookie-Editor**，打开 https://www.douyin.com 并登录，点 Export 选 **Netscape** 格式，保存为 `cookies.txt` 放在工作目录。详见 `references/cookies_guide.md`。
2. **提供博主主页链接**：把抖音 App 里博主主页的「分享 → 复制链接」发给我（形如 `https://v.douyin.com/xxxx/`）。
3. **运行流水线**：我会自动执行 M1→M4，把视频、字幕、发布文案、合并素材输出到工作目录。

## 已知坑（已在 SKILL.md 详细记录）

1. 抖音强制要求登录 Cookie，无 cookie 连单条视频都下不了
2. yt-dlp 的抖音 extractor 只认 `/video/{id}`，不认主页 `/user/{sec_uid}` —— 必须靠接口翻页抓 ID
3. 云端沙箱与用户本机隔离，`--cookies-from-browser` 物理不可行，只能手动导出 cookie 文件
4. HuggingFace 直连被墙 + 新版 `huggingface_hub` 默认 Xet 协议 401 —— 必须设 `HF_ENDPOINT=https://hf-mirror.com` 且 `HF_HUB_DISABLE_XET=1`
5. 沙箱回收站不可用，`safe-delete` 警告无害

## 免责声明

本工具仅用于个人备份与学习研究，请遵守抖音用户协议，勿将下载内容二次分发或商用。

## License

MIT
