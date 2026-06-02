import json
import sys
import os
from datetime import datetime
from pathlib import Path

class DashboardRenderer:
    TRANSLATIONS = {
        "en": {
            "lang": "en",
            "label_generated_at": "Generated at: ",
            "label_recommended_action": "Recommended Action",
            "label_business_impact": "Business Impact",
            "label_metric": "Metric"
        },
        "zh-TW": {
            "lang": "zh-Hant-TW",
            "label_generated_at": "產生時間：",
            "label_recommended_action": "建議行動",
            "label_business_impact": "業務影響",
            "label_metric": "指標"
        }
    }

    def __init__(self, spec_path, output_dir="output/dashboard", lang="en"):
        self.spec_path = spec_path
        self.output_dir = output_dir
        self.spec = None
        self.lang = lang
        self.templates = {}
        self.load_templates()

    def load_templates(self):
        template_dir = Path(__file__).parent / "templates"
        base_template_path = template_dir / "base.html"
        if not base_template_path.exists():
            raise FileNotFoundError(f"Base template not found at {base_template_path}")
            
        with open(base_template_path, "r", encoding="utf-8") as f:
            self.templates["base"] = f.read()

    def load_spec(self):
        with open(self.spec_path, "r", encoding="utf-8") as f:
            self.spec = json.load(f)
            if "lang" in self.spec:
                self.lang = self.spec["lang"]

    def render_kpi_mini(self, widget, trans):
        data = widget.get("data", {})
        current = data.get("current", 0)
        unit = data.get("unit", "")
        formatted_value = f"{current:,}" if isinstance(current, (int, float)) else current
        
        return f"""
        <div class="evidence-item kpi-mini">
            <div class="kpi-mini-value">{unit}{formatted_value}</div>
            <div class="kpi-mini-label">{widget.get('title', trans['label_metric'])}</div>
        </div>
        """

    def render_chart(self, widget, chart_id):
        return f"""
        <div class="evidence-item">
            <div style="font-size: 0.875rem; font-weight: 600; margin-bottom: 8px;">{widget.get('title', 'Chart')}</div>
            <div class="chart-container">
                <canvas id="chart-{chart_id}"></canvas>
            </div>
        </div>
        """

    def generate_chart_js(self, widget, chart_id):
        chart_type = widget["type"].replace("_chart", "")
        data = widget.get("data", {})
        labels = data.get("labels", [])
        
        if widget["type"] == "line_chart":
            datasets = []
            for ds in data.get("datasets", []):
                datasets.append({
                    "label": ds.get("label", "Series"),
                    "data": ds.get("values", []),
                    "borderColor": "rgb(37, 99, 235)",
                    "backgroundColor": "rgba(37, 99, 235, 0.05)",
                    "tension": 0.4,
                    "fill": True,
                    "pointRadius": 2
                })
        elif widget["type"] == "pie_chart":
            datasets = [{
                "data": data.get("values", []),
                "backgroundColor": [
                    "rgba(37, 99, 235, 0.8)",
                    "rgba(16, 185, 129, 0.8)",
                    "rgba(245, 158, 11, 0.8)",
                    "rgba(239, 68, 68, 0.8)",
                    "rgba(139, 92, 246, 0.8)"
                ],
                "borderWidth": 0
            }]
        else: # bar_chart
            if "datasets" in data:
                datasets = []
                colors = ["rgba(148, 163, 184, 0.5)", "rgba(37, 99, 235, 0.8)"]
                for i, ds in enumerate(data.get("datasets", [])):
                    datasets.append({
                        "label": ds.get("label", ""),
                        "data": ds.get("values", []),
                        "backgroundColor": colors[i % len(colors)],
                        "borderRadius": 4
                    })
            else:
                datasets = [{
                    "label": widget.get("title", "Value"),
                    "data": data.get("values", []),
                    "backgroundColor": "rgba(37, 99, 235, 0.8)",
                    "borderRadius": 4
                }]

        chart_config = {
            "type": chart_type,
            "data": { "labels": labels, "datasets": datasets },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": { 
                    "legend": { 
                        "display": True if widget["type"] in ["line_chart", "pie_chart"] or "datasets" in data else False,
                        "position": "bottom" if widget["type"] == "pie_chart" else "top",
                        "labels": { "boxWidth": 12, "usePointStyle": True }
                    }
                },
                "scales": { 
                    "x": { "grid": { "display": False }, "ticks": { "color": "#475569" } }, 
                    "y": { "grid": { "color": "#f1f5f9" }, "ticks": { "color": "#475569" } } 
                } if widget["type"] != "pie_chart" else {}
            }
        }
        return f"window.myCharts.push(new Chart(document.getElementById('chart-{chart_id}'), {json.dumps(chart_config)}));"

    def render_insight(self, insight, chart_counter, trans):
        evidence_html = ""
        charts_js = ""
        
        for item in insight.get("visualizations", []):
            if item["type"] == "kpi_card":
                evidence_html += self.render_kpi_mini(item, trans)
            else:
                chart_counter[0] += 1
                evidence_html += self.render_chart(item, chart_counter[0])
                charts_js += self.generate_chart_js(item, chart_counter[0]) + "\n"
        
        html = f"""
        <div class="insight-block">
            <div class="insight-header">
                <h3 class="finding-headline">{insight['finding']}</h3>
                <span class="signal-badge">{insight['decision_signal']}</span>
            </div>
            <div class="impact-section">
                <span class="impact-label">{trans['label_business_impact']}</span>
                <div class="impact-text">{insight['business_impact']}</div>
            </div>
            <div class="recommendation-box">
                <span class="recommendation-label">{trans['label_recommended_action']}</span>
                <div class="recommendation-text">👉 {insight['recommendation']}</div>
            </div>
            <div class="evidence-grid">
                {evidence_html}
            </div>
        </div>
        """
        return html, charts_js

    def render(self):
        self.load_spec()
        content_html = ""
        charts_js = ""
        chart_counter = [0]
        
        trans = self.TRANSLATIONS.get(self.lang, self.TRANSLATIONS["en"])

        if "sections" in self.spec:
            for section in self.spec.get("sections", []):
                content_html += f'<h2 class="section-title">{section["section_title"]}</h2>'
                for insight in section.get("insights", []):
                    i_html, i_js = self.render_insight(insight, chart_counter, trans)
                    content_html += i_html
                    charts_js += i_js
        else:
            for page in self.spec.get("pages", []):
                content_html += f'<h2 class="section-title">{page.get("page_title", "Summary")}</h2>'
                for finding in page.get("findings", []):
                    insight_map = {
                        "finding": finding.get("headline", ""),
                        "business_impact": finding.get("summary", "Analysis indicates measurable shifts in performance metrics."),
                        "decision_signal": finding.get("signal", "Observation"),
                        "recommendation": finding.get("recommendation", ""),
                        "visualizations": finding.get("evidence", [])
                    }
                    i_html, i_js = self.render_insight(insight_map, chart_counter, trans)
                    content_html += i_html
                    charts_js += i_js

        summary = self.spec.get("executive_summary", "")
        summary_section_html = f'<div class="executive-summary">{summary}</div>' if summary else ""

        final_html = self.templates["base"].replace("{{ title }}", self.spec.get("title", "Intelligence Report")) \
                                          .replace("{{ lang }}", trans["lang"]) \
                                          .replace("{{ label_generated_at }}", trans["label_generated_at"]) \
                                          .replace("{{ generated_at }}", datetime.now().strftime("%Y-%m-%d")) \
                                          .replace("{{ executive_summary_section }}", summary_section_html) \
                                          .replace("{{ content }}", content_html) \
                                          .replace("{{ charts_js }}", charts_js)

        os.makedirs(self.output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_path = Path(self.output_dir) / f"intelligence-report-{timestamp}.html"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_html)
        return str(output_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python render_dashboard.py <spec_path> [lang]")
        sys.exit(1)
    
    lang = sys.argv[2] if len(sys.argv) > 2 else "en"
    renderer = DashboardRenderer(sys.argv[1], lang=lang)
    print(f"Report generated: {renderer.render()}")
