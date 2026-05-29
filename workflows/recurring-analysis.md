# Recurring Analysis Workflow

Use this workflow when a scheduler, Codex Automation, CLI runner, or user asks to run a recurring task from `config/recurring-tasks.yml`.

This workflow does not replace `CLAUDE.md` `Mandatory Analysis Preflight`. Every recurring analysis still needs a fresh preflight before reading MCP, warehouse, CSV, `data/`, `test/`, or `exports/`.

If the user wants to create, change, pause, resume, or delete recurring tasks through conversation, use `workflows/recurring-task-wizard.md` first. This file is for running already-defined tasks.

## Purpose

Recurring tasks give marketers a default operating rhythm without needing to type the same prompt every day or every week.

Default MVP tasks:

- Daily: compare yesterday vs the day before yesterday.
- Weekly: compare last week vs the week before last.

All results are written to `output/` first. Slack, Microsoft Teams, email, or Google Sheets delivery can be added later, but must not store webhooks, tokens, or secrets in this repo.

## Relationship Between Task Table and Codex Automation

`config/recurring-tasks.yml` is the task table. It defines:

- Which tasks are enabled.
- When they should run.
- Which platforms are in scope.
- Which comparison periods to use.
- The user-facing question.
- Where output artifacts should be written.
- Whether notifications are disabled or routed elsewhere.

Codex Automation is the first scheduler. It should:

1. Wake up on the schedule configured in the Codex app.
2. Read `config/recurring-tasks.yml`.
3. Select tasks whose schedule matches the automation intent.
4. Run this workflow for each selected enabled task.
5. Return a concise summary and the generated `output/` path.

The Codex app schedule and `config/recurring-tasks.yml` schedule should match. The YAML is the source of truth for the task contract; the Codex app is the trigger.

## Codex Automation Prompts

Daily automation prompt:

```text
Every day at 09:00 Asia/Taipei, open this repo and run the enabled daily recurring analysis tasks in config/recurring-tasks.yml. Follow CLAUDE.md Mandatory Analysis Preflight, use workflows/recurring-analysis.md, write results to output/, and return only a concise summary plus output file paths. If production MCP is unavailable, use workflows/mcp-setup-wizard.md instead of fabricating data.
```

Weekly automation prompt:

```text
Every Monday at 09:00 Asia/Taipei, open this repo and run the enabled weekly recurring analysis tasks in config/recurring-tasks.yml. Follow CLAUDE.md Mandatory Analysis Preflight, use workflows/recurring-analysis.md, write results to output/, and return only a concise summary plus output file paths. If production MCP is unavailable, use workflows/mcp-setup-wizard.md instead of fabricating data.
```

## Execution Steps

For each recurring task:

1. Read `CLAUDE.md`.
2. Read this workflow.
3. Read `config/recurring-tasks.yml`.
4. Run `Mandatory Analysis Preflight`.
5. Read `skills/ads-analysis/SKILL.md`.
6. Read `modes/_shared.md`.
7. Read the relevant `modes/analyses/` file based on `analysis_intent`.
8. Read relevant `modes/platforms/` files based on `platforms`.
9. Re-read `config/data-sources.yml` or `DATA_SOURCE_CONFIG`.
10. Confirm `APP_ENV`.
11. Confirm allowed data sources.
12. If required production MCP is unavailable, stop analysis and use `workflows/mcp-setup-wizard.md`.
13. If allowed data sources are usable, run the matching recipe or MCP-backed analysis.
14. Write Markdown to `output/` using the normal `CLAUDE.md` output naming rules and the task `filename_scope`.
15. Reply with only:
    - Task name
    - Comparison period
    - High-signal summary
    - Data source status
    - Output file path

## Period Definitions

Use the scheduler timezone from `config/recurring-tasks.yml`.

- `yesterday`: the full calendar day before the run date.
- `day_before_yesterday`: the full calendar day two days before the run date.
- `last_week`: the previous completed Monday-Sunday week.
- `week_before_last`: the completed Monday-Sunday week before `last_week`.

If the business uses a different week definition, update `config/recurring-tasks.yml` before running weekly tasks.

## Output Requirements

Recurring task outputs must follow `CLAUDE.md` `Output Artifacts`:

- Write Markdown under `output/`.
- Do not put full analysis only in chat.
- Include Data sources, Environment Gate result, Analysis Trace, Observation, Inference, Recommendation, Risks, and Data gaps.
- Do not write secrets, tokens, private identifiers, or customer credentials.

## Notification Policy

The MVP notification mode is `output_only`.

When Slack or Microsoft Teams is added later:

- Store webhook URLs or tokens outside the repo.
- Keep only non-secret channel labels in config.
- Send a short summary and `output/` artifact path.
- Do not send raw secrets, customer private identifiers, or full unreviewed exports.
- If delivery fails, keep the Markdown output and report notification failure separately.

## Failure Behavior

Fail closed when data is unavailable.

Do not:

- Fabricate metrics.
- Silently fall back to CSV.
- Read `data/` without explicit user-provided files or allowed `manual_csv_fallback`.
- Treat mock MCP, CSV fixtures, or public sample data as production.

If a recurring task cannot run, write no analysis artifact unless enough verified data exists. Return a concise blocked status and the reason.
