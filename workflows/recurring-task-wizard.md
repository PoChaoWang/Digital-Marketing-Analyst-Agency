# Recurring Task Wizard

Use this workflow when a non-technical user wants to create, change, pause, resume, or delete a recurring analysis task without editing `config/recurring-tasks.yml` directly.

This wizard creates task definitions only. It does not run analysis by itself.

## Trigger Phrases

Start this wizard when the user says things like:

- "新增一個每天要看的任務"
- "每週幫我看 Meta 成效"
- "我想固定追蹤 CPA"
- "幫我建立一個自動週報"
- "不要再每天跑這個任務"
- "把週報改成每週二"

## Safety Rules

- Do not ask the user to write YAML.
- Do not ask the user to know cron syntax.
- Do not collect credentials, tokens, webhook URLs, or secrets.
- Keep notification mode as `output_only` unless the user has already configured a supported notification runtime outside the repo.
- Before changing `config/recurring-tasks.yml`, show the proposed task summary and ask for explicit confirmation.
- If the change affects campaign, budget, bid, targeting, creative, tracking, or status write actions, stop and require separate explicit approval. Recurring analysis tasks are read-only by default.

## Create Task Conversation

Ask only the questions needed to build a safe task definition.

Recommended question order:

1. What do you want to track?
2. How often should it run?
3. Which platforms should be included?
4. What period should it compare?
5. What should the result focus on?
6. What language should the output use?

Example:

```text
我可以幫你建立固定任務。請用自然語言回答即可。

1. 你想固定追蹤什麼？例如：整體成效、CPA、ROAS、landing page CVR、素材疲乏、跨平台比較。
2. 多久跑一次？例如：每天 09:00、每週一 09:00、每月第一天。
3. 要包含哪些資料？例如：Google Ads、Meta Ads、GA4。
4. 要比較哪兩段時間？例如：昨天 vs 前天、上週 vs 上上週、最近 7 天 vs 前 7 天。
5. 結果要特別提醒什麼？例如：異常波動、預算消耗、CPA 上升、ROAS 下降。
```

If the user already provided enough information, do not ask again. Infer conservatively and show the inferred summary for confirmation.

## Frequency Mapping

Convert natural language into cron only after confirmation.

Common mappings:

- "每天 09:00": `0 9 * * *`
- "每週一 09:00": `0 9 * * MON`
- "每週二 09:00": `0 9 * * TUE`
- "每月 1 號 09:00": `0 9 1 * *`

Use `Asia/Taipei` unless the user specifies another timezone.

## Analysis Intent Mapping

Map the user's plain language to an active analysis intent:

- Overall performance, daily changes, weekly changes: `performance_summary`
- Cross-channel comparison, allocation, blended CPA/ROAS: `cross_channel`
- Landing page CVR, onsite quality, traffic quality: `landing_page_quality`

If the user asks for a backlog-only capability such as deep CPA diagnosis, budget pacing, creative fatigue, or attribution tracking, create the task only if it can be framed through an active workflow. Otherwise explain that it is not yet a production recurring workflow.

## Platform Mapping

Allowed platform values:

- `google_ads`
- `meta_ads`
- `ga4`

Use `ga4` whenever the task needs onsite behavior, conversion quality, landing page quality, source / medium, or attribution sanity checks.

## Period Mapping

Allowed common period values:

- `yesterday`
- `day_before_yesterday`
- `last_week`
- `week_before_last`
- `last_7_days`
- `previous_7_days`
- `last_30_days`
- `previous_30_days`

Daily default:

- `current_period: yesterday`
- `previous_period: day_before_yesterday`

Weekly default:

- `current_period: last_week`
- `previous_period: week_before_last`

## Proposed Task Summary

Before editing the task table, show a concise summary:

```text
我會建立這個固定任務：

- 任務名稱：daily_cpa_watch
- 執行時間：每天 09:00 Asia/Taipei
- 分析目標：performance_summary
- 資料來源：Google Ads、Meta Ads、GA4
- 比較區間：昨天 vs 前天
- 輸出：output/ Markdown
- 通知：暫不通知，只寫入 output/
- 重點：CPA 是否上升、conversion 是否下降、GA4 onsite quality 是否異常

是否確認新增到 config/recurring-tasks.yml？
```

Only write the file after the user clearly confirms.

## Task ID Rules

Generate stable snake_case task IDs:

- Use English keywords.
- Keep it short.
- Include frequency or focus when useful.
- Avoid customer names or private identifiers.

Examples:

- `daily_cpa_watch`
- `weekly_roas_review`
- `daily_landing_page_quality`
- `weekly_cross_channel_delta`

If the generated ID already exists, append a short suffix such as `_2` or choose a more specific focus.

## YAML Output Contract

New tasks must follow this shape:

```yaml
task_id:
  enabled: true
  schedule: "0 9 * * *"
  schedule_description: "Every day at 09:00 Asia/Taipei"
  language: zh-TW
  analysis_intent: performance_summary
  comparison:
    current_period: yesterday
    previous_period: day_before_yesterday
  platforms:
    - google_ads
    - meta_ads
    - ga4
  question: "..."
  output:
    type: markdown
    directory: output/
    filename_scope: task-id
  notify:
    mode: output_only
```

Do not add Slack or Teams secrets.

## Change Existing Task

When editing an existing task:

1. Read `config/recurring-tasks.yml`.
2. Identify the matching task.
3. Summarize the current task.
4. Show the proposed changes.
5. Ask for explicit confirmation.
6. Preserve unrelated tasks and comments where practical.

For pause/resume:

- Pause means `enabled: false`.
- Resume means `enabled: true`.

For delete:

- Prefer disabling first unless the user explicitly asks to remove the task.

## After Updating

After writing `config/recurring-tasks.yml`, summarize:

```text
已更新固定任務表：
- 任務名稱
- 執行時間
- 比較區間
- 輸出位置

提醒：Codex app Automation 的 schedule 也要與這個任務時間一致，否則 YAML 只是任務定義，不會自己觸發。
```
