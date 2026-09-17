# 04 - Query Parameters in FastAPI

A concise guide to declaring, validating, and handling optional and multiple query parameters in FastAPI.

---

## 📌 Concepts Covered

1. **Query Parameter Detection**: Any function argument not declared in the URL path is automatically treated by FastAPI as a **Query Parameter** (e.g. `?key=value`).
2. **Path + Query Combination**: Combining path parameters and query parameters in one route (`/items/{item_id}?q=python`).
3. **Optional Parameters**: Using `Optional[type] = None` or default values (`limit: Optional[int] = 20`) to make query parameters non-mandatory.
4. **Multiple Query Parameters**: Handling multiple parameters simultaneously with automatic type casting (e.g. `?name=Phone&price=500&limit=10`).
5. **Type Safety & Validation**: If a query parameter is typed as `int`, passing text (e.g. `?limit=abc`) triggers an immediate `422 Unprocessable Entity` response.

---

## 🔍 Code Breakdown (`local-path/main.py`)

### 1. Combining Path and Query Parameters
```python
@app.get("/items/{item_id}")
def read_item_with_query(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```
- `item_id`: Extracted from the URL path.
- `q`: Extracted from the query string (e.g. `/items/5?q=electronics`).

### 2. Handling Multiple Optional Query Parameters
```python
from typing import Optional

@app.get("/items")
def search_items(
    name: Optional[str] = None,
    price: Optional[int] = 0,
    limit: Optional[int] = 20
):
    return {"name": name, "price": price, "limit": limit}
```
- Calling `/items` uses defaults: `name=None, price=0, limit=20`.
- Calling `/items?name=Laptop&price=1200&limit=5` overrides them.

---

## 🚀 How to Run & Test

1. **Start the server**:
   ```bash
   uvicorn main:app --reload
   ```

2. **Endpoints to test**:
   - Path + Query: [http://127.0.0.1:8000/items/10?q=books](http://127.0.0.1:8000/items/10?q=books)
   - Query Defaults: [http://127.0.0.1:8000/items](http://127.0.0.1:8000/items)
   - Multiple Queries: [http://127.0.0.1:8000/items?name=keyboard&price=45&limit=10](http://127.0.0.1:8000/items?name=keyboard&price=45&limit=10)
   - Swagger Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
