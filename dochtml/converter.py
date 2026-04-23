"""Markdown → HTML 変換コア"""
from __future__ import annotations

import re
from datetime import date as date_type, datetime
from pathlib import Path
from typing import Any

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

_PKG_DIR = Path(__file__).resolve().parent
_TEMPLATE_DIR = _PKG_DIR / "templates"
_THEME_DIR = _PKG_DIR / "themes"

TYPE_LABELS = {
    "report": "レポート",
    "runbook": "手順書",
    "note": "メモ",
    "spec": "仕様書",
}

VALID_TYPES = set(TYPE_LABELS.keys())


def parse_frontmatter(md_text: str) -> tuple[dict[str, Any], str]:
    """先頭の --- ブロックを YAML として切り出して返す

    Returns:
        (frontmatter_dict, body_text) タプル
    """
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", md_text, flags=re.DOTALL)
    if not m:
        return {}, md_text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        fm = {}
    body = md_text[m.end():]
    return fm, body


def _render_markdown(body: str) -> str:
    """markdown 拡張を適用して HTML 本文を返す"""
    md = markdown.Markdown(
        extensions=[
            "fenced_code",
            "codehilite",
            "tables",
            "toc",
            "attr_list",
            "sane_lists",
        ],
        extension_configs={
            "codehilite": {"css_class": "highlight", "guess_lang": False},
            "toc": {"title": "目次", "anchorlink": False, "permalink": False},
        },
    )
    html_body = md.convert(body)

    # [TOC] マーカーが無い場合は本文先頭に挿入
    if "[TOC]" not in body and '<div class="toc">' not in html_body and md.toc_tokens:
        md.reset()
        html_body = md.convert("[TOC]\n\n" + body)
    return html_body


def _normalize_date(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, (date_type, datetime)):
        return v.strftime("%Y-%m-%d")
    return str(v)


def convert(
    md_path: Path | str | None = None,
    *,
    md_text: str | None = None,
    title: str | None = None,
    subtitle: str | None = None,
    author: str | None = None,
    date: str | None = None,
    type: str = "report",
    tags: list[str] | None = None,
) -> str:
    """Markdown を HTML に変換

    md_path または md_text いずれかを指定。
    frontmatter の値は CLI 引数で上書き可能。
    """
    if md_path is not None:
        md_path = Path(md_path)
        md_text_read = md_path.read_text(encoding="utf-8")
    elif md_text is None:
        raise ValueError("md_path か md_text のいずれかを指定してください")
    else:
        md_text_read = md_text

    fm, body = parse_frontmatter(md_text_read)

    # frontmatter < CLI 引数 の優先度でマージ
    ctx_title = title or fm.get("title") or (md_path.stem if md_path else "無題")
    ctx_subtitle = subtitle or fm.get("subtitle")
    ctx_author = author or fm.get("author")
    ctx_date = date or _normalize_date(fm.get("date"))
    ctx_type = type or fm.get("type") or "report"
    ctx_tags = tags or fm.get("tags")

    if ctx_type not in VALID_TYPES:
        raise ValueError(f"type は {VALID_TYPES} のいずれかを指定: {ctx_type}")

    html_body = _render_markdown(body)
    css = (_THEME_DIR / "data_no_mori.css").read_text(encoding="utf-8")

    env = Environment(
        loader=FileSystemLoader(str(_TEMPLATE_DIR)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(f"{ctx_type}.html")
    return template.render(
        title=ctx_title,
        subtitle=ctx_subtitle,
        author=ctx_author,
        date=ctx_date,
        type=ctx_type,
        type_label=TYPE_LABELS.get(ctx_type, ctx_type),
        tags=ctx_tags if isinstance(ctx_tags, list) else None,
        year=(ctx_date[:4] if ctx_date and len(ctx_date) >= 4 else datetime.now().strftime("%Y")),
        body=html_body,
        css=css,
    )
