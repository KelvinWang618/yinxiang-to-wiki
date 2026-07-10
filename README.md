# 印象笔记 → Claude Code + Obsidian 知识库

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)

一键将印象笔记全部内容导入 Obsidian + Claude Code 知识库，支持自动分类、敏感信息脱敏、增量同步。

> 基于 [claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) 和 [evernote-backup](https://github.com/vzhd1701/evernote-backup) 构建。

---

## 一句话说明

**印象笔记里的几十上百条笔记，5 分钟全部变成 AI 可读、可问答的结构化知识库。**

---

## 解决了什么问题

| 痛点 | 本方案 |
|------|--------|
| 印象笔记 App 导出加密，第三方工具打不开 | 用 evernote-backup 从云端 API 下载不加密的笔记 |
| 导出后一堆文件不知道怎么整理 | 自动转 Markdown + Claude Code 自动归类 |
| 笔记含身份证、银行卡、密码等隐私 | 内置扫描+脱敏脚本，ingest 前自动替换 |
| 每次手动操作太麻烦 | 5 条命令，首次 10 分钟，增量 2 分钟 |

---

## 效果演示

```
印象笔记 80 条笔记
    ↓ evernote-backup sync（2 分钟）
本地数据库（不加密）
    ↓ export + convert（30 秒）
70 个 Markdown 文件
    ↓ scan + redact（10 秒）
脱敏后的干净文件
    ↓ Claude Code /wiki ingest（3 分钟）
Obsidian 知识库 — 自动分为投资/工作/运动/个人四赛道
    ↓
问"腾讯和绿的谐波哪个护城河更宽？"
    → Claude 读 wiki 页面 → 交叉对比 → 给出结构化回答
```

---

## 快速开始

### 环境要求

- macOS / Linux
- Python 3.10+
- [Obsidian](https://obsidian.md) 桌面版
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI
- 印象笔记账号

### 第一步：安装

```bash
# 克隆 claude-obsidian 项目（知识库框架）
git clone https://github.com/AgriciDaniel/claude-obsidian.git ~/claude-obsidian
cd ~/claude-obsidian
bash bin/setup-vault.sh

# 安装依赖
pip3 install evernote-backup

# 下载本项目脚本
git clone https://github.com/KelvinWang618/yinxiang-to-wiki.git
cp yinxiang-to-wiki/scripts/*.py scripts/
```

### 第二步：同步印象笔记

```bash
# 初始化并登录（替换为你的印象笔记用户名和密码）
python3 -m evernote_backup init-db --backend china -u <用户名> -p <密码> --force

# 同步全部笔记
python3 -m evernote_backup sync

# 导出为不加密的 ENEX
python3 -m evernote_backup export .raw/yinxiang-notes/
```

### 第三步：转换 + 脱敏

```bash
python3 scripts/convert_enex.py      # ENEX → Markdown
python3 scripts/scan_sensitive.py    # 扫描敏感信息
python3 scripts/redact_sensitive.py  # 自动脱敏
```

### 第四步：导入知识库

```bash
claude  # 在 ~/claude-obsidian 目录启动
```

在 Claude Code 对话中输入：

> 批量 ingest .raw/yinxiang-notes/ 目录下的所有文件，按四赛道自动分类归档

---

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `scripts/convert_enex.py` | 将 ENEX（XML）批量转为 Markdown |
| `scripts/scan_sensitive.py` | 扫描身份证/手机号/银行卡/密码/邮箱等敏感信息 |
| `scripts/redact_sensitive.py` | 将敏感信息替换为 `[已脱敏]` |

---

## 增量更新

印象笔记有新笔记后：

```bash
cd ~/claude-obsidian
python3 -m evernote_backup sync
python3 -m evernote_backup export .raw/yinxiang-notes/
python3 scripts/convert_enex.py
python3 scripts/redact_sensitive.py
# 然后在 Claude Code 里：ingest .raw/yinxiang-notes/ 下的新文件
```

---

## 隐私与安全

- **所有数据本地存储**：笔记以 Markdown 文件保存在本地，无云端同步
- **脱敏不可逆**：敏感信息替换后无法还原，建议操作前备份
- **Ingest 后 Claude 能读**：Claude Code 读取笔记时会发送内容到 Anthropic API 处理。脱敏后 ingest 是安全的
- **账号.md 默认排除**：含密集敏感信息的文件会被脚本自动跳过

---

## 相关项目

- [claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) — Claude + Obsidian 知识伴侣
- [evernote-backup](https://github.com/vzhd1701/evernote-backup) — Evernote/印象笔记备份工具
- [Karpathy's LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — 核心理念来源

---

## License

MIT © 2026 Kelvin Wang
