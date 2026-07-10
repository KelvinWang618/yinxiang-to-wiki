#!/usr/bin/env python3
"""ENEX → Markdown converter for Yinxiang/Evernote exports.

Converts .enex files (exported by evernote-backup) into readable .md files
with YAML frontmatter. Strips HTML tags, preserves plain text structure.

Usage:
    python3 convert_enex.py [--dir <notes_directory>]

Default input: ./.raw/yinxiang-notes/
"""
import re, os, sys, html as html_mod
import xml.etree.ElementTree as ET
from pathlib import Path

def extract_text(html_content):
    text = re.sub(r'<br\s*/?>', '\n', html_content)
    text = re.sub(r'<div[^>]*>', '\n', text)
    text = re.sub(r'</div>', '', text)
    text = re.sub(r'<p[^>]*>', '\n', text)
    text = re.sub(r'</p>', '\n', text)
    text = re.sub(r'<en-media[^>]*/>', '[附件]', text)
    text = re.sub(r'<en-todo[^>]*/>', '[ ] ', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = html_mod.unescape(text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def main():
    # Parse arguments
    raw_dir = "./.raw/yinxiang-notes"
    args = sys.argv[1:]
    if '--dir' in args:
        idx = args.index('--dir')
        if idx + 1 < len(args):
            raw_dir = args[idx + 1]

    raw_path = Path(raw_dir)
    if not raw_path.exists():
        print(f"❌ 目录不存在: {raw_dir}")
        sys.exit(1)

    enex_files = list(raw_path.glob("*.enex"))
    if not enex_files:
        print(f"⚠️  未找到 .enex 文件在 {raw_dir}")
        sys.exit(0)

    total = 0
    for enex_file in enex_files:
        print(f"处理: {enex_file.name}...")
        tree = ET.parse(str(enex_file))
        root = tree.getroot()

        for note in root.findall('note'):
            title = note.findtext('title', '无标题').strip()
            safe_title = re.sub(r'[<>:"/\\|?*]', '-', title).strip()
            if not safe_title:
                safe_title = f'note_{total}'

            content_elem = note.find('content')
            if content_elem is None or not content_elem.text:
                continue

            raw_content = content_elem.text.strip()
            note_text = extract_text(raw_content)

            if note_text and len(note_text) > 5:
                filepath = raw_path / f"{safe_title}.md"
                if filepath.exists():
                    old_len = len(filepath.read_text(encoding='utf-8'))
                    if old_len >= len(note_text) + 50:
                        continue

                filepath.write_text(
                    f"---\ntitle: {title}\nsource: 印象笔记\n---\n\n{note_text}",
                    encoding='utf-8'
                )
                total += 1
                print(f"  ✅ {title} ({len(note_text)} 字)")

        enex_file.unlink()

    print(f"\n===== {total} 条笔记已转换为 Markdown =====")

if __name__ == '__main__':
    main()
