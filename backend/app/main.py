from fastapi import FastAPI 
from app.routes.upload import router as upload_router
from app.routes.investigate import router as investigate_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://csv-detective.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/api")
app.include_router(
    investigate_router,
    prefix="/api"
)

@app.get("/")

def root():
    return {"message": "CSV Detective API is running"}