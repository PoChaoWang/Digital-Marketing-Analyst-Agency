# Routing Protocol

本文件是可執行的決策協議，不是參考規則。Agent 讀完後必須依序執行 Step 1–4，並輸出 Routing Result。未列入 Routing Result 的文件，本次任務不讀。

---

## 前置：每次都載入

在執行 Step 1 之前，無條件載入：

- `modes/_shared.md`
- `skills/ads-analysis/SKILL.md`

---

## Step 1：識別 Analysis Intent

對照使用者描述，選出**一個**主要 intent。若同時符合多個，選最具體的那個（例如「比較前後成效」比「成效總覽」更具體，選 cross-channel）。

| Intent | 觸發關鍵字 | 載入 |
|--------|-----------|------|
| `performance-summary` | 週報、月報、成效、過去N天、overview、總覽、這週、上週 | `modes/analyses/performance-summary.md` |
| `cross-channel` | 比較、前後、period、vs、跨平台、360、channel allocation、blended | `modes/analyses/cross-channel.md` |
| `landing-page` | landing page、CVR、onsite、品質、跳出、頁面、到達頁 | `modes/analyses/landing-page-quality.md` |

**若無法對應任何 intent：** 停止，詢問使用者「請問這次任務的主要目標是什麼？」，不要猜測，不要繼續執行。
**衝突範例：**
- 「上週成效 + 跟上上週比」→ cross-channel（有 period compare，更具體）
- 「Meta 這週花了多少」→ performance-summary（單平台單期間，無比較）
- 「landing page CVR 跟上個月比」→ cross-channel，追加 landing-page mode

---

## Step 2：識別 Involved Platforms

可複選。依使用者描述或資料來源判斷。

| 平台 | 觸發關鍵字 | 載入 |
|------|-----------|------|
| Google Ads | google ads、關鍵字、搜尋廣告、gclid、campaign（Google 脈絡） | `modes/platforms/google-ads.md` |
| Meta Ads | meta、facebook、fb、ig、instagram、素材、fbclid | `modes/platforms/meta-ads.md` |
| GA4 | ga4、網站、session、轉換、landing page、traffic acquisition、attribution | `modes/platforms/ga4.md` |

**特例：** intent 為 `cross-channel` 時，預設載入全部三個平台 mode，除非使用者明確指定只看特定平台。

---

## Step 3：識別 Special Handling

依任務特徵追加載入，可複選。

| 條件 | 追加載入 |
|------|---------|
| 任務涉及 period compare、360 table、前後比較、跨期分析 | `policies/recipe-runner-policy.md`、`workflows/360-table-workflow.md` |
| 任務涉及任何 campaign / budget / bid / targeting / creative / tracking / status 寫入 | `policies/approval-flow.md` |
| 遇到不認識的縮寫或術語 | `reference/GLOSSARY.md`（找不到的術語標記為 `unknown term`） |
| 沒有 native MCP 的資料來源（非 Google Ads / Meta Ads / GA4 MCP） | 通過 Environment Gate 後，依 `config/data-sources.yml` allowlist 確認可用來源 |

**遇到不認識的縮寫或是術語:** 不要亂猜，跟使用者做詢問，有必要的話加入到 glossary。


### Backlog Capabilities（需明確告知使用者）

以下情境有對應的 backlog 分析模式，但**尚未有 recipe 支援**，不是 MVP active workflow。若任務觸發以下情境，必須先告知使用者「目前此分析尚為 backlog capability，無法自動執行，是否仍要參考？」，取得確認後才載入。

| 情境 | Backlog 文件 | 可用現有 recipe 部分回答的替代方案 |
|------|-------------|----------------------------------|
| CPA 上升、轉換成本過高、conversion efficiency 深度診斷 | `modes/backlog/cpa-diagnosis.md` | `performance-summary` 或 `cross-channel` |
| 預算 pacing、budget allocation、reallocation 深度診斷 | `modes/backlog/budget-pacing.md` | `performance-summary` 或 `cross-channel` |
| Creative fatigue、素材疲乏、frequency/CTR/CPA trend 深度診斷 | `modes/backlog/creative-fatigue.md` | `performance-summary` |
| Conversion tracking、attribution mismatch、UTM/gclid/fbclid、GA4 與平台數字不一致深度診斷 | `modes/backlog/attribution-tracking.md` | `landing-page` 或 `cross-channel` |

---

## Step 4：輸出 Routing Result

完成 Step 1–3 後，輸出以下格式，再繼續執行任務。此清單同時寫入 output artifact 的 `Analysis Trace`。

```
Routing Result
──────────────
Intent:          [cross-channel | performance-summary | landing-page | dashboard]
Platforms:       [google-ads] [meta-ads] [ga4]
Files to load:   
  - modes/_shared.md
  - skills/ads-analysis/SKILL.md
  - modes/analyses/[對應 intent]
  - modes/platforms/[對應平台 × N]
  - [Step 3 追加的文件，若有]
Special:         [backlog capability 告知 / approval required / glossary lookup，若有]
──────────────
```

**未列入此清單的文件，本次任務不讀。**
