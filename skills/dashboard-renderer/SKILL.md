---
name: dashboard-renderer
description: |
  Renderer module for AI analytics dashboard generation. Converts structured Dashboard Specification (JSON) into a visual HTML report. Uses Chart.js for data visualization and modern CSS for layout.
---

# Dashboard Renderer Module v1

## Purpose
This skill defines how to transform a structured dashboard specification into a final, visually appealing HTML dashboard.

The Renderer is a PURE visualization layer. It MUST NOT perform analysis, recompute metrics, or access raw data.

---

## Input Contract (REQUIRED)

Renderer MUST only accept the following structured input:

### Dashboard Specification Schema
Reference: `skills/dashboard-renderer/dashboard-layout.schema.json`

- title
- layout
- pages[]
  - page_title
  - page_intent
  - widgets[]
    - type
    - title
    - data

The input is typically read from `tmp/dashboard-spec-{timestamp}.json`.

---

## Core Responsibilities

The Renderer is responsible for:

- Generating HTML structure based on the requested layout (hero-grid, one-column, two-column)
- Applying CSS styles for responsiveness and aesthetics
- Initializing Chart.js for all chart widgets
- Rendering KPI cards with trend indicators
- Exporting the final result to `output/dashboard-{timestamp}.html`

---

## Hard Constraints

- MUST NOT access raw data sources (BigQuery, GA4, CSVs, etc.)
- MUST NOT access Analysis Output directly
- MUST NOT modify the composition structure defined by the Composer
- MUST NOT perform new calculations (e.g. calculating % change) - these must be provided in the spec

---

## Layout Strategies

### hero-grid
- Featured KPIs at the top (hero section)
- Other widgets in a 2-column or 3-column grid below

### one-column
- All widgets stacked vertically in a single column
- Ideal for mobile or long-form narrative reports

### two-column
- Widgets split into two equal-width columns
- Good for side-by-side comparisons

---

## Widget Rendering Rules

### KPI Card
- Display `current` value prominently
- Display `change_pct` with color-coded trend (green for up, red for down, or according to metric meaning)
- Display `unit` (e.g. $, %, etc.)

### Line Chart
- Use Chart.js `line` type
- Map `labels` to X-axis
- Map `datasets` to Y-axis series
- Enable tooltips and legend

### Bar Chart
- Use Chart.js `bar` type
- Map `labels` to categories
- Map `values` to bar heights

---

## Output Rule

Renderer MUST write the final HTML file to:

output/dashboard-{timestamp}.html

Renderer MUST return:

- output_file_path
- status (success/failure)

---

## Failure Modes

- If `dashboard-spec.json` is missing or invalid → Log error and fail.
- If data for a widget is incomplete → Render a placeholder with an "Incomplete Data" message.
- If layout is unknown → Default to `one-column`.
