import io

import pandas as pd
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.profiler import profile_dataset
from app.agent.gemini_client import ask_gemini
from app.services.charts import build_charts

router = APIRouter()


@router.post("/investigate")
async def investigate(file: UploadFile = File(...)):

    # 1. Validate file
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file provided"
        )

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a CSV file"
        )

    # 2. Read CSV
    try:
        contents = await file.read()

        if len(contents) == 0:
            raise HTTPException(
                status_code=400,
                detail="Dataset is empty"
            )

        df = pd.read_csv(io.BytesIO(contents))

    except HTTPException:
        raise

    except Exception as e:
        print("CSV READ ERROR:", repr(e))

        raise HTTPException(
            status_code=400,
            detail="Could not read the CSV file"
        )

    # 3. Validate dataset
    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="Dataset is empty"
        )

    if len(df.columns) == 0:
        raise HTTPException(
            status_code=400,
            detail="CSV contains no columns"
        )

    # 4. Profile dataset
    try:
        profile = profile_dataset(df)

    except Exception as e:
        print("PROFILE ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail="Failed to profile the dataset"
        )

    # 5. AI investigation
    try:
        result = ask_gemini(
            "Investigate this dataset and identify important findings.",
            df
        )

    except Exception as e:
        print("GEMINI ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail="Investigation temporarily failed. Please try again."
        )

    # 6. Validate Gemini result
    if not isinstance(result, dict):
        raise HTTPException(
            status_code=500,
            detail="Investigation temporarily failed. Please try again."
        )

    if "answer" not in result or "investigation" not in result:
        raise HTTPException(
            status_code=500,
            detail="Investigation temporarily failed. Please try again."
        )

    # 7. Build charts
    try:
        charts = build_charts(result["investigation"])

    except Exception as e:
        print("CHART ERROR:", repr(e))

        # Investigation itself succeeded, so don't throw away
        # the useful AI result just because charts failed.
        charts = []

    # 8. Return result
    return {
        "profile": profile,
        "findings": result["answer"],
        "investigation": result["investigation"],
        "charts": charts
    }