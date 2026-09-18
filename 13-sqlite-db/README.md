# 🚀 FastAPI + SQLite: Database Connection & Schema Setup

Welcome! This project demonstrates how to connect a **FastAPI** web application directly to a local **SQLite** database and automatically initialize a database table on startup.

---

## 📖 Overview

At this stage, `main.py` serves as the foundation for a Todo API. When you run the application:
1. It connects to (or automatically creates) a local SQLite database file named `data.db`.
2. It sets up a `todos` table if one doesn't already exist.
3. It spins up a FastAPI server with a root endpoint (`/`) that confirms the database connection is live.

---

## 🧠 Code Breakdown (Step-by-Step)

Here is an intuitive walkthrough of what each section of `main.py` does:

### 1. Imports & FastAPI Initialization
```python
import sqlite3
from fastapi import FastAPI

app = FastAPI()
```
- `sqlite3` is part of Python's standard library, so no extra database drivers are required.
- `app = FastAPI()` creates the core application instance that routes incoming HTTP requests.

---

### 2. Establishing the Database Connection
```python
conn = sqlite3.connect('data.db', check_same_thread=False)
```
- **Automatic File Creation**: If `data.db` does not exist in the working directory, SQLite creates it automatically.
- **Why `check_same_thread=False`?**
  By default, Python's SQLite driver restricts database operations to the thread that created the connection. Because FastAPI handles requests asynchronously and across multiple threads in its worker pool, setting `check_same_thread=False` allows different threads to share this connection safely for simple queries.

---

### 3. The Cursor & The Spreadsheet Analogy
```python
cursor = conn.cursor()
```
> **💡 Intuitive Analogy:**
> Think of `conn` (the connection) as opening a spreadsheet workbook on your computer. The `cursor` is like your active mouse cursor inside the sheet—it points to where you want to read, write, or run commands.

---

### 4. Creating the `todos` Table
```python
cursor.execute('''
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY, 
    title TEXT NOT NULL,
    description TEXT,
    completed TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')
```
Using `CREATE TABLE IF NOT EXISTS` ensures that the app won't crash if you restart the server and the table already exists.

#### 🗄️ Table Schema

| Column | Type | Constraints / Default | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY` | Unique auto-incrementing identifier for each todo item. |
| `title` | `TEXT` | `NOT NULL` | The main task heading or title (mandatory). |
| `description` | `TEXT` | Nullable | Optional detailed notes for the task. |
| `completed` | `TEXT` | Nullable | Status indicator (e.g., `'true'`/`'false'` or `'pending'`/`'done'`). |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Automatically records when the item was inserted. |

---

### 5. Committing the Changes
```python
conn.commit()
```
Executing SQL statements stages your changes in memory. Calling `conn.commit()` writes and saves those changes permanently to `data.db`. Without this step, your table creation would be lost when the connection closes.

---

### 6. The Health Check Endpoint
```python
@app.get('/')
async def read_root():
    return {'DB connection': 'DB connection established successfully!'}
```
- Listens for `GET` requests on the root path `/`.
- Returns a JSON response indicating the server is running and the database setup executed without errors.

---

## 🛠️ Getting Started

### 1. Prerequisites
Ensure you have Python 3.9+ installed.

### 2. Install Dependencies
```bash
pip install fastapi uvicorn
```

### 3. Run the Development Server
```bash
uvicorn main:app --reload
```

The `--reload` flag enables auto-reload whenever you save changes to `main.py`.

### 4. Test the Endpoint
Open your browser or run curl:
```bash
curl http://127.0.0.1:8000/
```
Expected output:
```json
{"DB connection": "DB connection established successfully!"}
```

---

## 📚 Interactive API Documentation

FastAPI automatically generates interactive documentation for your endpoints:
- **Swagger UI**: Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: Visit [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 💡 Friendly Pro-Tips & Next Steps

1. **Boolean for `completed`**:
   SQLite doesn't have a dedicated `BOOLEAN` type; it typically represents booleans as `INTEGER` (`0` for false, `1` for true). You could refine the column to:
   ```sql
   completed INTEGER DEFAULT 0
   ```
2. **Connection Lifecycle & Dependency Injection**:
   As the app grows, instead of keeping a single global `conn`, consider opening and closing connections per request using FastAPI's dependency injection (`Depends`) or an ORM/query builder like SQLAlchemy or SQLModel.
3. **Build Full CRUD**:
   Add endpoints for:
   - `POST /todos` (Create a task)
   - `GET /todos` (Fetch all tasks)
   - `GET /todos/{id}` (Fetch a single task)
   - `PUT /todos/{id}` (Update a task)
   - `DELETE /todos/{id}` (Delete a task)
