#!/usr/bin/env python3
"""Call Dashboard Console /ai-tools/humanize (内容人性化/去AI化).

Supports:
- Bearer token provided via env DASHBOARD_TOKEN (required)
- content via --content or stdin

Exit codes:
- 0 success
- 2 bad args
- 3 auth failed (missing token)
- 4 request failed
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, Optional


DEFAULT_DASHBOARD_BASE_URL = "https://xiaonian.cc"
API_PREFIX = "/employee-console/dashboard/v2/api"


def _http_json(method: str, url: str, body: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, timeout_s: int = 300) -> Dict[str, Any]:
    data = None
    req_headers = {"Content-Type": "application/json"}
    if headers:
        req_headers.update(headers)

    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=req_headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            raw = resp.read().decode("utf-8")
            if not raw:
                return {}
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} {e.reason}: {raw}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e}") from e


def _get_token() -> Optional[str]:
    """Return token from DASHBOARD_TOKEN env var, or None if not set."""
    return os.getenv("DASHBOARD_TOKEN") or None


def _read_content(args: argparse.Namespace) -> str:
    if args.content is not None:
        return args.content

    if args.content_file:
        with open(args.content_file, "r", encoding="utf-8") as f:
            return f.read()

    # stdin
    if not sys.stdin.isatty():
        return sys.stdin.read()

    raise ValueError("No content provided. Use --content, --content-file, or pipe stdin.")


def main() -> int:
    ap = argparse.ArgumentParser(description="Dashboard Console: /ai-tools/humanize (去AI化/人性化)")
    ap.add_argument("--base-url", default=os.getenv("DASHBOARD_BASE_URL", DEFAULT_DASHBOARD_BASE_URL), help="Dashboard base url, e.g. https://xiaonian.cc")

    ap.add_argument("--title", default="", help="Content title")
    ap.add_argument("--content", default=None, help="Content text")
    ap.add_argument("--content-file", default=None, help="Read content from a UTF-8 text file")

    ap.add_argument("--prompt", default="", help="Custom prompt")
    ap.add_argument("--length", default="standard", choices=["short", "standard", "long"], help="Length type")
    ap.add_argument("--tone", default="normal", help="Tone, e.g. normal/professional/friendly")
    ap.add_argument("--purpose", default="general_writing", help="Purpose, e.g. general_writing/marketing")
    ap.add_argument("--language", default="Simplified Chinese", help="Language")

    ap.add_argument("--json", action="store_true", help="Output full JSON response")
    ap.add_argument("--no-auth", action="store_true", help="Do not send Authorization header (only works if endpoint allows anonymous access)")

    args = ap.parse_args()

    try:
        content = _read_content(args)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 2

    base_url = args.base_url.rstrip("/")
    url = base_url + API_PREFIX + "/ai-tools/humanize"

    headers: Dict[str, str] = {}
    if not args.no_auth:
        token = _get_token()
        if not token:
            print(
                "Missing auth. Set env DASHBOARD_TOKEN to your bearer token.",
                file=sys.stderr,
            )
            return 3
        headers["Authorization"] = f"Bearer {token}"

    payload = {
        "title": args.title,
        "content": content,
        "prompt": args.prompt,
        "length": args.length,
        "tone": args.tone,
        "purpose": args.purpose,
        "language": args.language,
    }

    try:
        resp = _http_json("POST", url, payload, headers=headers)
    except Exception as e:
        print(f"Request failed: {e}", file=sys.stderr)
        return 4

    if args.json:
        print(json.dumps(resp, ensure_ascii=False, indent=2))
        return 0

    # Dashboard convention: {"success": true, "data": {...}, "message": "..."}
    data = resp.get("data") if isinstance(resp, dict) else None
    if isinstance(data, dict) and ("content" in data or "title" in data):
        title = data.get("title") or ""
        out_content = data.get("content") or ""
        if title:
            print(title.strip())
            print()
        print(out_content.strip())
        return 0

    # Fallback
    print(json.dumps(resp, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
