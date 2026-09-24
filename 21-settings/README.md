# ⚙️ Simple FastAPI Settings & `.env` Guide

A lightweight and beginner-friendly project showing how to manage settings and secrets in **FastAPI** using a `.env` file and **Pydantic Settings**.

---

## 💡 How the 3 Files Work Together

```text
.env (Secrets)  ──▶  config.py (Loads & Validates)  ──▶  main.py (Uses Settings)
```

1. **`.env`**: Stores sensitive variables (like passwords, keys, and database names) outside your code.
2. **`config.py`**: Uses `pydantic-settings` to read `.env` and convert it into a clean Python `settings` object.
3. **`main.py`**: Imports `settings` to configure FastAPI and connect to the SQLite database.

---

## 📂 Project Structure

```text
21-settings/
│
├── .env              # Your secret keys and configuration
├── .gitignore        # Tells Git what files to ignore
├── config.py         # Loads and validates the settings
├── main.py           # FastAPI server & home route
├── requirements.txt  # Needed packages
└── README.md         # Simple documentation
```

---

## 🔍 Code Walkthrough

### 1. `.env` (The Secrets)
```env
APP_NAME="FastAPI Simple Settings"
ADMIN_EMAIL="admin@example.com"
SECRET_KEY="my_secret_token_123"
DATABASE_NAME="simple.db"
```

### 2. `config.py` (The Settings Loader)
```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Default App Name"
    admin_email: str = "default@example.com"
    secret_key: str = "default_secret"
    database_name: str = "simple.db"

    # Automatically load values from the .env file
    model_config = SettingsConfigDict(env_file=".env")

# Single instance used everywhere
settings = Settings()
```

### 3. `main.py` (Using the Settings)
```python
import sqlite3
from fastapi import FastAPI
from config import settings

app = FastAPI(title=settings.app_name)

# Uses DATABASE_NAME from config
def init_db():
    conn = sqlite3.connect(settings.database_name)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS system_status (id INTEGER PRIMARY KEY, message TEXT)")
    cursor.execute("INSERT OR IGNORE INTO system_status (id, message) VALUES (1, 'Database connected successfully!')")
    conn.commit()
    conn.close()

init_db()

@app.get("/")
def home():
    # Read from the SQLite database
    conn = sqlite3.connect(settings.database_name)
    cursor = conn.cursor()
    cursor.execute("SELECT message FROM system_status WHERE id = 1")
    db_message = cursor.fetchone()[0]
    conn.close()

    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "secret_key": settings.secret_key,
        "database_file": settings.database_name,
        "db_status": db_message
    }
```

---

## ⚠️ The `.gitignore` Production Rule

Look at your [`.gitignore`](file:///C:/Users/rahim_ullah/Downloads/FastAPI/21-settings/.gitignore):

```gitignore
# .env
```

- **In this tutorial**: `# .env` is commented out so you can easily see and run the example.
- **In real production**: You **MUST uncomment** `.env` (remove the `#`). 
- **Why?** Git should never track your real `.env` file. If you push `.env` to GitHub, anyone can see your private keys and database passwords!

---

## 🚀 How to Run

1. Open your terminal in this folder:
   ```bash
   cd 21-settings
   ```

2. Activate the virtual environment:
   - **Windows**: `.\.venv\Scripts\Activate.ps1`
   - **Mac/Linux**: `source .venv/bin/activate`

3. Run the server:
   ```bash
   python main.py
   ```

4. Open your browser at:
   - **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**
   - You will see the settings loaded from `.env` and the message from the SQLite database!
