# FastAPI & Pydantic: Request Bodies and Data Validation

Welcome to the **05-pydantic** module! This project demonstrates how data validation, request bodies, and data schemas work in FastAPI using **Pydantic**.

---

## 📌 Table of Contents
1. [Overview & Why Pydantic?](#-overview--why-pydantic)
2. [The 3 Approaches to Receiving POST Data](#-the-3-approaches-to-receiving-post-data)
   - [Method 1: Direct Parameters (Query Parameters in POST)](#1-method-1-direct-parameters-query-parameters-in-post)
   - [Method 2: Generic Dictionary (`user: dict`)](#2-method-2-generic-dictionary-user-dict)
   - [Method 3: Pydantic Model (`User(BaseModel)`)](#3-method-3-pydantic-model-userbasemodel)
3. [Summary Comparison Table](#-summary-comparison-table)
4. [Advanced Pydantic: Controlling Extra Fields](#-advanced-pydantic-controlling-extra-fields)
5. [How to Access and Return Pydantic Data](#-how-to-access-and-return-pydantic-data)
6. [Testing POST Endpoints (Swagger & Postman)](#-testing-post-endpoints-swagger--postman)
7. [Why Use `if __name__ == "__main__":`?](#-why-use-if-__name__--__main__)
8. [How to Run the Project](#-how-to-run-the-project)

---

## 📖 Overview & Why Pydantic?

In web APIs, clients (front-end apps, mobile apps, other microservices) send data to the server using HTTP methods like **POST**, **PUT**, or **PATCH**.

Before storing or processing incoming data, the server must answer three questions:
1. **Did the client send all required fields?**
2. **Are the values of the correct data types (e.g., integer for age, string for name)?**
3. **Is the data formatted properly?**

FastAPI relies on **Pydantic** to solve this problem cleanly through Python type annotations.

---

## 🛠 The 3 Approaches to Receiving POST Data

In `main.py`, three different approaches are explored:

```
Method 1: Direct Parameters ──► Unsafe & query-based
Method 2: Raw Dict ────────────► Flexible, but no schema/type validation
Method 3: Pydantic Model ──────► Safe, typed, auto-validated, self-documenting (Best Practice)
```

---

### 1. Method 1: Direct Parameters (Query Parameters in POST)

```python
@app.post("/create-user")
def create_user(name: str, age: int):
    return {"name": name, "age": age}
```

#### How it works:
When parameters are placed directly in the endpoint signature without a Pydantic model or `Body(...)`, FastAPI expects them as **Query Parameters** in the URL:
```http
POST /create-user?name=Rahim&age=22
```

#### Why this is considered primitive/unsafe for POST requests:
- **Sensitive data exposed:** Query strings are visible in browser history, proxy logs, and server access logs.
- **Size limitations:** URLs have length limitations (often 2048 characters).
- **Cannot handle nested structures:** You cannot easily pass complex, nested data (like lists, nested dictionaries) through query parameters.
- **Breaks REST conventions:** POST requests should send payload data in the **Request Body**, not in the URL query string.

---

### 2. Method 2: Generic Dictionary (`user: dict`)

```python
@app.post("/create-user-json")
def create_user_json(user: dict):
    return user
```

#### How it works:
FastAPI recognizes that `user: dict` should come from the **JSON Request Body**. You can pass any arbitrary JSON payload:

```json
{
  "Name": "Rahim Ullah",
  "Age": 22,
  "Dev": "Python",
  "Skill": ["cpp", "js", "fastapi"]
}
```

#### Why this is risky:
- ❌ **No Schema Enforcement:** If the client sends `"agggge"` instead of `"age"`, or capitalizes `"Name"` instead of `"name"`, Python accepts it without complaint.
- ❌ **No Type Safety:** A client can send `"Age": "twenty-two"` instead of an integer. You will only discover the bug when your code crashes later with a `TypeError`.
- ❌ **Poor API Documentation:** Swagger UI cannot display the expected schema or fields because it only knows it's a generic `object`.
- ❌ **No Editor Autocompletion:** You must access fields using string lookups like `user["name"]` instead of `user.name`.

---

### 3. Method 3: Pydantic Model (`User(BaseModel)`)

```python
class User(BaseModel):
    name: str
    age: int

@app.post("/create-user-pydantic")
def create_user_pydantic(user: User):
    return user
```

#### Why this is the Modern & Recommended Standard:
- ✅ **Automatic Type Validation:** If someone passes `"age": "abc"`, FastAPI automatically returns a descriptive `422 Unprocessable Entity` error before your function code even runs.
- ✅ **Type Coercion:** If someone sends `"age": "22"` (as a string containing digits), Pydantic intelligently converts it to integer `22`.
- ✅ **Interactive Documentation:** Swagger UI (`/docs`) automatically renders the complete JSON schema with an editable template and field types.
- ✅ **IDE Autocomplete:** Inside `create_user_pydantic`, your editor knows `user.name` is a `str` and `user.age` is an `int`.

---

## 📊 Summary Comparison Table

| Feature | Direct Query Params (`/create-user`) | Generic `dict` (`/create-user-json`) | Pydantic Model (`/create-user-pydantic`) |
| :--- | :--- | :--- | :--- |
| **Data Location** | URL Query String (`?name=...`) | Request Body (JSON) | Request Body (JSON) |
| **Type Validation** | Yes (basic) | ❌ None | ✅ Yes (strict & deep) |
| **Schema Definition** | ❌ None | ❌ None | ✅ Explicit & self-documenting |
| **Supports Complex Data** | ❌ No | ✅ Yes | ✅ Yes (lists, models, nested JSON) |
| **Auto-Generated Docs** | Basic query params | Empty object `{}` | Complete, interactive JSON schema |
| **Security / Best Practice** | ⚠️ Not recommended for payloads | ⚠️ Risky for production | ⭐ Industry standard |

---

## ⚙️ Advanced Pydantic: Controlling Extra Fields

What happens if a client sends extra fields that aren't defined in your Pydantic model?

For example:
```json
{
  "name": "Rahim",
  "age": 22,
  "role": "Admin",
  "salary": 100000
}
```

### 1. Default Behavior (`extra="ignore"`)
In Pydantic v2, extra fields are **silently ignored/skipped**. The returned `user` will only contain:
```json
{
  "name": "Rahim",
  "age": 22
}
```

### 2. Blocking Extra Fields (`extra="forbid"`)
If you want to prevent clients from sending unexpected fields (such as accidentally attempting mass assignment or typos), use `ConfigDict(extra="forbid")`:

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    age: int
```

- If extra fields are sent, FastAPI returns **`422 Unprocessable Entity`**:
```json
{
  "detail": [
    {
      "type": "extra_forbidden",
      "loc": ["body", "role"],
      "msg": "Extra inputs are not permitted",
      "input": "Admin"
    }
  ]
}
```

---

## 🔍 How to Access and Return Pydantic Data

Inside your endpoint function:

```python
@app.post("/create-user-pydantic")
def create_user_pydantic(user: User):
    # 1. Access attributes via dot notation:
    user_name = user.name
    user_age = user.age

    # 2. Convert to dictionary if needed:
    user_dict = user.model_dump()

    # 3. Return the model directly:
    # FastAPI automatically serializes Pydantic models to JSON
    return user
```

---

## 🧪 Testing POST Endpoints (Swagger & Postman)

Because web browsers only execute **GET** requests when entering a URL in the address bar, you cannot test **POST**, **PUT**, or **PATCH** endpoints directly by pressing Enter in the browser.

### Recommended Ways to Test:
1. **FastAPI Built-in Swagger UI (Fastest & Zero Setup):**
   - Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.
   - Click on the endpoint (e.g., `POST /create-user-pydantic`).
   - Click **Try it out**.
   - Fill in or modify the JSON payload in the request body editor.
   - Click **Execute** and review the response status code and body.

2. **ReDoc Alternative:**
   - Open [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) for clean, documentation-focused views.

3. **Postman / Thunder Client / cURL:**
   - Method: `POST`
   - URL: `http://127.0.0.1:8000/create-user-pydantic`
   - Headers: `Content-Type: application/json`
   - Body (raw JSON):
     ```json
     {
       "name": "Rahim",
       "age": 22
     }
     ```

---

## 💡 Why Use `if __name__ == "__main__":`?

In `main.py`, the server execution is wrapped with:

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
```

### Why this pattern is used:
1. **Direct Execution:** When you run `python main.py`, Python sets the special variable `__name__` to `"__main__"`. The condition evaluates to `True`, starting Uvicorn automatically.
2. **Safe Importing:** If another file imports `app` from `main.py` (for example, in automated tests or multi-file projects: `from main import app`), `__name__` will be `"main"`, NOT `"__main__"`. The server will **not** accidentally start in the background.

---

## 🚀 How to Run the Project

### 1. Run directly with Python:
```bash
python main.py
```

### 2. Or run via Uvicorn CLI:
```bash
uvicorn main:app --reload
```

### 3. Open the Interactive Docs:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
