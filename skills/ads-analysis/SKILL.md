# Ads Analysis Skill

## Purpose

Use this skill when the user asks for advertising, growth, paid media, GA4, onsite behavior, campaign audit, weekly performance, platform performance summary, landing page quality, or cross-channel analysis.

This skill fetches source data, applies the relevant analysis modes, and produces a structured analysis output that can be used directly or passed to another skill such as `skills/google-sheets-reporting/`.

This MVP only treats recipe-backed analyses as active workflows. Non-recipe-backed diagnosis modes live under `modes/backlog/` and should not be treated as default executable workflows unless the user explicitly asks to reference backlog material.

## Required Reading

Before fetching data or producing analysis, run `CLAUDE.md` `Mandatory Analysis Preflight`. This applies to every CLI, agent runtime, subagent, and automation runner unless the user explicitly says to skip it.

Always read:

- `CLAUDE.md`
- `modes/_shared.md`
- `config/data-sources.yml` or the file specified by `DATA_SOURCE_CONFIG`
- `templates/analysis-output.md` or the localized template selected by output language
- Matching `recipes/*.yml` when the request is a metric lookup, aggregation, period comparison, platform summary, or GA4 landing page quality task
- Matching `connectors/*.adapter.yml` when a recipe is used

Optionally read:

- `profile/business-context.md` if it exists. If it does not exist, record `Business context not provided` in Data Gaps and continue.

Then read relevant mode files:

Analysis modes, selected by user intent:

Active MVP analysis modes:

- Performance summary / weekly or monthly report: `modes/analyses/performance-summary.md`
- Landing page quality / onsite conversion quality: `modes/analyses/landing-page-quality.md`
- Cross-channel comparison / blended CPA or ROAS: `modes/analyses/cross-channel.md`

Backlog reference modes, not active workflows:

- CPA diagnosis / high CPA / conversion efficiency: `modes/backlog/cpa-diagnosis.md`
- Budget pacing / budget allocation: `modes/backlog/budget-pacing.md`
- Creative fatigue / frequency and creative performance: `modes/backlog/creative-fatigue.md`
- Attribution / tracking / conversion mismatch: `modes/backlog/attribution-tracking.md`

Only read a backlog reference mode when the user explicitly asks for that deeper diagnosis or when the active recipe-backed workflow is insufficient. In that case, disclose that the capability is backlog/reference-only and record it in Analysis Trace.

Platform modes, selected by involved data sources:

- Google Ads platform data: `modes/platforms/google-ads.md`
- Meta Ads platform data: `modes/platforms/meta-ads.md`
- GA4 / onsite analytics data: `modes/platforms/ga4.md`

Read `docs/GLOSSARY.md` when source data contains abbreviations, naming codes, ad format codes, or unclear report terminology.

## Inputs

Confirm or infer safely:

- Environment: `APP_ENV`
- Data source allowlist: `DATA_SOURCE_CONFIG` or `config/data-sources.yml`
- Business context: `profile/business-context.md` if available
- Output language / locale
- Date range
- Timezone
- Currency
- Platforms
- Account / property / campaign scope
- Data source type: native MCP, warehouse MCP / SQL, or CSV
- Requested report type or business question

If date range is missing, ask for it unless the user explicitly says to use a default such as last 7 days or last 30 days.

## Data Access Rules

- Run Environment Gate before looking for MCP tools, local CSV files, warehouse tables, `test/`, `data/`, or `exports/`.
- If a matching recipe exists under `recipes/`, use `scripts/run-recipe.mjs` instead of manually aggregating raw rows.
- Use available Google Ads MCP tools for Google Ads data only when the source is allowed by the current environment allowlist.
- Use available Meta Ads MCP tools only when the source is allowed by the current environment allowlist.
- Use available GA4 MCP tools only when the source is allowed by the current environment allowlist.
- Use BigQuery / SQL MCP only as read-only analytics source and only when allowed by the current environment allowlist.
- Use CSV only when explicitly allowed by `APP_ENV` and `config/data-sources.yml`; development/test CSV fixtures must live under `test/csv/` and be labeled clearly as `csv_fixture`.
- Use Mock MCP test sources only when explicitly allowed by `APP_ENV` and `config/data-sources.yml`; development/test Mock MCP assets must live under `test/mock-mcp/` and be labeled clearly as `mock_mcp`.
- Use official/public sample data only when explicitly allowed by `APP_ENV` and `config/data-sources.yml`; development/test public sample assets must live under `test/public-data/` and be labeled clearly as `public_sample`.
- Do not assume exact MCP tool names.
- If source tools are unavailable or not allowed by Environment Gate, state what is missing and do not fabricate metrics.

## Environment Gate

Before fetching data:

1. Read `APP_ENV`; if it is missing, assume `development` and disclose that assumption.
2. Read `DATA_SOURCE_CONFIG`; if missing, check `config/data-sources.yml`.
3. If the allowlist exists, list enabled sources whose `environment` matches `APP_ENV`.
4. In production, reject any source where `production_allowed` is not `true`, any `source_type: csv_fixture`, `mock_mcp`, or `public_sample`, and any direct use of `test/`. Allow `data/` only for explicit manual CSV fallback when `manual_csv_fallback` is enabled or the user provides exact CSV file paths; label it as `csv_export` / manual source.
5. In development/test, allow only matching enabled sources under `test/`; do not scan local directories beyond the allowlist.
6. If no source passes the gate, stop and report a data gap instead of analyzing.
7. Record the gate result in `analysis_trace.source_selection` and in the report's Data sources section.

## Analysis Steps

1. Run `Mandatory Analysis Preflight` from `CLAUDE.md`.
2. Run Environment Gate.
3. Determine analysis intent and read the matching active `modes/analyses/` file(s).
4. Determine involved platforms and read the matching `modes/platforms/` file(s).
5. Determine whether a matching recipe exists under `recipes/`.
6. If a recipe exists, run `scripts/run-recipe.mjs` and use its compact JSON output as the evidence source.
7. If no active recipe-backed workflow exists, stop and explain the gap unless the user explicitly asks to use backlog/reference material.
8. Normalize metrics and units.
9. Record data source, freshness, attribution window, timezone, currency, and conversion definition.
10. Record the analysis trace: preflight result, Environment Gate result, business context status, analysis modes, platform modes, recipe/script used, source selection, field mapping, metric formulas, assumptions, and decision log.
11. Produce observations from data only.
12. Produce inferences with confidence and assumptions.
13. Produce recommendations with priority and risk.
14. Record data gaps and follow-up questions.
15. Write the full analysis result as Markdown to `output/` using the selected analysis template when this is an analysis/reporting task.
16. Output data matching `skills/ads-analysis/output.schema.json` when the next step is automated reporting.

## Recipe Selection

Use these recipes when they match the request:

- `recipes/platform-campaign-performance.yml`: platform totals, campaign performance, spend / impressions / clicks lookup, CPA / ROAS summary for Google Ads or Meta Ads.
- `recipes/ga4-landing-page-quality.yml`: GA4 landing page quality, paid traffic onsite quality, landing page CVR.
- `recipes/cross-channel-period-compare.yml`: Google Ads + Meta Ads + GA4 period comparison, blended CPA / ROAS, attribution sanity check.

Example commands:

```bash
node scripts/run-recipe.mjs platform-campaign-performance --platform meta_ads
node scripts/run-recipe.mjs ga4-landing-page-quality
node scripts/run-recipe.mjs cross-channel-period-compare --start 2026-05-01 --end 2026-05-28 --previous-start 2026-04-03 --previous-end 2026-04-30
```

## Output Requirements

Every analysis must include:

- Date range
- Platform
- Account / campaign scope
- Mandatory Analysis Preflight result
- Environment Gate result
- Data sources
- Observation
- Inference
- Recommendation
- Analysis trace / reasoning basis
- Risks
- Data gaps

Use `Observation` only for facts shown in fetched data. Use `Inference` for interpretation. Use `Recommendation` for actions.

`Analysis trace` must be reviewable by a user. It should show which instructions/modes were used, why a source was selected, how fields were mapped, which metric formulas were applied, and what assumptions were made. Do not present private chain-of-thought; present concise, verifiable reasoning steps and evidence links/row references.

## Language and Template Selection

- Default output language follows the user's latest request language.
- If the user explicitly specifies `output_language`, report language, or locale, use that language.
- For Traditional Chinese output, use `templates/analysis-output.zh-TW.md`.
- For English or unknown language output, use `templates/analysis-output.md`.
- Keep common marketing analytics terms in English when practitioners commonly use them: CPA, ROAS, CTR, CVR, GA4, MCP, campaign, ad set, source / medium, landing page.
- Preserve raw identifiers and source values exactly: campaign names, ad names, account names, URLs, UTMs, source / medium, schema field names.
- Record selected output language and template in `Analysis Trace`.

## Local Markdown Output

For every analysis task in this repo, write the full analysis result as a Markdown file under `output/`. Do not put the full analysis only in the terminal response.

This output requirement applies to analysis/reporting tasks that fetch, compute, diagnose, compare, or recommend based on ad/GA4/warehouse/CSV data. It does not apply to pure configuration checks, rules discussion, implementation work, or clarification answers unless the user explicitly asks for an output artifact.

Use the template selected by `Language and Template Selection`. The file must include:

- Title:
  - `# This is TEST - {report_title}` for `APP_ENV=development` or `APP_ENV=test`
  - `# {report_title}` for `APP_ENV=production`
- Generated-at timestamp in the configured timezone, formatted as `YYYY-MM-DD HH:mm:ss {timezone}`
- Output file path
- Date range, platform, account/campaign scope
- Data sources and Environment Gate result
- Analysis Trace
- Executive summary
- Key findings
- Prioritized actions
- Risks and assumptions
- Data gaps

Use these filename patterns:

```text
output/zzz-test-analysis-{YYYYMMDD-HHMMSS}-{scope}.md
output/analysis-{YYYYMMDD-HHMMSS}-{scope}.md
```

Examples:

```text
output/zzz-test-analysis-20260528-143000-cross-channel.md
output/analysis-20260528-143000-google-ads.md
```

The terminal response should only summarize the result briefly and provide the Markdown file path.

Do not write raw source exports, secrets, tokens, or credentials to `output/`.

## Safety

- Read-only by default.
- Do not modify campaigns, budgets, bids, targeting, creatives, tracking, or status.
- For any write action request, stop and use `templates/change-approval.md`.
- Do not output secrets, tokens, private keys, customer credentials, or hidden config values.
