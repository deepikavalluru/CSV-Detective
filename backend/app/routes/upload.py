from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
import os
import uuid

router = APIRouter()

UPLOAD_DIR = "temp_uploads"
MAX_FILE_SIZE = 10*1024*1024
MIN_ROWS = 2

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):

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

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 10 MB"
        )

    if len(contents) == 0:
        raise HTTPException(
            status_code=400,
            detail="Dataset is empty"
        )

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    temp_filename = f"{uuid.uuid4()}.csv"
    temp_path = os.path.join(UPLOAD_DIR, temp_filename)

    with open(temp_path, "wb") as buffer:
        buffer.write(contents)

    try:
        df = pd.read_csv(temp_path)
    except Exception as e:
        print("CSV READ ERROR :", e)
        os.remove(temp_path)

        raise HTTPException(
            status_code=400,
            detail=f"Could not read the CSV file: {e}"
        )

    if len(df.columns) == 0:
        os.remove(temp_path)

        raise HTTPException(
            status_code=400,
            detail="CSV contains no columns"
        )

    if len(df) < MIN_ROWS:
        os.remove(temp_path)

        raise HTTPException(
            status_code=400,
            detail="Dataset is empty"
        )

    return {
        "success": True,
        "message": "CSV uploaded successfully",
        "filename": file.filename,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "temp_path": temp_path
    }