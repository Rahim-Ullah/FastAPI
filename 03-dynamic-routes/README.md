# 03 - Dynamic Routes & Catch-All Patterns

Learn how FastAPI handles dynamic URL parameters, type evaluation, and fallback catch-all routes.

---

## 📌 Concepts Covered

1. **Dynamic Path Parameters**: Passing variables directly in the URL (`/users/{name}`) and binding them with type hints (`name: str`).
2. **Type Coercion & Strings**:
   - Because URLs are inherently strings, accessing `/users/123` with `name: str` succeeds (treats `"123"` as text).
   - If typed as `name: int`, passing letters triggers FastAPI's automatic validation rejection (see [General_dt.md](General_dt.md) for a deep dive).
3. **Catch-All Wildcard Routes (`{path:path}`)**: Using Starlette's `:path` converter to capture any arbitrary sub-paths as a fallback handler.
4. **Route Precedence & Evaluation Order**:
   - Specific paths (`/users`) must be declared **before** dynamic paths (`/users/{name}`).
   - Catch-all routes (`/{path:path}`) must always be placed **at the very bottom** of your file.

---

## 🔍 Code Breakdown (`local-path/main.py`)

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

# Static route
@app.get("/users")
def get_all_users():
    return {"users": ["Rahim Ullah", "Ali Ullah"]}

# Dynamic route
@app.get("/users/{name}")
def read_user(name: str):
    return {"users": [name]}

# Fallback catch-all route (404 handler)
@app.get("/{path:path}")
def read_not_found(path: str):
    return {"message": "Error 404", "invalid_path": path}
```

> ⚠️ **Note on duplicate function names:** Ensure route handler functions have unique names (e.g. `get_all_users` vs `read_user`) to avoid function shadowing in Python.

---

## 🚀 How to Run & Test

1. **Start the server**:
   ```bash
   uvicorn main:app --reload
   ```

2. **Endpoints to test**:
   - Static list: [http://127.0.0.1:8000/users](http://127.0.0.1:8000/users)
   - Dynamic user: [http://127.0.0.1:8000/users/rahim](http://127.0.0.1:8000/users/rahim)
   - Dynamic with numbers: [http://127.0.0.1:8000/users/42](http://127.0.0.1:8000/users/42)
   - Catch-all 404: [http://127.0.0.1:8000/random/nested/route](http://127.0.0.1:8000/random/nested/route)
