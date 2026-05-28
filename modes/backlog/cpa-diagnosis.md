# CPA Diagnosis Analysis Mode

## 使用情境

使用者詢問 CPA 上升、轉換成本過高、conversion efficiency 變差、哪些 campaign/ad set 拉高 CPA 時使用此 mode。

## 診斷框架

CPA = Spend / Conversions。拆解時優先檢查：

1. CPC 是否上升：Spend / Clicks。
2. CVR 是否下降：Conversions / Clicks。
3. Spend 是否集中到低轉換 campaign/ad set。
4. Conversion definition 或 tracking 是否變動。
5. GA4 landing page CVR 是否同步下降。
6. 比較期是否可比：date range、weekday mix、seasonality、promotion、budget change。

## 必查資料

- spend, clicks, conversions, CPA
- CTR, CPC, CVR
- campaign/ad set/ad group detail
- conversion action / key event definition
- GA4 sessions, key events, landing page CVR
- device, audience, placement, search term, creative data if available

## 輸出要求

每個 finding 必須包含：

- CPA change or high CPA observation
- CPC vs CVR decomposition
- likely driver
- evidence / supporting rows
- recommendation
- confidence
- risk

若資料只有單一期間，不能宣稱「上升」或「下降」；只能描述相對於同期間其他 campaign 的高低。
