# Environment Gate

任何分析任務在讀取任何資料來源之前，依序執行以下三個確認。

---

## Step 1：確認環境

1. 讀取 `APP_ENV`；若未設定，預設為 `development`，並在輸出中揭露。
2. 讀取 `DATA_SOURCE_CONFIG`；若未設定，預設讀 `config/data-sources.yml`。

---

## Step 2：確認可用資料來源

依 `APP_ENV` 套用對應規則：

| APP_ENV | 可用來源條件 | 禁止來源 |
|---------|------------|---------|
| `production` | `enabled: true` 且 `production_allowed: true` | `test/`、`csv_fixture`、`mock_mcp`、`public_sample` |
| `development` / `test` | `enabled: true` 且環境相符的 allowlist 來源 | production MCP、正式 warehouse |

**`data/` 的特別規則（所有環境適用）：**
- 只能作為 explicit manual CSV fallback，不得自動讀取。
- 允許條件：使用者明確提供檔案路徑，**或** `config/data-sources.yml` 啟用 `manual_csv_fallback`。
- 即使在 production，`data/` 也只能標示為手動匯入來源，不得呈現為 native MCP。

**CSV 欄位判斷原則：**
- Environment Gate 只確認來源是否被授權，不驗證欄位內容。
- CSV 欄位是否足夠由分析任務本身判斷：agent 讀取 CSV 後，自行評估現有欄位能支援哪些分析、缺少哪些維度，並在 Data Gaps 中回報不足之處。
- 不因欄位不完整而拒絕讀取；而是讀取後說明可做什麼、不可做什麼。

---

## Step 3：無可用來源時的處理

| 情況 | 動作 |
|------|------|
| 需要 production MCP，但無可用來源 | 執行 `workflows/mcp-setup-wizard.md`；使用者不想設定則停止分析 |
| 需要 `data/` CSV，但環境只允許 test 來源 | 停止，詢問使用者要提供哪些檔案或是否調整 `config/data-sources.yml` |
| allowlist 不存在或無符合環境的來源 | 停止，回報缺少可用資料來源；不自動掃描任何資料夾 |

任何情況下，不得以「找不到可用來源」為由自動改用不相關的 enabled source 產生分析。

---

## Gate Result 輸出

每次分析輸出必須在 `Data sources` 與 `Analysis Trace` 中記錄：

```
Environment Gate Result
───────────────────────
APP_ENV:         [production | development | test]
Data sources:    [列出本次使用的來源與 source_type]
Fallback used:   [若有，說明原因]
Blocked sources: [若有，說明為何被排除]
───────────────────────
```