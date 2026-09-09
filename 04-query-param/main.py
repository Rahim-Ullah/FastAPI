from fastapi import FastAPI
from typing import Optional

app = FastAPI()


@app.get("/")
def read_items():
    return {"Hello": "World"}



@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# trying optional kw
@app.get("/items")
def read_item(item_id: Optional[int] = None): # this would be considered as optional but if provided then it should go as an int
    return {"item_id": item_id}



# 404 NOT FOUND
@app.get("{path:path}")
def path_not_found(path: str):
    return {"path": f"{path} was not found"}