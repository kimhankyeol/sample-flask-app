from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "TEST FAST API! change 2025 06 19 17 51"}