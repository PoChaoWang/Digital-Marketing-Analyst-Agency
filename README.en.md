# AI Ads Analyst Agent

[繁體中文](README.md) | [English](README.en.md)

## Table of Contents

- [What This MVP Is](#what-this-mvp-is)
- [What It Can Do Today](#what-it-can-do-today)
- [What It Cannot Do Today](#what-it-cannot-do-today)
- [Initial Setup](#initial-setup)
  - [1. Set up `.env`](#1-set-up-env)
  - [2. Optionally set up `config/accounts.yml`](#2-optionally-set-up-configaccountsyml)
  - [3. Set up `config/data-sources.yml`](#3-set-up-configdata-sourcesyml)
  - [4. What to ask AI if you do not understand MCP](#4-what-to-ask-ai-if-you-do-not-understand-mcp)
  - [5. If you do not have MCP, place CSV files in `data/`](#5-if-you-do-not-have-mcp-place-csv-files-in-data)
- [Business Context](#business-context)
- [Production MCP Adapters](#production-mcp-adapters)
- [Analysis Output](#analysis-output)
- [Glossary](#glossary)
- [Skill-Based Workflow](#skill-based-workflow)
- [Write Action Approval Policy](#write-action-approval-policy)
- [Troubleshooting](#troubleshooting)
- [Additional Notes](#additional-notes)

## What This MVP Is

AI Ads Analyst Agent is currently an MVP, or minimum viable product.

It is not a complete SaaS product. It is a safe, expandable workflow for AI-assisted advertising analysis. A marketer can ask the agent, in natural language, to analyze Google Ads, Meta Ads, GA4, or manually exported CSV reports.

The main goals are:

- Help marketers quickly review ad and website performance.
- Compare performance across time periods.
- Show data sources and analysis logic, so the analysis is not a black box.
- Allow manual CSV analysis when real MCP connections are not available.
- Stay read-only by default and avoid changing ad accounts.

## What It Can Do Today

- Analyze Google Ads, Meta Ads, and GA4 performance data.
- Compare the last 7, 14, 30 days, or another user-specified period.
- Report CPA, ROAS, CTR, CVR, CPM, CPC, spend, conversions, and revenue.
- Compare performance across Google Ads, Meta Ads, and GA4.
- Use GA4 to review landing pages, source / medium, campaign, and onsite behavior.
- Write full Markdown analysis reports to `output/`.
- Show Data sources, Environment Gate, Analysis Trace, and Data gaps in reports.
- Use CSV files under `data/` as explicit manual data sources in production.
- Use test data or Mock MCP under `test/` for development testing.
- Prepare Google Sheets report output when requested; actually creating a Sheet still requires Google Sheets / Google Drive tools in the runtime.

## What It Cannot Do Today

- It cannot invent performance numbers when data is missing.
- It cannot automatically modify campaigns, budgets, bids, targeting, creative, tracking, or status.
- It cannot automatically publish, pause, or delete ads.
- It cannot present test data as production data.
- It cannot present CSV, BigQuery, or SQL data as native platform MCP data.
- It cannot silently switch to another data source when MCP fails.
- `scripts/run-recipe.mjs` currently mainly supports the development Mock MCP path; production MCP and manual CSV runner support are future work.
- The BigQuery production source is currently marked as planned.

## Initial Setup

### 1. Set up `.env`

Copy:

```text
.env.example
```

to:

```text
.env
```

The most important settings are:

```env
APP_ENV=production
DATA_SOURCE_CONFIG=config/data-sources.yml
```

Common environments:

- `development`: for testing, mainly using data under `test/`.
- `production`: for real analysis, using production MCP, BigQuery / SQL, or explicitly provided CSV files under `data/`.

Do not commit API keys, OAuth secrets, access tokens, refresh tokens, client secrets, or developer tokens to git.

#### Where to find `.env` values

`.env` contains two kinds of values: environment settings and platform connection values.

Environment settings are usually decided by the person using this repo:

```env
APP_ENV=production
DATA_SOURCE_CONFIG=config/data-sources.yml
```

Platform connection values usually come from platform admin pages, developer dashboards, an agency, or an engineering / systems team. It is normal for marketers not to know how to generate every value.

Common Google Ads values:

- `GOOGLE_ADS_CUSTOMER_ID`: the Google Ads account ID you want to analyze. It is usually visible in the Google Ads UI near the account switcher.
- `GOOGLE_ADS_LOGIN_CUSTOMER_ID`: usually the MCC / manager account ID when accounts are managed through a manager account.
- `GOOGLE_ADS_CLIENT_ID` / `GOOGLE_ADS_CLIENT_SECRET`: OAuth client values, usually created in Google Cloud Console.
- `GOOGLE_ADS_DEVELOPER_TOKEN`: Google Ads API developer token, usually provided by someone with Google Ads API access.
- `GOOGLE_ADS_REFRESH_TOKEN`: OAuth refresh token, usually generated with help from someone familiar with OAuth.

Common Meta Ads values:

- `META_AD_ACCOUNT_ID`: the Meta ad account ID. It may look like `act_123456789` or a numeric ID and can usually be found in Ads Manager or Business Settings.
- `META_BUSINESS_ID`: the Business Manager / Business Portfolio ID.
- `META_APP_ID` / `META_APP_SECRET`: Meta Developer App values, usually created by someone with Meta Developer access.
- `META_ACCESS_TOKEN`: Meta API access token, usually provided by an admin, agency, or engineering team.

Common GA4 values:

- `GA4_PROPERTY_ID`: GA4 property ID, available in GA4 Admin under Property settings.
- `GA4_CREDENTIALS_JSON`: service account JSON, usually created by a Google Cloud / GA4 admin.
- `GA4_CLIENT_EMAIL` / `GA4_PRIVATE_KEY`: fields from a service account. If `GA4_CREDENTIALS_JSON` is used, these may not need to be filled separately.
- `GA4_CLIENT_ID` / `GA4_CLIENT_SECRET` / `GA4_REFRESH_TOKEN`: used only for OAuth-based setups.

If you are unsure which values are needed, check the MCP server documentation you plan to use. Different MCP servers may require different variables.

Safety reminders:

- Do not paste `.env` contents into README files, GitHub issues, public Slack channels, or analysis reports.
- For debugging, show only whether a value is present or missing, such as `GOOGLE_ADS_REFRESH_TOKEN=present`. Do not show the actual value.
- If a token was pasted publicly, treat it as leaked and regenerate it.

### 2. Optionally set up `config/accounts.yml`

If `.env` or your MCP runtime already manages account IDs and property IDs, you may not need `config/accounts.yml`.

`config/accounts.yml` is for human-readable account context, such as account labels, brand names, timezones, currencies, notes, or multi-account mapping. It should not require you to manually enter the same IDs already stored in `.env`.

If you want this extra context, copy:

```text
config/accounts.example.yml
```

to:

```text
config/accounts.yml
```

Useful fields include:

- account label
- brand / client name
- timezone
- currency
- notes

Do not commit `config/accounts.yml` to GitHub. It may contain client account context or internal naming.

### 3. Set up `config/data-sources.yml`

Copy:

```text
config/data-sources.example.yml
```

to:

```text
config/data-sources.yml
```

This file tells the agent:

- whether the current environment is development, test, or production
- which data sources are enabled
- which sources are test-only
- which sources are allowed for production analysis

Production sources should use:

- `production_allowed: true`
- `enabled: true`

### 4. What to ask AI if you do not understand MCP

MCP connects platforms such as Google Ads, Meta Ads, and GA4 to the AI agent, so the agent can read data directly.

If you do not have MCP right now, you can skip this step and use CSV import in the next step.

If you are not sure what MCP is, whether you need it, or whether you can set it up yourself, ask AI first. You do not need to understand command, runtime, or token details upfront.

You can ask:

```text
I want to use this repo to analyze Google Ads / Meta Ads / GA4.
I am not sure whether I have MCP or how to configure it.
Please inspect this repo and tell me which setup steps I can do myself and which may need technical help.
Do not ask me to paste any token or secret.
```

If you use Claude Code, you can ask:

```text
I use Claude Code.
Please inspect README.md, mcp.example.json, config/data-sources.yml, and docs/MCP_SETUP.md.
Tell me what I need to prepare for Google Ads / Meta Ads / GA4 MCP, and how to check whether MCP tools are visible.
Do not display or ask me to paste any token.
```

To check `.env` safely, ask:

```text
Please check whether .env has the required fields.
Only tell me which variables are present or missing. Do not display any real values.
```

If you do not have MCP and want to use CSV:

```text
I do not have MCP right now.
I will place Google Ads / Meta Ads / GA4 exported CSV files in data/.
Please tell me how to name the files and which columns are needed for safe analysis.
```

If you eventually need help from an engineer, agency, or system administrator, ask AI to prepare the request:

```text
Please create an MCP setup checklist for this repo.
Include:
- platforms to connect
- account/property IDs needed
- tokens or OAuth permissions needed
- where Claude Code / Codex / Cursor may need MCP settings
- how to verify that MCP tools are visible after setup
Do not include any real secrets.
```

If AI confirms that MCP is available, then your agent runtime needs to know:

- which MCP server to start
- which command starts it
- which `.env` variables should be passed to the server
- where the MCP settings live in your runtime, such as Claude Code, Claude Desktop, Codex, Cursor, or Windsurf

This repo only provides an example:

```text
mcp.example.json
```

It is a conceptual example and is not automatically loaded by every tool.

`mcp.example.json` does not take effect by itself. It only shows that MCP settings usually need `command`, `args`, and `env`. Copy the relevant ideas into your own agent runtime's MCP configuration.

If you need help, share the following with the person helping you:

- the platforms you want to connect, such as Google Ads, Meta Ads, GA4, or another platform
- the AI tool you use, such as Claude Code, Claude Desktop, Codex, Cursor, or Windsurf
- the `.env` variable names you have prepared, without real token values
- this repo's `mcp.example.json` and `docs/MCP_SETUP.md`

After setup, ask them to confirm that the AI tool can see the MCP tools.

Official MCP references:

- Google Ads MCP: https://developers.google.com/google-ads/api/docs/developer-toolkit/mcp-server
- Meta Ads MCP: https://www.facebook.com/business/help/1456422242197840
- GA4 MCP: https://developers.google.com/analytics/devguides/MCP

### 5. If you do not have MCP, place CSV files in `data/`

If MCP is not available, place manually exported CSV files in:

```text
data/
```

Use clear file names, for example:

```text
google_ads_YYYY-MM-DD_to_YYYY-MM-DD.csv
meta_campaign_YYYY-MM-DD_to_YYYY-MM-DD.csv
ga4_landing_page_YYYY-MM-DD_to_YYYY-MM-DD.csv
line_ads_campaign_YYYY-MM-DD_to_YYYY-MM-DD.csv
```

File names do not need to follow one exact format, but humans should be able to understand:

- source platform
- report level
- date range

When CSV is used, the agent must label the data as `csv_export` or manual source. It must not label CSV data as native MCP.

## Business Context

If you want the agent to understand the brand, KPI, and client priorities, copy:

```text
profile.example/business-context.md
```

to:

```text
profile/business-context.md
```

You can include:

- what the brand is
- main KPI, such as CPA, ROAS, revenue, signups, or leads
- what the client cares about most
- preferred reporting tone, such as executive summary or detailed analysis

Do not commit `profile/` to GitHub.

Business context only changes recommendation framing and communication. It does not replace real platform, GA4, warehouse, CSV, or MCP data.

## Production MCP Adapters

If you use real MCP, use production adapters:

- `connectors/google-ads-mcp.adapter.yml`
- `connectors/meta-ads-mcp.adapter.yml`
- `connectors/ga4-mcp.adapter.yml`

These adapters tell the agent:

- which platform the MCP source belongs to
- which MCP tool can fetch campaign performance
- how returned fields map to spend, clicks, conversions, revenue, and other metrics

The adapters currently contain placeholders such as:

```yaml
tool: REPLACE_WITH_GOOGLE_ADS_CAMPAIGN_PERFORMANCE_TOOL
```

Replace these with the actual MCP tool names exposed by your runtime.

If a production adapter still contains `REPLACE_WITH_...`, use one of these safe options:

1. Set the matching source in `config/data-sources.yml` to `enabled: false`.
2. Keep `enabled: true`, but the agent must fail closed at runtime and report that the MCP tool is not configured.

Before going live, option 1 is recommended.

Do not modify `connectors/mock-mcp.adapter.yml` for production data. Mock MCP is only for development / test.

## Analysis Output

Analysis results are written to:

```text
output/
```

The report language follows the user's main language. If the user asks in English, the report is in English. If the user asks in Traditional Chinese, the report is in Traditional Chinese.

Test environment filename example:

```text
output/zzz-test-analysis-20260528-143000-cross-channel.md
```

Production filename example:

```text
output/analysis-20260528-143000-google-ads.md
```

In test environments, the first Markdown line must clearly say:

```markdown
# This is TEST - Cross-channel Ads Performance Analysis
```

Production reports do not need an extra production marker.

Every report should include:

- Data sources
- Environment Gate result
- Analysis Trace
- Observations
- Inferences
- Recommendations
- Risks
- Data gaps

## Glossary

Terms, abbreviations, field codes, and ad format codes live in:

```text
docs/GLOSSARY.md
```

This helps the agent use consistent wording and avoid misunderstanding campaign names or field abbreviations.

Example Meta / Facebook ad format codes:

- `car`: Carousel Ads
- `img`: Image Ads
- `col`: Collection Ads
- `vid`: Video Ads

If you later use LINE Ads, TikTok Ads, or another platform, add common terms to the glossary.

## Skill-Based Workflow

This repo separates analysis rules into layers so they are easier to maintain.

### Main file responsibilities

- `CLAUDE.md`: top-level operating rules, such as source safety, environment checks, output rules, and approval policy.
- `modes/_shared.md`: shared metrics and rules used by all analyses.
- `skills/ads-analysis/SKILL.md`: the analysis workflow, including required files, source selection, and output.
- `modes/analyses/`: defines what kind of analysis is being performed.
- `modes/platforms/`: defines platform-specific interpretation rules.
- `docs/GLOSSARY.md`: term and abbreviation definitions.
- `templates/`: report formats.

### How the agent chooses modes

The agent first decides what kind of analysis the user wants, then determines which platforms are involved.

For example:

```text
Compare the last 7 days with the previous 7 days.
```

This should use:

- `modes/analyses/performance-summary.md`

If the data includes Google Ads, Meta Ads, and GA4, it should also use:

- `modes/analyses/cross-channel.md`
- `modes/platforms/google-ads.md`
- `modes/platforms/meta-ads.md`
- `modes/platforms/ga4.md`

Simple rule:

- `modes/analyses/`: analysis method
- `modes/platforms/`: platform knowledge

### Adding a GA4 User Journey analysis

If this is a new report or analysis method, add:

```text
modes/analyses/user-journey.md
```

If it is still exploratory and the data format is not stable, start with:

```text
modes/backlog/user-journey.md
```

Move it into `modes/analyses/` once the data fields and analysis method are stable.

### Adding LINE Ads analysis

If LINE Ads becomes a recurring data source, add:

```text
modes/platforms/line-ads.md
```

Also consider:

- adding LINE Ads terms to `docs/GLOSSARY.md`
- adding LINE Ads CSV column detection to `connectors/manual-csv.adapter.yml`
- adding a LINE Ads source entry to `config/data-sources.yml`

### Changing analysis logic

Change the right layer for the change:

- Data safety or folder access rules: `CLAUDE.md`
- Shared formulas or shared metrics: `modes/_shared.md`
- Performance summary, period comparison, or cross-channel logic: `modes/analyses/`
- Platform interpretation for Google Ads, Meta Ads, GA4, or LINE Ads: `modes/platforms/`
- Terms and abbreviations: `docs/GLOSSARY.md`
- Report structure: `templates/`

When changing logic:

- Do not let production silently read test data.
- Do not label CSV as MCP.
- Do not let the agent guess missing numbers.
- If you add a new analysis method, include example questions and expected data gaps.

## Write Action Approval Policy

The agent is read-only by default. It reads data and writes analysis reports.

Any change to an ad account requires explicit user approval first, including:

- campaign changes
- budget changes
- bid changes
- targeting changes
- creative changes
- tracking changes
- pausing or enabling ads
- status changes

Before approval, the agent may only make recommendations.

Creating or updating a Google Sheet report is a report artifact write, not an ad account change. However, any recommendation that changes campaigns or budgets still requires separate approval.

## Troubleshooting

### MCP tools are not visible

Check:

- whether the runtime loaded the MCP config
- whether the MCP command can run
- whether secrets are available to the runtime
- whether `REPLACE_WITH_...` placeholders were replaced with real MCP tool names

### The agent says no data source is available

Check:

- whether `.env` has the correct `APP_ENV`
- whether `config/data-sources.yml` has the right `enabled: true` source
- whether production sources have `production_allowed: true`
- if using CSV, whether `manual_csv_fallback` is enabled or exact CSV file paths were provided

### CSV files are in `data/`, but the agent does not read them

This is usually correct safety behavior. The agent should not scan `data/` automatically.

Provide exact files, for example:

```text
Please use data/google_ads_2026-05-01_to_2026-05-28.csv to analyze the last 28 days.
```

### The report starts with `# This is TEST`

This means the environment is development or test. Check `.env`:

```env
APP_ENV=production
```

### Numbers differ from the platform UI

Common reasons:

- date range mismatch
- timezone mismatch
- attribution window mismatch
- conversion definition mismatch
- GA4 key events are not the same as platform conversions
- data delay
- incomplete CSV export columns

### Google Sheets report was not created

The Google Sheets reporting skill defines the workflow, but creating or updating a Sheet requires Google Sheets / Google Drive tools in the runtime. If those tools are unavailable, the agent should write Markdown or a structured report instead of pretending that a Sheet was created.

## Additional Notes

### Test data and production data

- `test/`: development / test data only.
- `data/`: manually imported CSV files. Production can use this only when explicit.
- `output/`: analysis results. Do not commit generated reports to GitHub.

### Common data source types

- Native MCP: platform MCP sources such as Google Ads, Meta Ads, or GA4.
- Manual CSV: CSV files exported manually by users.
- BigQuery / SQL: future warehouse sources. The production BigQuery source is currently marked as planned.

### Related files

- `CLAUDE.md`: main agent operating rules.
- `DATA_CONTRACT.md`: data layering and commit rules.
- `docs/MCP_SETUP.md`: MCP and data source safety rules.
- `docs/GLOSSARY.md`: glossary and naming reference.
- `docs/GOOGLE_SHEETS_REPORTING.md`: Google Sheets reporting workflow.
