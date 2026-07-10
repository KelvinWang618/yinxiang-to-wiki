#!/usr/bin/env python3
"""Sensitive information scanner for note files.

Scans Markdown files for patterns that may contain personal/private data.

Detected patterns:
    - Chinese ID card numbers (18 digits)
    - Chinese mobile phone numbers
    - Bank card numbers (16-19 consecutive digits)
    - Password fields
    - Email addresses
    - IP addresses
    - License plate numbers

Usage:
    python3 scan_sensitive.py [--dir <notes_directory>]

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

    patterns = {
        '身份证': r'\b\d{6}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]\b',
        '手机号': r'\b1[3-9]\d{9}\b',
        '银行卡': r'\b\d{16,19}\b',
        '密码': r'(密码|password|pwd|pass)\s*[：:=]\s*\S+',
        '邮箱': r'\b[\w.-]+@[\w.-]+\.\w+\b',
        'IP地址': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
        '车牌号': r'\b[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤川青藏琼宁][A-Z][A-HJ-NP-Z0-9]{4,5}[A-HJ-NP-Z0-9挂学警港澳]\b',
    }

    results = {}
    for filepath in sorted(notes_path.glob("*.md")):
        content = filepath.read_text(encoding='utf-8')
        hits = {}
        for name, pattern in patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                unique = list(set(matches))[:5]
                hits[name] = unique

        if hits:
            results[filepath.name] = hits

    if results:
        print(f"⚠️  {len(results)} 个文件含疑似敏感信息：\n")
        for filename, hits in sorted(results.items()):
            print(f"📄 {filename}")
            for name, samples in hits.items():
                masked = [s[:3] + '***' + s[-2:] if len(s) > 6 else '***' for s in samples]
                print(f"   {name}: {', '.join(masked)}")
            print()
    else:
        print("✅ 未发现明显敏感信息")

if __name__ == '__main__':
    main()
