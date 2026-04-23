# DocHTML_Skin

**「データの杜」トーンで Markdown をスタンドアロン HTML に変換**するドキュメント用スキン。

## 特徴

- 🎨 統一トーン (ゴシック + 深緑ヘッダ・フッタ + 和紙色背景)
- 📝 4 テンプレート: `report` / `runbook` / `note` / `spec`
- 🔖 YAML frontmatter でタイトル・作成者・日付を制御
- 📦 スタンドアロン HTML (CSS 埋込、外部依存なし)
- 🔗 コードハイライト (Pygments)
- 📑 目次自動生成

## インストール

```bash
git clone git@github.com:takedais/DocHTML_Skin.git
cd DocHTML_Skin
python3 -m venv venv
./venv/bin/pip install -e .
```

## 使い方

### 最もシンプル

```bash
dochtml report.md              # frontmatter から作成者・タイトル取得
dochtml report.md -o out.html  # 出力先指定
```

### YAML frontmatter の例

```markdown
---
title: 緊急医薬品管理アプリ 本番移行レポート
subtitle: kami-futagoyama から LLMBOX への切替記録
author: 竹田@データの杜
date: 2026-04-23
type: report       # report / runbook / note / spec
---

# 本文はここから (h1 はタイトルに使われるので h2 から始める推奨)
```

### CLI オプション

```bash
dochtml --help
dochtml report.md --type runbook --title "タイトル上書き"
dochtml --list-templates
```

## 4 テンプレート

| タイプ | 用途 | 特徴 |
|---|---|---|
| `report` | 移行レポート、監査レポート | 表紙・目次あり |
| `runbook` | 手順書 | Step 番号強調、チェックリスト |
| `note` | 日々のメモ、議事録 | 余白広め、メタ情報最小 |
| `spec` | 仕様書、設計書 | 目次常時表示、用語集セクション対応 |

## ライセンス

Private / 社内利用
