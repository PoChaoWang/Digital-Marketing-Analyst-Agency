# Meta Ads Mode

## 使用情境

使用者詢問 Meta Ads、Facebook Ads、Instagram Ads、campaigns、ad sets、ads、creative fatigue、CPM、CTR、CPC、CPA、ROAS、frequency、reach、learning phase、placements 或 pixel/conversion event 時，使用此 mode。

先讀 `modes/_shared.md` 與任務對應的 `modes/analyses/`。使用可用且通過 Environment Gate 的 Meta Ads MCP tools 讀取資料；不要假設實際 MCP tool 名稱。

如果資料中有 `ad_format`、`ad_format_label`、campaign/ad naming code 或 creative code，先讀 `reference/GLOSSARY.md` 做名詞對照。常見 code：

- `car`：Carousel Ads
- `img`：Image Ads
- `col`：Collection Ads
- `vid`：Video Ads

報表中第一次提及時使用 `code (Canonical name)`，例如 `car (Carousel Ads)`。若 code 與 label 衝突，列為 data gap。

## 必查資料

- ad account
- campaigns
- ad sets
- ads
- creatives
- placements
- breakdowns if available
- pixel/conversion event status if available

## 分析重點

- CPM
- CTR
- CPC
- CPA
- ROAS
- frequency
- reach
- learning phase
- creative fatigue
- audience overlap
- placement performance

## 診斷框架

- High frequency + declining CTR：可能是 creative fatigue 或 audience saturation。
- High CPM：檢查 audience size、auction pressure、seasonality、objective、placement restriction。
- Low outbound CTR：檢查 creative hook、offer-message fit、CTA、destination mismatch。
- Poor landing page conversion：用 GA4 檢查 landing page CVR、engagement、device、page path。
- Creative fatigue：檢查 frequency、CTR trend、CPA trend、spend concentration by creative。
- Event tracking issue：檢查 pixel/conversion event status、event volume anomaly、GA4 key event 對照。
- Unstable learning phase：檢查 ad set edits、budget changes、conversion volume、event priority。

## 建議輸出格式

每個 finding 使用：

- What is happening
- Why it may be happening
- What to check next
- Recommended action
- Risk
