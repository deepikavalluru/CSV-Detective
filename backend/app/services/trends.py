import pandas as pd


def analyze_trend(
    df: pd.DataFrame,
    value_column: str,
    date_column: str
):
    # 1. Check that the requested columns exist
    if value_column not in df.columns:
        raise ValueError(
            f"Column '{value_column}' does not exist"
        )

    if date_column not in df.columns:
        raise ValueError(
            f"Column '{date_column}' does not exist"
        )

    # 2. Check that the value column is numeric
    if not pd.api.types.is_numeric_dtype(df[value_column]):
        raise ValueError(
            f"Column '{value_column}' must be numeric"
        )

    # 3. Convert date column
    data = df.copy()

    data[date_column] = pd.to_datetime(
        data[date_column],
        errors="coerce"
    )

    # 4. Remove invalid rows
    data = data.dropna(
        subset=[date_column, value_column]
    )

    # 5. Check whether anything remains
    if data.empty:
        raise ValueError(
            "This dataset doesn't contain enough structured data "
            "for trend analysis."
        )

    # 6. Sort by date
    data = data.sort_values(date_column)

    # 7. Calculate trend
    trend = (
        data.groupby(date_column)[value_column]
        .sum()
        .reset_index()
    )

    return {
        "tool": "analyze_trend",
        "chart_type": "line",
        "date_column": date_column,
        "value_column": value_column,
        "results": [
            {
                "date": str(row[date_column]),
                "value": float(row[value_column])
            }
            for _, row in trend.iterrows()
        ]
    }