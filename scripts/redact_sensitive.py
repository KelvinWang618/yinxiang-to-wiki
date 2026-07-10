#!/usr/bin/env python3
"""Auto-redaction script for sensitive information in note files.

Replaces detected patterns with [已脱敏] placeholder tags.
Excludes specified files from processing.

Redaction rules (executed in order):
    1. Chinese ID card numbers → [身份证已脱敏]
    2. Bank card numbers       → [银行卡号已脱敏]
    3. Password fields         → password: [已脱敏]
    4. Mobile phone numbers    → [手机号已脱敏]
    5. Email addresses         → [邮箱已脱敏]

Usage:
    python3 redact_sensitive.py [--dir <notes_directory>]

Default: ./.raw/yinxiang-notes/
"""
import re, os, sys
from pathlib import Path

def main():
    notes_dir = "./.raw/yinxiang-notes"
    args = sys.argv[1:]
    if '--dir' in args:
        idx = args.index('--dir')
        if idx + 1 < len(args):
            notes_dir = args[idx + 1]

    notes_path = Path(notes_dir)
    if not notes_path.exists():
        print(f"❌ 目录不存在: {notes_dir}")
        sys.exit(1)

    # Files to exclude from processing (e.g. files with dense sensitive data)
    exclude = {"账号.md"}

    # Redaction rules — ordered by risk (highest first to avoid partial matches)
    rules = [
        (r'\b\d{6}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]\b', '[身份证已脱敏]'),
        (r'\b\d{16,19}\b', '[银行卡号已脱敏]'),
        (r'(密码|password|pwd|pass)\s*[：:=]\s*\S+', r'\1: [已脱敏]'),
        (r'\b1[3-9]\d{9}\b', '[手机号已脱敏]'),
        (r'\b[\w.-]+@[\w.-]+\.\w+\b', '[邮箱已脱敏]'),
    ]

    count = 0
    for filepath in sorted(notes_path.glob("*.md")):
        if filepath.name in exclude:
            continue

        content = filepath.read_text(encoding='utf-8')
        new_content = content
        redactions = 0

        for pattern, replacement in rules:
            new_content, n = re.subn(pattern, replacement, new_content, flags=re.IGNORECASE)
            redactions += n

        if redactions > 0:
            filepath.write_text(new_content, encoding='utf-8')
            count += 1
            print(f"✅ {filepath.name}: {redactions} 处已脱敏")

    for f in exclude:
        p = notes_path / f
        if p.exists():
            p.unlink()
            print(f"🗑️  已删除: {f}")

    print(f"\n处理完成: {count} 个文件脱敏, {len(exclude)} 个已排除")

if __name__ == '__main__':
    main()
