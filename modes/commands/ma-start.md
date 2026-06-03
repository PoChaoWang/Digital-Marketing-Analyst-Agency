# /ma-start

## 目的

引導使用者完成初次設定，或重新確認現有設定是否可用。
設定完成後使用者可以直接開始分析任務。

## 適用情境

- 第一次使用這個專案
- 不確定目前設定是否正確
- 想知道現在能用 MCP、CSV，還是需要補設定

## 執行流程

### 0. 讀取現有狀態

執行偵測腳本，讀取輸出結果：

```bash
bash scripts/check-setup.sh
```

根據輸出的 YAML 判斷哪些步驟需要執行、哪些可以跳過。
顯示目前狀態摘要與本次 checklist 給使用者確認。

---

### 1. 確認資料來源模式

問使用者一個問題：

> 你想用 MCP 直接連接廣告平台，還是手動匯入 CSV 檔案？
> - **MCP**：需要填入憑證，設定完成後可自動拉取資料
> - **CSV**：不需要憑證，手動匯出後上傳即可

- 選 **CSV** → 跳到 Step 4
- 選 **MCP** → 繼續 Step 2

---

### 2. MCP 憑證引導（選 MCP 才執行）

若 `.env` 不存在，先說明：

> 請在專案根目錄建立 `.env` 檔案，填入以下欄位。
> 憑證值請勿分享給他人，也不要提交到 git。

依平台分組說明欄位與取得方式：

**基本環境**
```
APP_ENV=production
DATA_SOURCE_CONFIG=config/data-sources.yml
```

**Google Ads**（若需要）
```
GOOGLE_ADS_CLIENT_ID=        # Google Cloud Console → OAuth 2.0 用戶端 ID
GOOGLE_ADS_CLIENT_SECRET=    # 同上
GOOGLE_ADS_DEVELOPER_TOKEN=  # Google Ads API Center
GOOGLE_ADS_REFRESH_TOKEN=    # OAuth 授權流程取得
GOOGLE_ADS_LOGIN_CUSTOMER_ID= # MCC 帳戶 ID（若有）
GOOGLE_ADS_CUSTOMER_ID=      # 廣告帳戶 ID
```

**Meta Ads**（若需要）
```
META_APP_ID=          # Meta for Developers → 應用程式 ID
META_APP_SECRET=      # 同上 → 應用程式密鑰
META_ACCESS_TOKEN=    # Meta Business Suite → 系統用戶存取權杖
META_AD_ACCOUNT_ID=   # 廣告帳戶 ID（格式：act_XXXXXXXX）
META_BUSINESS_ID=     # Business Manager ID
```

**GA4**（若需要）
```
GA4_PROPERTY_ID=       # GA4 管理介面 → 資源設定
GA4_CREDENTIALS_JSON=  # Google Cloud Console → 服務帳戶金鑰 JSON 路徑
GA4_CLIENT_EMAIL=      # 服務帳戶 Email
GA4_PRIVATE_KEY=       # 服務帳戶私鑰
GA4_CLIENT_ID=         # OAuth 用戶端 ID
GA4_CLIENT_SECRET=     # OAuth 用戶端密鑰
GA4_REFRESH_TOKEN=     # OAuth 授權流程取得
```

使用者填完後，重新執行 `bash scripts/check-setup.sh` 確認欄位狀態。
若仍有 `empty` 欄位，詢問使用者是否要繼續或稍後補填。

---

### 3. Adapter 設定（選 MCP 才執行）

說明：

> `connectors/` 裡的 adapter 檔案需要填入你的 MCP server 實際提供的 tool 名稱。
> 這個步驟需要參考你使用的 MCP server 文件，目前請先跳過，待確認 tool 名稱後再手動填入。
> 填入位置：`connectors/*.adapter.yml` 中標示 `REPLACE_WITH_*` 的欄位。

在 checklist 標記此步驟為「待完成」，繼續下一步。

---

### 4. accounts.yml 填寫（選 MCP 才需要，CSV 可選填）

若 `config/accounts.yml` 不存在，引導使用者填入以下資訊：

- 品牌名稱
- 各平台帳戶標籤（方便識別用）
- 幣別
- 時區
- 備註（選填）

參考格式見 `config/accounts.example.yml`。

填完後由 agent 寫入 `config/accounts.yml`，請使用者確認內容後再存檔。

---

### 5. Business Context 填寫

若 `profile/business-context.md` 不存在或區塊為空，對話式引導填入：

**依序問以下問題（每次只問一個）：**

1. 品牌名稱是什麼？主要市場和商業模式？
2. 主要 KPI 是什麼？（例如 CPA、ROAS、營收、註冊數、名單數）
3. 客戶最在意什麼？最不希望看到什麼？
4. 報告偏好高階摘要還是細節分析？

收集完畢後，顯示整理好的內容請使用者確認，確認後寫入 `profile/business-context.md`。

---

### 6. 完成摘要

顯示本次設定結果：

```
設定完成摘要
────────────
✓ 資料來源模式：[MCP / CSV]
✓ .env 欄位：[X 個已填 / Y 個待補]
✓ accounts.yml：[已建立 / 跳過]
✓ business-context.md：[已建立 / 已更新 / 跳過]
⚠ Adapter 設定：待完成（需手動填入 MCP tool 名稱）
────────────
下一步：[根據狀態給出建議，例如「可以開始跑分析」或「請先補完待填欄位」]

提醒：reference/GLOSSARY.md 已有基本術語定義，有需要可自行新增或請 agent 協助補充。
```

---

## 例外處理

- `.env` 填完但連線失敗：告知使用者可能是憑證值有誤，引導排查，不讀取 secret 值本身。
- 使用者想跳過某個步驟：允許跳過，在摘要標記為「跳過」。
- 使用者中途有問題：直接回答，不需要重跑整個流程。
- Adapter 設定不知道怎麼填：說明需要參考 MCP server 文件，標記待完成。

## 邊界

- 不讀取、顯示或記錄任何 secret 值。
- 不自動修改 `.env`，secrets 由使用者自行填寫。
- `config/accounts.yml` 和 `profile/business-context.md` 由 agent 在使用者確認後寫入。
- 不跑完整分析任務。