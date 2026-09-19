from fastapi import FastAPI 

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "CSV Detective API is running"
    }