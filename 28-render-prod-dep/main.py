# basic api just to test in production (render)
from fastapi import FastAPI


app = FastAPI()

@app.get("/home")
def home():
    return {
        "Welcome :": "To testing in production tutorial!"
    }


