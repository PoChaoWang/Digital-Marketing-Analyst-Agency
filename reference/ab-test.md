# Reference: A/B Test Analysis

## 適用情境

使用者要求分析 A/B test 結果，例如：
- 「這兩個 creative 哪個比較好？」
- 「我們在測不同的 landing page，看看哪個版本表現比較好」
- 「這個 campaign 在跑 A/B test，幫我出報告」

---

## 前置步驟：測試定義

A/B test 分析必須先確立測試的定義，才能決定比較哪些指標。以下步驟**不得跳過或假設**。

**1. 判斷測試對象**

從使用者描述推斷這次測試的對象類型：

| 測試對象 | 說明 | 主要關注指標 |
|---------|------|------------|
| Creative | 圖片、影片、文案、格式 | CTR、CVR、CPA、ROAS |
| Landing Page | 落地頁設計、內容、CTA | CVR、Bounce Rate、Revenue（GA4） |
| 受眾 | Audience targeting、lookalike | CPM、CTR、CPA、ROAS |
| 出價策略 | Bid strategy、budget allocation | CPC、CPM、CPA、ROAS |

若無法從描述判斷，在 Analysis Plan 標記「測試對象不明」，列出推論選項，請使用者確認。

**2. 判斷 A/B 邊界**

從使用者描述推斷 A / B 兩組的資料邊界：

- **Campaign 層級**：兩個 campaign 互相比較
- **Ad Set 層級**：同一 campaign 下的不同 ad set
- **Creative 層級**：同一 ad set 下的不同 creative

若邊界不明確，在 Analysis Plan 列出推斷的邊界定義，請使用者確認後再繼續。

**3. 詢問測試目的與主要判斷指標**

這步必須詢問使用者，不得自行假設。在 Analysis Plan 宣告測試對象與邊界後，**停止並詢問**：

```
這次 A/B test 的主要測試目的是什麼？
希望以哪個指標作為判斷勝負的主要依據？
（例如：ROAS、CPA、CVR、CTR，或其他）
```

收到回答後才繼續執行分析。

---

## 區間設定確認

確認測試目的後，比照 `reference/period-comparison.md` 的區間設定規則：

- 確認 A / B 兩組的時間區間長度是否一致
- 若為前後期比較（先跑 A 再跑 B），確認指定日期的歸屬（預設納入後期 B 組）
- 若為同期並行測試（A / B 同時跑），不需要前後期確認，但需確認兩組的時間範圍完全重疊

---

## 分析執行

**Layer 1：整體比較**

依測試對象，比較 A / B 兩組的核心指標：

廣告平台數據：Impressions、Clicks、Spend、CPC、CTR、CPM、廣告平台轉換數
GA4 數據：Revenue、Conversions、ROAS、ROI、CPA、CVR

指標顯著變動門檻沿用 `reference/period-comparison.md` 的規則：
- 曝光、點擊、費用、CPM、廣告平台轉換數：±15%
- CPC、CTR：±10%
- Revenue、Conversions、ROAS、ROI、CPA、CVR：不套固定門檻，以方向性變化呈現

**Layer 2：主要判斷指標的深入比較**

針對使用者指定的主要判斷指標，進行更細緻的比較：

- 列出 A / B 兩組的絕對數值與差異幅度
- 說明差異方向（A 優於 B / B 優於 A / 無明顯差異）
- 標注數值的可靠性（樣本量是否足夠、區間是否足夠長）

**資料來源規則**

與 period-comparison 相同：Revenue、Conversions、ROAS、ROI、CPA、CVR 以 GA4 為準；曝光、點擊、費用、CPC、CTR、CPM 以廣告平台為準。

---

## 輸出結構

1. **測試定義摘要**：測試對象、A/B 邊界、測試目的、主要判斷指標
2. **區間確認**：A / B 兩組時間範圍、並行 vs 前後期
3. **整體指標比較**：A / B 兩組所有指標並列，標注 `[顯著差異]`
4. **主要判斷指標深入比較**
5. **Observation**：資料直接顯示的事實
6. **Inference**：推論，標明信心程度與假設前提；若樣本量不足，必須標注 `[樣本量警告]`
7. **Recommendation**：建議採用哪個版本，或建議延長測試，標明理由與風險等級
8. **Data Gaps**：資料不足或無法判斷的項目

---

## 注意事項

- A / B 兩組的 spend 若差異懸殊（超過 30%），在 Observation 標記 `[預算不均]`，Inference 需說明此差異可能影響比較公平性。
- 同期並行測試若有受眾重疊的可能，在 Data Gaps 標記，不推論影響程度。
- 不主動宣告哪個版本「獲勝」，只呈現數據差異與方向，最終判斷交給人工。
- 若測試期間發生外部事件（例如節假日、其他活動同時進行），在 Analysis Trace 標記，Inference 需說明可能的干擾。