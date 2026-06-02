import json
import sys
import os
from datetime import datetime
from pathlib import Path

class DashboardRenderer:
    def __init__(self, spec_path, output_dir="output/dashboard"):
        self.spec_path = spec_path
        self.output_dir = output_dir
        self.spec = None
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

    def render_kpi_card(self, widget):
        data = widget.get("data", {})
        current = data.get("current", 0)
        change_pct = data.get("change_pct", 0)
        unit = data.get("unit", "")
        
        delta_class = "delta-up" if change_pct >= 0 else "delta-down"
        delta_sign = "+" if change_pct >= 0 else ""
        
        # Format current value with commas
        formatted_value = f"{current:,}" if isinstance(current, (int, float)) else current
        
        return f"""
        <div class="widget kpi-card">
            <div class="widget-title">{widget.get('title', 'KPI')}</div>
            <div class="kpi-value">{unit}{formatted_value}</div>
            <div class="kpi-delta {delta_class}">{delta_sign}{change_pct}% vs previous</div>
        </div>
        """

    def render_chart(self, widget, chart_id):
        return f"""
        <div class="widget chart-widget">
            <div class="widget-title">{widget.get('title', 'Chart')}</div>
            <div class="chart-container">
                <canvas id="chart-{chart_id}"></canvas>
            </div>
            <p style="font-size: 0.8rem; color: #64748b; margin-top: 10px;">{widget.get('rationale', '')}</p>
        </div>
        """

    def generate_chart_js(self, widget, chart_id):
        chart_type = "line" if widget["type"] == "line_chart" else "bar"
        data = widget.get("data", {})
        
        labels = data.get("labels", [])
        
        if widget["type"] == "line_chart":
            datasets = []
            for ds in data.get("datasets", []):
                datasets.append({
                    "label": ds.get("label", "Series"),
                    "data": ds.get("values", []),
                    "borderColor": "rgb(37, 99, 235)",
                    "tension": 0.1,
                    "fill": False
                })
        else: # bar_chart
            datasets = [{
                "label": widget.get("metric") or widget.get("title") or "Value",
                "data": data.get("values", []),
                "backgroundColor": "rgba(37, 99, 235, 0.6)",
                "borderWidth": 1
            }]

        chart_config = {
            "type": chart_type,
            "data": {
                "labels": labels,
                "datasets": datasets
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "legend": {
                        "display": True if widget["type"] == "line_chart" else False
                    }
                }
            }
        }
        
        return f"new Chart(document.getElementById('chart-{chart_id}'), {json.dumps(chart_config)});"

    def render(self):
        self.load_spec()
        
        content_html = ""
        charts_js = ""
        chart_counter = 0
        
        layout_class = f"layout-{self.spec.get('layout', 'hero-grid')}"
        
        for page in self.spec.get("pages", []):
            content_html += f'<section class="page">'
            content_html += f'<h2 class="page-title">{page.get("page_title", "Untitled Page")}</h2>'
            content_html += f'<div class="{layout_class}">'
            
            for widget in page.get("widgets", []):
                if widget["type"] == "kpi_card":
                    content_html += self.render_kpi_card(widget)
                else:
                    chart_counter += 1
                    content_html += self.render_chart(widget, chart_counter)
                    charts_js += self.generate_chart_js(widget, chart_counter) + "\n"
            
            content_html += "</div></section>"

        final_html = self.templates["base"].replace("{{ title }}", self.spec.get("title", "Dashboard")) \
                                          .replace("{{ generated_at }}", datetime.now().strftime("%Y-%m-%d %H:%M:%S")) \
                                          .replace("{{ content }}", content_html) \
                                          .replace("{{ charts_js }}", charts_js)
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Use provided metadata or current time for filename
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_filename = f"dashboard-{timestamp}.html"
        output_path = Path(self.output_dir) / output_filename
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_html)
            
        return str(output_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python render_dashboard.py <spec_path>")
        sys.exit(1)
    
    spec_path = sys.argv[1]
    if not os.path.exists(spec_path):
        print(f"Error: Specification file not found at {spec_path}")
        sys.exit(1)
        
    renderer = DashboardRenderer(spec_path)
    path = renderer.render()
    print(f"Dashboard generated: {path}")
