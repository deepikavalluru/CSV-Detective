import os
import json

import pandas as pd
from dotenv import load_dotenv
from google import genai 

from app.services.profiler import profile_dataset
from app.services.trends import analyze_trend
from app.services.comparisons import compare_groups
from app.services.anomalies import detect_anomalies
from app.services.statistics import (
    calculate_correlation,
    get_top_values
)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# Validation helpers
def validate_column(df, column):
    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist in the dataset."
        )

def validate_numeric_column(df, column):

    validate_column(df, column)
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(
            f"Column '{column}' must be numeric"
        )

# Gemini investigation

def ask_gemini(prompt: str, df):
    investigation_steps = []

    tools = [
        {
            "type": "function",
            "name": "profile_dataset",
            "description": (
                "Get an overview of the CSV dataset including row count, column count, numeric columns, date columns, categorical columns, missing values, unique counts, and column types."
            ),
            "parameters": {
                "type": "object",
                "properties": {}
            }
        },

        {
            "type": "function",
            "name": "get_top_values",
            "description": (
                "Find the most frequent values in a column. Useful for understanding the most common categories or values in a dataset"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "column": {
                        "type": "string",
                        "description": "The column to analyze."
                    },
                    "n": {
                        "type": "integer",
                        "description": (
                            "Maximum number of top values to return."
                        )
                    },
                },
                "required": ["column"]
            }
        },

        {
            "type": "function",
            "name": "compare_groups",
            "description": (
                "Compare the total value of a numeric column across different groups in another column."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "value_column": {
                        "type": "string",
                        "description": (
                            "The numeric column whose values should be summed."
                        )
                    },
                    "group_column": {
                        "type": "string",
                        "description": (
                            "The column containing the groups to compare."
                        )
                    }
                },
                "required": [
                    "value_column",
                    "group_column"
                ]
            }
        },

        {
            "type": "function",
            "name": "analyze_trend",
            "description": (
                "Analyze how a numeric value changes over time using a date column"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "value_column": {
                        "type": "string",
                        "description": (
                            "The numeric column to analyze."
                        )
                    },
                    "date_column": {
                        "type": "string",
                        "description": (
                            "The date or time column."
                        )
                    }
                },
                "required": [
                    "value_column",
                    "date_column"
                ]
            }
        },

        {
            "type": "function",
            "name": "detect_anomalies",
            "description": (
                "Detect unusual values in a numeric column using the IQR anomaly detection method."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "column": {
                        "type": "string",
                        "description": (
                            "The numeric column to check for anomalies."
                        )
                    }
                },
                "required": [
                    "column"
                ]
            }
        },
        
        {
            "type": "function",
            "name": "calculate_correlation",
            "description": (
                "Calculate the Pearson correlation between two numeric columns."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "column_a": {
                        "type": "string",
                        "description": (
                            "First numeric column."
                        )
                    },
                    "column_b": {
                        "type": "string",
                        "description": (
                            "Second numeric column."
                        )
                    }
                },
                "required": [
                    "column_a",
                    "column_b"
                ]
            }
        }
    ]

    # System Prompt

    system_prompt = """
        You are a data investigation agent.

        Your job is to investigate an unfamiliar CSV dataset and identify
        important findings using the available analysis tools.

        Investigation process:

        1. Always call profile_dataset first.
        2. Inspect the profile to understand the dataset structure.
        3. If the dataset contains categorical columns and numeric columns,
           use compare_groups to investigate meaningful group differences.
        4. If the dataset contains a date column and numeric columns,
           use analyze_trend to investigate important changes over time.
        5. If the dataset contains two or more numeric columns,
           use calculate_correlation when their relationship may be meaningful.
        6. Use get_top_values when important categorical distributions need
           to be understood.
        7. Use detect_anomalies when a numeric column may contain unusual
           values.
        8. Do not repeatedly call the same tool unless there is a different
           meaningful combination of columns to investigate.
        9. Use only tools that are relevant to the dataset.
        10. Never invent numerical results.
        11. Treat tool results as evidence.
        12. When enough evidence has been gathered, provide concise findings
            supported by the tool results.

        IMPORTANT:
        - Only use column names that actually exist in the dataset.
        - Never invent a column name.
        - Before calling a tool, verify from the profile that the required
          columns exist and have the required data type.
        - Do not call analyze_trend unless there is both a date column and
          at least one numeric column.
        - Do not call calculate_correlation unless there are at least two
          numeric columns.
        - Do not call compare_groups unless there is at least one numeric
          column and one group/category column.
        - Do not call detect_anomalies on a non-numeric column.

        The goal is not to use every tool.
        The goal is to investigate the dataset intelligently and gather
        useful evidence.

        Note:
        Never claim causation from correlation.
        Report associations as associations unless the analysis provides
        evidence of causality.

        Do not invent numerical values.
        Every numerical finding must come from a tool result.
    """


    # Initial Gemini Request
    interaction = client.interactions.create(
        model="gemini-3.1-flash-lite",
        system_instruction=system_prompt,
        input=prompt,
        tools=tools 
    )

    print("STATUS:", interaction.status)
    print("STEPS:", interaction.steps)
    print("OUTPUT:", interaction.output_text)

    # Tool Execution Loop

    MAX_TOOL_CALLS = 8
    tool_call_count = 0

    while True:

        function_calls = [
            step
            for step in interaction.steps
            if step.type == "function_call"
        ]

        # Gemini has finished investigating
        if not function_calls:
            return {
                "answer": interaction.output_text,
                "investigation": investigation_steps
            }

        for step in function_calls:
            tool_call_count += 1

            if tool_call_count > MAX_TOOL_CALLS:
                return {
                    "answer": (
                        "Investigation has stopped because the maximum number of tool calls was reached. "
                    ),
                    "investigation": investigation_steps
                }

            # Get tool arguments safely
            arguments = step.arguments
            
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except json.JSONDecodeError:
                    arguments = {}

            if arguments is None:
                arguments = {}

            # exceute requested tool safely

            try:
                if step.name == "profile_dataset":
                    result = profile_dataset(df)
                elif step.name == "get_top_values":
                    column = arguments.get("column")

                    if not column:
                        raise ValueError(
                            "A column is required."
                        )

                    validate_column(df, column)

                    n = arguments.get("n", 10)

                    if not isinstance(n, int) or n <= 0:
                        raise ValueError(
                            "The value of 'n' must be a positive integer."
                        )

                    result = get_top_values(
                        df,
                        column=column,
                        n=n
                    )
                elif step.name == "compare_groups":

                    value_column = arguments.get("value_column")
                    group_column = arguments.get("group_column")

                    if not value_column:
                        raise ValueError("A value_column is required.")
                    
                    validate_numeric_column(
                        df, 
                        value_column
                    )

                    validate_column(
                        df,
                        group_column
                    )

                    result  = compare_groups(
                        df,
                        value_column=value_column,
                        group_column=group_column
                    )
                
                elif step.name == "analyze_trend":
                    value_column = arguments.get("value_column")
                    group_column = arguments.get("date_column")

                    if not value_column:
                        raise ValueError(
                            "A value_column is required."
                        )

                    if not date_column:
                        raise ValueError(
                            "A date_column is required."
                        )

                    validate_numeric_column(
                        df,
                        value_column
                    )

                    validate_column(
                        df,
                        date_column
                    )

                    result = analyze_trend(
                        df, 
                        value_column=value_column,
                        date_column=date_column
                    )
                
                elif step.name == "detect_anomalies":
                    column = arguments.get("column")

                    if not column:
                        raise ValueError(
                            "A column is required."
                        )

                    validate_numeric_column(
                        df,
                        column
                    )

                    result = detect_anaomalies(
                        df,
                        column=column
                    )

                elif step.name == "calculate_correlation":
                    column_a = arguments.get("column_a")
                    column_b = arguments.get("column_b")

                    if not column_a:
                        raise ValueError(
                            "A column_a is required."
                        )

                    if not column_b:
                        raise ValueError(
                            "A column_b is required."
                        )

                    if column_a == column_b:
                        raise ValueError(
                            "Correlation requires two different columns."
                        )

                    validate_numeric_column(
                        df,
                        column_a
                    )

                    validate_numeric_column(
                        df,
                        column_b
                    )

                    result = calculate_correlation(
                        df,
                        column_a=column_a,
                        column_b=column_b
                    )

                else:
                    raise ValueError(
                        f"Unknown tool requested: {step.name}"
                    )

                tool_status = "completed"

            except ValueError as e:
                # Invalid Gemini arguments should not crash
                # the entire investigation.

                result = {
                    "error": str(e)
                }

                tool_status = "failed"

                print(
                    f"TOOL VALIDATION ERROR: {step.name}: {e}"
                )
            
            except Exception as e:
                # Unexpected tool errors are also returned to Gemini instead of crashing the investigation loop.

                result = {
                    "error": (
                        "This tool could not be executed safely."
                    )
                }

                tool_status = "failed"

                print(f"TOOL ERROR: {step.name}: {repr(e)}")

            # Store investigation step

            investigation_steps.append({
                "tool": step.name,
                "status": tool_status,
                "result": result
            })

            print(
                f"TOOL USED: {step.name}"
                f"({tool_status})"
            )

            # Send tool result back to Gemini

            interaction = client.interactions.create(
                model="gemini-3.1-flash-lite",
                system_instruction=system_prompt,
                previous_interaction_id=interaction.id,
                input=[
                    {
                        "type": "function_result",
                        "name": step.name,
                        "call_id": step.id,
                        "result": [
                            {
                                "type": "text",
                                "text": json.dumps(result)
                            }
                        ]
                    }
                ],
                tools=tools
            )

# --------------------------------------------------
# Local testing
# --------------------------------------------------

if __name__ == "__main__":

    df = pd.DataFrame({
        "sales": [100, 150, 120, 200, 150],
        "profit": [20, 30, 25, 45, 30],
        "region": [
            "South",
            "North",
            "South",
            "East",
            "North"
        ],
        "date": [
            "2026-01-01",
            "2026-01-02",
            "2026-01-03",
            "2026-01-04",
            "2026-01-05"
        ]
    })

    result = ask_gemini(
        "Which region has the highest sales?",
        df
    )

    print(result)