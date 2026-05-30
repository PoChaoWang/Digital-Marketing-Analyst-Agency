# Shared Mode

## Operating Principles
- 預設 read-only analysis。
- 不得以記憶或 benchmark 取代帳戶資料。
- 資料不足時明確說不能判斷，列出需補的資料，不要猜測或編造。
- 每個判斷標明是 Observation、Inference 還是 Recommendation。

## Data Freshness and Date Range Requirements

- 資料有延遲、抽樣、timezone 限制時，必須明確揭露。
- 跨期比較前，確認 period length、weekday mix、seasonality、promotion、budget change 是否可比。

## Metric Definitions

conversion / revenue / CVR / CPA / ROAS / ROI 一律以 GA4 為 source of truth。
平台端 conversions / revenue 只做差異檢查，不作為主要成效判斷。
指標定義見 `docs/GLOSSARY.md`。

## Output Checklist
每份分析輸出必須包含：
- [ ] Date range、platform、account / campaign scope
- [ ] Data sources & Environment Gate result
- [ ] Analysis Trace（含 Routing Result）
- [ ] Executive summary
- [ ] Key findings（Observation / Inference / Recommendation 三層分離）
- [ ] Prioritized actions（高風險建議標注 `Risk: High` 並說明原因）
- [ ] Open questions / data gaps

## Safety Rule

- Read-only by default。Write action 必須先走 `policies/approval-flow.md`。
- 不自動發布、暫停、刪除任何廣告單元。

## Secret Handling

- 不讀取、輸出或保存任何 token / key / secret / credential。
- 發現時提醒使用者 rotate 並移到安全儲存。

