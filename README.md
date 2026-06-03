# AI Ads Analyst Agent

[繁體中文](README.zh-tw.md) | [English](README.md)

## Table of Contents

- [What AI Ads Analyst Agent Is](#what-ai-ads-analyst-agent-is)
- [What It Can Do Today](#what-it-can-do-today)
- [What It Cannot Do Today](#what-it-cannot-do-today)
- [Initial Setup](#initial-setup)
- [Analysis Output](#analysis-output)
- [Skill-Based Workflow](#skill-based-workflow)
  - [Main File Responsibilities](#main-file-responsibilities)
  - [How the Agent Chooses Modes](#how-the-agent-chooses-modes)
  - [Adding a GA4 User Journey Analysis](#adding-a-ga4-user-journey-analysis)
  - [Adding LINE Ads Analysis](#adding-line-ads-analysis)
  - [Changing Analysis Logic](#changing-analysis-logic)
- [Write Action Approval Policy](#write-action-approval-policy)
- [Troubleshooting](#troubleshooting)
  - [MCP tools are not visible](#mcp-tools-are-not-visible)
  - [The agent says no data source is available](#the-agent-says-no-data-source-is-available)
  - [CSV files are in `data/`, but the agent does not read them](#csv-files-are-in-data-but-the-agent-does-not-read-them)
  - [The report starts with `# This is TEST`](#the-report-starts-with--this-is-test)
  - [Numbers differ from the platform UI](#numbers-differ-from-the-platform-ui)
  - [Google Sheets report was not created](#google-sheets-report-was-not-created)
- [Additional Notes](#additional-notes)
  - [Test data and production data](#test-data-and-production-data)
  - [Common data source types](#common-data-source-types)
  - [Related files](#related-files)

## What AI Ads Analyst Agent Is

AI Ads Analyst Agent is currently an MVP, or minimum viable product.

Its goal is not to become a complete SaaS product yet. The purpose is to establish a safe, testable, and gradually extensible AI advertising analysis workflow. Users can ask AI, in natural language, to analyze Google Ads, Meta Ads, GA4, or manually imported CSV reports.

The core goals are:

- Help marketers quickly summarize advertising and website performance.
- Compare performance changes across different time periods.
- Label data sources and analysis logic to avoid black-box analysis.
- Support manual CSV analysis when real MCP connections are unavailable.
- Stay read-only by default and avoid changing ad accounts directly.

## What It Can Do Today

- Analyze Google Ads, Meta Ads, and GA4 performance data.
- Compare the past 7, 14, 30 days, or another specified period.
- Produce metrics such as CPA, ROAS, CTR, CVR, CPM, CPC, spend, conversions, and revenue.
- Compare cross-platform performance across Google Ads, Meta Ads, and GA4.
- Use GA4 to inspect landing page, source / medium, campaign, and onsite behavior performance.
- Write complete Markdown analysis results to `output/`.
- Show Data sources, Environment Gate, Analysis Trace, and Data gaps in reports.
- Use CSV files under `data/` as explicit manual import sources in production.
- Use test data or Mock MCP under `test/` for development testing.
- Plan Google Sheets reports when requested; actually creating a Sheet still requires Google Sheets / Google Drive tools in the runtime.

## What It Cannot Do Today

- It cannot invent performance numbers when data is missing.
- It cannot automatically modify campaign, budget, bid, targeting, creative, tracking, or status.
- It cannot automatically publish, pause, or delete ads.
- It cannot present test data as production data.
- It cannot present CSV, BigQuery, or SQL data as native platform MCP data.
- It cannot silently switch to another data source when MCP fails.
- `scripts/run-recipe.mjs` is currently treated as a legacy / development-only runner, mainly for Mock MCP and older recipe validation. Production-style cross-channel period comparison should use the Python + SQL 360 table workflow.
- The BigQuery production source is currently marked as planned and will be developed later.

## Initial Setup

Start with `/ma-start` so the agent can help you check and configure the environment through a guided conversation.

### Step 0. Read Current State

- The system detects the current environment and shows the setup progress and checklist.

### Step 1. Choose Data Source Mode

- **MCP mode**: connects to data sources such as Google Ads, Meta Ads, and GA4. This requires credentials and MCP tool mapping.
- **CSV mode**: manually imports report data. This does not require platform credentials; you can skip Step 2 and Step 3, then optionally complete Step 4 and Step 5.

### Step 2. Credential Setup (MCP Mode Only)

- Guides you to create a `.env` file in the repo root and fill in the environment variables required by Google Ads / Meta Ads / GA4.
- Do not commit API keys, OAuth secrets, access tokens, refresh tokens, client secrets, or developer tokens to git.

### Step 3. Adapter Tool Mapping (MCP Mode Only)

- The system prompts you to fill in the actual MCP server tool names in `connectors/*.adapter.yml`.
- You can skip this during initial setup and return to it after confirming that MCP tools are visible.

### Step 4. Create Account Context (`config/accounts.yml`)

- Recommended for MCP mode; optional for CSV mode.
- You can record brand, ad account labels, currency, timezone, and notes so the agent can produce clearer analysis.

### Step 5. Fill In Business Context

- Through guided questions, collect brand market, main KPI, client preferences, and reporting style.
- After confirmation, write the result to `profile/business-context.md`.

### Step 6. Setup Summary

- Shows the final setup status and recommended next step.
- If data sources are available, you can start running analysis tasks.

## Analysis Output

Analysis results are written to the `output/` folder.

According to `policies/language-policy.md`, the report language follows the user's primary language. If the user asks in Traditional Chinese, the report is in Traditional Chinese. If the user asks in English, the report is in English.

In test environments, filenames start with `zzz-test`, for example:

```text
output/zzz-test-analysis-20260528-143000-cross-channel.md
```

Production filename example:

```text
output/analysis-20260528-143000-google-ads.md
```

In test environments, the first Markdown line must clearly indicate:

```markdown
# This is TEST - Cross-channel Ads Performance Analysis
```

Production reports do not need an additional production marker.

Every analysis report should include:

- Data sources
- Environment Gate result
- Analysis Trace
- Observations
- Inferences
- Recommendations
- Risks
- Data gaps

## Skill-Based Workflow

This repo separates analysis rules into layers so they are easier to maintain.

### Main File Responsibilities

- `CLAUDE.md`: top-level operating rules, such as data safety, environment checks, output rules, and whether user approval is required.
- `modes/_shared.md`: shared metrics and rules used by all analyses.
- `skills/ads-analysis/SKILL.md`: the analysis workflow, including which files to read first, how to choose data sources, and how to output results.
- `modes/analyses/`: defines what type of analysis is being run.
- `modes/platforms/`: defines which platform the data comes from and what to watch for during interpretation.
- `reference/GLOSSARY.md`: term and abbreviation reference.
- `templates/`: report formats.

### How the Agent Chooses Modes

The agent first determines what type of analysis the user wants, then determines which platforms are involved.

For example:

```text
Compare the past 7 days with the previous 7 days.
```

This should prioritize:

- `modes/analyses/cross-channel.md`

If the data includes Google Ads, Meta Ads, and GA4, it also uses:

- `modes/platforms/google-ads.md`
- `modes/platforms/meta-ads.md`
- `modes/platforms/ga4.md`

Simple rule:

- `modes/analyses/`: analysis method
- `modes/platforms/`: platform knowledge

### Adding a GA4 User Journey Analysis

If this is a new report or analysis method, add:

```text
modes/analyses/user-journey.md
```

If you only want to record the idea for now, or the data format is still unstable, start with:

```text
modes/backlog/user-journey.md
```

Move it into `modes/analyses/` after the data fields and analysis method are stable.
If you are not familiar with how to add it, you can also ask the agent for help.

### Adding LINE Ads Analysis

If LINE Ads becomes a regular data source, add:

```text
modes/platforms/line-ads.md
```

Also consider:

- Adding LINE Ads common terms to `reference/GLOSSARY.md`.
- Adding LINE Ads CSV column detection to `connectors/manual-csv.adapter.yml`.
- Adding a LINE Ads data source setting to `config/data-sources.yml`.

### Changing Analysis Logic

Choose the file based on what you want to change:

- To change data safety or whether a folder can be read: edit `CLAUDE.md`.
- To change shared metric formulas: edit `modes/_shared.md`.
- To change performance summary, period comparison, or cross-channel analysis logic: edit `modes/analyses/`.
- To change platform interpretation for Google Ads, Meta Ads, GA4, or LINE Ads: edit `modes/platforms/`.
- To change terms and abbreviations: edit `reference/GLOSSARY.md`.
- To change report appearance: edit `templates/`.

When changing logic:

- Do not let production automatically read test data.
- Do not mislabel CSV as MCP.
- Do not let the agent guess missing numbers.
- If you add a new analysis method, it is best to also add example questions and expected data gaps.

## Write Action Approval Policy

This agent is read-only by default. It reads data and produces analysis.

Any action that changes an ad account must receive explicit user approval first, for example:

- Changing campaign
- Changing budget
- Changing bid
- Changing targeting
- Changing creative
- Changing tracking
- Pausing or enabling ads
- Changing status

Before approval, the agent can only make recommendations and must not execute changes directly.

Creating or updating a Google Sheet report is a report artifact and is not the same as changing an ad account. However, if the report recommends changing campaign or budget, that change still requires separate approval.

## Troubleshooting

### MCP tools are not visible

Check:

- Whether the runtime actually loaded the MCP config.
- Whether the MCP command can run.
- Whether secrets are loaded by the runtime.
- Whether `REPLACE_WITH_...` in adapters has been replaced with actual tool names.

### The agent says no data source is available

Check:

- Whether `.env` has the correct `APP_ENV`.
- Whether `config/data-sources.yml` has the correct `enabled: true`.
- Whether production sources have `production_allowed: true`.
- If using CSV, whether `manual_csv_fallback` is enabled or an exact CSV file path was provided.

### CSV files are in `data/`, but the agent does not read them

This is usually correct safety behavior. The agent should not automatically scan `data/`.

Specify the file explicitly, for example:

```text
Please use data/google_ads_2026-05-01_to_2026-05-28.csv to analyze the past 28 days.
```

### The report starts with `# This is TEST`

This means the current environment is development or test. Check `.env` or runtime environment variables:

```env
APP_ENV=production
```

### Numbers differ from the platform UI

Common reasons:

- Date range mismatch
- Timezone mismatch
- Attribution window mismatch
- Conversion definition mismatch
- GA4 key event and platform conversion are not the same event
- Data delay
- Incomplete CSV export columns

### Google Sheets report was not created

The Google Sheets reporting skill defines the workflow, but actually creating or updating a Sheet requires Google Sheets / Google Drive tools in the runtime. If the tools are unavailable, the agent should output Markdown or a structured report first and should not pretend that a Sheet was created.

## Additional Notes

### Test data and production data

- `test/`: only for development / test data.
- `data/`: for manually imported CSV files. Production can use it, but the file must be explicit.
- `output/`: for analysis results. Do not commit it to GitHub.

### Common data source types

- Native MCP: platform MCP sources such as Google Ads, Meta Ads, and GA4.
- Manual CSV: CSV files manually exported by the user.
- BigQuery / SQL: can be used as a warehouse source in the future. The production BigQuery source is currently marked as planned.

#### MCP setup wizard, added 5/29

`workflows/mcp-setup-wizard.md` is the conversational fallback for MCP setup.

It appears when an analysis or reporting task needs production MCP data, but preflight cannot find any usable production MCP source. Common causes include:

- `config/data-sources.yml` enables Google Ads, Meta Ads, or GA4 MCP, but the runtime does not have matching MCP tools.
- The production adapter still contains `REPLACE_WITH_*` placeholder tool names.
- The enabled source does not pass the current `APP_ENV` / Environment Gate.

What it does:

- Shows which data source settings have already been checked.
- Asks whether the user wants help setting up MCP.
- Guides setup for Google Ads, Meta Ads, GA4, and, if needed, BigQuery / SQL.
- Provides a skip option for each MCP source.
- Collects only non-sensitive setup information and runtime tool mapping.

How to modify it:

- To change the conversation flow, prompt text, platform order, or validation checklist, edit `workflows/mcp-setup-wizard.md`.
- To change when the wizard triggers, edit `CLAUDE.md`.
- Do not add token, secret, webhook, client secret, refresh token, developer token, or private key collection to this workflow.
- Do not modify `connectors/mock-mcp.adapter.yml` to represent production MCP.

#### Recurring task wizard, added 5/29

`workflows/recurring-task-wizard.md` lets non-technical users add, modify, pause, resume, or delete recurring analysis tasks through conversation without directly editing YAML.

It appears when the user asks for scheduled or repeated analysis, for example:

- "Check whether CPA gets worse every morning."
- "Compare last week and the week before every Monday."
- "Pause the daily performance check."

What it does:

- Uses natural language questions and does not require the user to know YAML or cron.
- Converts user answers into a proposed task definition.
- Shows a summary before modifying `config/recurring-tasks.yml`.
- Requires explicit user confirmation before writing task changes.
- By default, outputs results only as Markdown under `output/`.

How to modify it:

- To change questions, task ID rules, natural language mapping, or confirmation format, edit `workflows/recurring-task-wizard.md`.
- Actual recurring task definitions live in `config/recurring-tasks.yml`.
- Execution for already-defined tasks lives in `workflows/recurring-analysis.md`.
- Keep notification mode as `output_only` until Slack, Teams, or email delivery is configured outside this repo.
- Do not put Slack webhooks, Teams webhooks, tokens, or secrets in this repo.

### Related files

- `CLAUDE.md`: main agent operating rules.
- `policies/`: split policy files referenced by `CLAUDE.md`.
- `DATA_CONTRACT.md`: data layering and commit rules.
- `reference/MCP_SETUP.md`: MCP and data source safety rules.
- `reference/GLOSSARY.md`: glossary.
- `reference/GOOGLE_SHEETS_REPORTING.md`: Google Sheets reporting workflow.
- `config/recurring-tasks.yml`: recurring analysis task table.
- `config/priority-overrides.example.yml`: source priority override example.
- `sql/build_360_table.sql`: readable SQL for paid media union, source priority, dedupe, and GA4 left join.
- `scripts/combine_to_360_table.py`: applies SQL and writes `exports/360_table.csv`.
- `scripts/period_compare_360_table.py`: runs period comparison using `exports/360_table.csv`.
- `workflows/360-table-workflow.md`: SQL-backed 360 table and period comparison workflow.
- `workflows/mcp-setup-wizard.md`: conversational MCP setup fallback.
- `workflows/recurring-task-wizard.md`: conversational recurring task creation and editing workflow.
- `workflows/recurring-analysis.md`: execution workflow for already-defined recurring tasks.
