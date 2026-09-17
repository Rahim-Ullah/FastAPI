# 02 - First App & Route Basics

A practical look at building multiple static endpoints, working with synchronous vs asynchronous handlers, and custom app instance naming in FastAPI.

---

## 📌 Concepts Covered

1. **Custom App Variable Names**: Naming the FastAPI instance `ourApp` instead of `app`, and how that changes your Uvicorn startup command (`uvicorn main:ourApp --reload`).
2. **Multiple Route Endpoints**: Registering separate endpoints (`/`, `/about`, `/members`) on a single app.
3. **`def` vs `async def`**:
   - `def read_root()`: Standard synchronous function executed in an external threadpool by FastAPI.
   - `async def about_page()`: Asynchronous coroutine executed directly on the main event loop (ideal for non-blocking I/O operations).
4. **Complex Data Serialization**: Automatically serializing Python lists and nested dictionaries into JSON.

---

## 🔍 Code Breakdown (`local-path/main.py`)

```python
from fastapi import FastAPI

ourApp = FastAPI()

@ourApp.get("/")
def read_root():
    return {"message": "Welcome to our first FasAPI app!"}

@ourApp.get("/about")
async def about_page():
    return {"message": "This is the about page"}

@ourApp.get("/members")
def read_members():
    return {
        "message": "This is the members page",
        "Members": ["Rahim Ullah", "Ahmed", "Mohammed"]
    }
```

### Key Takeaways:
- **`ourApp` instance:** You can name the FastAPI instance anything. Just remember to tell Uvicorn: `<filename>:<variable_name>`.
- **Async vs Sync flexibility:** FastAPI lets you mix `async def` and normal `def` routes in the same file based on whether you're doing asynchronous I/O or CPU-bound tasks.

---

## 🚀 How to Run & Test

1. **Start the server**:
   ```bash
   uvicorn main:ourApp --reload
   ```

2. **Endpoints to test**:
   - Root: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - About: [http://127.0.0.1:8000/about](http://127.0.0.1:8000/about)
   - Members: [http://127.0.0.1:8000/members](http://127.0.0.1:8000/members)
   - Swagger Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
