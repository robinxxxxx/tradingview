# -*- coding: utf-8 -*-
import os, sys
from dulwich import porcelain
from dulwich.repo import Repo

REPO_DIR = r"C:\Users\m1596\Doubao\chats\2026-09-07\new-chat"
REMOTE = "https://github.com/robinxxxxx/tradingview.git"
USER = "robinxxxxx"
EMAIL = "david7664259@gmail.com"
TOKEN = sys.argv[1]

repo = Repo(REPO_DIR)

# 添加所有文件
os.chdir(REPO_DIR)
for f in os.listdir(REPO_DIR):
    if f.endswith('.csv') or f.endswith('.py'):
        path = os.path.join(REPO_DIR, f)
        if os.path.isfile(path):
            porcelain.add(repo, paths=[path])
            print(f"add: {f}")

# 提交
author = f"{USER} <{EMAIL}>".encode('utf-8')
try:
    cid = porcelain.commit(repo, message=b"update pcr", author=author, committer=author)
    print(f"commit: {cid.decode()}")
except Exception as e:
    print(f"commit: {e}")

# 确保 main 分支指向 HEAD
head = repo.head()
repo.refs[b'refs/heads/main'] = head
print(f"main -> {head.decode()}")

# push main
print("pushing...")
porcelain.push(
    repo,
    remote_location=REMOTE,
    refspecs=b"refs/heads/main:refs/heads/main",
    username=USER.encode(),
    password=TOKEN.encode(),
)
print("DONE! https://github.com/robinxxxxx/tradingview")
