from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "SOC AI Assistant API is running"}