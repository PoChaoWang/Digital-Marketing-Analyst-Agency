# /ma-test

## 目的

做非破壞性的驗證，用來確認設定、routing 與工作流程是否可用。

## 適用情境

- 正式分析前先檢查環境
- 修改規則後先驗證流程
- 想知道目前資料來源或工具是否可用

## 先讀哪些檔案

- `policies/interaction-command-policy.md`
- `CLAUDE.md`
- `policies/environment-gate.md`
- `policies/routing.md`
- `modes/_shared.md`

如果測試內容涉及特定平台，再補讀對應 platform mode。

## 執行重點

- 只做 read-only 檢查
- 驗證環境與資料來源 allowlist
- 確認可用工具與 routing 是否合理
- 不可修改 campaign、budget、bid、targeting、creative、tracking 或 status

## 範圍說明
本指令只做使用者層級的環境與 routing 檢查。
技術層級的 script 與輸出結構驗證見 `test/smoke-test-prompt.md`。

## 回應格式

- 通過 / 失敗狀態
- 檢查了什麼
- 缺少什麼或被什麼阻擋
- 建議下一步

## 例外處理

- 如果發現不相容設定，直接說明原因
- 如果測試成功，也要保留簡短的檢查摘要
- 如果測試只到部分流程，明確說明範圍
