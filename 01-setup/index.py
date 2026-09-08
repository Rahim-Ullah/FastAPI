from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
	return {"message": "Hello, World! from index!"}
# A simple string can also be returned here just as a normal function retuning a string

@app.get("/items/{item_id}")
def read_item(item_id: int):
	return {"item_id": item_id}