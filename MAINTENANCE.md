# Maintenance Guide

這份文件記錄架構的耦合點與維護 checklist。每次改動文件時，對照下方表格確認需要同步更新的地方。

---

## 檔案耦合對照表

### 新增 Analysis Mode

新增 `modes/analyses/` 下的分析模式時：

- [ ] `policies/routing.md`：Step 1 表格加入對應觸發關鍵字
- [ ] `CLAUDE.md`：Mode And Workflow Index 加入新 mode
- [ ] `skills/ads-analysis/SKILL.md`：若有對應 recipe，更新 Recipe Selection 表格

### 新增 Platform Mode

新增 `modes/platforms/` 下的平台模式時：

- [ ] `policies/routing.md`：Step 2 表格加入平台觸發關鍵字
- [ ] `connectors/`：新增對應 adapter yml
- [ ] `CLAUDE.md`：Mode And Workflow Index 加入新 platform mode

### 新增 Recipe

新增 `recipes/` 下的 recipe 時：

- [ ] `skills/ads-analysis/SKILL.md`：Recipe Selection 表格加入新 recipe 與範例指令
- [ ] `policies/recipe-runner-policy.md`：若有特殊規則，補充說明

### 新增 Workflow

新增 `workflows/` 下的 workflow 時：

- [ ] `CLAUDE.md`：Mode And Workflow Index 加入新 workflow
- [ ] `policies/routing.md`：Step 3 若有觸發條件，加入對應載入規則

### 修改 Output 規則

修改輸出格式、檔名規則或報告結構時：

- [ ] `policies/output-artifacts.md`：主要定義
- [ ] `skills/ads-analysis/SKILL.md`：Output Rules 區塊是否需要同步

### 修改 Environment Gate 規則

- [ ] `policies/environment-gate.md`：主要定義
- [ ] `modes/_shared.md`：若有相關原則需要更新

### 新增 /ma-* 指令
- [ ] `policies/interaction-command-policy.md`：登記指令名稱與路由
- [ ] `modes/commands/`：新增對應指令流程檔案
- [ ] `CLAUDE.md`：Policy Index 和 Mode And Workflow Index 各加一行

---

## 核心文件異動原則

以下文件影響範圍大，改動前先確認是否真的需要全域修改，還是只是特定任務的例外情況：

| 文件 | 影響範圍 | 建議 |
|------|---------|------|
| `CLAUDE.md` | 所有任務的入口與 preflight | 改動前確認不會破壞現有任務 |
| `policies/environment-gate.md` | 所有資料來源存取 | 特殊情況優先用 config 層級 override |
| `modes/_shared.md` | 所有分析任務的共用規則 | 只放真正每次都需要的規則 |
| `policies/routing.md` | 所有任務的文件載入決策 | 新增觸發關鍵字時確認不與現有條目衝突 |

**原則：** 特殊情況優先用 `profile/business-context.md` 或任務層級的參數處理，不要修改全域規則。

---

## 測試建議

每次修改文件後，用以下方式驗證：

1. 跑一個對應任務，確認 `Analysis Trace` 裡的 Routing Result 載入了正確的文件清單。
2. 確認沒有多載入不相關的文件。
3. `APP_ENV=development` 下跑 smoke test，確認 Environment Gate result 符合預期。

---

## 文件更新紀錄

| 日期 | 文件 | 異動摘要 |
|------|------|---------|
| 2026-05-30 | 全面優化 | routing 改為決策格式、SKILL.md 移除重複定義、environment-gate 加入 CSV 欄位判斷原則、360-table-workflow 加入執行步驟與 handoff |