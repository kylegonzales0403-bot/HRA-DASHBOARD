#!/usr/bin/env python3
"""
Generate HR Dashboard as standalone index.html for GitHub Pages
"""

import json
import base64

# HR Metrics Data
data = {
    "sites": ["Sec 1", "Sec 2", "Sec 3", "Sec 4"],
    "metrics": {
        "Absenteeism Rate": [0.0645, 0.0208, 0.0, 0.0],
        "Tardiness Rate": [0.0045, 0.0033, 0.0012, 0.0050],
        "Undertime Rate": [0.0000, 0.0002, 0.0000, 0.0000],
        "Turnover Rate": [0.3355, 0.2727, 0.2500, 0.0000],
        "Retention Rate": [0.6667, 0.7222, 0.7500, 1.0000],
        "Flight Risk Rate": [0.3396, 0.2674, 0.2500, 0.0000],
        "Overtime Rate": [0.2816, 0.0822, 0.1502, 0.0031]
    },
    "colors": {
        "Absenteeism Rate": "#1f77b4",
        "Tardiness Rate": "#ff7f0e",
        "Undertime Rate": "#2ca02c",
        "Turnover Rate": "#d62728",
        "Retention Rate": "#9467bd",
        "Flight Risk Rate": "#8c564b",
        "Overtime Rate": "#e377c2"
    }
}

# Generate chart configs for Plotly
def generate_chart_config(metric_name, values):
    """Generate Plotly chart configuration"""
    colors = data["colors"][metric_name]
    chart_config = {
        "data": [
            {
                "x": data["sites"],
                "y": values,
                "type": "bar",
                "marker": {"color": colors},
                "text": [f"{v:.2%}" for v in values],
                "textposition": "outside",
                "hovertemplate": "%{x}<br>Rate: %{text}<extra></extra>"
            }
        ],
        "layout": {
            "title": {"text": metric_name, "font": {"size": 16}},
            "xaxis": {"title": ""},
            "yaxis": {"title": "Rate", "tickformat": ".0%"},
            "margin": {"b": 40, "l": 50, "r": 40, "t": 40},
            "height": 350,
            "showlegend": False
        },
        "config": {"responsive": True, "displayModeBar": False}
    }
    return chart_config

# Generate HTML
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HR Metrics Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        header {
            background: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        header h1 {
            color: #333;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        header p {
            color: #666;
            font-size: 1.1em;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            transition: box-shadow 0.3s ease;
        }
        
        .card:hover {
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
        }
        
        .chart-container {
            width: 100%;
            height: 400px;
            min-height: 400px;
        }
        
        .table-container {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            overflow-x: auto;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95em;
        }
        
        thead {
            background-color: #f8f9fa;
            border-bottom: 2px solid #dee2e6;
        }
        
        th {
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #333;
        }
        
        td {
            padding: 12px;
            border-bottom: 1px solid #dee2e6;
            color: #666;
        }
        
        tbody tr:hover {
            background-color: #f8f9fa;
        }
        
        .metric-value {
            font-weight: 600;
            color: #667eea;
        }
        
        footer {
            text-align: center;
            color: rgba(255, 255, 255, 0.8);
            margin-top: 30px;
            padding: 20px;
            background: rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }
        
        @media (max-width: 768px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
            
            header h1 {
                font-size: 1.8em;
            }
            
            th, td {
                padding: 8px;
                font-size: 0.85em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 HR Metrics Dashboard</h1>
            <p>Comprehensive view of HR performance metrics across all sites</p>
        </header>
        
        <div class="dashboard-grid">
            <div class="card">
                <div id="chart-absenteeism" class="chart-container"></div>
            </div>
            <div class="card">
                <div id="chart-tardiness" class="chart-container"></div>
            </div>
            <div class="card">
                <div id="chart-undertime" class="chart-container"></div>
            </div>
            <div class="card">
                <div id="chart-turnover" class="chart-container"></div>
            </div>
            <div class="card">
                <div id="chart-retention" class="chart-container"></div>
            </div>
            <div class="card">
                <div id="chart-flightrisk" class="chart-container"></div>
            </div>
            <div class="card">
                <div id="chart-overtime" class="chart-container"></div>
            </div>
        </div>
        
        <div class="table-container">
            <h2 style="margin-bottom: 20px; color: #333;">Summary Table</h2>
            <table>
                <thead>
                    <tr>
                        <th>Site</th>
                        <th>Absenteeism</th>
                        <th>Tardiness</th>
                        <th>Undertime</th>
                        <th>Turnover</th>
                        <th>Retention</th>
                        <th>Flight Risk</th>
                        <th>Overtime</th>
                    </tr>
                </thead>
                <tbody>
"""

# Add table rows
sites = data["sites"]
for i, site in enumerate(sites):
    html_content += "                    <tr>\n"
    html_content += f"                        <td><strong>{site}</strong></td>\n"
    for metric in ["Absenteeism Rate", "Tardiness Rate", "Undertime Rate", "Turnover Rate", "Retention Rate", "Flight Risk Rate", "Overtime Rate"]:
        value = data["metrics"][metric][i]
        html_content += f"                        <td class='metric-value'>{value:.2%}</td>\n"
    html_content += "                    </tr>\n"

html_content += """                </tbody>
            </table>
        </div>
        
        <footer>
            <p>Generated: May 4, 2026 | HR Dashboard v1.0</p>
            <p><small>Powered by Plotly.js | GitHub Pages Ready</small></p>
        </footer>
    </div>
    
    <script>
        // Chart configurations
        const charts = {
"""

# Generate Plotly JavaScript
for metric_name in data["metrics"].keys():
    config = generate_chart_config(metric_name, data["metrics"][metric_name])
    chart_id = "chart-" + metric_name.lower().replace(" ", "-")
    html_content += f"            '{chart_id}': "
    html_content += json.dumps(config) + ",\n"

html_content = html_content.rstrip(",\n") + "\n        };\n"

html_content += """
        // Render all charts
        Object.entries(charts).forEach(([id, config]) => {
            const element = document.getElementById(id);
            if (element) {
                Plotly.newPlot(element, config.data, config.layout, config.config);
            }
        });
        
        // Responsive chart sizing
        window.addEventListener('resize', () => {
            Object.keys(charts).forEach(id => {
                const element = document.getElementById(id);
                if (element) {
                    Plotly.Plots.resize(element);
                }
            });
        });
    </script>
</body>
</html>
"""

# Write the HTML file
with open("index.html", "w") as f:
    f.write(html_content)

print("✓ Dashboard successfully generated!")
print("✓ Output file: index.html")
print("✓ Ready for GitHub Pages deployment!")
print("\nDashboard features:")
print("  - 7 interactive bar charts for HR metrics")
print("  - Responsive design (mobile-friendly)")
print("  - Data summary table")
print("  - Self-contained (no external data files needed)")
print("\nTo deploy to GitHub Pages:")
print("  1. Push index.html to your repository")
print("  2. Enable GitHub Pages in repository settings")
print("  3. Your dashboard will be live at: https://<username>.github.io/HRA-DASHBOARD/")
