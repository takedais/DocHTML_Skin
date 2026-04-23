---
title: EmergencyDrug 本番切替 Runbook
subtitle: 2026-04-23 22:00 実施
author: 竹田@データの杜
date: 2026-04-23
type: runbook
---

## Step 0. 事前確認

- kami-futagoyama 到達性
- LLMBOX 到達性

## Step 1. kami 停止

```bash
ssh kami-futagoyama "sudo systemctl stop emergency-drug-api"
```

## Step 6. 整合性検証 (GO/NO-GO)

```bash
./backend/venv/bin/python tools/verify_migration.py \
    data/snapshot_2026-04-22.db \
    /tmp/medicine_inventory_final.db \
    data/medicine_inventory.db
```

exit code 0 = OK、1 = NG。NG の場合は即ロールバック。

## 完了確認

- [x] kami 停止
- [x] ホットバックアップ
- [x] LLMBOX 差替
- [x] 整合性検証 OK
- [ ] 翌朝 Tamamon 緑確認
- [ ] 2026-04-30 に kami 完全削除
