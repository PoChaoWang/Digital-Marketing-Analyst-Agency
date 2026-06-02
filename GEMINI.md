# Gemini CLI Project Instructions

## Foundational Mandates
- **Always adhere to `CLAUDE.md`**: This is the primary authority for data safety, environment gates, and analysis logic.
- **Read-Only by Default**: No write actions to ad platforms without explicit user approval.
- **Environment Awareness**: Always check `.env` and `APP_ENV` before proceeding with any analysis.

## Core Workflows
1. **Performance Analysis**: Use `scripts/combine_to_360_table.py` for data aggregation and `scripts/period_compare_360_table.py` for period comparisons.
2. **Reporting**: Follow `skills/ads-analysis/SKILL.md` for Markdown output and `scripts/push_to_sheets.py` for Google Sheets sync.
3. **Logic Reference**: Prioritize definitions in `modes/_shared.md` and `modes/analyses/` for metric calculations.

## Specialized Skills
- **Python Environment**: Use the `.venv` virtual environment for all python scripts.
- **MCP Integration**: Refer to `connectors/*.adapter.yml` for tool mapping.
