# 01 - FastAPI Setup & First Steps

A quick-start guide to initializing and running your very first FastAPI project.

---

## 📌 Concepts Covered

1. **FastAPI Instance**: Creating the core application object (`app = FastAPI()`).
2. **Path Operations**: Using decorators like `@app.get("/")` to bind HTTP GET requests to Python functions.
3. **Automatic Serialization**: Returning Python dictionaries directly as JSON responses.
4. **Path Parameters & Type Hinting**: Declaring `{item_id}` in the path and typing it as `int` in the function (`item_id: int`).
5. **Optional Query Parameters**: Adding non-path parameters with default values (`q: str = None`).
6. **Naming Conventions**: Why files are conventionally named `main.py` and application instances named `app` (explained in [why.md](why.md)).

---

## 🔍 Code Breakdown (`local-path/main.py`)

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World from main!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

### How it works:
- **`@app.get("/")`**: Listens for HTTP GET requests at the root URL. Returns a clean JSON greeting.
- **`@app.get("/items/{item_id}")`**:
  - `item_id: int`: FastAPI automatically parses and validates that `item_id` is an integer. Passing letters (e.g. `/items/foo`) triggers an automatic `422 Unprocessable Entity` validation error.
  - `q: str = None`: Because `q` is not in the path, FastAPI treats it as an optional query parameter (`/items/5?q=python`).

---

## 🚀 How to Run & Test

1. **Install requirements** (in your virtual environment):
   ```bash
   pip install fastapi uvicorn
   ```

2. **Start the development server**:
   ```bash
   uvicorn main:app --reload
   ```
   *(If running `index.py`, use `uvicorn index:app --reload`)*

3. **Endpoints to test**:
   - Root: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Path + Query: [http://127.0.0.1:8000/items/42?q=fastapi](http://127.0.0.1:8000/items/42?q=fastapi)
   - Interactive Docs (Swagger): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
