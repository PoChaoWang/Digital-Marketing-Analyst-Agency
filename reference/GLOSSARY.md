# Glossary

本文件定義常見命名縮寫、平台術語與報表用語。分析時若 campaign、ad set、ad、creative、UTM 或 CSV 欄位中出現縮寫，先查本表；若找不到，保留原字串並在 `Data Gaps` 或 `Analysis Trace` 中標記為 unknown term。

## Usage Rules

- 第一次出現縮寫時，使用 `code (Canonical name)`，例如 `car (Carousel Ads)`。
- 報表內同一欄位應使用 canonical name；必要時在 notes 保留原始 code。
- 不要只憑 code 推斷 campaign objective、placement 或 funnel stage；需搭配欄位如 `funnel`、`campaign_name`、`ad_set`、`ad_name`、`placement`。
- 若資料中有 `ad_format_label`，優先使用該欄位；若沒有，再用本表由 code 對照。
- 若 code 與 label 衝突，列為 data gap，不要自行修正原始資料。

## Metric Definitions

- Spend：指定期間內平台花費，需標明 currency。
- Impressions：廣告曝光次數。
- Clicks：廣告點擊次數。
- CTR：Clicks / Impressions。
- CPC：Spend / Clicks。
- CPM：Spend / Impressions * 1000。
- Conversions：依平台或 GA4 定義記錄的轉換數，必須標明 conversion definition。
- CVR：Conversions / Clicks，或在 GA4 onsite context 中使用 Conversions / Sessions 並明確標示。
- CPA：Spend / Conversions。
- Revenue：指定期間內歸因或記錄的營收，需標明 source 與 currency。
- ROAS：Revenue / Spend。
- Frequency：Impressions / Reach，常用於 Meta Ads fatigue 判斷。
- Sessions：GA4 session 數。
- Users：GA4 users 數。
- Engaged sessions：GA4 engaged sessions 數。
- Engagement rate：Engaged sessions / Sessions。
- Key events：GA4 key events，舊稱 conversions；需標明事件名稱。
- Event count：GA4 event 觸發次數。
- Landing page CVR：Landing page sessions 到 key event 或 purchase 的 conversion rate。

## Report Terminology

本節定義報表中的固定用語，避免不同分析輸出使用不同名稱。分析與報表產出時應優先使用 `Preferred wording`。

| Term | Preferred wording | Notes |
| --- | --- | --- |
| `Data source` | Data source | 每份分析都必須顯示來源名稱、類型、環境、日期範圍與限制。 |
| `Analysis Trace` | Analysis Trace | 顯示可審查的分析邏輯：source selection、rules applied、field mapping、metric formulas、assumptions、decision log。 |
| `Observation` | Observation | 僅描述資料直接顯示的事實。 |
| `Inference` | Inference | 由 observation 推論出的解釋，必須附 confidence 或 reasoning basis。 |
| `Recommendation` | Recommendation | 建議動作；若會修改 campaign、budget、bid、targeting、creative、tracking、status，必須標記需要 approval。 |

## Format Codes

本節收錄各平台、資料源或內部命名常見的格式縮寫。未來可依平台或資料源繼續追加；若同一 code 在不同平台代表不同意思，請另列一行並在 `Official Name` 或 `Analysis Notes` 中標明平台。

| Code | Official Name | Chinese Description | Analysis Notes |
| --- | --- | --- | --- |
| `car` | Carousel Ads | 輪播廣告。通常包含多張卡片，可展示多個商品、賣點或使用情境。 | Meta / Facebook 常見廣告形式。分析時注意 card-level creative、商品順序、第一張卡片 hook、CTR 與 post-click CVR。 |
| `img` | Image Ads | 單圖廣告。以一張圖片搭配文案、標題與 CTA 呈現。 | Meta / Facebook 常見廣告形式。分析時注意視覺 hook、offer clarity、疲乏速度、CTR 與 CPA trend。 |
| `col` | Collection Ads | 精品欄廣告 / 目錄集合廣告。常用於行動裝置，主視覺下方搭配商品集合或 Instant Experience。 | Meta / Facebook 常見廣告形式。分析時注意 product feed quality、商品組合、mobile shopping intent、landing experience 與 ROAS。 |
| `vid` | Video Ads | 影片廣告。以影片素材承載品牌、產品或 offer message。 | Meta / Facebook 常見廣告形式。分析時注意 thumb-stop、前 3 秒 hook、video engagement、CTR、post-click CVR，避免只用 view metric 判斷成效。 |
