# 360 Table Workflow

跨期比較分析的標準執行路徑：

```
raw MCP / CSV sources
  → exports/360_table.csv     （Step 2：combine_to_360_table.py）
  → exports/period_compare.json （Step 3：period_compare_360_table.py）
  → AI 分析與報告               （Step 4：Handoff to Analysis）
```

本 workflow 由 `policies/routing.md` 在識別到 period compare / 前後比較 / 跨期分析任務時載入。

---

## Script Language Policy

- Production 資料清洗、360 table 建立、period compare 使用 Python + SQL。
- `scripts/run-recipe.mjs` 為 legacy / development-only，僅用於 Mock MCP 與舊 recipe 驗證。
- 新的 production 分析 script 應遵循 Python + SQL 模式。

---

## Step 1：確認輸入資料

執行前確認以下資料已通過 Environment Gate，來源符合 `config/data-sources.yml` allowlist：

| 資料 | 欄位最低要求 | 來源優先順序 |
|------|------------|------------|
| Google Ads | date, campaign_name, spend, clicks, impressions | MCP > CSV |
| Meta Ads | date, campaign_name, spend, clicks, impressions | MCP > CSV |
| GA4 | date, utm_campaign, sessions, conversions, revenue | MCP > CSV |

**欄位不足時：** 不拒絕執行，繼續跑 script，在 Data Gaps 標記缺少的欄位與影響範圍。

**Source Priority Override：** 若需要覆蓋預設優先順序，使用 `config/priority-overrides.example.yml` 格式：

```yaml
priority_overrides:
  - date: 2026-05-20
    platform: meta_ads
    prefer: csv
    reason: "MCP missing late imported conversions"
```

---

## Step 2：建立 360 Table

清洗邏輯在 `sql/build_360_table.sql`，runner 將資料載入 SQLite staging，輸出至 `exports/360_table.csv`。

**Grain：** `date + platform + campaign_name + ad_group_name + ad_name`

**GA4 欄位對應：**
- `utm_campaign` → `campaign_name`
- `utm_id` → `ad_group_name`
- `utm_content` → `ad_name`

**執行指令：**

```bash
# Development（使用 test/ fixtures）
python3 scripts/combine_to_360_table.py \
  --google-ads-csv test/csv/google_ads_raw.csv \
  --meta-ads-csv test/csv/meta_ads_raw.csv \
  --ga4-csv test/csv/ga4_raw.csv \
  --out exports/360_table.csv

# Production（使用 data/ 手動匯入 CSV）
python3 scripts/combine_to_360_table.py \
  --google-ads-csv data/google_ads.csv \
  --meta-ads-csv data/meta_ads.csv \
  --ga4-csv data/ga4.csv \
  --priority-overrides config/priority-overrides.example.yml \
  --out exports/360_table.csv
```

**輸出 source metadata 欄位：**
- `source_type`：`mcp` or `csv`
- `platform_name`：例如 `google_ads_mcp_production` 或 `manual_csv_fallback`
- `source_file`：CSV 來源路徑（CSV rows 才有）
- `source_priority`：`default_mcp` / `default_csv` / `user_override_mcp` / `user_override_csv`
- `loaded_at`：載入時間戳記

---

## Step 3：Period Compare

確認比較期間後執行。**期間定義規則：**

- 預設不重疊區間：以切分日為界，切分日不放入任一期間
  - 例：以 5/15 為切分點 → 前期 5/8–5/14，後期 5/16–5/22
- 若使用者希望包含切分日，必須明確指定
- 比較前確認 period length、weekday mix、seasonality、promotion、budget change 是否可比

**執行指令：**

```bash
python3 scripts/period_compare_360_table.py \
  --input exports/360_table.csv \
  --current-start {YYYY-MM-DD} \
  --current-end {YYYY-MM-DD} \
  --previous-start {YYYY-MM-DD} \
  --previous-end {YYYY-MM-DD} \
  --out exports/period_compare.json
```

輸出 `exports/period_compare.json` 作為 AI 分析依據。

---

## Step 4：Handoff to Analysis

`period_compare.json` 產出後，交由 `skills/ads-analysis/SKILL.md` 執行分析。

**指標來源規則：**

| 指標 | 使用欄位 | 說明 |
|------|---------|------|
| spend / impressions / clicks | 平台欄位 | 平台資料為準 |
| CVR | `ga4_conversions / clicks` | GA4 為 source of truth |
| CPA | `spend / ga4_conversions` | GA4 為 source of truth |
| ROAS | `ga4_revenue / spend` | GA4 為 source of truth |
| ROI | `(ga4_revenue - spend) / spend` | GA4 為 source of truth |
| 平台端 conversions / revenue | 保留於 360 table | 只做差異檢查，不作為主要成效判斷 |

**分析結果依 `skills/ads-analysis/SKILL.md` Output Rules 寫入 `output/`。**
