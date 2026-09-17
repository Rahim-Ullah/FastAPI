# 10 - Status Codes & Custom Exception Handling

A practical guide to working with HTTP status codes, throwing built-in `HTTPException`, and creating custom domain exceptions with global exception handlers.

---

## 📌 Concepts Covered

1. **Explicit Status Codes**: Using FastAPI's `status` constants (`status.HTTP_201_CREATED`, `status.HTTP_200_OK`) to avoid hardcoded magic numbers.
2. **Setting Route Status Codes**: Specifying default success codes right in the route decorator (`status_code=status.HTTP_201_CREATED`).
3. **Standard `HTTPException`**: Raising quick, built-in errors for simple client error cases (e.g. `400 Bad Request`).
4. **Custom Exception Classes**: Creating domain-specific error classes (`class UserNotFoundException(Exception)`).
5. **Global Exception Handlers (`@app.exception_handler`)**: Catching custom exceptions globally across all routes and returning custom `JSONResponse` objects.
6. **Route Disambiguation**: Using clear path namespaces (`/get_users/by_name/{name}` vs `/get_users/by_id/{id}`) to prevent path collisions.

---

## 🔍 Code Breakdown (`local-path/main.py`)

### 1. Declarative Status Codes
```python
from fastapi import FastAPI, status as status_codes

app = FastAPI()

@app.post("/create_user", status_code=status_codes.HTTP_201_CREATED)
async def create_user():
    return {"message": "User created successfully"}
```
- Returning `201 Created` indicates a new resource was successfully created.

### 2. Custom Exception & Global Handler
```python
from fastapi import Request
from fastapi.responses import JSONResponse

class UserNotFoundException(Exception):
    def __init__(self, user_name: str, detail: str = None):
        self.user_name = user_name
        self.detail = detail

@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=status_codes.HTTP_404_NOT_FOUND,
        content={
            "message": f"User with name {exc.user_name} not found",
            "detail": exc.detail,
            "status_code": status_codes.HTTP_404_NOT_FOUND,
        },
    )
```
- Whenever any route raises `UserNotFoundException`, FastAPI jumps straight to this handler and formats a clean, standardized 404 response.
- Note: Exception handlers **must** return a `Response` instance (like `JSONResponse`), not a raw dictionary.

### 3. Raising Custom vs Built-in Exceptions
```python
from fastapi import HTTPException as http_exception

# Custom Exception
@app.get("/get_users/by_name/{user_name}")
async def get_user_by_name(user_name: str):
    if user_name != "rahim":
        raise UserNotFoundException(user_name, detail="Invalid user name Passed!")
    return {"message": f"User {user_name} retrieved", "status_code": 200}

# Built-in HTTPException
@app.get("/get_users/by_id/{user_id}")
async def get_user_by_id(user_id: int):
    if user_id != 1:
        raise http_exception(status_code=400, detail="Invalid user ID Passed! The ID should be 1")
    return {"message": f"User with ID {user_id} retrieved", "status_code": 200}
```

---

## ⚙️ Request Flow

```
Request: GET /get_users/by_name/john
                 │
                 ▼
      User != "rahim"? ──► raise UserNotFoundException("john")
                                       │
                                       ▼
                     @app.exception_handler(UserNotFoundException)
                                       │
                                       ▼
                     JSONResponse (HTTP 404)
                     {
                       "message": "User with name john not found",
                       "detail": "Invalid user name Passed!",
                       "status_code": 404
                     }
```

---

## 🚀 How to Run & Test

1. **Start the server**:
   ```bash
   uvicorn main:app --reload
   ```

2. **Test endpoints**:
   - Create user (201):
     ```bash
     curl -X POST http://127.0.0.1:8000/create_user
     ```
   - Success by name (200):
     ```bash
     curl http://127.0.0.1:8000/get_users/by_name/rahim
     ```
   - Custom 404 error:
     ```bash
     curl http://127.0.0.1:8000/get_users/by_name/unknown
     ```
   - Built-in 400 error:
     ```bash
     curl http://127.0.0.1:8000/get_users/by_id/99
     ```
