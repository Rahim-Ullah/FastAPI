import sqlite3
from fastapi import FastAPI

app = FastAPI()

# this step is kinda creating a connection to the database we have created, if the database does not exist, it will be created automatically. The connection object allows us to interact with the database and execute SQL commands.
conn = sqlite3.connect('data.db', check_same_thread=False)
# the check_same_thread=False parameter allows the connection to be shared across multiple threads, which is useful in a multi-threaded application.


# this step is kinda creating a cursor object, which allows us to execute SQL commands on the database. The cursor object is created by the connection object. It is like opening the excel file so that then your cursor can read and write data to it. The cursor object is used to execute SQL commands and retrieve data from the database.
cursor = conn.cursor()


# NOTE: the sqlite3 follows 99 ASCI SQL standard, so you can use any of the following commands to create a table in the database.
cursor.execute('''
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY, 
    title TEXT NOT NULL,
    description TEXT,
    completed TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')
# completed INTEGER NOT NULL? It is a boolean value that is either 0 or 1.

conn.commit()  # this step is kinda saving the changes we made to the database. The commit() method is used to save the changes made to the database. If we don't call commit(), the changes will not be saved and will be lost when the connection is closed.


@app.get('/')
async def read_root():
    return {'DB connection': 'DB connection established successfully!'}