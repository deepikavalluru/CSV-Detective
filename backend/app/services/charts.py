def build_charts(investigation_steps):
    charts = []

    for step in investigation_steps:

        if step["tool"] == "compare_groups":

            result = step["result"]

            charts.append({
                "type": "bar",
                "title": (
                    f'{result["column"]} by '
                    f'{result["group_by"]}'
                ),
                "xKey": "group",
                "yKey": "value",
                "data": result["results"]
            })

        elif step["tool"] == "calculate_correlation":

            result = step["result"]

            if result["correlation"] is not None:
                charts.append({
                    "type": "scatter",
                    "title": (
                        f'{result["column_a"]} vs '
                        f'{result["column_b"]}'
                    ),
                    "columnA": result["column_a"],
                    "columnB": result["column_b"],
                    "correlation": result["correlation"],
                    "data": result["points"]
                })

        elif step["tool"] == "analyze_trend":

            result = step["result"]

            charts.append({
                "type": "line",
                "title": (
                    f'{result["value_column"]} over '
                    f'{result["date_column"]}'
                ),
                "xKey": "date",
                "yKey": "value",
                "data": result["results"]
            })

    return charts