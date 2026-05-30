# Recipe Runner And 360 Table Policy

## 架構說明

- `modes/analyses/`：MVP active analysis workflow
- `modes/backlog/`：尚未 recipe-backed 的未來分析假設
- `modes/platforms/`：平台知識
- `recipes/`：固定取數與計算規格
- `connectors/`：MCP / source adapter
- `scripts/`：deterministic computation layer
- `skills/`：可重複執行的能力模組
- `workflows/`：跨 skill 的執行順序

---

## Script 使用規則

- Production 資料清洗、360 table 建置與 period compare 統一使用 Python + SQL。
- `scripts/run-recipe.mjs` 是 legacy / development-only runner，主要用於 Mock MCP 與舊 recipe 驗證；不得作為 production period compare 主流程。
- 對固定 metric lookup、aggregation、platform summary、GA4 landing page quality 這類可重複計算任務，若尚未有 Python + SQL 對應流程且 `recipes/` 中已有對應 recipe，可使用 `scripts/run-recipe.mjs`，但必須在 Analysis Trace 標明它是 legacy/dev runner。
- 若沒有 matching recipe，才可由 agent 直接查資料，但必須在 Analysis Trace 說明原因。

---

## Recipe 與 Connector 規則

- Recipe runner 的輸出是 compact JSON，AI 只負責解讀結果、標記 data gaps、產生 Observation / Inference / Recommendation。
- `recipes/` 不綁定實際 MCP tool 名稱；實際 tool 對應由 `connectors/*.adapter.yml` 描述。
- Development 可使用 `connectors/mock-mcp.adapter.yml` 與 `test/mock-mcp/`；production 必須使用正式 MCP / warehouse adapter，不能使用 mock source。

---

## 跨平台 Period Compare

執行流程與 GA4 metric policy 見 `workflows/360-table-workflow.md`。

重點摘要：
- 優先使用 360 table workflow，`recipes/*.yml` 在此流程中作為資料抽取規格、欄位規格與 validation contract。
- CVR / CPA / ROAS / ROI 使用 GA4 欄位（`ga4_conversions`、`ga4_revenue`）；平台端 `conversions` / `revenue` 只作為稽核與差異檢查。
- 360 table 是可重建的 derived artifact，不得當成唯一 source of truth。