---
name: dashboard-composer
description: |
  Composer module for AI analytics dashboard generation. Converts structured Analysis Output (insights, decision_signals, key_drivers) into dashboard composition specs including pages, charts, and layout decisions. Use when building or modifying dashboard structure from analysis results.
---

# Dashboard Composer Module v1

## Purpose
This skill defines how to transform structured analysis output into a deterministic dashboard composition plan.

The Composer does NOT perform analysis or recompute metrics. It only maps semantic outputs into visualization structure.

---

## Input Contract (REQUIRED)

Composer MUST only accept the following structured input:

### Analysis Output Schema
- insights[]
- decision_signals[]
- key_drivers[]
- recommendation_priority[]

Any raw data or unstructured analysis MUST be ignored.

---

## Core Responsibilities

The Composer is responsible for:

- Selecting which insights become visualizations
- Converting decision signals into actionable chart types
- Grouping related insights into dashboard pages
- Defining chart types and metrics mapping
- Ensuring information density constraints are respected

---

## Hard Constraints

- MAX pages: 3
- MAX charts per page: 3
- MUST prioritize decision_signals over insights
- MUST NOT perform new analysis or recalculation
- MUST NOT access raw data sources
- MUST NOT override analysis output

---

## Selection Priority Rules

1. decision_signals (highest priority)
2. high-confidence insights
3. key_drivers (for breakdown views only)

If conflict exists, decision_signals always win.

---

## Insight → Visualization Mapping

### Insight Type Mapping

- diagnostic → line chart (trend analysis required)
- confirmatory → KPI card or bar chart
- causal → grouped bar chart or segmented comparison
- anomaly → line chart with highlight markers

---

## Decision Signal → Chart Mapping

- increase → positive trend / uplift visualization
- decrease → declining trend visualization
- hold → flat trend or stability comparison
- shift → before/after comparison chart

---

## Key Driver Mapping Rules

Key drivers MUST be mapped into segmentation dimensions:

- channel
- campaign
- audience
- device
- geography (if available)

Output MUST include at least one breakdown chart if key_drivers exist.

---

## Dashboard Composition Structure

Composer MUST output the following structure:

### Pages

Each page MUST contain:

- page_title
- page_intent (overview / diagnosis / breakdown)
- charts[]

---

### Chart Spec

Each chart MUST include:

- chart_type (line / bar / KPI)
- metric(s)
- dimension(s)
- source_reference (insight or decision_signal id)
- title
- rationale (1 sentence)

---

## Page Design Rules

### Page 1: Executive Overview
- Only top decision_signals
- KPI-heavy layout
- Maximum 3 KPIs

### Page 2: Diagnostic View
- Root cause analysis charts
- Trend + comparison

### Page 3: Breakdown View (optional)
- segmentation by key_drivers
- deeper drill-down only

---

## Grouping Rules

Composer MUST group items when:

- same platform involved
- same metric family (CTR / CPC / ROAS)
- same time window comparison

Do NOT scatter related insights across pages.

---

## Output Rule

Composer MUST write the generated dashboard specification to:

tmp/dashboard-spec-{timestamp}.json

The output file MUST be valid JSON and conform to the Dashboard Composition Schema.

The output file becomes the single source of truth for downstream rendering.

Renderer MUST consume this file and MUST NOT re-read analysis results directly.

Composer MUST return:

- output_file_path
- page_count
- chart_count
- dashboard_title

---

## Output Format (v2.0 Insight-Centric Schema)

Composer MUST output strictly structured JSON conforming to version 2.0:

{
  "version": "2.0",
  "title": "Marketing Intelligence Report",
  "executive_summary": "High level summary...",
  "sections": [
    {
      "section_title": "Primary Performance Drivers",
      "insights": [
        {
          "finding": "Meta spend increased 35% while ROAS decreased 18%",
          "business_impact": "Marketing efficiency is deteriorating, increasing CPA across the board.",
          "decision_signal": "Review campaign targeting",
          "recommendation": "Audit audience segments and creative performance",
          "visualizations": [
            {
              "type": "line_chart",
              "title": "Spend vs ROAS Correlation",
              "data": {}
            }
          ]
        }
      ]
    }
  ]
}

---

## Failure Modes

If input is invalid:

* If missing decision_signals → return minimal KPI overview only
* If insights unstructured → ignore and rely on decision_signals only
* If conflicts exist → log and prioritize decision_signals

## Key Principle

The Composer is NOT intelligent in analysis.

It is a deterministic translation layer:

Analysis → Meaning
Composer → Structure
Renderer → Visualization

## Renderer Boundary

Renderer MUST only read:

tmp/dashboard-spec-{timestamp}.json

Renderer MUST NOT:

- access raw data
- access analysis output
- generate new insights
- modify composition decisions
