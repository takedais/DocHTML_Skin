---
title: 緊急医薬品管理アプリ 本番移行レポート
subtitle: kami-futagoyama から LLMBOX への切替記録
author: 竹田@データの杜
date: 2026-04-23
type: report
tags:
  - migration
  - emergency-drug
  - llmbox
---

## 1. 背景

kami-futagoyama は LLM を動かす **GPU リソースが不足** していたため、RTX 5090 を 2 枚搭載した LLMBOX にアプリを集約し、メンテナンス先を 1 台に統一する方針を採った。

## 2. 手順

1. kami-futagoyama の停止
2. SQLite ホットバックアップ取得
3. LLMBOX へ転送・差替
4. 整合性検証

```python
def diff_transactions(before: dict, after: dict) -> dict:
    before_ids = set(before.keys())
    after_ids  = set(after.keys())
    return {"new": [after[i] for i in sorted(after_ids - before_ids)]}
```

## 3. 結果

| 指標 | 値 |
|---|---|
| 作業時間 | 32 分 |
| 書込不可期間 | 6 分 |
| 整合性 | exit 0 (完全一致) |
