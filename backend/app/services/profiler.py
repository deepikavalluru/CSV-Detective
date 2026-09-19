import pandas as pd

def profile_dataset(df):
    profile = {}

    # 1. Basic datset size
    profile["rows"] = len(df)
    profile["column"] = len(df.columns)

    # 2. Detect completely empty columns
    empty_columns = [
        column
        for column in df.columns
        if df[column].isna().all()
    ]

    profile["empty_columns"] = empty_columns

    # Only analyze columns that contain at least some actual data.
    usable_columns = [
        column
        for column in df.columns
        if column not in empty_columns
    ]

    usable_df = df[usable_columns]

    # 3. Numeric columns
    profile["numeric_columns"] = (
        usable_df
        .select_dtypes(include="number")
        .columns
        .tolist()
    )

    # 4. Date columns
    profile["date_columns"] = (
        usable_df
        .select_dtypes(include="datetime")
        .columns.tolist()
    )

    # 5. Object/String columns are candidates
    categorical_candidates = (
        usable_df
        .select_dtypes(include=["object", "string"])
        .columns
        .tolist()
    )

    # Column names that commonly indicate dates 
    date_keywords = [
        "date",
        "time",
        "timestamp",
        "created",
        "updated"
    ]

    for column in categorical_candidates:
        column_lower = column.lower()

        # Only try date parsing when the column name
        # suggests that it might contain dates
        if any(
            keyword in column_lower
            for keyword in date_keywords
        ):
            parsed = pd.to_datetime(
                usable_df[column],
                errors="coerce"
            )

            valid_ratio = parsed.notna().mean()

            if valid_ratio >= 0.8:
                profile["date_columns"].append(column)

    # 5. Categorical columns
    profile["categorical_columns"] = [
        column
        for column in categorical_candidates
        if column not in profile["date_columns"]
    ]

    # 6. Missing values
    profile["missing_values"] = (
        df.isna()
        .sum()
        .to_dict()
    )

    # 7. Unique values
    profile["unique_counts"] = (
        df.nunique()
        .to_dict
    )

    # 8. Column -> type mapping
    column_types = {}

    for column in df.columns:

        if column in profile["empty_columns"]:
            column_types[column] = "empty"
        elif column in profile["numeric_columns"]:
            column_types[column] = "numeric"
        elif column in profile["date_columns"]:
            column_types[column] = "date"
        elif column in profile["categorical_columns"]:
            column_types[column] = "categorical"

        else:
            column_types[column] = "unknown"

    profile["column_types"] = column_types

    # 9. Return profile
    return {
        "tool": "profile_dataset",
        "results": profile
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
            "2026-01-03",
            "2026-01-04",
            "2026-01-05",
            "2026-01-06",
            "2026-01-07",
            "2026-01-08"
        ]
    })

    profile = profile_dataset(df)

    print(profile)