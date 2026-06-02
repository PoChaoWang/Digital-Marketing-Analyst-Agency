# Output Artifacts Policy

- 一般分析任務必須輸出 Markdown 到 `output/`，不得只把完整結果寫在終端機。
- 本規則適用於會 fetch、計算、診斷、比較或提出建議的分析 / 報表任務；純設定確認、規則討論、實作修改或澄清回答不需輸出到 `output/`，除非使用者明確要求。
- 終端機回覆只提供簡短摘要、資料來源提醒與 `output/` 檔案路徑。
- `APP_ENV=development` 或 `test` 時，Markdown 檔名使用 `output/zzz-test-analysis-{generated_at}-{scope}.md`，例如 `output/zzz-test-analysis-20260528-143000-cross-channel.md`。
- `APP_ENV=production` 時，Markdown 檔名使用 `output/analysis-{generated_at}-{scope}.md`，例如 `output/analysis-20260528-143000-google-ads.md`。
- 測試 Markdown 第一行必須重點強調測試：`# This is TEST - {report_title}`。
- Production Markdown 第一行不用額外標示 production，直接使用正常報告標題：`# {report_title}`。
- Markdown 標題下方必須顯示輸出日期與時間：`Generated at: YYYY-MM-DD HH:mm:ss {timezone}`。
- Markdown 結構使用 `templates/analysis-output.md`，使用語言依照`policies/language-policy.md`。
- `output/` 是本機 artifact 目錄，不應提交到 git；只保留 `output/.gitkeep` 讓目錄存在。
- Markdown 分析結果必須包含 Data sources、Environment Gate result、Analysis Trace、Observation、Inference、Recommendation、Risks、Data gaps。
- 不得把 secrets、tokens、client secrets、refresh tokens、developer tokens、customer private identifiers 寫入 `output/`。
