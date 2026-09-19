import pandas as pd


def detect_anomalies(
    df: pd.DataFrame,
    column: str
):
    # -------------------------
    # 1. Validate column
    # -------------------------

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist"
        )

    # -------------------------
    # 2. Validate numeric type
    # -------------------------

    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(
            f"Column '{column}' must be numeric"
        )

    # -------------------------
    # 3. Remove missing values
    # -------------------------

    series = df[column].dropna()

    # -------------------------
    # 4. Check usable data
    # -------------------------

    if series.empty:
        return {
            "tool": "detect_anomalies",
            "column": column,
            "method": "IQR",
            "status": "insufficient_data",
            "message": (
                "There is no usable numeric data "
                "for anomaly detection."
            ),
            "anomalies": [],
            "count": 0
        }

    # IQR is not meaningful with very small datasets.
    if len(series) < 4:
        return {
            "tool": "detect_anomalies",
            "column": column,
            "method": "IQR",
            "status": "insufficient_data",
            "message": (
                "There are not enough numeric values "
                "for reliable anomaly detection."
            ),
            "anomalies": [],
            "count": 0
        }

    # -------------------------
    # 5. Calculate quartiles
    # -------------------------

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)

    iqr = q3 - q1

    # -------------------------
    # 6. Handle constant values
    # -------------------------

    if iqr == 0:
        return {
            "tool": "detect_anomalies",
            "column": column,
            "method": "IQR",
            "status": "no_variation",
            "lower_bound": float(q1),
            "upper_bound": float(q3),
            "count": 0,
            "anomalies": []
        }

    # -------------------------
    # 7. Calculate bounds
    # -------------------------

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # -------------------------
    # 8. Detect anomalies
    # -------------------------

    anomaly_mask = (
        (series < lower_bound) |
        (series > upper_bound)
    )

    anomalies = series[anomaly_mask]

    # -------------------------
    # 9. Return results
    # -------------------------

    return {
        "tool": "detect_anomalies",
        "column": column,
        "method": "IQR",
        "status": "completed",
        "lower_bound": float(lower_bound),
        "upper_bound": float(upper_bound),
        "count": int(len(anomalies)),
        "anomalies": [
            {
                "index": int(index),
                "value": float(value)
            }
            for index, value in anomalies.items()
        ]
    }