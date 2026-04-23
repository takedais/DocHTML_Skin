---
title: migration_diff ツール 仕様書
author: 竹田@データの杜
date: 2026-04-23
type: spec
---

## 概要

緊急医薬品管理アプリ本番移行時に、DB の移行漏れを検出する検証ツール。

## 入力

- `before.db` — 移行前 SQLite
- `after.db` — 移行後 SQLite

## 出力

HTML レポート:

- 新規取引 (全件)
- 在庫変化一覧
- 時刻別集計

## 検出アルゴリズム

`transactions.id` の集合演算で追加分 (`after - before`) を抽出。
`medicines.current_stock` の値比較で在庫差分を検出。

## 用語集

| 用語 | 定義 |
|---|---|
| ホットバックアップ | `sqlite3.Connection.backup()` で稼働中にスナップショット取得 |
| 整合性検証 | 3 DB 比較で移行の正確性を客観判定 |
