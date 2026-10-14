# -*- coding: utf-8 -*-
"""直接用 GitHub API 上传文件"""
import base64, os, sys, requests

TOKEN = sys.argv[1]
REPO = "robinxxxxx/tradingview"
DIR = r"C:\Users\m1596\Doubao\chats\2026-09-07\new-chat"

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

files = [f for f in os.listdir(DIR) if f.endswith('.csv') or f.endswith('.py')]
print(f"准备上传 {len(files)} 个文件: {files}")

for fname in files:
    path = os.path.join(DIR, fname)
    with open(path, 'rb') as f:
        content = base64.b64encode(f.read()).decode()

    url = f"https://api.github.com/repos/{REPO}/contents/{fname}"

    # 检查文件是否已存在
    r = requests.get(url, headers=HEADERS)
    sha = r.json().get('sha') if r.status_code == 200 else None

    data = {
        "message": f"update {fname}",
        "content": content,
        "branch": "main"
    }
    if sha:
        data["sha"] = sha

    r = requests.put(url, headers=HEADERS, json=data)
    if r.status_code in (200, 201):
        print(f"  OK: {fname}")
    else:
        print(f"  FAIL: {fname} -> {r.status_code} {r.text[:200]}")

print(f"\n完成! https://github.com/{REPO}")
