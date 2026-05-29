# Recipe Runner And 360 Table Policy

`modes/analyses/` 是 MVP active analysis workflow；`modes/backlog/` 是尚未 recipe-backed 的未來分析假設；`modes/platforms/` 是平台知識；`recipes/` 是固定取數與計算規格；`connectors/` 是 MCP/source adapter；`scripts/` 是 deterministic computation layer；`skills/` 是可重複執行的能力模組；`workflows/` 定義跨 skill 的執行順序。

- Production 資料清洗、360 table 建置與 period compare 腳本統一使用 Python + SQL。
- `scripts/run-recipe.mjs` 暫列 legacy / development-only runner，主要用於 Mock MCP 與舊 recipe 驗證；不要把它當成 production period compare 主流程。
- 對固定 metric lookup、aggregation、platform summary、GA4 landing page quality 這類可重複計算任務，若尚未有 Python + SQL 對應流程且 `recipes/` 中已有對應 recipe，可使用 `scripts/run-recipe.mjs`，但必須在 Analysis Trace 標明它是 legacy/dev runner。
- Recipe runner 的輸出是 compact JSON，AI 只負責解讀結果、標記 data gaps、產生 Observation / Inference / Recommendation。
- `recipes/` 不綁定實際 MCP tool 名稱；實際 tool 對應由 `connectors/*.adapter.yml` 描述。
- Development 可使用 `connectors/mock-mcp.adapter.yml` 與 `test/mock-mcp/`；production 必須使用正式 MCP / warehouse adapter，不能使用 mock source。
- 若沒有 matching recipe，才可由 agent 直接查資料，但必須在 Analysis Trace 說明原因。
- 對跨平台 period compare，優先使用 360 table workflow：先用 `scripts/combine_to_360_table.py` 套用 `sql/build_360_table.sql` 產生 `exports/360_table.csv`，再用 `scripts/period_compare_360_table.py` 產生比較 JSON，最後由 AI 解讀。`recipes/*.yml` 在此流程中作為資料抽取規格、欄位規格與 validation contract。
- 360 table 的 conversion、order、revenue、conversion_value 相關計算必須使用 GA4 欄位，例如 CVR、CPA、ROAS、ROI 使用 `ga4_conversions` 與 `ga4_revenue`，平台回報的 `conversions` / `revenue` 只作為稽核與差異檢查。
- 360 table 是可重建的 derived artifact，預設輸出到 `exports/360_table.csv`；不得把它當成唯一 source of truth。
