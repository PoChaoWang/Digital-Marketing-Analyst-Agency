# MCP Setup Wizard

Use this workflow when an analysis or reporting request needs production MCP data, but the runtime has no usable Google Ads, Meta Ads, GA4, BigQuery, or SQL MCP source after `CLAUDE.md` `Mandatory Analysis Preflight` and `Environment Gate`.

This workflow is only for guided configuration. It must not collect, print, store, or commit secrets.

## Trigger Conditions

Start this wizard only after checking all of the following:

1. `DATA_SOURCE_CONFIG` or `config/data-sources.yml` has been freshly read.
2. `APP_ENV` has been resolved.
3. Enabled sources were checked against `environment`, `source_type`, and `production_allowed`.
4. Runtime MCP tools were checked without assuming exact tool names.
5. Production adapters were checked for placeholder tool names such as `REPLACE_WITH_*`.
6. No allowed production MCP source is usable for the requested analysis.

If at least one allowed production MCP source is usable, do not start the wizard. Show the available data sources and continue with the normal analysis flow.

## Initial Response

If no usable production MCP source is available, reply with a short status summary:

```text
目前沒有偵測到可用的 production MCP 資料來源。

已檢查：
- config/data-sources.yml 或 DATA_SOURCE_CONFIG
- APP_ENV
- enabled / environment / source_type / production_allowed
- runtime MCP tools
- production adapter tool mapping

是否需要協助設定 MCP？
1. 需要
2. 不需要
3. 不需要，並且不再顯示，有需要會再下指令
```

Do not run analysis until the user provides a usable data source or explicitly switches to an allowed fallback.

## Choice Handling

- `1. 需要`: start the platform-by-platform setup flow.
- `2. 不需要`: stop the setup flow and explain that analysis cannot use production MCP data until a usable source is configured.
- `3. 不需要，並且不再顯示，有需要會再下指令`: stop the setup flow and record the preference only in a local non-committed profile file if the user explicitly allows writing it.

Suggested local preference file:

```text
profile/mcp-onboarding.yml
```

Do not create this file without explicit user confirmation.

## Platform Setup Order

Ask one platform at a time. Each platform must include a skip option.

Default order:

1. Google Ads MCP
2. Meta Ads MCP
3. GA4 MCP
4. BigQuery / SQL MCP, only if the user needs warehouse-backed analytics

## Google Ads MCP Prompt

```text
要設定 Google Ads MCP 嗎？
1. 設定 Google Ads MCP
2. 略過 Google Ads MCP
```

If the user chooses setup, ask only for non-secret information:

- Account label for reporting
- Google Ads customer ID
- Login customer ID, if needed
- Timezone
- Currency
- Runtime MCP tool names exposed by the current agent runtime

Never ask for or store:

- Developer token
- Client secret
- Refresh token
- Access token
- Service account private key

Configuration targets:

- Runtime / secret manager: credentials and MCP command
- `connectors/google-ads-mcp.adapter.yml`: runtime tool mapping only
- `config/data-sources.yml`: source enablement only
- `config/accounts.yml` or `profile/`: readable account labels only, if needed and kept out of git

## Meta Ads MCP Prompt

```text
要設定 Meta Ads MCP 嗎？
1. 設定 Meta Ads MCP
2. 略過 Meta Ads MCP
```

If the user chooses setup, ask only for non-secret information:

- Account label for reporting
- Meta ad account ID
- Business label, if useful
- Pixel ID or event source label, if needed for diagnostics
- Timezone
- Currency
- Runtime MCP tool names exposed by the current agent runtime

Never ask for or store:

- App secret
- Access token
- System user token
- Long-lived token

Configuration targets:

- Runtime / secret manager: credentials and MCP command
- `connectors/meta-ads-mcp.adapter.yml`: runtime tool mapping only
- `config/data-sources.yml`: source enablement only
- `config/accounts.yml` or `profile/`: readable account labels only, if needed and kept out of git

## GA4 MCP Prompt

```text
要設定 GA4 MCP 嗎？
1. 設定 GA4 MCP
2. 略過 GA4 MCP
```

If the user chooses setup, ask only for non-secret information:

- Property label for reporting
- GA4 property ID
- Timezone
- Currency
- Key event names, if already known
- Runtime MCP tool names exposed by the current agent runtime

Never ask for or store:

- Client secret
- Refresh token
- Access token
- Service account private key

Configuration targets:

- Runtime / secret manager: credentials and MCP command
- `connectors/ga4-mcp.adapter.yml`: runtime tool mapping only
- `config/data-sources.yml`: source enablement only
- `config/accounts.yml` or `profile/`: readable property labels only, if needed and kept out of git

## BigQuery / SQL MCP Prompt

Use this step only when native platform MCPs are unavailable or the user explicitly needs warehouse data.

```text
要設定 BigQuery / SQL MCP 做 read-only analytics 嗎？
1. 設定 BigQuery / SQL MCP
2. 略過 BigQuery / SQL MCP
```

If the user chooses setup, ask only for non-secret information:

- Warehouse type
- Project or connection label
- Dataset / schema label
- Summary table names
- Required date column names
- Query cost guardrails
- Runtime MCP tool names exposed by the current agent runtime

Never ask for or store database passwords, private keys, access tokens, or service account secrets.

BigQuery / SQL MCP must remain read-only analytics source unless a separate write connector exists and the user explicitly approves the write action.

## Validation After Setup

After each configured platform:

1. Re-read `config/data-sources.yml` or `DATA_SOURCE_CONFIG`.
2. Re-read the relevant adapter.
3. Confirm no `REPLACE_WITH_*` placeholder remains for required capabilities.
4. Confirm the runtime exposes the named MCP tools.
5. Run only a minimal read-only metadata check, if the runtime supports one.
6. Report the status as `usable`, `configured but not validated`, `skipped`, or `blocked`.

Do not fetch campaign, budget, bid, targeting, creative, tracking, or status data until the normal `Mandatory Analysis Preflight` confirms the source is allowed for the current request.

## Status Summary Format

After the wizard finishes or the user stops it, summarize:

```text
MCP 設定狀態：
- Google Ads MCP: usable / configured but not validated / skipped / blocked
- Meta Ads MCP: usable / configured but not validated / skipped / blocked
- GA4 MCP: usable / configured but not validated / skipped / blocked
- BigQuery / SQL MCP: usable / configured but not validated / skipped / blocked

下一步：
- 可以開始分析的資料來源
- 仍缺少的 runtime 設定或 adapter tool mapping
- 是否需要使用 manual CSV fallback
```

Keep the response concise. Do not include secrets or private identifiers unless the user explicitly provided non-secret labels for display.
