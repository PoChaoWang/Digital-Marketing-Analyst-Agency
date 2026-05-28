# Attribution and Tracking Analysis Mode

## 使用情境

使用者詢問 conversion tracking、GA4 與廣告平台數字不一致、UTM/gclid/fbclid、attribution mismatch、key event 設定、tracking 是否壞掉時使用此 mode。

## 診斷框架

比較資料時不可直接把平台 conversions 相加。必須檢查：

- attribution window
- conversion definition / key event definition
- timezone
- lookback window
- click vs session vs user scope
- deduplication logic
- consent mode / ad blocker / cross-domain tracking
- data delay
- UTM consistency and missing campaign/source/medium

## 必查資料

- platform conversions and conversion value
- GA4 key events, conversions, revenue
- source / medium / campaign
- landing_page
- event names and key event settings if available
- tracking status / diagnostics if available

## 輸出要求

- What each source reports
- Why numbers may differ
- Evidence from fields or source definitions
- Tracking risks
- Verification checklist
- Data gaps

若缺少 tracking settings 或 event definitions，必須把 conclusion 降為 low confidence。
