# FastAPI + SQLite Database Initialization

A clean, minimalist FastAPI starter demonstrating direct embedded SQLite integration, automated schema initialization on startup, and API health verification.

---

## 📌 Overview

This project provides a foundational setup for a Todo REST API built with **FastAPI** and Python's native **SQLite** engine (`sqlite3`).

When `main.py` is executed:
1. It opens or automatically creates a local SQLite database file named `data.db`.
2. It initializes the `todos` table schema if it does not already exist.
3. It exposes an asynchronous HTTP endpoint verifying database initialization and server health.

---

## 📁 Project Structure

```text
.
├── main.py       # Application entry point, DB configuration, and routes
├── data.db       # SQLite database file (generated automatically on startup)
└── README.md     # Project documentation
```

---

## 🗄️ Database Architecture & Schema

### Connection Management
```python
conn = sqlite3.connect('data.db', check_same_thread=False)
cursor = conn.cursor()
```
- **Automatic Storage Creation**: If `data.db` does not exist in the working directory, SQLite creates the file automatically upon connection.
- **Thread Sharing (`check_same_thread=False`)**: Standard SQLite connections in Python are bound to the creating thread. Because FastAPI handles requests across an asynchronous event loop and a thread worker pool, `check_same_thread=False` allows cross-thread access for simple concurrent operations.

### Schema: `todos` Table

The application executes a data definition query (`CREATE TABLE IF NOT EXISTS`) to ensure the table is ready without error on subsequent restarts:

```sql
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY, 
    title TEXT NOT NULL,
    description TEXT,
    completed TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Field Specifications

| Column | Data Type | Constraints / Default | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY` | Auto-incrementing unique identifier. |
| `title` | `TEXT` | `NOT NULL` | Required name or summary of the task. |
| `description` | `TEXT` | `NULL` | Optional detailed information about the task. |
| `completed` | `TEXT` | `NULL` | Task completion status. |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Automatic UTC creation timestamp. |

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9 or higher
- `pip` (Python package manager)

### 2. Environment Setup

Create and activate a virtual environment:

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### 3. Install Dependencies

Install FastAPI and an ASGI web server (Uvicorn):

```bash
pip install fastapi uvicorn
```

*(Note: `sqlite3` is part of Python's standard library and requires no separate installation.)*

### 4. Run the Application

Start the local development server with auto-reload:

```bash
uvicorn main:app --reload
```

The server will bind to `http://127.0.0.1:8000`.

---

## 📡 API Reference

### Health Check / Root Endpoint

Verifies server availability and successful database connection setup.

- **Method:** `GET`
- **Path:** `/`
- **Response Format:** `application/json`
- **Status Code:** `200 OK`

#### Example Request
```bash
curl -X GET http://127.0.0.1:8000/
```

#### Example Response
```json
{
  "DB connection": "DB connection established successfully!"
}
```

---

## 📖 Interactive Documentation

FastAPI automatically generates interactive OpenAPI documentation out of the box:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🛠️ Architectural Recommendations & Best Practices

For extending this project into a production-grade application, consider the following engineering improvements:

1. **Per-Request Connection Lifecycle (Dependency Injection):**
   Avoid sharing a single global `conn` object across the entire process. Instead, use FastAPI dependencies (`Depends`) with a generator pattern to yield and properly close a connection per request:
   ```python
   def get_db():
       conn = sqlite3.connect('data.db', check_same_thread=False)
       try:
           yield conn
       finally:
           conn.close()
   ```

2. **Schema Optimization for Boolean Values:**
   SQLite does not have an internal boolean data type; booleans are conventionally stored as `INTEGER` (`0` for false, `1` for true):
   ```sql
   completed INTEGER DEFAULT 0
   ```

3. **Data Validation with Pydantic:**
   Define Pydantic schemas (`BaseModel`) for request body validation and response serialization when implementing CRUD routes (`POST /todos`, `GET /todos`, etc.).

4. **Async Database Drivers:**
   For high-concurrency environments, consider asynchronous database libraries such as `aiosqlite` or ORMs like SQLAlchemy (async mode) or SQLModel to prevent blocking the event loop during database operations.
