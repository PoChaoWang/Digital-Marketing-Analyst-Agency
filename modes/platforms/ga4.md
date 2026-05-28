# GA4 Mode

GA4 在本 MVP 中不是另一個廣告投放平台，而是 analytics / attribution / onsite behavior layer，用來驗證廣告流量進站後實際發生什麼。

## 使用情境

- 分析 paid traffic 進站後的品質。
- 檢查 conversion / key event tracking。
- 驗證 Google Ads / Meta Ads reported conversions 是否合理。
- 分析 landing page performance。
- 分析 source / medium / campaign / channel group。
- 檢查 UTM / gclid / fbclid / campaign naming 是否斷裂或不一致。

先讀 `modes/_shared.md` 與任務對應的 `modes/analyses/`。使用可用且通過 Environment Gate 的 GA4 MCP tools 讀取資料；不要假設實際 MCP tool 名稱。

## 必查資料

- property
- date range
- traffic acquisition
- user acquisition
- source / medium
- session campaign
- default channel group
- landing pages
- events
- key events / conversions
- ecommerce revenue / purchase data if available
- device
- geography
- funnel or path data if available

## 分析重點

- sessions
- users
- engaged sessions
- engagement rate
- event count
- key event rate
- conversion rate
- revenue
- landing page CVR
- source / medium quality
- campaign naming consistency
- attribution gaps

## 診斷框架

- High paid traffic low conversion：檢查 landing page、traffic source quality、device、event setup。
- Landing page underperformance：比較 sessions、engagement rate、landing page CVR、revenue。
- Paid traffic engagement problem：檢查 engaged sessions、bounce-like signals、session duration if available。
- UTM mismatch：檢查 source / medium / campaign 命名不一致、大小寫、missing campaign。
- Missing gclid / fbclid attribution：檢查 paid clicks 與 GA4 paid sessions 差距。
- Conversion tracking drop：檢查 key event volume、event count、tag release、consent mode。
- Event volume anomaly：比較同週期、同 weekday、最近 tracking changes。
- Revenue mismatch：檢查 ecommerce event、purchase value、currency、refund/order source。
- Source attribution inconsistency：比較 default channel group、source / medium、session campaign。
- Google Ads / Meta Ads conversions differ from GA4：檢查 attribution window、timezone、conversion definition、lookback window、去重邏輯。

## 輸出格式

每個 finding 使用：

- What GA4 shows
- What this means for paid media
- What to verify in tracking setup
- Recommended action
- Risk / confidence level
