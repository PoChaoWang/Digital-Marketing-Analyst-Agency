# Ads Analysis Skill

## Purpose

執行廣告與網站分析任務，產出結構化分析報告。涵蓋 Google Ads、Meta Ads、GA4 onsite behavior、campaign audit、weekly performance、landing page quality 與 cross-channel comparison。

分析結果可直接輸出為 Markdown 報告，或作為結構化 JSON 傳給 `skills/google-sheets-reporting/`。

本 skill 只執行有 recipe 支援的 active workflow。非 recipe-backed 的診斷能力在 `modes/backlog/`，不作為預設執行路徑。

---

## Prerequisites

執行任何分析前，必須完成 `CLAUDE.md` 的 Mandatory Analysis Preflight。Preflight 已涵蓋：

- Environment Gate（見 `policies/environment-gate.md`）
- Routing 與 mode 載入（見 `policies/routing.md`）
- Output language 與 template 選擇（見 `policies/language-policy.md`）
- Safety 與 secret handling（見 `modes/_shared.md`）

以上規則本文件不重複定義。

---

## Recipe Selection

依任務類型選擇對應 recipe：

| 任務類型 | Recipe | 範例指令 |
|---------|--------|---------|
| 平台成效、campaign 總覽、spend / CPA / ROAS 查詢 | `recipes/platform-campaign-performance.yml` | `node scripts/run-recipe.mjs platform-campaign-performance --platform meta_ads` |
| GA4 landing page 品質、paid traffic onsite CVR | `recipes/ga4-landing-page-quality.yml` | `node scripts/run-recipe.mjs ga4-landing-page-quality` |
| 跨平台期間比較、blended CPA / ROAS、attribution sanity check | `recipes/cross-channel-period-compare.yml` | `node scripts/run-recipe.mjs cross-channel-period-compare --start 2026-05-01 --end 2026-05-28 --previous-start 2026-04-03 --previous-end 2026-04-30` |

若任務無法對應任何 active recipe，停止並說明缺口。使用者明確要求時才參考 `modes/backlog/`，並在 Analysis Trace 標記為 backlog/reference-only。

---

## Execution Steps

Preflight 與 routing 完成後，依序執行：

1. 確認對應 recipe，執行 `scripts/run-recipe.mjs`，取得 compact JSON 作為分析依據。
2. 依 routing 結果載入的 `modes/analyses/` 與 `modes/platforms/` 執行診斷。
3. 正規化指標與單位：統一 currency、timezone、attribution window、conversion definition，並在 Analysis Trace 記錄。
4. 產出分析結果，三層分離：
   - **Observation**：只陳述資料直接顯示的事實。
   - **Inference**：根據資料的推論，標明信心程度與假設前提。
   - **Recommendation**：建議行動，標明優先順序與風險等級；高風險建議標注 `Risk: High`。
5. 記錄 Analysis Trace（見下方規格）。
6. 記錄 Data Gaps：資料不足、欄位缺失、無法判斷的項目。
7. 若下一步是 `skills/google-sheets-reporting/`，輸出須符合 `skills/ads-analysis/output.schema.json`。
8. 將完整分析寫入 `output/`（見 Output Rules）。

---

## Analysis Trace 規格

Analysis Trace 必須可供使用者審閱，記錄：

- Preflight 結果
- Environment Gate 結果
- Business context 狀態（provided / not provided）
- 本次載入的 analysis mode 與 platform mode
- 使用的 recipe 與 script
- 資料來源選擇依據與 source_type
- 欄位對應（field mapping）
- 指標計算公式與假設
- 重要決策點與理由

不呈現內部推理過程；只呈現可驗證的執行步驟與資料依據。

---

## Output Rules

### 檔案位置與命名

所有分析任務必須將完整報告寫入 `output/`，不得只回覆在終端機或 chat。

```text
# development / test 環境
output/zzz-test-analysis-{YYYYMMDD-HHMMSS}-{scope}.md

# production 環境
output/analysis-{YYYYMMDD-HHMMSS}-{scope}.md
```

範例：

```text
output/zzz-test-analysis-20260528-143000-cross-channel.md
output/analysis-20260528-143000-google-ads.md
```

### 報告標題

- `APP_ENV=development` 或 `test`：`# This is TEST - {report_title}`
- `APP_ENV=production`：`# {report_title}`

### 終端機 / chat 回覆

只提供簡短摘要（關鍵發現 3 條以內）與 output 檔案路徑，不放完整分析內容。

### 禁止寫入 output/ 的內容

raw source exports、secrets、tokens、credentials、private config values。
