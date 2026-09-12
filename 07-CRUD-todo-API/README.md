# FastAPI CRUD Todo API

A lightweight, beginner-friendly RESTful Todo API built using [FastAPI](https://fastapi.tiangolo.com/), [Pydantic](https://docs.pydantic.dev/), and [Uvicorn](https://www.uvicorn.org/). This project demonstrates foundational concepts of backend API development in Python, including routing, data modeling, automatic request validation, and in-memory CRUD (Create, Read, Update, Delete) operations.

---

## Table of Contents

- [Project Architecture & Structure](#project-architecture--structure)
- [Technologies Used](#technologies-used)
- [Detailed Code Breakdown](#detailed-code-breakdown)
  - [1. Imports and Setup](#1-imports-and-setup)
  - [2. FastAPI Application Instance](#2-fastapi-application-instance)
  - [3. Data Model (`Todo`)](#3-data-model-todo)
  - [4. In-Memory Database Simulator](#4-in-memory-database-simulator)
  - [5. API Endpoints & Route Handlers](#5-api-endpoints--route-handlers)
    - [Root Endpoint (`GET /`)](#root-endpoint-get-)
    - [Create Todo (`POST /todos`)](#create-todo-post-todos)
    - [Get All Todos (`GET /todos`)](#get-all-todos-get-todos)
    - [Get Single Todo (`GET /todos/{id}`)](#get-single-todo-get-todosid)
    - [Update Todo (`PUT /todos/{id}`)](#update-todo-put-todosid)
    - [Delete Todo (`DELETE /todos/{id}`)](#delete-todo-delete-todosid)
  - [6. Application Entry Point](#6-application-entry-point)
- [API Endpoints Summary](#api-endpoints-summary)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Server](#running-the-server)
  - [Interactive API Documentation](#interactive-api-documentation)
- [Sample Usage](#sample-usage)

---

## Project Architecture & Structure

```
07-CRUD-todo-API/
│
├── main.py          # Application source code (FastAPI app, schema, routes, runner)
├── README.md        # Comprehensive documentation
└── .venv/           # Python virtual environment (if configured)
```

The application is structured in [`main.py`](main.py) covering:
1. **Schema Definition**: Data validation and structure via Pydantic.
2. **State Management**: In-memory list simulation of a database.
3. **HTTP Route Handlers**: CRUD endpoints mapped to HTTP methods (`GET`, `POST`, `PUT`, `DELETE`).
4. **Server Execution**: Development server invocation via Uvicorn.

---

## Technologies Used

- **Python 3.10+**: Core programming language.
- **[FastAPI](https://fastapi.tiangolo.com/)**: Modern, high-performance web framework for building APIs.
- **[Pydantic](https://docs.pydantic.dev/)**: Data validation and settings management using Python type annotations.
- **[Uvicorn](https://www.uvicorn.org/)**: Lightning-fast ASGI (Asynchronous Server Gateway Interface) server implementation.

---

## Detailed Code Breakdown

### 1. Imports and Setup

```python
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
```

- **`from typing import Optional`**: Provides type hinting for fields that are not strictly required or can hold `None` alongside their primary type (e.g., `Optional[str]` is equivalent to `str | None`).
- **`from fastapi import FastAPI`**: Imports the central class used to initialize the web application and register API route decorators.
- **`from pydantic import BaseModel`**: Imports the base class for defining data models. Models enforce type checking, automatic conversion, and JSON schema generation for request/response payloads.

---

### 2. FastAPI Application Instance

```python
app = FastAPI()
```

- **What it is**: An instance of the `FastAPI` class.
- **How it works**:
  - Serves as the primary application registry for all route handlers.
  - Automatically provisions the OpenAPI specifications.
  - Generates interactive Swagger UI documentation at `/docs` and ReDoc at `/redoc`.
  - Serves as the ASGI callable that the Uvicorn server interacts with.

---

### 3. Data Model (`Todo`)

```python
class Todo(BaseModel):
    id: int
    title: str = "My-Todo"
    description: Optional[str] = None
    status: Optional[str] = "pending"
    completed: bool = False
```

- **What it is**: A Pydantic data model representing the schema of a single Todo item.
- **Fields and Types**:
  - **`id: int`**: A unique identifier for the todo item. Required.
  - **`title: str = "My-Todo"`**: The title/name of the task. If omitted from the request body, defaults to `"My-Todo"`.
  - **`description: Optional[str] = None`**: An optional textual description explaining the task. Defaults to `None`.
  - **`status: Optional[str] = "pending"`**: Current status string (e.g., `"pending"`, `"in-progress"`, `"done"`). Defaults to `"pending"`.
  - **`completed: bool = False`**: Boolean flag indicating whether the task is finished. Defaults to `False`.
- **How it works**:
  - Whenever a client sends JSON data to an endpoint expecting a `Todo`, FastAPI validates each field against these rules.
  - If a client provides an invalid type (e.g., a string for `id`), FastAPI automatically rejects the request with a structured `422 Unprocessable Entity` error.

---

### 4. In-Memory Database Simulator

```python
# db simulator list
todos = []
```

- **What it is**: A Python list acting as an in-memory data store.
- **How it works**:
  - Stores instances of the `Todo` model during runtime.
  - Allows fast CRUD operations (`append`, iteration, `remove`) without needing an external database setup like PostgreSQL or SQLite.
- **Note**: Because data is stored in memory, all records reset whenever the server restarts.

---

### 5. API Endpoints & Route Handlers

#### Root Endpoint (`GET /`)

```python
@app.get("/")
def read_root():
    return {"Hello": "Welcome to our TODO app!"}
```

- **Method**: `GET`
- **Path**: `/`
- **Function**: `read_root()`
- **Purpose**: Serves as a health check or landing message for the API.
- **Response**: A JSON dictionary welcoming the user.

---

#### Create Todo (`POST /todos`)

```python
@app.post("/todos")
def create_todo(todo: Todo):
    todos.append(todo)
    return {"message": "Todo created successfully!", "Todo-Data": todo}
```

- **Method**: `POST`
- **Path**: `/todos`
- **Function**: `create_todo(todo: Todo)`
- **Parameters**:
  - `todo: Todo` — The request body is automatically parsed and validated into an instance of the `Todo` class.
- **How it works**:
  1. Validates the client's JSON request body against the `Todo` schema.
  2. Appends the validated `todo` object to the `todos` list.
  3. Returns a JSON response containing a success message and the newly created `Todo-Data`.

---

#### Get All Todos (`GET /todos`)

```python
@app.get("/todos")
def read_todos():
    if len(todos) == 0:
        return {"message": "No todos found!"}
    return {"message": "Todos retrieved successfully!", "Todo-Data": todos}
```

- **Method**: `GET`
- **Path**: `/todos`
- **Function**: `read_todos()`
- **How it works**:
  1. Checks if the `todos` list is empty (`len(todos) == 0`).
  2. If empty, returns a friendly `{"message": "No todos found!"}` notification.
  3. If items exist, returns the complete list of todos under the key `"Todo-Data"`.

---

#### Get Single Todo (`GET /todos/{id}`)

```python
@app.get("/todos/{id}")
def read_todo(id: int):
    for todo in todos:
        if todo.id == id:
            return {"message": "Todo retrieved successfully!", "Todo-Data": todo}
    return {"message": "Todo not found!"}
```

- **Method**: `GET`
- **Path**: `/todos/{id}`
- **Function**: `read_todo(id: int)`
- **Parameters**:
  - `id: int` — Path parameter extracted from the URL, automatically cast to an integer.
- **How it works**:
  1. Iterates through the in-memory `todos` list.
  2. Compares each item's `id` with the requested `id`.
  3. If found, immediately returns the matching todo item.
  4. If the loop completes without finding a match, returns `{"message": "Todo not found!"}`.

---

#### Update Todo (`PUT /todos/{id}`)

```python
@app.put("/todos/{id}")
def update_todo(id: int, new_todo: Todo):
    for todo in todos:
        if todo.id == id:
            todo.id = new_todo.id
            todo.title = new_todo.title
            todo.description = new_todo.description
            todo.status = new_todo.status
            todo.completed = new_todo.completed
            return {"message": "Todo updated successfully!", "Todo-Data": new_todo}
    return {"message": "Todo not found!"}
```

- **Method**: `PUT`
- **Path**: `/todos/{id}`
- **Function**: `update_todo(id: int, new_todo: Todo)`
- **Parameters**:
  - `id: int` — Path parameter indicating which todo item to update.
  - `new_todo: Todo` — Request body containing the updated todo fields.
- **Design Note**: Notice that the parameter is named `new_todo` rather than `todo` to prevent variable name shadowing against the loop variable `for todo in todos`.
- **How it works**:
  1. Searches the `todos` list for an item whose `id` matches the path parameter.
  2. If found, updates all fields (`id`, `title`, `description`, `status`, `completed`) of the existing object in-place with the attributes from `new_todo`.
  3. Returns a confirmation message and the updated data.
  4. If no item matches the `id`, returns `{"message": "Todo not found!"}`.

---

#### Delete Todo (`DELETE /todos/{id}`)

```python
@app.delete("/todos/{id}")
def delete_todo(id: int):
    for todo in todos:
        if todo.id == id:
            todos.remove(todo)
            return {"message": "Todo deleted successfully!"}
    return {"message": "Todo not found!"}
```

- **Method**: `DELETE`
- **Path**: `/todos/{id}`
- **Function**: `delete_todo(id: int)`
- **Parameters**:
  - `id: int` — Path parameter specifying the ID of the todo to delete.
- **How it works**:
  1. Loops through `todos` to locate the item with matching `id`.
  2. Calls `todos.remove(todo)` to delete the item from the list.
  3. Returns a confirmation message `{"message": "Todo deleted successfully!"}`.
  4. If no matching item is found, returns `{"message": "Todo not found!"}`.

---

### 6. Application Entry Point

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
```

- **`if __name__ == "__main__":`**: Ensures that the server is only started if the file is executed directly (e.g., `python main.py`), and not when imported by other modules or tests.
- **`import uvicorn`**: Dynamically imports the ASGI server library.
- **`uvicorn.run(...)`**:
  - `app`: The FastAPI application instance to serve.
  - `host="127.0.0.1"`: Listens locally (localhost).
  - `port=8000`: Binds the server to port 8000.
  - `reload=True`: Enables auto-reload, automatically restarting the server whenever code changes are saved (ideal for development).

---

## API Endpoints Summary

| HTTP Method | Endpoint | Description | Request Body / Params | Expected Success Response |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/` | Welcome / Health check | None | `{"Hello": "Welcome to our TODO app!"}` |
| **POST** | `/todos` | Create a new todo | JSON (`Todo` model) | `{"message": "Todo created successfully!", "Todo-Data": {...}}` |
| **GET** | `/todos` | List all todos | None | `{"message": "Todos retrieved successfully!", "Todo-Data": [...]}` |
| **GET** | `/todos/{id}` | Get a single todo by ID | `id: int` (path parameter) | `{"message": "Todo retrieved successfully!", "Todo-Data": {...}}` |
| **PUT** | `/todos/{id}` | Update an existing todo | `id: int` (path) + JSON (`Todo`) | `{"message": "Todo updated successfully!", "Todo-Data": {...}}` |
| **DELETE** | `/todos/{id}` | Delete a todo by ID | `id: int` (path parameter) | `{"message": "Todo deleted successfully!"}` |

---

## Getting Started

### Prerequisites

- Python 3.10+ installed on your system.
- `pip` package manager.

### Installation

1. **Activate your virtual environment** (or create one):
   ```bash
   # Windows (PowerShell)
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. **Install required dependencies**:
   ```bash
   pip install fastapi uvicorn pydantic
   ```

### Running the Server

Run the script directly:
```bash
python main.py
```

Alternatively, you can run it via Uvicorn command-line:
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Once running, the server will be available at `http://127.0.0.1:8000`.

### Interactive API Documentation

FastAPI provides built-in interactive documentation:
- **Swagger UI**: Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to test endpoints directly in your browser.
- **ReDoc**: Visit [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) for clean, publication-style documentation.

---

## Sample Usage

### 1. Create a Todo
**Request:**
```http
POST /todos HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json

{
  "id": 1,
  "title": "Buy Groceries",
  "description": "Milk, eggs, bread, and fruits",
  "status": "pending",
  "completed": false
}
```

**Response (200 OK):**
```json
{
  "message": "Todo created successfully!",
  "Todo-Data": {
    "id": 1,
    "title": "Buy Groceries",
    "description": "Milk, eggs, bread, and fruits",
    "status": "pending",
    "completed": false
  }
}
```

### 2. Fetch All Todos
**Request:**
```http
GET /todos HTTP/1.1
Host: 127.0.0.1:8000
```

### 3. Update a Todo
**Request:**
```http
PUT /todos/1 HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json

{
  "id": 1,
  "title": "Buy Groceries",
  "description": "Milk, eggs, bread, and fruits",
  "status": "completed",
  "completed": true
}
```

### 4. Delete a Todo
**Request:**
```http
DELETE /todos/1 HTTP/1.1
Host: 127.0.0.1:8000
```
