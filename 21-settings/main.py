import sqlite3
from fastapi import FastAPI
from config import settings

app = FastAPI(title=settings.app_name)


# 1. Initialize simple SQLite database using setting from config.py
def init_db():
    conn = sqlite3.connect(settings.database_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_status (
            id INTEGER PRIMARY KEY,
            message TEXT
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO system_status (id, message) VALUES (1, 'Database connected successfully!')")
    conn.commit()
    conn.close()


init_db()


# 2. Home Route: shows settings from .env and data from SQLite
@app.get("/")
def home():
    # Fetch message from SQLite database
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
