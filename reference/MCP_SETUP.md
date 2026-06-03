# MCP Setup Guide

本文件比 README 更詳細，專門說明 AI Ads Analyst Agent 的 MCP 設定、安全原則與常見問題。

## MCP 是什麼

MCP（Model Context Protocol）是一種讓 agent runtime 連接外部工具與資料來源的協定。對本 repo 來說，MCP server 可以把 Google Ads、Meta Ads、GA4、BigQuery 或 SQL database 暴露給 agent 使用。

MCP tools 是廣告與分析帳戶資料的 source of truth。agent 不應憑記憶或猜測產生帳戶數字。

## MCP Server 與 Agent Runtime 的關係

MCP server 是提供工具的一端；agent runtime 是執行 AI agent 並載入 MCP server 的環境。Claude Desktop、Claude Code、Codex、Cursor、Windsurf 或其他支援 MCP 的工具，都可能有不同 config 路徑與格式。

本 repo 的 `mcp.example.json` 只是範例。請把概念移植到你的 runtime config。

如果要產出 Google Sheets 報表，runtime 也需要提供 Google Sheets 或 Google Drive 相關 MCP tools。這些 tools 負責建立 spreadsheet、建立 tabs、寫入 values、套用格式與讀回驗證。不同 runtime 的 tool name 可能不同，本 repo 不假設固定名稱。

## Repo 內哪些檔案是範例，哪些不能提交

可以提交：

- `.env.example`
- `mcp.example.json`
- `config/accounts.example.yml`
- `config/data-sources.example.yml`
- `CLAUDE.md`
- `AGENTS.md`
- `modes/*`
- `templates/*`
- `reference/*`

不能提交：

- `.env`
- `.env.*`，但 `.env.example` 例外
- `config/accounts.yml`
- `config/data-sources.yml`
- `data/*`
- `test/public-data/*`
- `reports/*`
- `exports/*`
- OAuth token、refresh token、developer token、client secret、service account private key

## Local `.env` 設定

`.env.example` 只放變數名稱。請建立 `.env` 並填入真實值。若 runtime 不會自動載入 `.env`，請改用 runtime 自己的 secrets 設定，或用 shell / process manager 注入環境變數。

## OAuth Token / Refresh Token / Developer Token 安全原則

- 使用最小權限 scope。
- 不把 token 貼進 prompt、README、issue、commit message、log。
- 不把 token 存進 `data/`、`reports/`、`exports/`。
- 若懷疑外洩，立即 rotate。
- 定期盤點仍在使用的 OAuth client、refresh token、service account key。

## Google Ads 常見 Credentials

- OAuth client ID：OAuth app 的 client ID。
- OAuth client secret：OAuth app 的 client secret。
- Developer token：Google Ads API developer token。
- Refresh token：讓 MCP server 取得 access token 的長期憑證。
- Login customer ID：manager account / MCC 情境常用。
- Customer ID：實際分析的 Google Ads account。

不同 Google Ads MCP server 可能需要 handle 不同變數名稱，請以實際 server 文件為準。

## Meta Ads 常見 Credentials

- App ID：Meta app ID。
- App secret：Meta app secret。
- Access token：可讀取 ad account insights 的 token。
- Ad account ID：常見格式為 `act_...`。
- Business ID：Meta Business account ID。

請確認 token 具有讀取 ads insights、campaign、ad set、ad、creative、pixel/event 相關資料的權限。

## GA4 常見 Credentials

- GA4 property ID：要查詢的 GA4 property。
- Service account JSON：server-to-server 存取常用。
- OAuth client ID / secret / refresh token：代表使用者授權存取。

### GA4 Service Account 與 OAuth 的差異

Service account 適合固定 server 或 automated analysis。需要把 service account email 加到 GA4 property，並授予適當權限。

OAuth 適合代表使用者讀取其可存取的 GA4 property。需要處理 consent、refresh token 與 scope。

### GA4 Data API 權限與 Property Access

- 確認 Google Analytics Data API 已啟用。
- 確認 service account 或 OAuth user 對 GA4 property 有存取權。
- 確認使用的是正確 property ID。
- 若查不到 ecommerce revenue 或 key events，檢查事件是否被設定為 key event，以及資料是否已進 GA4。

## BigQuery MCP / SQL MCP 使用情境

BigQuery MCP / SQL MCP 適合：

- 沒有 native MCP 的平台資料。
- 已由 ETL 匯入的 Google Ads、Meta Ads、TikTok Ads、LINE Ads、LinkedIn Ads、Yahoo Ads、Criteo、Amazon Ads、affiliate、CRM、Shopify、orders、offline conversions。
- 已匯入 warehouse 的 GA4 或 CSV exports。
- 需要跨平台、跨系統 join 與 blended metrics 的分析。

BigQuery / SQL MCP 是 read-only analytics source。除非另有 native write connector，agent 不得宣稱可以把建議直接套用回來源平台。

## Google Sheets / Google Drive MCP 使用情境

Google Sheets / Google Drive MCP 適合：

- 建立 weekly performance report。
- 更新既有 Google Sheet 報表。
- 寫入 platform summary、campaign detail、GA4 onsite quality、findings、recommended actions、data gaps。
- 讀回 Sheet metadata 或 tab row counts 進行驗證。

建立或更新 Google Sheet 是報表 artifact 寫入，不是廣告帳戶 write action。任何會修改廣告平台 campaign、budget、bid、targeting、creative、tracking、status 的建議，仍必須另走 approval flow。

## BigQuery Service Account / OAuth / Project 權限注意事項

- 使用最小權限，優先給 dataset/table read access。
- 避免給過大的 project owner/editor 權限。
- 明確指定 project ID、dataset、table。
- 若使用 service account key，請放在 secret manager 或 `.env` 指向的安全位置，不要提交 JSON key。
- 對客戶資料建立 dataset 權限邊界，避免跨客戶查詢。

## Warehouse Data 與 Native Platform Data 的差異

Warehouse data 是資料副本或匯入資料。它可能有 ETL 延遲、欄位轉換、匯率轉換、去重邏輯、抽樣或資料缺漏。

Native platform data 通常更接近平台當下回報。做決策時應標明資料來源，並避免把 warehouse data 當成可直接控制原平台 campaign 的憑證。

## Manual CSV Import 注意事項

CSV 匯入時需檢查：

- export date / generated at
- date range
- timezone
- currency
- attribution window
- conversion definition
- 欄位名稱與型別
- 是否有 campaign_id、ad_group_id / ad_set_id、ad_id
- 是否有 duplicate rows
- spend、revenue 是否同幣別

建議把 raw exports 放 `exports/`，清理後資料放 `data/`。兩者都不應提交到 git。

## 如何檢查 MCP Server 是否被 Agent 看見

在 runtime 中確認：

- MCP server 是否啟動成功。
- Agent 是否列出 Google Ads / Meta Ads / GA4 / BigQuery / SQL 對應 tools。
- Tool call 是否能完成 authentication。
- 查詢簡單 metadata，例如 account、property、campaign list，而不是直接跑大型報表。

## MCP Unavailable 時 Agent 應如何回應

Agent 必須明確說明：

- 哪個 MCP connector 不可用。
- 缺少的是 runtime config、server command、credentials、permission，或 account/property access。
- 目前無法讀取真實帳戶資料。
- 可替代方案是接上 MCP、查 warehouse、或提供 CSV。

Agent 不可假裝已讀取資料，也不可用一般經驗編造帳戶數字。

在 `APP_ENV=production` 時，MCP unavailable 必須 fail closed。Agent 不可自動改讀 `test/`、Mock MCP 或 CSV fixture；除非使用者明確要求切換到 development/test 測試情境，否則應停止正式分析並列出缺少的 connector、credentials、permission 或 account/property access。若要改讀 `data/`，必須由使用者明確提供 CSV file path，或啟用 `manual_csv_fallback`，並在報告中標示為 `csv_export` / manual source。

若使用者明確要求 manual CSV fallback，可將 CSV 放在 `data/` 並啟用 `manual_csv_fallback` 或提供明確 file path。CSV 檔名不需要固定，但 agent 必須透過明確路徑、allowlist 或欄位驗證確認來源；不可盲目掃描整個 `data/`。

## Production Source Guardrails

正式上線時建議使用 `config/data-sources.yml` 作為資料來源 allowlist，並遵守下列規則：

- production 只允許 `production_allowed: true` 且 `enabled: true` 的來源。
- `source_type: csv_fixture`、`mock_mcp`、`public_sample` 永遠不得用於 production。
- 本機 `test/` 只用於 development/test；development 環境的測試 CSV、Mock MCP server 與官方 / 公開資料測試應集中放在 `test/`。`data/` 可用於 production explicit manual CSV fallback，但不可 silent fallback。
- 真實 MCP source 應使用 production adapter，例如 `connectors/google-ads-mcp.adapter.yml`、`connectors/meta-ads-mcp.adapter.yml`、`connectors/ga4-mcp.adapter.yml`。
- Manual CSV fallback 使用 `connectors/manual-csv.adapter.yml`，且必須 explicit enable / explicit file path，不可 silent fallback。
- 每次分析都要輸出 data source name、source type、environment、date range、platform、account/campaign scope、currency、timezone 與 data gaps。
- BigQuery / SQL MCP 應要求 date range、dry run 或 cost estimate，並優先查 summary tables。
- 若 allowlist 與 runtime 可用 tools 不一致，以 fail closed 處理，不自動猜測替代來源。

## 權限最小化原則

- 分析任務優先 read-only scope。
- 分帳戶、分客戶管理 credentials。
- Warehouse 權限只給需要的 dataset/table。
- 若未來啟用 write action，應使用獨立 credentials、獨立 approval flow 與 audit log。

## Token Rotate 建議

- 人員異動後 rotate。
- 發現 token/key 出現在 repo、prompt、log、issue、chat 時立即 rotate。
- 定期 rotate long-lived refresh token 與 service account key。
- 移除不再使用的 OAuth app、service account 與 MCP server credentials。
