from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home_view():
    return {"message": "hello from fastapi"}