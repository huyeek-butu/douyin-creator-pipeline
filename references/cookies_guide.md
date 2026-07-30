# 获取抖音 cookies.txt

抖音强制要求登录态 cookie，无 cookie 时连单条视频都下载不了。本指引用浏览器扩展导出 Netscape 格式的 cookie 文件。

## 步骤（Edge / Chrome 通用）

1. 用 **Edge 或 Chrome** 打开 `https://www.douyin.com` 并**登录**你的抖音账号。
2. 安装扩展 **Cookie-Editor**（Edge 外接程序商店 / Chrome 网上应用店均有）。
3. 点击扩展图标 → 右上角 **Export** 按钮 → 格式选择 **Netscape**（不要选 JSON）。
4. 将导出内容保存为纯文本文件，命名为 `cookies.txt`。
5. 把 `cookies.txt` 放到你的**工作目录**（即运行本 skill 脚本的目录）。

## 注意事项

- 文件必须是 **Netscape 格式**（以 `# Netscape HTTP Cookie File` 开头），JSON 格式 yt-dlp 不认。
- `cookies.txt` 含登录凭证，**勿外传**；用于一次性下载后，可在抖音网页退出登录使其失效。
- cookie 有时效（通常几天到几周），若下载时报 `status_code` 非 0 或 "fresh cookies needed"，重新导出覆盖即可。
- **云端 WorkBuddy 沙箱无法读取你本机浏览器的 cookie**（`--cookies-from-browser` 会报 "Could not copy Chrome cookie database"），务必走"手动导出文件"这条路。
