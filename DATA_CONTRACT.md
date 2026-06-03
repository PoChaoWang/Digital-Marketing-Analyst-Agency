# Data Contract

本文件定義 AI Ads Analyst Agent repo 中的 System Layer 與 User Layer 邊界。目標是讓 agent instructions 可以被版本控管，同時避免覆蓋或洩漏使用者資料、客戶資料與 secrets。

## User Layer

以下內容屬於使用者資料或本機執行資料，不應被系統更新覆蓋，也不應提交到 git：

- `.env`
- local MCP credentials
- `config/accounts.yml`
- `config/data-sources.yml`
- `profile/*`
- `data/*`
- `test/public-data/*`
- `reports/*`
- `exports/*`
- `output/*`
- `tmp/recipe-results/*`
- customer/account-specific files
- GA4 property IDs and exported analytics data
- Google Sheet URLs / IDs if tied to customer reports

## System Layer

以下內容屬於 repo 的系統說明、範例與模板，可以提交到 git：

- `CLAUDE.md`
- `AGENTS.md`
- `modes/*`
- `modes/backlog/*`
- `skills/*`
- `recipes/*`
- `connectors/*`
- `scripts/*`
- `workflows/*`
- `templates/*`
- `reference/*`
- `profile.example/*`
- `output/.gitkeep`
- `tmp/recipe-results/.gitkeep`
- `test/.gitkeep`
- `test/csv/.gitkeep`
- `test/csv/*.csv`
- `test/mock-mcp/.gitkeep`
- `test/mock-mcp/*`
- `test/public-data/.gitkeep`
- `.env.example`
- `mcp.example.json`
- `config/accounts.example.yml`
- `config/data-sources.example.yml`
- `templates/analysis-output.md`

## 核心規則

- 使用者資料不可被系統更新覆蓋。
- secrets 不可提交到 git。
- 真實 account IDs 若屬於客戶資料，應視為敏感資料。
- `profile/` 屬於客戶 / 品牌 / 業務情境資料，不應提交到 git；只提交 `profile.example/`。
- report outputs 應放 `reports/`。
- analysis markdown artifacts 應放 `output/`，且不應提交到 git。
- recipe runner 的暫時計算結果應放 `tmp/recipe-results/`，且不應提交到 git。
- raw exports 應放 `exports/` 或 `data/`。
- `data/` 是 manual CSV fallback / local user data，不提交客戶 CSV；只提交 `data/README.md` 與 `data/.gitkeep`。
- Google Sheets 報表是 report artifact；若含客戶資料，Sheet 本身與 URL / ID 應視為 user data。
- `.env.example`、`mcp.example.json`、`config/accounts.example.yml`、`config/data-sources.example.yml` 只能放 placeholder、範例路徑或空值。
- 若 agent 發現 token、key、secret、credential 被貼到 repo，應提醒使用者 rotate 並移出版本控管。
- Production analysis 必須使用明確 allowlist 的正式資料來源；若正式 MCP / warehouse 不可用，必須 fail closed，不得自動 fallback 到 `test/` 或 `data/`。
- 測試資料必須放在 `test/`，並標記為 `csv_fixture`、`mock_mcp`、`public_sample` 或其他 development/test source，不得在報告中呈現為 native platform source。可重現的小型 CSV fixture 與 Mock MCP 可提交；大型 public sample 內容預設不提交。
- `recipes/*` 是資料擷取與計算規格，`connectors/*` 是資料來源 adapter 描述，`scripts/*` 是可重複執行的本機工具。它們不可包含真實 account IDs、customer exports 或 secrets。
- `connectors/mock-mcp.adapter.yml` 只用於 development/test；production MCP 應使用獨立 adapter，不要覆寫 mock adapter。
