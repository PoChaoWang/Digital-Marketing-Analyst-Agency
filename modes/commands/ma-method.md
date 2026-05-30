# /ma-method

## 目的

新增或修改研究方法、分析方法、工作流程模式。

## 適用情境

- 使用者要新增一種分析方式
- 使用者要調整既有 method 的邏輯或結構
- 使用者要讓 agent 多看一種判斷方式

## 先讀哪些檔案

- `policies/interaction-command-policy.md`
- `CLAUDE.md`
- `modes/_shared.md`
- 與變更內容相關的 `modes/analyses/*`、`modes/platforms/*`、`workflows/*` 或 `policies/*`

## 執行重點

- 先釐清 method 名稱與用途
- 說明這個 method 解決什麼問題
- 說明需要哪些資料
- 說明預期輸出長什麼樣子
- 標示會影響哪些檔案或規則
- 若會影響分析行為，要直接講清楚影響範圍

## 回應格式

- Method 名稱
- 目的
- 必要輸入
- 預期輸出
- 受影響的檔案或規則
- 假設或限制

## 例外處理

- 如果使用者描述太模糊，先問最少量的釐清問題
- 如果變更會碰到 approval boundary，要先標示
- 如果只是概念討論，不要擅自改檔
