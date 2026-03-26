---
name: baidu-humanize
description: 文案去AI味服务，当用户要求"去AI化/人性化/降低AI味/改得像人写的"并希望通过小念AI后端实现而不是手动重写提示词时使用。
---

# Dashboard Humanize（去AI化/人性化）

Use the bundled script to call the existing Dashboard Console API.

## Auth 配置

登录小念后台，在个人设置中复制你的 Access Token，然后在终端中设置：

```bash
export DASHBOARD_TOKEN="your_token_here"
```

或在项目根目录创建 `.env` 文件（确保已加入 `.gitignore`）：

```
DASHBOARD_TOKEN=your_token_here
```

## Quick start

Pipe stdin:

```bash
echo "这里是一段明显AI味的文案..." | python3 skills/local/dashboard-humanize/scripts/humanize.py \
  --title "标题" \
  --tone normal \
  --purpose general_writing \
  --length standard
```

From a file:

```bash
python3 skills/local/dashboard-humanize/scripts/humanize.py --content-file input.txt > output.txt
```

Return full JSON (includes ai_score / detailed_result when available):

```bash
python3 skills/local/dashboard-humanize/scripts/humanize.py --content "..." --json
```

## What to send to the API

Payload fields map 1:1 to `HumanizerRequest`:

- `title` (optional)
- `content` (required)
- `prompt` (optional)
- `length` default `standard` (script choices: short|standard|long)
- `tone` default `normal`
- `purpose` default `general_writing`
- `language` default `Simplified Chinese`

For exact request/response shapes, read: `references/api.md`.

## Notes

- Full route path is `/employee-console/dashboard/v2/api/ai-tools/humanize`.
- Token 通过环境变量 `DASHBOARD_TOKEN` 提供，脚本不内置任何默认凭据。
