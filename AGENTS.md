# Codex 入口說明

本 repo 的主要 agent 操作手冊是 `CLAUDE.md`。Codex 執行任何分析、文件產出或 MCP 讀取任務時，必須遵守 `CLAUDE.md` 的規則。

同一套規則也適用於任何 CLI、agent runtime、subagent 或 automation runner。除非使用者明確要求跳過，任何分析 / 報表任務在讀取資料或產出結果前，都必須先執行 `CLAUDE.md` 的 `Mandatory Analysis Preflight`。

核心要求：

- 任何 CLI / agent runtime 都必須先跑 `Mandatory Analysis Preflight`，除非使用者明確說不用。
- 每次分析 / 報表任務都必須重新讀取並確認 `config/data-sources.yml` 或 `DATA_SOURCE_CONFIG` 指定檔案；不得沿用上一輪資料來源狀態。
- 先讀 `modes/_shared.md`，再依任務先讀對應 `modes/analyses/`，再讀對應 `modes/platforms/`。
- 分析任務優先使用 `skills/ads-analysis/SKILL.md`。
- Google Sheets 報表任務先分析，再使用 `skills/google-sheets-reporting/SKILL.md` 與 `workflows/weekly-google-sheet-report.md`。
- 優先使用既有 `modes/` 與 `templates/`，不要臨時改寫安全邊界。
- secrets、tokens、client secrets、developer tokens、refresh tokens 不得進 repo。
- 預設只做 read-only analysis。
- 任何 campaign、budget、bid、targeting、creative、tracking、status 的 write action，都必須先取得使用者明確確認。
