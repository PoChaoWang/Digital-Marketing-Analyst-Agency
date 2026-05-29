# MCP Policy

- MCP tools 是廣告與分析帳戶資料的 source of truth。
- MCP tool 可用且通過 Environment Gate / allowlist 時，必須先查真實資料再分析。
- MCP tool 不可用、未通過 Environment Gate，或未在目前環境 allowlist 中啟用時，要明確告知缺少連線、憑證、runtime 設定或允許的資料來源，不可假裝已有資料。
- 不要假設 Google Ads MCP、Meta Ads MCP、GA4 MCP 的實際 tool name；使用目前 runtime 中可用的對應 MCP tools。
- 真實 MCP source 應使用對應 production adapter，例如 `connectors/google-ads-mcp.adapter.yml`、`connectors/meta-ads-mcp.adapter.yml`、`connectors/ga4-mcp.adapter.yml`；不要修改 `connectors/mock-mcp.adapter.yml` 來接 production。
- BigQuery MCP / SQL MCP 是 analytics source，不是原廣告平台控制層。除非另有 native write connector 且取得使用者同意，不可宣稱能把建議直接套用回來源平台。
- 當 MCP tool 不可用、adapter 仍包含 `REPLACE_WITH_*` placeholder、或 runtime tool mapping 尚未完成時，使用 `workflows/mcp-setup-wizard.md` 協助使用者逐一設定 Google Ads、Meta Ads、GA4 與必要的 BigQuery / SQL MCP。
- MCP setup wizard 只能收集非敏感設定資訊與 runtime tool mapping；不得要求、顯示或寫入 developer tokens、client secrets、refresh tokens、access tokens、service account private keys 或其他 secrets。
