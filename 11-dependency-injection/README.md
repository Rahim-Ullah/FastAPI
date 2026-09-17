# 11 - Dependency Injection & Reusable Logic

A clean, practical guide to FastAPI's Dependency Injection system (`Depends`), header extraction, and sharing logic across endpoints.

---

## 📌 Concepts Covered

1. **What is Dependency Injection?**: A pattern where endpoints declare what dependencies (data, auth, database sessions) they need, and FastAPI automatically executes and injects them.
2. **`Depends()`**: FastAPI's mechanism for executing callable dependencies before running route functions.
3. **DRY Code**: Reusing logic (like `get_current_user`) across multiple routes without duplicating code.
4. **Header Validation**: Reading and enforcing required HTTP headers (`Header(...)`) inside a dependency.
5. **Security Gatekeeping**: Halting requests early with `HTTPException` inside a dependency so invalid requests never reach the endpoint handler.

---

## 🔍 Code Breakdown (`local-path/main.py`)

### 1. Basic Reusable Dependencies
```python
from fastapi import FastAPI, Depends, HTTPException, Header

app = FastAPI()

def common_logic():
    return {"message": "Common logic executed"}

def get_current_user():
    return {"user": "Rahim", "email": "rahimullah@gmail.com"}
```

### 2. Header Verification Dependency
```python
def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return x_token
```
- `Header(...)`: Extracts the `X-Token` request header (automatically converts snake_case to kebab-case).
- If the token doesn't match, `HTTPException(400)` is raised immediately. The endpoint function never runs.

### 3. Injecting Dependencies into Endpoints
```python
# Shared logic injection
@app.get("/home")
async def root(data = Depends(common_logic)):
    return data

# Reusing the user dependency across routes
@app.get("/dashboard")
async def dashboard(data = Depends(get_current_user)):
    return data

@app.get("/dashboard/user")
async def dashboard_user(data = Depends(get_current_user)):
    return data

# Securing a route with a dependency
@app.get("/dashboard/auth")
async def dashboard_auth(x_token = Depends(verify_token)):
    return {"message": "Authenticated", "token": x_token}
```

---

## ⚙️ How Dependency Injection Works

```
Incoming Request: GET /dashboard/auth (Header: X-Token: "fake-super-secret-token")
                                │
                                ▼
                   FastAPI resolves Depends(verify_token)
                                │
                                ▼
                       verify_token() runs
                                │
               ┌────────────────┴────────────────┐
          Token matches                     Token invalid
               │                                 │
               ▼                                 ▼
      dashboard_auth() runs             HTTPException(400) raised
      HTTP 200: Authenticated           Endpoint never executes!
```

---

## 🚀 How to Run & Test

1. **Start the server**:
   ```bash
   uvicorn main:app --reload
   ```

2. **Test public endpoints**:
   ```bash
   curl http://127.0.0.1:8000/home
   curl http://127.0.0.1:8000/dashboard
   ```

3. **Test auth endpoint without header (Fails 422 - Missing Header)**:
   ```bash
   curl http://127.0.0.1:8000/dashboard/auth
   ```

4. **Test auth endpoint with wrong token (Fails 400 - Invalid Header)**:
   ```bash
   curl -H "x-token: wrong-secret" http://127.0.0.1:8000/dashboard/auth
   ```

5. **Test auth endpoint with valid token (Succeeds 200)**:
   ```bash
   curl -H "x-token: fake-super-secret-token" http://127.0.0.1:8000/dashboard/auth
   ```

6. **Interactive Swagger Docs**:
   - Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - FastAPI automatically generates a dedicated input box for `x-token` in `/dashboard/auth`!
