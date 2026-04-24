"""dochtml CLI"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .converter import convert, VALID_TYPES, TYPE_LABELS
from . import __version__


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="dochtml",
        description="Markdown を「データの杜」トーンのスタンドアロン HTML に変換",
    )
    p.add_argument("input", nargs="?", help="Markdown ファイルパス")
    p.add_argument("-o", "--output", help="出力 HTML パス (省略時は入力.html)")
    p.add_argument("--type", choices=sorted(VALID_TYPES), help="テンプレ種別")
    p.add_argument("--title", help="タイトル (frontmatter を上書き)")
    p.add_argument("--subtitle", help="サブタイトル")
    p.add_argument("--author", help="作成者 (frontmatter を上書き)")
    p.add_argument("--date", help="日付 YYYY-MM-DD")
    p.add_argument("--tags", nargs="*", help="タグ (複数可)")
    p.add_argument("--list-templates", action="store_true", help="テンプレ一覧表示")
    p.add_argument("--stdout", action="store_true", help="HTML を標準出力に出力")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return p


def main() -> int:
    args = build_parser().parse_args()

    if args.list_templates:
        print("利用可能なテンプレート:")
        for k, v in TYPE_LABELS.items():
            print(f"  {k:8s} — {v}")
        return 0

    if not args.input:
        print("入力ファイルを指定してください。--help でヘルプ。", file=sys.stderr)
        return 2

    in_path = Path(args.input).resolve()
    if not in_path.exists():
        print(f"ファイルが見つかりません: {in_path}", file=sys.stderr)
        return 1

    html = convert(
        in_path,
        title=args.title,
        subtitle=args.subtitle,
        author=args.author,
        date=args.date,
        type=args.type,  # None なら frontmatter → デフォルト "report" の順で解決
        tags=args.tags,
    )

    if args.stdout:
        sys.stdout.write(html)
        return 0

    out_path = Path(args.output) if args.output else in_path.with_suffix(".html")
    out_path.write_text(html, encoding="utf-8")
    print(f"wrote: {out_path} ({len(html):,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
