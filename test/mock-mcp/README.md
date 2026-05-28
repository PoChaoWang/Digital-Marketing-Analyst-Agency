# Mock MCP Server

This is a zero-dependency MCP protocol server for development tests. It exposes fake Google Ads, Meta Ads, and GA4 tools over stdio, so agents can test MCP tool discovery and tool calls without real ad accounts.

## Purpose

- Verify the agent can see MCP tools.
- Verify `APP_ENV=development` uses `mock_mcp_development` instead of CSV fixtures.
- Verify analysis output labels the source as `mock_mcp`.
- Avoid real Google Ads, Meta Ads, GA4 credentials during development.

## Run Smoke Test

```bash
cd test/mock-mcp
npm run smoke
```

The smoke test starts `server.js`, calls `initialize`, lists tools, and calls one Google Ads tool.

## MCP Runtime Config Example

From the repo root:

```json
{
  "mcpServers": {
    "mock-ads": {
      "command": "node",
      "args": ["test/mock-mcp/server.js"]
    }
  }
}
```

## Tools

- `get_environment_info`
- `get_google_ads_campaign_performance`
- `get_meta_ads_campaign_performance`
- `get_ga4_landing_page_performance`

All performance tools accept:

```json
{
  "start_date": "2026-04-29",
  "end_date": "2026-05-28"
}
```

Dates are optional. If omitted, the fixture date range is returned.

## Fixture Policy

Fixtures in this directory are fake development data. They are safe to commit and must never be used in production analysis.
