import pandas as pd

# Calculate correlation

def calculate_correlation(
    df: pd.DataFrame,
    column_a: str, 
    column_b: str,
):
    # 1. Validate columns
    if column_a not in df.columns:
        raise ValueError(
            f"Column '{column_a}' does not exist"
        )
    
    if column_b not in df.columns:
        raise ValueError(
            f"Column '{column_b}' does not exist"
        )

    # 2. Prevent same-column correlation
    if column_a == column_b:
        raise ValueError(
            "Correlation requires two different columns"
        )

    # 3. Validate numeric types
    if not pd.api.types.is_numeric_dtype(
        df[column_a]
    ):
        raise ValueError(
            f"Column '{column_a}' must be numeric"
        )

    if not pd.api.types.is_numeric_dtype(
        df[column_b]
    ):
        raise ValueError(
            f"Column '{column_b}' must be numeric"
        )

    # 4. Keep usable pairs
    data = (
        df[[column_a, column_b]].dropna()
    )

    # 5. Check sufficient data
    if len(data) < 2:
        return {
            "tool": "calculate_correlation",
            "column_a": column_a,
            "column_b": column_b,
            "status": "insufficient_data",
            "message": (
                "There are not enough valid data points to calculate correlation."
            ),
            "correlation": None,
            "points": []
        }

    # 6. Check variation
    if data[column_a].nunique() < 2:
        return {
            "tool": "calculate_correlation",
            "column_a": column_a,
            "column_b": column_b,
            "status": "no_variation",
            "message": (
                f"Column '{column_a}' has no variation, so correlation cannot be calculated."
            ),
            "correlation": None,
            "points": [
                {
                    column_a: float(row[column_a]),
                    column_b: float(row[column_b])
                }
                for _, row in data.iterrows()
            ]
        }

    if data[column_b].nunique() < 2:
        return {
            "tool": "calculate_correlation",
            "column_a": column_a,
            "column_b": column_b,
            "status": "no_variation",
            "message": (
                f"Column '{column_b}' has no variation, so correlation cannot be calculated."
            ),
            "correlation": None,
            "points": [
                {
                    column_a: float(row[column_a]),
                    column_b: float(row[column_b])
                }
                for _, row in data.iterrows()
            ]
        }

    # 7. Calculate correlation
    correlation = data[column_a].corr(data[column_b])

    # 8. Return results
    return {
        "tool": "calculate_correlation",
        "column_a": column_a,
        "column_b": column_b,
        "status": "completed",
        "correlation": (
            None
            if pd.isna(correlation)
            else float(correlation)
        ),
        "points": [
            {
                column_a: float(row[column_a]),
                column_b: float(row[column_b])
            }
            for _, row in data.iterrows()
        ]
    }

# Get Top Values

def get_top_values(
    df: pd.DataFrame,
    column: str,
    n: int = 10
):
    # 1. Validate column
    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist"
        )

    # 2. Validate limit
    if not isinstance(n, int) or n <= 0:
        raise ValueError(
            "The value of 'n' must be a positive integer."
        )

    # 3. Remove missing values
    series = df[column].dropna()

    # 4. Check usable data
    if series.empty:
        return {
            "tool": "get_top_values",
            "column": column,
            "limit": n,
            "status": "insufficient_data",
            "message": (
                f"Column '{column}' contains no usable values."
            ),
            "results": []
        }

    # 5. Calculate top values
    values = (
        series
        .value_counts()
        .head(n)
    )

    # 6. Return results
    return {
        "tool": "get_top_values",
        "column": column,
        "limit": n,
        "status": "completed",
        "results": [
            {
                "value": str(value),
                "count": int(count)
            }
            for value, count in values.items()
        ]
    } 

   # Test

if __name__ == "__main__":

    df = pd.DataFrame({
        "sales": [
            100, 150, 120, 200, 150, 180, 90, 250
        ],
        "profit": [
            20, 30, None, 45, 30, 35, 15, None
        ],
        "region": [
            "South", "North", "South", "East", "North", "West", "South", "East"
        ],
        "product": [
            "Laptop", "Mouse", "Laptop", "Keyboard", "Mouse", "Laptop", "Keyboard", "Laptop"
        ],
        "date": [
            "2026-01-01",
            "2026-01-02",
            "2026-01-02",
            "2026-01-04",
            "2026-01-05",
            "2026-01-05",
            "2026-01-07",
            "2026-01-08"
        ]
    })

    results = get_top_values(df, "product", 3)

    print(results)

