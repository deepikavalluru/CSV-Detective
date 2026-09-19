from fastapi import FastAPI 
from app.routes.upload import router as upload_router

app = FastAPI()

app.include_router(upload_router, prefix="/api")

@app.get("/")
def root():
    return {
        "message": "CSV Detective API is running"
    }