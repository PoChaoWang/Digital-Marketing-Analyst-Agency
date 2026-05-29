# Workflow Policy

## Ads Analysis Workflow

1. 使用 `skills/ads-analysis/SKILL.md`。
2. 先通過 Environment Gate。
3. 判斷 analysis intent，讀取必要的 `modes/analyses/`。
4. 判斷 involved platforms，讀取必要的 `modes/platforms/`。
5. 若是跨平台 period compare，先使用 360 table workflow；其他 matching recipe 才使用 `scripts/run-recipe.mjs` 產出 compact JSON。
6. 產出符合 `skills/ads-analysis/output.schema.json` 的結構化結果。

## Google Sheets Reporting Workflow

1. 先完成 Ads analysis workflow。
2. 使用 `skills/google-sheets-reporting/SKILL.md`。
3. 依 `templates/google-sheet-weekly-report.md` 建立或更新 Sheet。
4. 驗證 tabs、row counts、date range、scope 與 data gaps。

## Recurring Analysis Workflow

1. 使用 `workflows/recurring-analysis.md` 與 `config/recurring-tasks.yml`。
2. 每次排程執行仍必須重新跑 `Mandatory Analysis Preflight`。
3. 預設只將結果寫入 `output/`；Slack、Teams、Email 或其他 notify channel 未設定前不得假裝已送出通知。
4. 若 production MCP 不可用，使用 `workflows/mcp-setup-wizard.md`，不得產生假資料或靜默 fallback。
5. 若使用者要用對話方式新增、修改、暫停、恢復或刪除固定任務，使用 `workflows/recurring-task-wizard.md`；修改 `config/recurring-tasks.yml` 前必須先顯示摘要並取得明確確認。
