# Cross-Channel Mode

## 三層資料來源架構

1. Native MCP Connectors：直接讀取 Google Ads、Meta Ads、GA4 等平台資料。
2. Warehouse Connectors：透過 BigQuery MCP / SQL MCP 讀取已匯入的廣告平台、GA4、CRM、orders、offline conversion、CSV exports。
3. Manual / CSV Import：使用者手動提供資料，AI 只做 read-only analysis。

如果使用者詢問沒有 native MCP 的平台，例如 TikTok Ads、LINE Ads、LinkedIn Ads、Yahoo Ads、Criteo、Amazon Ads、affiliate network、CRM 或 Shopify，先確認資料是否已存在於 BigQuery / SQL warehouse / uploaded CSV。

使用 warehouse data 時，必須明確說明這是資料副本或匯入資料，不代表 AI 能直接修改原平台 campaign。

## 跨平台比較原則

- Google Ads 與 Meta Ads 指標不可直接粗暴比較，要考慮 intent、attribution、placement、funnel stage。
- GA4 應作為 onsite behavior、conversion quality 與 attribution sanity check 的驗證層。
- 不要假設 Google Ads、Meta Ads、GA4 回報的 conversions 可以直接相加或直接比較。
- 必須檢查 attribution window、conversion definition、timezone、lookback window 與去重邏輯。

## Warehouse / SQL / CSV 欄位對齊

跨平台資料應優先對齊以下欄位：

- date
- platform
- account_id
- campaign_id
- campaign_name
- ad_group_id / ad_set_id
- ad_group_name / ad_set_name
- ad_id
- ad_name
- spend
- impressions
- clicks
- conversions
- revenue
- currency

## 統一比較必須標明

- date range
- attribution window
- conversion definition
- currency
- timezone
- GA4 property
- GA4 key event / conversion definition

## 分析

- budget allocation
- blended CPA
- blended ROAS
- funnel coverage
- marginal efficiency
- channel saturation
- reporting inconsistencies
- onsite conversion quality
- landing page performance by channel
- UTM consistency
- attribution mismatch between ad platforms and GA4

## 輸出

- Executive summary
- Channel comparison table
- GA4 onsite quality summary
- Budget reallocation hypothesis
- Risks and assumptions
- Data gaps

