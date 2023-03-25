from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"status": 200,
            "detail": "Success",
            "data": None}


@app.get("/about")
def about():
    return {"status": 200,
            "detail": "Success",
            "data": "This is about section"}
