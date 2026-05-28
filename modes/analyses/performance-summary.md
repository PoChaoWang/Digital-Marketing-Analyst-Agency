# Performance Summary Analysis Mode

## 使用情境

使用者要求整體成效、週報、月報、過去 N 天表現、platform comparison、campaign summary、executive summary 時使用此 mode。

先讀 `modes/_shared.md`，再依資料來源讀取相關 platform modes，例如 `modes/platforms/google-ads.md`、`modes/platforms/meta-ads.md`、`modes/platforms/ga4.md`。

## 必查資料

- date range
- platform / account / campaign scope
- data source type and Environment Gate result
- spend, impressions, clicks, conversions, revenue, currency
- GA4 sessions, engaged sessions, key events, landing page data if available
- attribution window and conversion definition if available

## 分析重點

- total spend, conversions, revenue, CPA, ROAS
- CTR, CPC, CVR, CPM
- platform-level and campaign-level outliers
- spend concentration
- high spend low return segments
- GA4 onsite quality sanity check
- data freshness and gaps

## 輸出要求

- Executive summary
- Platform summary table
- Top wins
- Top losses
- Key risks and assumptions
- Prioritized next actions
- Data gaps

所有 observation 必須直接對應資料；inference 必須附 reasoning basis。
