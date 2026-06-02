# Language Policy

- 預設 output language 跟隨使用者最新請求的主要語言。
- 若使用者明確指定 `output_language`、報表語言或 locale，優先使用使用者指定語言。
- 若使用者語言不明，預設使用英文。
- 使用者使用英文或未指定語言時，分析 Markdown 使用 `templates/analysis-output.md`。
- 必要的行銷與分析術語可保留英文，例如 CPA、ROAS、CTR、CVR、GA4、MCP、campaign、ad set、source / medium、landing page。
- 不翻譯 campaign name、ad name、account name、URL、UTM、source / medium、schema 欄位名稱或原始資料值。
- 若報表與 chat 回覆語言不同，必須在 Analysis Trace 標明原因。
