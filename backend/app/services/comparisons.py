import pandas as pd

def compare_groups(
    df: DataFrame,
    value_column: str, 
    group_column: str,
):
    # 1. Validate columns
    if value_column not in df.columns:
        raise ValueError(
            f"Column '{value_column}' does not exist"
        )

    if group_column not in df.columns:
        raise ValueError(
            f"Column '{group_column}' does not exist"
        )

    # 2. Validate numeric column
    if not pd.api.types.is_numeric_dtype(
        df[value_column]
    ):
        raise ValueError(
            f"Column '{value_column}' must be numeric"
        )

    # 3. Keep usable rows
    data = df[
        [group_column, value_column]
    ].dropna()

    # 4. Check usable data
    if data.empty:
        return {
            "tool": "compare_groups",
            "column": value_column,
            "group_by": group_column,
            "status": "insufficient_data",
            "message": (
                "There is not enough usable data to compare groups."
            ),
            "results": []
        }

    # 5. Group and aggregate
    result = (
        data.groupby(group_column)[value_column]
        .sum()
        .sort_values(ascending=False)
    )

    # 6. Check whether groups exist
    if result.empty:
        return {
            "tool": "compare_groups",
            "column": value_column,
            "group_by": group_column,
            "status": "insufficient_data",
            "message": (
                "No valid groups were found for comparison."
            ),
            "results": []
        }

    # 7. Return results
    return {
            "tool": "compare_groups",
            "column": value_column,
            "group_by": group_column,
            "status": "completed",
            "results": [
                {
                    "group": str(group),
                    "value": float(value)
                }
                for group, value in result.items()
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

    result = compare_groups(df, "sales", "date")

    print(result)