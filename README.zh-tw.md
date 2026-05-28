# AI Ads Analyst Agent

[繁體中文](README.zh-tw.md) | [English](README.md)

## 目錄

- [AI Ads Analyst Agent](#ai-ads-analyst-agent)
  - [目錄](#目錄)
  - [AI Ads Analyst Agent 是什麼](#ai-ads-analyst-agent-是什麼)
  - [目前可以做到的事情](#目前可以做到的事情)
  - [目前不能做到的事情](#目前不能做到的事情)
  - [初期設定](#初期設定)
    - [1. 設定 `.env`](#1-設定-env)
      - [`.env` 的資料要去哪裡找](#env-的資料要去哪裡找)
    - [2. 視需要設定 `config/accounts.yml`](#2-視需要設定-configaccountsyml)
    - [3. 設定資料來源 `config/data-sources.yml`](#3-設定資料來源-configdata-sourcesyml)
    - [4. 不懂 MCP 時可以怎麼問 AI](#4-不懂-mcp-時可以怎麼問-ai)
    - [5. 如果沒有 MCP，可以把 CSV 放在 `data/`](#5-如果沒有-mcp可以把-csv-放在-data)
  - [Business Context](#business-context)
  - [Production MCP Adapters](#production-mcp-adapters)
  - [Analysis Output](#analysis-output)
  - [Glossary / 名詞對照表](#glossary--名詞對照表)
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
- 目前 `scripts/run-recipe.mjs` 主要支援 development 的 Mock MCP；production MCP 與 manual CSV 的 runner 串接仍是後續工作。
- BigQuery production source 目前標記為 planned，之後再開發。

## 初期設定

### 1. 設定 `.env`

請先複製主目錄底下的：

```text
.env.example
```

成為：

```text
.env
```

最重要的是設定目前環境：

```env
APP_ENV=production
DATA_SOURCE_CONFIG=config/data-sources.yml
```

常見環境：

- `development`：測試用，主要使用 `test/` 裡的測試資料。
- `production`：正式用，使用正式 MCP、BigQuery / SQL，或 `data/` 裡明確指定的 CSV。

請不要把 API key、OAuth secret、access token、refresh token、client secret、developer token 放進 git。

#### `.env` 的資料要去哪裡找

`.env` 裡有兩種資料：一種是環境設定，一種是平台連線資料。

環境設定通常由這個 repo 的使用者自己決定：

```env
APP_ENV=production
DATA_SOURCE_CONFIG=config/data-sources.yml
```

平台連線資料通常需要從平台後台、開發者後台、或代理商 / 工程團隊取得。行銷人員不一定會自己產生這些值，這是正常的。

Google Ads 常見需要的資料：

- `GOOGLE_ADS_CUSTOMER_ID`：Google Ads 帳戶 ID，可在 Google Ads 後台右上角或帳戶切換器看到。
- `GOOGLE_ADS_LOGIN_CUSTOMER_ID`：如果透過 MCC / manager account 管理帳戶，通常是 manager account ID。
- `GOOGLE_ADS_CLIENT_ID` / `GOOGLE_ADS_CLIENT_SECRET`：OAuth client 資訊，通常由 Google Cloud Console 建立。
- `GOOGLE_ADS_DEVELOPER_TOKEN`：Google Ads API developer token，通常由擁有 Google Ads API 權限的人提供。
- `GOOGLE_ADS_REFRESH_TOKEN`：OAuth 授權後產生的 refresh token，通常需要工程或熟悉 OAuth 的人協助取得。

Meta Ads 常見需要的資料：

- `META_AD_ACCOUNT_ID`：Meta 廣告帳戶 ID，可在 Meta Ads Manager 或 Business Settings 找到。
- `META_BUSINESS_ID`：Business Manager / Business Portfolio ID，可在 Business Settings 找到。
- `META_APP_ID` / `META_APP_SECRET`：Meta Developer App 的資訊，通常由有 Meta Developer 權限的人建立。
- `META_ACCESS_TOKEN`：Meta API access token，通常由系統管理員、代理商或工程團隊提供。

GA4 常見需要的資料：

- `GA4_PROPERTY_ID`：GA4 property ID，可在 GA4 Admin 的 Property settings 找到。
- `GA4_CREDENTIALS_JSON`：service account JSON，通常由 Google Cloud / GA4 管理者建立。
- `GA4_CLIENT_EMAIL` / `GA4_PRIVATE_KEY`：service account 裡的欄位。如果已使用 `GA4_CREDENTIALS_JSON`，不一定需要拆開填。
- `GA4_CLIENT_ID` / `GA4_CLIENT_SECRET` / `GA4_REFRESH_TOKEN`：OAuth 方式才可能需要。

如果你不確定要填哪一種，先確認你使用的 MCP server 文件。不同 MCP server 需要的變數可能不同。

安全提醒：

- 不要把 `.env` 內容貼到 README、GitHub issue、Slack 公開頻道或分析報告裡。
- 如果要請人協助除錯，只提供變數名稱與是否已填，例如 `GOOGLE_ADS_REFRESH_TOKEN=present`，不要提供真實值。
- 如果 token 曾經被貼到公開地方，請視為已外洩並重新產生。

### 2. 視需要設定 `config/accounts.yml`

如果 `.env` 或 MCP runtime 已經管理 account ID / property ID，`config/accounts.yml` 不一定要建立。

`config/accounts.yml` 的用途是補充人類可讀的帳戶資訊，例如帳戶名稱、品牌、幣別、時區、備註、多帳戶對照。它不應要求你把 `.env` 裡已經填過的 ID 再手動填一次。

如果你需要補充這些資訊，請複製：

```text
config/accounts.example.yml
```

成為：

```text
config/accounts.yml
```

可以填入類似這些資訊：

- account label / 顯示名稱
- brand / client name
- timezone
- currency
- notes

`config/accounts.yml` 不應上傳到 GitHub，因為它可能包含客戶帳戶資訊或內部命名。

### 3. 設定資料來源 `config/data-sources.yml`

請複製：

```text
config/data-sources.example.yml
```

成為：

```text
config/data-sources.yml
```

這個檔案用來告訴 agent：

- 現在是 development、test 還是 production。
- 哪些資料來源可以使用。
- 哪些資料來源只是測試資料。
- 哪些資料來源可以在正式分析中使用。

正式環境只應使用：

- `production_allowed: true`
- `enabled: true`

### 4. 不懂 MCP 時可以怎麼問 AI

MCP 可以把 Google Ads、Meta Ads、GA4 這些平台接到 AI agent，讓 agent 直接讀取資料。

如果你現在沒有 MCP，這一步可以先跳過，改用下一步的 CSV 匯入方式。

如果你不確定 MCP 是什麼、要不要設定、或自己能不能設定，可以直接問 AI。你不需要一開始就知道 command、runtime、token 這些細節。

可以先這樣問：

```text
我想用這個專案分析 Google Ads / Meta Ads / GA4。
我目前不確定有沒有 MCP，也不確定怎麼設定。
請先檢查這個 repo 需要哪些設定，告訴我哪些可以自己做，哪些可能需要技術協助。
不要要求我貼出任何 token 或 secret。
```

如果你使用 Claude Code，可以問：

```text
我使用 Claude Code。
請檢查這個 repo 的 README.md、mcp.example.json、config/data-sources.yml 和 docs/MCP_SETUP.md。
告訴我如果要設定 Google Ads / Meta Ads / GA4 MCP，需要準備哪些資料，以及要怎麼確認 MCP tools 是否可見。
不要顯示或要求我貼出任何 token。
```

如果你想先確認 `.env`，可以問：

```text
請幫我檢查 .env 是否有必要欄位。
只告訴我哪些變數是 present / missing，不要顯示任何真實值。
```

如果你目前沒有 MCP、只想用 CSV，可以問：

```text
我目前沒有 MCP。
我會把 Google Ads / Meta Ads / GA4 匯出的 CSV 放在 data/。
請告訴我 CSV 檔名與欄位需要怎麼準備，才能讓你安全分析。
```

如果你最後真的需要找工程、代理商或系統管理員協助，也可以請 AI 先幫你整理需求：

```text
請根據這個 repo 產出一份 MCP 設定需求清單。
請包含：
- 要接的平台
- 需要準備的 account/property ID
- 需要的 token 或 OAuth 權限
- Claude Code / Codex / Cursor 可能需要設定的位置
- 設定完成後怎麼驗證 MCP tools 是否可見
不要包含任何真實 secrets。
```

如果 AI 判斷你已經有 MCP，才需要進一步設定你的 agent runtime。這一步不是填表單，而是要告訴你使用的 AI 工具：

- 要啟動哪一個 MCP server。
- 要用什麼 command 啟動。
- 要把哪些 `.env` 變數交給 MCP server。
- 要在哪個 agent runtime 裡設定，例如 Claude Code、Claude Desktop、Codex、Cursor、Windsurf。

這個 repo 只提供範例：

```text
mcp.example.json
```

它只是概念範例，不保證每個工具都會自動讀取。

`mcp.example.json` 不會自動生效。它只是告訴你 MCP 設定通常需要 `command`、`args`、`env`。請依你使用的 agent runtime，把這些內容複製到該 runtime 的 MCP 設定檔。

如果你需要請人協助，最務實的做法是把以下資訊交給對方：

- 你要接的平台：Google Ads、Meta Ads、GA4 或其他平台。
- 你使用的 AI 工具：Claude Code、Claude Desktop、Codex、Cursor、Windsurf 等。
- `.env` 裡已經準備好的變數名稱，不要提供真實 token。
- 這個 repo 的 `mcp.example.json` 與 `docs/MCP_SETUP.md`。

設定完成後，可以請對方確認 AI 工具裡是否看得到 MCP tools。

MCP 官方參考：

- Google Ads MCP: https://developers.google.com/google-ads/api/docs/developer-toolkit/mcp-server
- Meta Ads MCP: https://www.facebook.com/business/help/1456422242197840
- GA4 MCP: https://developers.google.com/analytics/devguides/MCP

### 5. 如果沒有 MCP，可以把 CSV 放在 `data/`

如果暫時沒有 MCP，也可以把手動匯出的 CSV 放在：

```text
data/
```

建議檔名寫清楚，例如：

```text
google_ads_YYYY-MM-DD_to_YYYY-MM-DD.csv
meta_campaign_YYYY-MM-DD_to_YYYY-MM-DD.csv
ga4_landing_page_YYYY-MM-DD_to_YYYY-MM-DD.csv
line_ads_campaign_YYYY-MM-DD_to_YYYY-MM-DD.csv
```

檔名不一定要完全固定，但必須讓人看得出：

- 來源平台
- 報表層級
- 日期區間

使用 CSV 時，agent 必須把資料標示為 `csv_export` 或 manual source，不能標示成 native MCP。

## Business Context

如果你希望 agent 知道品牌、KPI 與客戶在意的重點，可以複製：

```text
profile.example/business-context.md
```

成為：

```text
profile/business-context.md
```

可以放入：

- 品牌是誰
- 主要 KPI 是 CPA、ROAS、營收、註冊、名單，或其他指標
- 客戶最在意什麼
- 報告語氣要偏高階摘要還是細節分析

`profile/` 不應上傳到 GitHub。

Business Context 只會影響建議的角度與溝通方式，不會取代實際資料。

## Production MCP Adapters

如果你使用真實 MCP，需要使用 production adapter：

- `connectors/google-ads-mcp.adapter.yml`
- `connectors/meta-ads-mcp.adapter.yml`
- `connectors/ga4-mcp.adapter.yml`

這些 adapter 會告訴 agent：

- 這個 MCP 是哪個平台。
- 哪個 MCP tool 可以抓 campaign performance。
- 回傳欄位要如何對應到 spend、clicks、conversions、revenue 等指標。

目前 adapter 裡有像這樣的 placeholder：

```yaml
tool: REPLACE_WITH_GOOGLE_ADS_CAMPAIGN_PERFORMANCE_TOOL
```

這代表你還需要換成 MCP runtime 實際提供的 tool name。

如果 production adapter 還有 `REPLACE_WITH_...`，有兩種安全做法：

1. 先把 `config/data-sources.yml` 裡對應 source 的 `enabled` 設成 `false`。
2. 保持 `enabled: true`，但 agent 執行時必須 fail closed，回報 MCP tool 尚未設定完成。

正式上線前建議使用第一種做法。

不要修改 `connectors/mock-mcp.adapter.yml` 來接正式資料；Mock MCP 只給 development / test 使用。

## Analysis Output

分析結果會輸出到：

```text
output/
```

分析語言會跟隨使用者的主要語言。例如使用者用繁體中文提問，報告就用繁體中文；使用者用英文提問，報告就用英文。

測試環境的檔名範例：

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

## Glossary / 名詞對照表

名詞、縮寫、欄位代碼與廣告格式可以放在：

```text
docs/GLOSSARY.md
```

這可以幫 agent 統一用詞，避免不同人寫的 campaign name 或欄位縮寫造成誤解。

例如 Meta / Facebook ad format code：

- `car`: Carousel Ads
- `img`: Image Ads
- `col`: Collection Ads
- `vid`: Video Ads

如果之後有 LINE Ads、TikTok Ads 或其他平台，也可以把常見術語補進 glossary。

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

- `modes/analyses/performance-summary.md`

如果資料包含 Google Ads、Meta Ads、GA4，還會使用：

- `modes/analyses/cross-channel.md`
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

代表目前是 development 或 test 環境。請確認 `.env`：

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

### 相關文件

- `CLAUDE.md`：agent 主要操作規則。
- `DATA_CONTRACT.md`：資料分層與哪些檔案可提交。
- `docs/MCP_SETUP.md`：MCP 與資料來源安全規則。
- `docs/GLOSSARY.md`：名詞對照表。
- `docs/GOOGLE_SHEETS_REPORTING.md`：Google Sheets 報表流程。
