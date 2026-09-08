from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
	return {"message": "Hello, World from main!"}
# A simple string can also be returned here just as a normal function retuning a string

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
	return {"item_id": item_id, "q": q}