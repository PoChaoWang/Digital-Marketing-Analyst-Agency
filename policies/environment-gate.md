# Environment Gate

任何分析、文件產出或報表任務在讀取 `test/`、`data/`、`exports/`、MCP 或 warehouse 之前，必須先確認目前環境與資料來源 allowlist：

1. 讀取 `APP_ENV`；若未設定，預設視為 `development`，但必須在輸出中揭露。
2. 讀取 `DATA_SOURCE_CONFIG`；若未設定，預設檢查 `config/data-sources.yml`。
3. 若 `config/data-sources.yml` 存在，先用其中 `enabled`、`environment`、`source_type`、`production_allowed` 決定可用資料來源。
4. `APP_ENV=production` 時，只能使用 `enabled: true` 且 `production_allowed: true` 的正式來源；不得讀取 `test/` 或 `source_type: csv_fixture` / `mock_mcp` / `public_sample`。`data/` 只有在 `manual_csv_fallback` 啟用，或使用者明確提供 CSV file path 時可讀取，且必須標示為 `csv_export` / manual source。
5. `APP_ENV=development` 或 `test` 時，只有 allowlist 中 enabled 且環境相符的 `test/` 來源可以使用；測試 CSV、Mock MCP server 與官方 / 公開測試資料都應放在 `test/` 底下。
6. 若 allowlist 不存在或沒有符合環境的來源，必須先回報缺少可用資料來源；不可自動掃描 `data/` 當作 fallback。
7. `data/` 只可作為 explicit manual CSV fallback。MCP / warehouse 失效時，不得自動讀取 `data/`；必須由使用者明確提供檔案或在 `config/data-sources.yml` 啟用 `manual_csv_fallback`。即使在 production，`data/` 也只能作為手動匯入資料來源，不得呈現為 native MCP。
8. Manual CSV fallback 不要求固定檔名，但必須透過明確檔案路徑、allowlist entry 或平台必要欄位驗證確認來源。
9. 若使用者的問題明顯需要 `data/` 中的手動 CSV，但目前 `APP_ENV` / allowlist 只允許 `test/`、Mock MCP 或其他不匹配來源，必須先停止並向使用者確認要使用哪些 `data/` 檔案或是否要調整 `config/data-sources.yml`；不得直接改用不相干的 enabled source 產生分析。
10. 若分析 / 報表任務需要 production MCP，但沒有任何允許且可用的 production MCP source，讀取並使用 `workflows/mcp-setup-wizard.md` 啟動對話式設定流程；若使用者不想設定，必須停止分析或改請使用者明確提供允許的 manual CSV fallback。

每次分析輸出都必須在 `Data sources` 與 `Analysis Trace` 中顯示 Environment Gate 的判斷結果。
