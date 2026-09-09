from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/users")
def read_root():
    return {"users": ["Rahim Ullah", "Ali Ullah"]}


@app.get("/users/{name}")
def read_users(name: str): 
    # in the browser URL we are allowed to enter a nuber because the url is a string by default and that number would be returned as a string
    return {"users": [name]}


# 404
@app.get("/{path:path}")
def read_not_found(path: str):
    return {"message": "Error 404"}