# Google Ads Mode

## 使用情境

使用者詢問 Google Ads campaigns、Search、Performance Max、Display、YouTube、Shopping、keywords、search terms、budget pacing、conversion tracking、CPA、ROAS、CTR、CPC、CVR 或 impression share 時，使用此 mode。

先讀 `modes/_shared.md` 與任務對應的 `modes/analyses/`。使用可用且通過 Environment Gate 的 Google Ads MCP tools 讀取資料；不要假設實際 MCP tool 名稱。

## 必查資料

- account/customer
- campaigns
- ad groups
- ads/assets
- keywords
- search terms
- conversion actions
- campaign budget
- impression share / lost IS if available

## 分 Campaign Type 分析

### Search

- 檢查 keyword intent、match type、search terms、negative keywords。
- 比對 CTR、CPC、CVR、CPA、ROAS。
- 查看 impression share、lost IS budget、lost IS rank if available。

### Performance Max

- 檢查 asset group、listing group、audience signals、conversion goals。
- 注意 PMax 黑盒限制，避免過度推論單一 placement 或 query。
- 與 GA4 landing page、source / medium、campaign quality 做 sanity check。

### Display

- 檢查 placement、audience、creative、frequency、view-through conversion 定義。
- 區分 prospecting 與 remarketing。

### YouTube

- 檢查 view metrics、engagement、audience、creative、conversion lag。
- 注意 upper-funnel campaign 不應只用 last-click CPA 評估。

### Shopping

- 檢查 product / item performance、feed quality、merchant center issue if available。
- 分析 spend concentration、ROAS、conversion value、product margin context。

## 診斷框架

- High spend low conversion：檢查 search terms、landing page、conversion action、audience、budget concentration。
- Low CTR：檢查 query intent、ad relevance、creative/message、position、asset strength。
- High CPC：檢查競爭、quality score proxies、bid strategy、match type、audience。
- Low CVR：檢查 landing page、offer、traffic intent、device、tracking。
- High CPA：拆成 CPC 與 CVR 問題，再檢查 conversion definition。
- Poor ROAS：檢查 revenue tracking、product mix、margin、conversion value、bid strategy。
- Limited by budget：檢查 lost IS budget、highest efficiency campaigns、budget pacing。
- Search term waste：找出高花費低轉換或低意圖 query，提出 negative keyword 候選。
- Tracking/conversion issues：檢查 conversion actions、status、recent volume changes、GA4 對照。

## 建議輸出格式

每個 finding 使用：

- What is happening
- Why it may be happening
- What to check next
- Recommended action
- Risk
