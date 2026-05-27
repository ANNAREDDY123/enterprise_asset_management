from fastapi import FastAPI

app = FastAPI(title="Enterprise Asset Management System")

@app.get("/")
def home():
    return {"message": "Enterprise Asset Management API is running"}

@app.get("/health")
def health_check():
    return {"status": "OK"}
