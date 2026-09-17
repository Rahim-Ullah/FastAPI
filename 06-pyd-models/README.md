# 06 - Nested Pydantic Models & Embedded Schemas

Learn how to define, validate, and process complex, nested JSON data structures in FastAPI using nested Pydantic models.

---

## 📌 Concepts Covered

1. **Nested / Embedded Models**: Using one Pydantic model (`Address`) as a field type inside another model (`User`).
2. **Deep Data Validation**: FastAPI validates every level of the JSON payload. If `postal_code` inside `address` is invalid, the error accurately points to `["body", "address", "postal_code"]`.
3. **Clean Attribute Access**: Access nested fields cleanly in Python using dot notation (`user.address.city`).
4. **Self-Documenting Schemas**: Swagger UI (`/docs`) automatically renders the complete nested JSON structure for testing.

---

## 🔍 Code Breakdown (`local-path/main.py`)

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 1. Child Model (Sub-schema)
class Address(BaseModel):
    city: str
    district: str
    postal_code: int

# 2. Parent Model with Embedded Child Model
class User(BaseModel):
    name: str
    age: int
    email: str
    address: Address

@app.post("/create-users")
async def create_user(user: User):
    return {
        "message": f"Hello {user.name}",
        "user_city": user.address.city,
        "details": user
    }
```

### Expected JSON Request Body:
```json
{
  "name": "Rahim",
  "age": 22,
  "email": "rahim@example.com",
  "address": {
    "city": "Peshawar",
    "district": "Peshawar",
    "postal_code": 25000
  }
}
```

---

## 🚀 How to Run & Test

1. **Start the server**:
   ```bash
   uvicorn main:app --reload
   ```

2. **Test using cURL**:
   ```bash
   curl -X POST http://127.0.0.1:8000/create-users \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Rahim",
       "age": 22,
       "email": "rahim@example.com",
       "address": {
         "city": "Peshawar",
         "district": "Peshawar",
         "postal_code": 25000
       }
     }'
   ```

3. **Test in Swagger UI**:
   - Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Expand `POST /create-users`, click **Try it out**, edit the nested JSON, and click **Execute**.
