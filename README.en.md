# Yinxiang → Claude Code + Obsidian Knowledge Base

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![中文文档](https://img.shields.io/badge/文档-中文-red)](README.md)

One-click migration of your entire Yinxiang (Evernote China) notebook into a Claude Code + Obsidian AI-powered knowledge base. Auto-classification, PII redaction, incremental sync.

> Built on [claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) and [evernote-backup](https://github.com/vzhd1701/evernote-backup).

---

## TL;DR

**Turn 80+ Yinxiang notes into a structured, AI-queryable knowledge base in 5 minutes.**

---

## What Problem This Solves

| Pain Point | Our Solution |
|------------|-------------|
| Yinxiang App exports are AES-encrypted — unusable by third-party tools | Use evernote-backup cloud API to download unencrypted notes |
| Exported notes are a mess of XML files with no structure | Auto-convert to Markdown + Claude Code auto-classifies into tracks |
| Notes contain ID numbers, bank accounts, passwords | Built-in scanner + redaction script replaces PII before AI ingestion |
| Manual workflow is tedious and error-prone | 5 commands, first run ~10 min, incremental sync ~2 min |

---

## Quick Start

### Prerequisites

- macOS / Linux
- Python 3.10+
- [Obsidian](https://obsidian.md) desktop app
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI (installed & logged in)
- Yinxiang (印象笔记) account credentials

### Step 1: Install

```bash
# Clone the claude-obsidian knowledge base framework
git clone https://github.com/AgriciDaniel/claude-obsidian.git ~/claude-obsidian
cd ~/claude-obsidian
bash bin/setup-vault.sh

# Install dependencies
pip3 install evernote-backup

# Clone this toolkit
git clone https://github.com/KelvinWang618/yinxiang-to-wiki.git
cp yinxiang-to-wiki/scripts/*.py scripts/
```

### Step 2: Sync Yinxiang Notes

```bash
# Authenticate (replace <username> and <password>)
python3 -m evernote_backup init-db --backend china -u <username> -p <password> --force

# Download all notes (~2 min)
python3 -m evernote_backup sync

# Export as unencrypted ENEX files
python3 -m evernote_backup export .raw/yinxiang-notes/
```

### Step 3: Convert & Redact

```bash
python3 scripts/convert_enex.py      # ENEX → Markdown
python3 scripts/scan_sensitive.py    # Scan for PII
python3 scripts/redact_sensitive.py  # Auto-redact sensitive info
```

### Step 4: Ingest into Knowledge Base

```bash
cd ~/claude-obsidian
claude  # Start Claude Code
```

In the Claude Code session, type:

> "Batch ingest all files under .raw/yinxiang-notes/, auto-classify into investment / work / fitness / personal tracks"

---

## How It Works

```
Yinxiang Cloud (89 notes)
    ↓ evernote-backup sync (cloud API, unencrypted)
Local SQLite DB (en_backup.db)
    ↓ export to ENEX (6 notebook files)
Raw ENEX XML
    ↓ convert_enex.py (parse XML, strip HTML)
70+ Markdown files (.md)
    ↓ scan_sensitive.py + redact_sensitive.py
Clean, redacted Markdown
    ↓ Claude Code /wiki ingest
Structured Obsidian vault — 4 tracks (investment / work / fitness / personal)
    ↓
Ask: "Compare Tencent and Nvidia's moat width"
    → Claude reads wiki pages → cross-references → structured answer
```

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/convert_enex.py` | Batch-convert ENEX (XML) to Markdown |
| `scripts/scan_sensitive.py` | Scan for ID cards, phone numbers, bank accounts, passwords, emails |
| `scripts/redact_sensitive.py` | Replace PII with `[REDACTED]` placeholders |

All scripts support `--dir <path>` to specify a custom notes directory.

---

## Incremental Sync

When you add new notes to Yinxiang:

```bash
cd ~/claude-obsidian
python3 -m evernote_backup sync
python3 -m evernote_backup export .raw/yinxiang-notes/
python3 scripts/convert_enex.py
python3 scripts/redact_sensitive.py
# Then in Claude Code: ingest new files from .raw/yinxiang-notes/
```

---

## Redaction Details

### Detection Patterns

| Type | Pattern | Replacement |
|------|---------|------------|
| Chinese ID card | 18-digit with checksum | `[身份证已脱敏]` |
| Mobile phone | 1xx-xxxx-xxxx | `[手机号已脱敏]` |
| Bank card | 16-19 consecutive digits | `[银行卡号已脱敏]` |
| Password | keyword + value | `password: [已脱敏]` |
| Email | user@domain | `[邮箱已脱敏]` |

### Why Redact Before AI Ingestion?

When Claude Code ingests notes, content is sent to Anthropic's API for processing. While Anthropic does not train on API data, redacting personally identifiable information before ingestion is a defense-in-depth best practice.

### Limitations

Regex patterns cannot catch all edge cases. Manually review flagged files before ingestion, especially notes containing financial or identity documents.

---

## Privacy & Security

- **All data stays local**: Notes are stored as plain Markdown files. No cloud sync, no database.
- **Redaction is irreversible**: PII replacement cannot be undone. Keep backups of original exports.
- **API exposure is controlled**: Only redacted content reaches Anthropic's API during ingestion.
- **`账号.md` is auto-excluded**: Files likely containing dense PII are skipped by default.

---

## FAQ

**Q: Why not export directly from the Yinxiang Mac app?**
A: The Mac app only exports AES-encrypted ENEX (with no HTML option). evernote-backup downloads unencrypted notes directly from Yinxiang's cloud API.

**Q: Can the scanner guarantee 100% PII detection?**
A: No. Regex has inherent limitations. Always manually spot-check high-risk files (e.g., financial notes, ID documents) before ingestion.

**Q: What if init-db fails?**
A: Common causes: (1) wrong password, (2) account locked after repeated failed attempts, (3) network issues reaching app.yinxiang.com. Troubleshoot in order.

**Q: How do I migrate to a new machine?**
A: Copy the entire `~/claude-obsidian/` directory and the `en_backup.db` file. On the new machine, just `pip3 install evernote-backup` — no need to re-run init-db.

---

## Related Projects

- [claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) — Claude + Obsidian knowledge companion (our knowledge base engine)
- [evernote-backup](https://github.com/vzhd1701/evernote-backup) — Evernote/Yinxiang backup tool (our cloud sync layer)
- [Karpathy's LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — The vision that inspired this workflow
- [yarle](https://github.com/akosbalasko/yarle) — ENEX to Markdown converter (alternative ENEX parser)
- [llm-wiki-template](https://github.com/bigfish24/llm-wiki-template) — Reusable LLM wiki template for Obsidian

---

## License

MIT © 2026 Kelvin Wang
