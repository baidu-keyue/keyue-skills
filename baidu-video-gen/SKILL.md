---
name: baidu-video-gen
description: 营销视频生成服务，通过小念AI的视频模块快速生成营销视频：当用户说"快速生成视频/生成一个视频/做个视频/把这个需求直接生成视频"并希望通过小念AI生成结果而不是手动编写时使用。
---

# video-quick-gen

Generate a video end-to-end via dashboard-console.

## Prereqs

- Service base: `https://xiaonian.cc`
- API prefix: `https://xiaonian.cc/employee-console/dashboard/v2/api`
- Auth: 需要在环境变量中配置你的 Bearer Token（见下方 Auth 配置）。

## Auth 配置

登录小念后台，在个人设置中复制你的 Access Token，然后在终端中设置：

```bash
export DASHBOARD_TOKEN="your_token_here"
```

或在项目根目录创建 `.env` 文件（确保已加入 `.gitignore`）：

```
DASHBOARD_TOKEN=your_token_here
```

## Workflow

1) Generate script
- `POST /video/script/gen` → returns `script`

2) Create video task
- `POST /video/task/create` → returns `task_id`

3) Poll until done
- `GET /video/task/state?task_id=...` → returns `status/progress/video_url`

## Quick start

```bash
python3 skills/local/video-quick-gen/scripts/video_quick_gen.py \
  --request "<用户需求，尽量原样保留>" \
  --video-type AUTO \
  --duration 15 \
  --orientation portrait \
  --hd \
  --out /tmp/video.mp4
```

Optional:
- Provide reference image URL: `--image-url "<bos_url>"`
- Disable subtitles: `--no-subtitle`

## Output

JSON returned to the agent (always present):
- `state` — `"SUCCESS"`
- `task_id`
- `script` — the generated video script text (agent should read and summarize this to the user)
- `video_url` — final video URL
- `downloaded_to` — local path (only when `--out` is provided)

After the script runs, summarize both the script content and the video URL to the user.

## Troubleshooting

- status=failed:
  - Check `failed_reason` and backend logs.
