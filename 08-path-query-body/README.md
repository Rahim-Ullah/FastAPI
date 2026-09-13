# 08 - Path Parameters, Query Parameters, and Request Body in FastAPI

This guide breaks down how FastAPI handles **Path Parameters**, **Query Parameters**, and **Request Bodies** simultaneously in a single application, using your exact code structure.

---

## 📌 Table of Contents
1. [Core Concepts: How FastAPI Tells Them Apart](#core-concepts-how-fastapi-tells-them-apart)
2. [Why Swagger Worked But Postman Failed (The Mystery Explained)](#why-swagger-worked-but-postman-failed)
3. [Analysis of Your `main.py` (Bugs & Edge Cases)](#analysis-of-your-mainpy-bugs--edge-cases)
4. [Endpoint by Endpoint Breakdown](#endpoint-by-endpoint-breakdown)
5. [How This Actually Works in Industry](#how-this-actually-works-in-industry)
6. [Testing Guide (Postman & Swagger)](#testing-guide-postman--swagger)

---

## 1. Core Concepts: How FastAPI Tells Them Apart

When an HTTP request arrives, data can live in three different places:
- **Path**: Inside the URL itself (e.g. `/users/0`)
- **Query**: In the query string after `?` (e.g. `/users/0?notify=true`)
- **Body**: In the raw HTTP JSON payload

FastAPI follows a strict, predictable rule to determine what is what:

| Parameter Declaration in Python | Where FastAPI Extracts It From |
| :--- | :--- |
| Any parameter declared in the route path (e.g. `@app.put("/users/{user_id}")` with `user_id: int`) | **Path Parameter** |
| Any parameter with a primitive type (`bool`, `str`, `int`) **not** declared in the path (e.g. `notify: bool = False`) | **Query Parameter** |
| Any parameter declared with a Pydantic model type (e.g. `user: User`) | **Request Body (JSON)** |

You don't need manual parsing logic—FastAPI inspects your function signature and route string, matching each parameter to its correct HTTP layer.

---

## 2. Why Swagger Worked But Postman Failed

### In Swagger UI (`/docs`)
Swagger automatically inspects your FastAPI schema:
- It creates a dedicated input box for `user_id` (Path).
- It creates a dedicated input box / dropdown for `notify` (Query).
- It creates a JSON editor for `user` (Body) with pre-filled fields `{"name": "string", "age": 0}`.
- When you press **Execute**, Swagger constructs the exact HTTP request correctly behind the scenes.

### In Postman (What Went Wrong)
In Postman, you are in full manual control of the HTTP request. Here is why the error occurred:
1. **Object Wrapping vs Root Payload**:
   When developers write `def update_user(user_id: int, user: User)`:
   - They often think the JSON in Postman must wrap the object like:
     ```json
     // ❌ WRONG in Postman:
     {
       "user": {
         "name": "Rahim",
         "age": 25
       }
     }
     ```
   - Because `user: User` is the only Pydantic body model, FastAPI expects the payload at the **root** of the JSON:
     ```json
     // ✅ CORRECT in Postman:
     {
       "name": "Rahim",
       "age": 25
     }
     ```
2. **Postman Variable Syntax `{{}}`**:
   Using `{{}}` in Postman is reserved for environment variables (e.g. `{{base_url}}`). If entered directly into the JSON body, Postman either sends an unescaped string or invalid JSON, triggering a `422 Unprocessable Entity` or `400 Bad Request`.
3. **Putting Path / Query Params in the Body**:
   If `user_id` or `notify` are placed inside the JSON body instead of the URL (`http://127.0.0.1:8000/users/0?notify=true`), FastAPI will not see them, causing errors.

---

## 3. Analysis of Your `main.py` (Bugs & Edge Cases)

Here is the exact analysis of your current code:

### ⚠️ Bug 1: Function Name Shadowing (Line 31 & Line 40)
```python
@app.put("/users/update-by-name")
def update_user(user: User, notify: bool = False):
    ...

@app.put("/users/{user_id}")
def update_user(user_id: int, user: User, notify: bool = False):
    ...
```
- **What is wrong**: Both functions have the exact same name: `update_user`.
- **The problem**: In Python, when you define two functions with the same name in the same module scope, the second definition overwrites the first one in the module dictionary. While FastAPI's decorator registers the endpoint, having duplicate function names can cause duplicate OpenAPI `operation_id` generation issues, makes unit testing difficult, and violates Python clean code practices.
- **Fix**: Rename one to `update_user_by_name` and the other to `update_user_by_id`.

---

### 🐛 Bug 2: Python Negative Indexing Flaw (Line 43)
```python
if user_id < len(users):
    users[user_id] = user
    return {"message": "User updated", "user": user, "notify": notify}
```
- **What is wrong**: If a client sends `PUT /users/-1`, Python evaluates `-1 < len(users)` as `True`!
- **The problem**: In Python, `users[-1]` targets the **last item** in the list. So passing `-1` will quietly overwrite your last user without an error, instead of telling the client that `-1` is an invalid ID!
- **Fix**: Check `if 0 <= user_id < len(users):`.

---

### ℹ️ Bug 3: Returning `200 OK` for "User Not Found" (Line 36 & 46)
```python
return {"message": "User not found"}
```
- **What is wrong**: This returns an HTTP status code of `200 OK`.
- **The problem**: REST clients, frontends (React, Angular, mobile apps), and API gateways check the HTTP status code. If your API returns `200 OK`, frontend libraries like Axios or `fetch` consider the call a success.
- **Fix**: Use FastAPI's `HTTPException`:
  ```python
  from fastapi import HTTPException, status
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
  ```

---

### ℹ️ Bug 4: Indentation Inconsistency (Lines 44-45)
```python
if user_id < len(users):
        users[user_id] = user
        return {"message": "User updated", "user": user, "notify": notify}
```
- **What is wrong**: Lines 44 and 45 are indented by 8 spaces (2 indent levels) inside the `if` statement rather than the standard 4 spaces. While valid in Python, linters will flag this.

---

## 4. Endpoint by Endpoint Breakdown

### 1. `POST /users` (Request Body Only)
```python
@app.post("/users")
def create_user(user: User):
    users.append(user)
    return {"message": "User created", "user": user}
```
- **Inputs**: Request Body (`user: User`).
- **How it works**: Client sends `{ "name": "Alice", "age": 22 }`. Pydantic validates the structure, and it gets appended to the `users` list.

---

### 2. `GET /users` (No Parameters)
```python
@app.get("/users")
def read_users():
    return users
```
- **Inputs**: None.
- **How it works**: Returns the raw list of all currently stored users.

---

### 3. `PUT /users/update-by-name` (Body + Query Parameter)
```python
@app.put("/users/update-by-name")
def update_user(user: User, notify: bool = False):
    for i, u in enumerate(users):
        if u.name == user.name:
            users[i] = user
            return {"message": "User updated", "user": user, "notify": notify}
    return {"message": "User not found"}
```
- **Inputs**:
  - `user: User`: Received via Request Body.
  - `notify: bool = False`: Received via Query Parameter (`?notify=true`).
- **How it works**: Searches the list for an existing user whose name matches `user.name`, and replaces it.

---

### 4. `PUT /users/{user_id}` (Path + Body + Query Parameter)
```python
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User, notify: bool = False):
    if user_id < len(users):
        users[user_id] = user
        return {"message": "User updated", "user": user, "notify": notify}
    return {"message": "User not found"}
```
- **Inputs**:
  - `user_id: int`: Received via Path (`/users/0`).
  - `user: User`: Received via Request Body JSON (`{"name": "...", "age": ...}`).
  - `notify: bool = False`: Received via Query (`?notify=true`).
- **How it works**: The complete trifecta! FastAPI parses all three inputs from their respective places in one clean function.

---

## 5. How This Actually Works in Industry

In real-world production backends:

1. **Database vs In-Memory List**:
   - In-memory lists (`users = []`) reset every time the server restarts.
   - Using list index as an ID (`users[0]`) is dangerous: if user 0 is deleted, all subsequent indices shift.
   - Industry uses real databases (PostgreSQL, MySQL) with an ORM (SQLAlchemy, SQLModel) where each user has a fixed primary key (`id: int` or `id: uuid4`).

2. **PUT vs PATCH**:
   - **`PUT`**: Intended to **replace** the entire resource.
   - **`PATCH`**: Intended for **partial updates** (e.g. only updating `age` without sending `name`).

3. **Query Parameters in Production**:
   Query parameters are standard for:
   - Pagination: `?page=1&limit=20`
   - Filtering: `?role=admin&active=true`
   - Sorting: `?sort=desc`

---

## 6. Testing Guide (Postman & Swagger)

### Testing `PUT /users/{user_id}` in Postman

1. **Set HTTP Method**: Select `PUT`.
2. **URL**: Enter `http://127.0.0.1:8000/users/0`
3. **Query Parameter**:
   - Click the **Params** tab.
   - Key: `notify` | Value: `true`
   - Postman will automatically update the URL to:
     `http://127.0.0.1:8000/users/0?notify=true`
4. **Body**:
   - Click the **Body** tab.
   - Select **raw** radio button.
   - Select **JSON** from the format dropdown.
   - Enter:
     ```json
     {
       "name": "Rahim",
       "age": 25
     }
     ```
5. **Send**: You will receive:
   ```json
   {
     "message": "User updated",
     "user": {
       "name": "Rahim",
       "age": 25
     },
     "notify": true
   }
   ```
