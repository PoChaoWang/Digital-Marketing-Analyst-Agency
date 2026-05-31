# AI Ads Analyst Agent

[繁體中文](README.zh-tw.md) | [English](README.md)

## 目錄

- [AI Ads Analyst Agent](#ai-ads-analyst-agent)
  - [目錄](#目錄)
  - [AI Ads Analyst Agent 是什麼](#ai-ads-analyst-agent-是什麼)
  - [目前可以做到的事情](#目前可以做到的事情)
  - [目前不能做到的事情](#目前不能做到的事情)
  - [初期設定](#初期設定)
    - [Step 0. 讀取現有狀態](#step-0-讀取現有狀態)
    - [Step 1. 選擇資料來源模式](#step-1-選擇資料來源模式)
    - [Step 2. 憑證設定（僅 MCP 模式）](#step-2-憑證設定僅-mcp-模式)
    - [Step 3. Adapter 工具對接（僅 MCP 模式）](#step-3-adapter-工具對接僅-mcp-模式)
    - [Step 4. 建立帳戶資訊（`config/accounts.yml`）](#step-4-建立帳戶資訊configaccountsyml)
    - [Step 5. 填寫商業背景（Business Context）](#step-5-填寫商業背景business-context)
    - [Step 6. 設定完成摘要](#step-6-設定完成摘要)
  - [Analysis Output](#analysis-output)
  - [Skill-Based Workflow](#skill-based-workflow)
    - [主要檔案怎麼分工](#主要檔案怎麼分工)
    - [Agent 如何判斷要用哪個 mode](#agent-如何判斷要用哪個-mode)
    - [如果想新增 GA4 User Journey 分析](#如果想新增-ga4-user-journey-分析)
    - [如果想新增 LINE Ads 分析](#如果想新增-line-ads-分析)
    - [如果想修改分析邏輯](#如果想修改分析邏輯)
  - [Write Action Approval Policy](#write-action-approval-policy)
  - [Troubleshooting](#troubleshooting)
    - [MCP tools 不可見](#mcp-tools-不可見)
    - [Agent 說沒有可用資料來源](#agent-說沒有可用資料來源)
    - [CSV 放在 `data/` 但 agent 沒有讀](#csv-放在-data-但-agent-沒有讀)
    - [報告出現 `# This is TEST`](#報告出現--this-is-test)
    - [數字和平台後台不同](#數字和平台後台不同)
    - [Google Sheets 報表沒有建立](#google-sheets-報表沒有建立)
  - [補充說明](#補充說明)
    - [測試資料與正式資料](#測試資料與正式資料)
    - [常見資料來源](#常見資料來源)
      - [MCP setup wizard，5/29 新增](#mcp-setup-wizard529-新增)
      - [固定任務 wizard，5/29 新增](#固定任務-wizard529-新增)
    - [相關文件](#相關文件)

## AI Ads Analyst Agent 是什麼

AI Ads Analyst Agent 目前是一個 MVP（Minimum Viable Product）。

它目前的目的不是做成完整 SaaS，而是先建立一套可以安全測試、可以慢慢擴充的 AI 廣告分析工作流程。使用者可以用自然語言要求 AI 分析 Google Ads、Meta Ads、GA4，或手動匯入的 CSV 報表。

這個 agent 的核心目標是：

- 幫行銷人員快速整理廣告與網站成效。
- 比較不同期間的成效變化。
- 標示資料來源與分析邏輯，避免黑箱分析。
- 在沒有真實 MCP 連線時，也可以用 CSV 做手動分析。
- 預設只讀資料，不會直接修改廣告帳戶。

## 目前可以做到的事情

- 分析 Google Ads、Meta Ads、GA4 的成效資料。
- 比較過去 7 天、14 天、30 天，或其他指定期間的成效變化。
- 產出 CPA、ROAS、CTR、CVR、CPM、CPC、花費、轉換、營收等指標。
- 做跨平台比較，例如 Google Ads、Meta Ads 與 GA4 的整體變化。
- 用 GA4 檢查 landing page、source / medium、campaign 的網站行為表現。
- 把完整分析結果輸出成 Markdown 到 `output/`。
- 在報告中顯示 Data sources、Environment Gate、Analysis Trace、Data gaps。
- 使用 `data/` 裡的 CSV 作為正式環境的手動匯入資料來源。
- 使用 `test/` 裡的測試資料或 Mock MCP 做 development 測試。
- 在使用者要求時，依 Google Sheets workflow 產出報表規劃；實際建立 Sheet 仍需要 runtime 有 Google Sheets / Google Drive tools。

## 目前不能做到的事情

- 不能在沒有資料的情況下編造成效數字。
- 不能自動修改 campaign、budget、bid、targeting、creative、tracking 或 status。
- 不能自動發布、暫停、刪除廣告。
- 不能把測試資料假裝成正式資料。
- 不能把 CSV、BigQuery 或 SQL 資料假裝成原生平台 MCP 資料。
- 不能在 MCP 壞掉時偷偷改讀其他資料來源。
- `scripts/run-recipe.mjs` 目前視為 legacy / development-only runner，主要用於 Mock MCP 與舊 recipe 驗證。正式風格的跨平台 period compare 應使用 Python + SQL 的 360 table workflow。
- BigQuery production source 目前標記為 planned，之後再開發。

## 初期設定

建議先使用 `/ma-start`，讓 agent 透過對話協助你檢查並設定環境。

### Step 0. 讀取現有狀態

- 系統會偵測目前環境，顯示設定進度與 checklist。

### Step 1. 選擇資料來源模式

- **MCP 模式**：連接 Google Ads、Meta Ads、GA4 等平台資料來源，需要準備憑證與 MCP tool mapping。
- **CSV 模式**：手動匯入報表資料，不需要平台憑證；可以跳過 Step 2、Step 3，視需要補 Step 4 與 Step 5。

### Step 2. 憑證設定（僅 MCP 模式）

- 引導你在根目錄建立 `.env` 檔案，填入 Google Ads / Meta Ads / GA4 所需的環境變數。
- 不要把 API key、OAuth secret、access token、refresh token、client secret、developer token 提交到 git。

### Step 3. Adapter 工具對接（僅 MCP 模式）

- 系統會提示你在 `connectors/*.adapter.yml` 補上 MCP server 實際提供的 tool 名稱。
- 初次設定時可以先跳過，等 MCP tools 確認可見後再補。

### Step 4. 建立帳戶資訊（`config/accounts.yml`）

- MCP 模式建議建立；CSV 模式可選填。
- 可記錄品牌、廣告帳戶標籤、幣別、時區與備註，協助 agent 產出更清楚的分析內容。

### Step 5. 填寫商業背景（Business Context）

- 透過對話式問答，收集品牌市場、主要 KPI、客戶偏好與報告風格。
- 確認後寫入 `profile/business-context.md`。

### Step 6. 設定完成摘要

- 顯示最終設定狀態與下一步建議。
- 若資料來源已可用，就可以開始執行分析任務。

## Analysis Output

分析結果會輸出到 `output/` 資料夾。

依 `policies/language-policy.md`，分析結果的語言會跟隨使用者的主要語言。例如使用者用繁體中文提問，報告就用繁體中文；使用者用英文提問，報告就用英文。

在測試環境時，檔名前方會出現 `zzz-test`，例如：

```text
output/zzz-test-analysis-20260528-143000-cross-channel.md
```

正式環境的檔名範例：

```text
output/analysis-20260528-143000-google-ads.md
```

如果是測試環境，Markdown 第一行必須明確標示：

```markdown
# This is TEST - Cross-channel Ads Performance Analysis
```

正式環境不需要額外標示 production。

每份分析報告都應包含：

- Data sources
- Environment Gate result
- Analysis Trace
- Observations
- Inferences
- Recommendations
- Risks
- Data gaps

## Skill-Based Workflow

這個 repo 把分析規則拆成幾個層次，讓之後比較好維護。

### 主要檔案怎麼分工

- `CLAUDE.md`：最高層操作規則，例如資料安全、環境判斷、輸出規則、是否需要使用者批准。
- `modes/_shared.md`：所有分析都會用到的共同指標與共同規則。
- `skills/ads-analysis/SKILL.md`：分析流程，包含要先讀哪些檔案、怎麼選資料來源、怎麼輸出。
- `modes/analyses/`：定義「這次要做哪一種分析」。
- `modes/platforms/`：定義「這些資料來自哪個平台，解讀時要注意什麼」。
- `docs/GLOSSARY.md`：術語與縮寫對照。
- `templates/`：報告格式。

### Agent 如何判斷要用哪個 mode

agent 會先判斷使用者想做哪一種分析，再判斷資料來自哪些平台。

例如：

```text
請比較過去 7 天與前 7 天的成效變化
```

這會優先使用：

- `modes/analyses/cross-channel.md`

如果資料包含 Google Ads、Meta Ads、GA4，還會使用：

- `modes/platforms/google-ads.md`
- `modes/platforms/meta-ads.md`
- `modes/platforms/ga4.md`

簡單記法：

- `modes/analyses/`：分析方法
- `modes/platforms/`：平台知識

### 如果想新增 GA4 User Journey 分析

如果這是一種新的報告或分析方法，建議新增：

```text
modes/analyses/user-journey.md
```

如果還只是想先記錄想法、資料格式還不穩定，可以先放：

```text
modes/backlog/user-journey.md
```

等資料欄位與分析方式穩定後，再移到 `modes/analyses/`。
如果不熟悉如何新增，也可以請 agent 協助。

### 如果想新增 LINE Ads 分析

如果 LINE Ads 會變成常態資料來源，建議新增：

```text
modes/platforms/line-ads.md
```

並同步考慮：

- 在 `docs/GLOSSARY.md` 補 LINE Ads 常見術語。
- 在 `connectors/manual-csv.adapter.yml` 補 LINE Ads CSV 欄位判斷。
- 在 `config/data-sources.yml` 補 LINE Ads 的資料來源設定。

### 如果想修改分析邏輯

請依照修改目的選位置：

- 想改資料安全或是否可以讀某個資料夾：改 `CLAUDE.md`。
- 想改共同指標公式：改 `modes/_shared.md`。
- 想改成效總覽、期間比較、跨平台分析方式：改 `modes/analyses/`。
- 想改 Google Ads、Meta Ads、GA4、LINE Ads 的平台解讀：改 `modes/platforms/`。
- 想改術語與縮寫：改 `docs/GLOSSARY.md`。
- 想改報告長相：改 `templates/`。

修改時要注意：

- 不要讓 production 自動讀測試資料。
- 不要讓 CSV 被誤標成 MCP。
- 不要讓 agent 在資料不足時補猜數字。
- 如果新增分析方法，最好也補對應範例問題與 data gaps。

## Write Action Approval Policy

這個 agent 預設是 read-only，也就是只讀資料與產出分析。

任何會修改廣告帳戶的行為，都必須先取得使用者明確同意，例如：

- 修改 campaign
- 修改 budget
- 修改 bid
- 修改 targeting
- 修改 creative
- 修改 tracking
- 暫停或啟用廣告
- 修改 status

在取得同意前，agent 只能提出建議，不能直接執行。

建立或更新 Google Sheet 報表屬於 report artifact，不等於修改廣告帳戶。但如果報表裡有建議要改 campaign 或 budget，仍然需要另行取得批准。

## Troubleshooting

### MCP tools 不可見

請檢查：

- runtime 是否真的載入 MCP config。
- MCP command 是否可執行。
- secrets 是否有被 runtime 載入。
- adapter 裡的 `REPLACE_WITH_...` 是否已換成實際 tool name。

### Agent 說沒有可用資料來源

請檢查：

- `.env` 的 `APP_ENV` 是否正確。
- `config/data-sources.yml` 是否有正確的 `enabled: true`。
- production source 是否有 `production_allowed: true`。
- 如果使用 CSV，是否有啟用 `manual_csv_fallback` 或明確指定 CSV file path。

### CSV 放在 `data/` 但 agent 沒有讀

這通常是正確的安全行為。agent 不應自動掃描 `data/`。

請明確指定檔案，例如：

```text
請使用 data/google_ads_2026-05-01_to_2026-05-28.csv 分析過去 28 天成效
```

### 報告出現 `# This is TEST`

代表目前是 development 或 test 環境。請確認 `.env` 或 runtime 環境變數：

```env
APP_ENV=production
```

### 數字和平台後台不同

常見原因：

- 日期區間不同
- timezone 不同
- attribution window 不同
- conversion definition 不同
- GA4 key event 與平台 conversion 不是同一件事
- 資料延遲
- CSV 匯出欄位不完整

### Google Sheets 報表沒有建立

Google Sheets reporting skill 已定義流程，但實際建立或更新 Sheet 需要 runtime 提供 Google Sheets / Google Drive tools。如果工具不可用，agent 應先輸出 Markdown 或 structured report，不應假裝 Sheet 已建立。

## 補充說明

### 測試資料與正式資料

- `test/`：只放 development / test 測試資料。
- `data/`：放使用者手動匯入的 CSV，production 可用，但必須 explicit。
- `output/`：放分析結果，不提交到 GitHub。

### 常見資料來源

- Native MCP：Google Ads、Meta Ads、GA4 等平台 MCP。
- Manual CSV：使用者手動匯出的 CSV。
- BigQuery / SQL：之後可作為資料倉儲來源，目前 production BigQuery source 先標記為 planned。

#### MCP setup wizard，5/29 新增

`workflows/mcp-setup-wizard.md` 是 MCP 設定用的對話式 fallback。

它會在分析或報表任務需要 production MCP 資料，但 preflight 找不到任何可用 production MCP source 時出現。常見原因包含：

- `config/data-sources.yml` 已啟用 Google Ads、Meta Ads 或 GA4 MCP，但 runtime 沒有對應 MCP tools。
- production adapter 裡仍有 `REPLACE_WITH_*` placeholder tool name。
- enabled source 沒有通過目前 `APP_ENV` / Environment Gate。

它的作用：

- 顯示已經檢查過哪些資料來源設定。
- 詢問使用者是否需要協助設定 MCP。
- 依序協助設定 Google Ads、Meta Ads、GA4，以及必要時的 BigQuery / SQL。
- 每一個 MCP source 都提供略過選項。
- 只收集非敏感設定資訊與 runtime tool mapping。

修改方式：

- 若要改對話流程、提示文字、平台順序或驗證清單，修改 `workflows/mcp-setup-wizard.md`。
- 若要改 wizard 什麼時候觸發，才修改 `CLAUDE.md`。
- 不要在這個 workflow 裡加入 token、secret、webhook、client secret、refresh token、developer token 或 private key 的收集流程。
- 不要修改 `connectors/mock-mcp.adapter.yml` 來代表 production MCP。

#### 固定任務 wizard，5/29 新增

`workflows/recurring-task-wizard.md` 讓沒有技術背景的使用者，可以用對話方式新增、修改、暫停、恢復或刪除固定分析任務，不需要直接編輯 YAML。

它會在使用者提出排程或重複分析需求時出現，例如：

- 「每天早上幫我看 CPA 有沒有變差」
- 「每週一比較上週跟上上週」
- 「暫停每天成效檢查」

它的作用：

- 用自然語言提問，不要求使用者知道 YAML 或 cron。
- 把使用者回答轉成 proposed task definition。
- 修改 `config/recurring-tasks.yml` 前先顯示摘要。
- 取得使用者明確確認後才寫入任務變更。
- 預設只把結果輸出成 `output/` Markdown。

修改方式：

- 若要改問題、任務 ID 規則、自然語言對應或確認格式，修改 `workflows/recurring-task-wizard.md`。
- 實際固定任務定義放在 `config/recurring-tasks.yml`。
- 已定義任務的執行方式放在 `workflows/recurring-analysis.md`。
- Slack、Teams 或 email delivery 尚未在 repo 外部設定前，notification mode 保持 `output_only`。
- 不要把 Slack webhook、Teams webhook、tokens 或 secrets 放進這個 repo。

### 相關文件

- `CLAUDE.md`：agent 主要操作規則。
- `policies/`：由 `CLAUDE.md` 引用的拆分政策檔。
- `DATA_CONTRACT.md`：資料分層與哪些檔案可提交。
- `docs/MCP_SETUP.md`：MCP 與資料來源安全規則。
- `docs/GLOSSARY.md`：名詞對照表。
- `docs/GOOGLE_SHEETS_REPORTING.md`：Google Sheets 報表流程。
- `config/recurring-tasks.yml`：固定分析任務表。
- `config/priority-overrides.example.yml`：source priority override 範例。
- `sql/build_360_table.sql`：paid media union、source priority、dedupe、GA4 left join 的可讀 SQL。
- `scripts/combine_to_360_table.py`：套用 SQL 並輸出 `exports/360_table.csv`。
- `scripts/period_compare_360_table.py`：使用 `exports/360_table.csv` 做 period compare。
- `workflows/360-table-workflow.md`：SQL-backed 360 table 與 period compare 流程。
- `workflows/mcp-setup-wizard.md`：MCP 設定用的對話式 fallback。
- `workflows/recurring-task-wizard.md`：固定任務新增與修改的對話式流程。
- `workflows/recurring-analysis.md`：已定義固定任務的執行流程。
