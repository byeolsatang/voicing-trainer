#!/usr/bin/env python3
"""
GitHub issue の指示を読んで Claude API に渡し、index.html を修正するスクリプト。
GitHub Actions の環境変数から ANTHROPIC_API_KEY / ISSUE_TITLE / ISSUE_BODY を取得する。
"""

import os
import json
import re
import urllib.request
import urllib.error
import sys

API_KEY   = os.environ["ANTHROPIC_API_KEY"]
TITLE     = os.environ.get("ISSUE_TITLE", "")
BODY      = os.environ.get("ISSUE_BODY", "")
MODEL     = "claude-sonnet-4-6"
MAX_TOKENS = 16000

# 対象ファイル（複数あれば追加可）
TARGET_FILES = ["index.html", "midi-setup-guide.html"]

def read_file(path):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read()
    return None

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def strip_code_fence(text):
    """Claude がコードフェンスで囲んで返した場合に中身だけ取り出す"""
    match = re.search(r"```(?:html)?\n([\s\S]*?)```", text)
    if match:
        return match.group(1)
    return text

def call_claude(prompt):
    payload = json.dumps({
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "messages": [{"role": "user", "content": prompt}]
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
        return result["content"][0]["text"]
    except urllib.error.HTTPError as e:
        print(f"API error: {e.code} {e.read().decode()}", file=sys.stderr)
        sys.exit(1)

def main():
    print(f"Issue: {TITLE}")
    print(f"Body:\n{BODY}\n")

    # 現在のファイル内容を読み込む
    files_content = ""
    for fname in TARGET_FILES:
        content = read_file(fname)
        if content:
            files_content += f"\n\n=== {fname} ===\n{content}"

    prompt = f"""あなたはジャズピアノのロートレスヴォイシング練習アプリ（静的HTML/JS）の開発者です。
以下の GitHub issue の指示に従って、ファイルを修正してください。

## Issue タイトル
{TITLE}

## Issue 内容
{BODY}

## 現在のファイル内容
{files_content}

## 指示
- 修正が必要なファイルだけを返してください
- 各ファイルは以下の形式で返してください（複数ファイルある場合も同様）:

FILE: index.html
```html
（修正後の完全な内容）
```

FILE: midi-setup-guide.html
```html
（修正後の完全な内容）
```

- 変更不要なファイルは返さなくてよいです
- コードの外にコメントや説明を書かないでください
"""

    print("Calling Claude API...")
    response = call_claude(prompt)
    print("Done.\n")

    # レスポンスから各ファイルの内容を抽出して書き込む
    changed = False
    for fname in TARGET_FILES:
        pattern = rf"FILE:\s*{re.escape(fname)}\s*```(?:html)?\n([\s\S]*?)```"
        match = re.search(pattern, response)
        if match:
            new_content = match.group(1)
            write_file(fname, new_content)
            print(f"✅ {fname} を更新しました")
            changed = True
        else:
            print(f"ℹ️  {fname} は変更なし")

    if not changed:
        # フォールバック: FILE: 形式でなければ index.html 全体として扱う
        fallback = strip_code_fence(response)
        if fallback.strip().startswith("<!"):
            write_file("index.html", fallback)
            print("✅ index.html を更新しました（フォールバック）")
        else:
            print("⚠️  変更が見つかりませんでした", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
