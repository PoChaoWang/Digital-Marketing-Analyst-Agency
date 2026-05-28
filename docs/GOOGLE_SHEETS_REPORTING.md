# Google Sheets Reporting

本文件說明如何把 AI Ads Analyst Agent 的分析結果產出到 Google Sheets。

## 核心概念

Google Sheets 報表不是廣告帳戶 write action。它是報告 artifact，因此在使用者要求產出報表時可以建立或更新 Sheet。

但任何會修改 Google Ads、Meta Ads、GA4 tracking、campaign、budget、bid、targeting、creative、status 的行為，仍然必須走 `templates/change-approval.md` approval flow。

## Skill-Based Workflow

本 repo 將能力拆成兩個 skill：

1. `skills/ads-analysis/`
   - 讀取 Google Ads / Meta Ads / GA4 / BigQuery / SQL / CSV。
   - 先套用 `modes/analyses/` 中的分析任務邏輯，再套用 `modes/platforms/` 中的平台知識。
   - 產出符合 `skills/ads-analysis/output.schema.json` 的結構化分析。

2. `skills/google-sheets-reporting/`
   - 接收結構化分析結果。
   - 建立或更新 Google Sheet。
   - 寫入 tabs、tables、findings、recommendations、data gaps。

完整順序寫在 `workflows/weekly-google-sheet-report.md`。

## 建議 Google Sheet Tabs

- `Config`
- `Analysis Trace`
- `Executive Summary`
- `Platform Summary`
- `Campaign Detail`
- `GA4 Onsite Quality`
- `Findings`
- `Recommended Actions`
- `Data Gaps`
- `Change Approval`

欄位定義在 `templates/google-sheet-weekly-report.md`。

## Google Sheets / Google Drive MCP

實際建立或更新 Google Sheets 需要 runtime 提供 Google Sheets 或 Google Drive 相關 MCP tools。不同 runtime 的 tool name 可能不同，本 repo 不假設固定名稱。

如果 Google Sheets MCP 不可用，agent 應：

- 明確說明無法建立或更新 Google Sheet。
- 仍可產出符合 schema 的 JSON 或 markdown 報表草稿。
- 請使用者接上 Google Drive / Google Sheets connector，或提供可寫入的 Sheet 工具。

## Create vs Update

建立新 Sheet：

- 使用者只要求產報表，且沒有提供既有 Sheet。
- 報表標題建議：`Weekly Ads Performance Report - {date_range}`。

更新既有 Sheet：

- 使用者提供 Google Sheet URL / ID。
- 若目標 Sheet 身分不明，先確認。
- 不覆蓋使用者手動維護的額外 tabs，除非使用者明確要求。

## 驗證要求

產出後應確認：

- 預期 tabs 是否存在。
- `Config` 是否包含 date range、timezone、currency、platform、account scope。
- `Analysis Trace` 是否包含 source selection、rules applied、field mapping、metric formulas、assumptions 與 decision log。
- `Platform Summary`、`Campaign Detail`、`Findings`、`Recommended Actions`、`Data Gaps` row counts 是否符合分析輸出。
- `Findings` 是否包含 observation、inference、reasoning_basis、recommendation，讓使用者可以審查分析邏輯。
- Recommendations 中涉及廣告帳戶修改者，`requires_approval` 必須為 true。

## 範例 Prompts

- 「請產出上週 Google Ads / Meta Ads / GA4 週報到新的 Google Sheet。」
- 「請用最近 30 天資料做 campaign audit，並把結果寫進這個 Google Sheet：{sheet_url}。」
- 「請先分析 GA4 paid traffic landing page 表現，再產出 Google Sheet 報表。」
- 「請把 recommendations 分成 P0/P1/P2，所有會改 campaign 的項目都標記 requires approval。」

## 不可做的事

- 不可把 secrets、tokens、private keys 寫入 Sheet。
- 不可把 Google Sheet 報表更新當成廣告帳戶 approval。
- 不可透過 BigQuery / SQL / CSV 宣稱可以直接修改原廣告平台。
- 不可在沒有資料來源時編造數據填入 Sheet。
