# Smoke Test：跨平台期間比較

## 任務描述

比較 2026-05-08 到 2026-05-14（前期）與 2026-05-16 到 2026-05-22（後期）的跨平台成效。

使用 `test/csv/` 下的 fixture 資料：
- `test/csv/google_ads_raw.csv`
- `test/csv/meta_ads_raw.csv`
- `test/csv/ga4_raw.csv`

APP_ENV=development

---

## 預期 Routing Result

Analysis Trace 裡應出現以下內容，用來驗證 routing 是否正確：

```
Routing Result
──────────────
Intent:          cross-channel
Platforms:       google-ads, meta-ads, ga4
Files to load:
  - modes/_shared.md
  - skills/ads-analysis/SKILL.md
  - modes/analyses/cross-channel.md
  - modes/platforms/google-ads.md
  - modes/platforms/meta-ads.md
  - modes/platforms/ga4.md
  - policies/recipe-runner-policy.md
  - workflows/360-table-workflow.md
Special:         （無）
──────────────
```

---

## 預期 Environment Gate Result

```
Environment Gate Result
───────────────────────
APP_ENV:         development
Data sources:    test/csv/google_ads_raw.csv, test/csv/meta_ads_raw.csv, test/csv/ga4_raw.csv
Fallback used:   （無）
Blocked sources: （無）
───────────────────────
```

---

## 預期執行流程

1. Preflight 完成
2. Routing Result 輸出（如上）
3. Environment Gate 通過
4. 執行 `scripts/combine_to_360_table.py`，產出 `exports/360_table.csv`
5. 執行 `scripts/period_compare_360_table.py`，產出 `exports/period_compare.json`
6. AI 解讀 JSON，產出分析報告
7. 報告寫入 `output/zzz-test-analysis-{timestamp}-cross-channel.md`
8. 終端機只回覆摘要與 output 路徑

---

## 驗證 Checklist

跑完之後確認：

- [ ] Analysis Trace 裡的 Routing Result 與預期一致
- [ ] Environment Gate result 顯示 development，資料來源為 test/csv/
- [ ] `exports/360_table.csv` 有產出
- [ ] `exports/period_compare.json` 有產出
- [ ] `output/` 下有 `zzz-test-` 開頭的 Markdown 檔案
- [ ] 報告標題第一行是 `# This is TEST - ...`
- [ ] 終端機回覆只有摘要與路徑，沒有完整分析內容
- [ ] 報告包含 Observation / Inference / Recommendation 三層
- [ ] 報告包含 Data gaps 區塊