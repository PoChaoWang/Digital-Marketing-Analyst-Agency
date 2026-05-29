# Routing Policy

所有任務都先讀 `modes/_shared.md`，再依需求讀取 active analysis modes 與 platform modes。Routing 順序是：先判斷 analysis intent，再判斷 involved platforms。

MVP active analysis modes 只包含目前有 recipe 支援、可重複執行的三條 workflow：

- 成效總覽、週報、月報、過去 N 天成效：讀 `modes/analyses/performance-summary.md`。
- landing page、onsite quality、paid traffic CVR：讀 `modes/analyses/landing-page-quality.md`。
- 跨平台比較、blended CPA/ROAS、channel allocation：讀 `modes/analyses/cross-channel.md`。

`modes/backlog/` 是尚未 recipe-backed 的分析假設與未來擴充素材，不是 MVP active workflow。除非使用者明確要求參考 backlog，否則不要把 backlog mode 當作正式執行步驟。

- 一般廣告、GA4、跨平台分析任務：使用 `skills/ads-analysis/SKILL.md`，並先讀對應 `modes/analyses/`，再讀對應 `modes/platforms/`。
- 需要產出 Google Sheet 報表：先使用 `skills/ads-analysis/SKILL.md` 產出結構化分析，再使用 `skills/google-sheets-reporting/SKILL.md`，並依 `workflows/weekly-google-sheet-report.md` 執行。
- CPA 上升、轉換成本過高、conversion efficiency：若可用現有 recipe 回答，使用 `modes/analyses/performance-summary.md` 或 `modes/analyses/cross-channel.md`；若需要更深診斷，標記為 backlog capability，參考 `modes/backlog/cpa-diagnosis.md` 前先告知使用者目前尚非 active workflow。
- 預算 pacing、budget allocation、reallocation hypothesis：若可用現有 recipe 回答，使用 `modes/analyses/performance-summary.md` 或 `modes/analyses/cross-channel.md`；若需要 pacing 專用診斷，標記為 backlog capability，參考 `modes/backlog/budget-pacing.md` 前先告知使用者目前尚非 active workflow。
- creative fatigue、素材疲乏、frequency/CTR/CPA trend：若可用現有 recipe 回答，使用 `modes/analyses/performance-summary.md`；若需要素材疲乏專用診斷，標記為 backlog capability，參考 `modes/backlog/creative-fatigue.md` 前先告知使用者目前尚非 active workflow。
- conversion tracking、attribution mismatch、UTM/gclid/fbclid、GA4 與平台數字不一致：若可用現有 recipe 回答，使用 `modes/analyses/landing-page-quality.md` 或 `modes/analyses/cross-channel.md`；若需要 tracking 專用診斷，標記為 backlog capability，參考 `modes/backlog/attribution-tracking.md` 前先告知使用者目前尚非 active workflow。
- Google Ads 資料或 Google Ads 平台特有問題：讀 `modes/platforms/google-ads.md`。
- Meta Ads 資料或 Meta Ads 平台特有問題：讀 `modes/platforms/meta-ads.md`。
- GA4、onsite behavior、traffic acquisition、landing page、conversion tracking、attribution sanity check 資料：讀 `modes/platforms/ga4.md`。
- 沒有 native MCP 的廣告平台或資料來源：先通過 Environment Gate，確認 `APP_ENV` 與 `config/data-sources.yml` allowlist，再依允許來源檢查 BigQuery / SQL warehouse / uploaded CSV data。
- 遇到 campaign、ad set、ad、creative、UTM 或欄位縮寫時，讀 `docs/GLOSSARY.md` 做名詞對照；找不到的縮寫要標記為 unknown term。
