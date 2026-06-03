# Reference: Period Comparison Analysis

## 適用情境

使用者要求比較兩個時間區間的廣告成效，包含：
- 週報（WoW）：上週 vs 上上週
- 自訂區間：活動前後、素材上線前後、指定日期區間對比

---

## 區間設定確認（執行前必查）

在載入任何資料前，必須先確認以下三點，並在 Analysis Plan 中明確宣告：

**1. 區間長度是否一致**
前期與後期的天數必須相同。若不一致，停止並請使用者確認，不得以不等長區間進行比較。

**2. 週報的週起始日**
WoW 比較時，確認該客戶的週是從週一還是週日開始。若不確定，在 Analysis Plan 標記假設並請使用者確認。

**3. 指定日期的歸屬**
當使用者指定某個日期作為分界點（例如「5/15 前後七天」），預設將該日期納入**後期**區間。
若使用者未明確說明，在 Analysis Plan 宣告此預設，並請使用者確認後再繼續。

---

## 分析層級與順序

### Layer 1：Campaign 層級（大方向判斷）

先從 campaign 層級掌握整體方向，判斷是哪些 campaign 驅動了變化。

**使用廣告平台數據**，比較以下指標：

| 指標 | 顯著變動門檻 |
|------|------------|
| 曝光（Impressions） | ±15% |
| 點擊（Clicks） | ±15% |
| 費用（Spend） | ±15% |
| CPC | ±10% |
| CTR | ±10% |
| CPM | ±15% |
| 廣告平台回報轉換數 | ±15% |

超過門檻的指標在 Observation 標記為 `[顯著變動]`。

**使用 GA4 數據**，比較以下指標：

| 指標 | 備註 |
|------|------|
| Revenue | 以 GA4 為準，廣告平台數值僅供參考 |
| Conversions | 以 GA4 為準 |
| ROAS / ROI | 以 GA4 revenue 計算 |
| CPA | 以 GA4 conversions 計算 |
| CVR | 以 GA4 conversions 計算 |

Revenue、Conversions、ROAS、ROI、CPA、CVR 的變動幅度本身波動較大，**不套用固定門檻**，改以 Inference 層標注方向性變化（上升 / 下降 / 持平），並說明幅度供人工判斷。

### Layer 2：Creative 層級（WoW 細項比較）

確認 campaign 層級的大方向後，進入 creative 層級找出具體驅動因素。

**廣告平台數據**（曝光、點擊面）：

比較每個 creative 的 Impressions、Clicks、Spend、CPC、CTR、CPM，門檻同 Layer 1。

**GA4 數據**（轉換、營收面）：

以下指標以 GA4 為準：Revenue、Conversions、ROAS / ROI、CPA、CVR。同樣不套用固定門檻，以方向性變化呈現。

**標記重點 creative**：

符合以下任一條件者，在 Observation 標記 `[Notable Creative]`：
- 任一廣告平台指標達顯著變動門檻
- GA4 revenue 或 conversions 出現明顯方向性變化
- 前期有投放但後期消失（或反之）

---

## 資料來源規則

| 指標類型 | 資料來源 | 說明 |
|---------|---------|------|
| 曝光、點擊、費用、CPC、CTR、CPM、廣告平台轉換數 | 廣告平台（Meta Ads / Google Ads） | 平台側數值 |
| Revenue、Conversions、ROAS、ROI、CPA、CVR | GA4 | 必須以 GA4 為準，廣告平台數值不用於計算這些指標 |

若 GA4 資料不可用，在 Data Gaps 標記，GA4 相關指標欄位留空，不以廣告平台數值替代計算。

---

## 輸出結構

分析報告依序包含以下區塊：

1. **區間確認**：前期 / 後期日期範圍、天數、指定日期歸屬（若有）
2. **Campaign 層級摘要**：各 campaign 顯著變動指標，標注 `[顯著變動]`
3. **Creative 層級摘要**：標注 `[Notable Creative]` 的 creative 及其變動方向
4. **Observation**：資料直接顯示的事實
5. **Inference**：推論，標明信心程度與假設前提
6. **Recommendation**：建議行動，標明優先順序與風險等級
7. **Data Gaps**：資料不足或無法判斷的項目

---

## 注意事項

- 若同一個 creative 在不同 campaign 下都有出現，分開記錄，不合併。
- 週報模式下，若某一週因假日或特殊事件造成天數內的流量分佈不均，在 Analysis Trace 標記，不調整數值，由人工判斷。
- 跨平台（Meta + Google）比較時，各平台分開呈現，不加總 campaign 層指標，blended 指標只在 GA4 層計算。