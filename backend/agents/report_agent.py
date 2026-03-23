def generate_html_report(results: dict):
    print("COMPLETENESS RESULT:", results.get("completeness"))

    # ---------- NULLS ----------
    nulls = results.get("nulls", {})
    if isinstance(nulls, list):
        nulls = nulls[0] if nulls else {}
    null_count = nulls.get("NULL_COUNT") or nulls.get("null_count", 0)

    # ---------- DUPLICATES ----------
    dup = results.get("duplicates", {})
    if isinstance(dup, list):
        dup = dup[0] if dup else {}
    total_rows = dup.get("TOTAL_ROWS") or dup.get("total_rows", 0)
    duplicate_rows = dup.get("DUPLICATE_ROWS") or dup.get("duplicate_rows", 0)

    # ---------- COMPLETENESS ----------
    comp = results.get("completeness")
    if isinstance(comp, list):
        comp = comp[0] if comp else {}

    if isinstance(comp, dict):
        completeness = (
            comp.get("completeness_percent")
            or comp.get("COMPLETENESS_PERCENT")
            or comp.get("completeness")
            or comp.get("score")
            or 0
        )
    else:
        completeness = 0

    print("COMPLETENESS RESULT:", comp)

    # ---------- HTML ----------
    html = f"""
    <html>
    <head>
        <title>Data Quality Report</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {{ font-family: Arial; padding: 20px; }}
            h1 {{ color: #2c3e50; }}
            .card {{
                background: #f8f9fa;
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
            }}
        </style>
    </head>
    <body>
        <h1>📊 Data Quality Dashboard</h1>

        <div class="card">
            <canvas id="dqChart"></canvas>
        </div>

        <script>
            const ctx = document.getElementById('dqChart');

            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: ['Nulls', 'Duplicates', 'Completeness %'],
                    datasets: [{{
                        label: 'Data Quality Metrics',
                        data: [{null_count}, {duplicate_rows}, {completeness}],
                    }}]
                }}
            }});
        </script>

    </body>
    </html>
    """
    return html