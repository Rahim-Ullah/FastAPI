from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"} # during test this same statement is being tested in test_main.py as a response.json() call


@app.get("/add")
def add_numbers(a: int, b: int):
    return {"result": a + b}