from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session as DBSession, sessionmaker
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI()

engine = create_engine('sqlite:///database.db', echo=True, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True) # index is used to speed up the search of the database... for more go down to the end of file

    title = Column(String)
    description= Column(String)
    completed = Column(Integer)
    # user_id = Column(Integer, ForeignKey('users.id'))


class TodoUpdate(BaseModel):
    title: str
    description: str
    completed: int



Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Connection": "Database connected successfully!"} 

@app.post("/todos")
# def create_todo(todo: User, db: session = Depends(get_db)):
def create_todo(title: str, db: DBSession = Depends(get_db)):
    # create todo object
    todo = Todo(title=title, description="This is a sample todo", completed=0)
    db.add(todo) # adding object to db
    db.commit() # saving db changes (in sql a commit is must to save the current changes to the database)
    db.refresh(todo) # refreshing the object to get the latest changes
    return {"Message": f"Todo {todo.title} created successfully!"} # returning the message to the user through the api, the return is just for api call not db changes

@app.get("/todos")
def read_todos(db: DBSession = Depends(get_db)):
    todos = db.query(Todo).all() # querying the database to fetch all the todos (query is the select version of sql)
    return {"Total": f"Total {len(todos)} todos found!"," Todos": todos} # returning the todos to the user through the api so that user can see what has been return from db or the api calls tell user what changes has been made to the database


@app.get("/todos/{id}")
def read_todo(id: int, db: DBSession = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first() # querying the database to fetch the todo with the id {.first() is used to get the first result of the query} but in our case our id is unique so we can skip the .first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
        # if httpexception was not raise then we can simply written our own return statement error
        # return {"Message": f"Todo with id {id} not found! make sure to enter the correct id..."} # returning the message to the user through the api, the return is just for api call not db changes
    return {"Todo": todo} # returning the todo to the user through the api so that user can see what has been return from db or the api calls tell user what changes has been made to the database

"""
# @app.put("/todos/{id}") # PUT is used to update the todo (whole todo object) if we just need a minor change like changing title or description we can use PATCH method
# def update_todo(id: int, todo_update: TodoUpdate, db: DBSession = Depends(get_db)):
#     todo = db.query(Todo).filter(Todo.id == id).first() # querying the database to fetch the todo with the id {.first() is used to get the first result of the query} but in our case our id is unique so we can skip the .first()
#     if not todo:
#         raise HTTPException(status_code=404, detail="Todo not found")
#         # if httpexception was not raise then we can simply written our own return statement error
#         # return {"Message": f"Todo with id {id} not found! make sure to enter the correct id..."} # returning the message to the user through the api, the return is just for api call not db changes
#     todo.title = todo_update.title
#     todo.description = todo_update.description
#     todo.completed = todo_update.completed
#     db.commit() # saving db changes (in sql a commit is must to save the current changes to the database)
#     db.refresh(todo) # refreshing the object to get the latest changes
#     return {"Message": f"Todo {todo.title} updated successfully!"} # returning the message to the user through the api, the return is just for api call not db changes
"""


# clear put method

#  The Clean, Fixed Version:
@app.put("/todos/{id}")
def update_todo(id: int, title: str, db: DBSession = Depends(get_db)):
    todo : Todo | None = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
        
    todo.title = title # type: ignore
    db.commit()
    db.refresh(todo)
    return {"Message": f"Todo {todo.title} updated successfully!"}



@app.delete("/todos/{id}")
def delete_todo(id: int, db: DBSession = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first() # querying the database to fetch the todo with the id {.first() is used to get the first result of the query} but in our case our id is unique so we can skip the .first()
    if not todo:
        return {"Message": f"Todo with id {id} not found! make sure to enter the correct id..."} # returning the message to the user through the api, the return is just for api call not db changes
    title = todo.title
    db.delete(todo) # deleting the todo from the database
    db.commit() # saving db changes (in sql a commit is must to save the current changes to the database)
    return {"Message": f"Todo {title} deleted successfully!"} # returning the message to the user through the api, the return is just for api call not db changes











# Some more on primary key?
# How the primary key gets new value for each todo? on the primary key autoincrement=True by default]
# PostgreSQL: SERIAL / IDENTITY column
# MySQL: AUTO_INCREMENT
# SQLite: INTEGER PRIMARY KEY becomes an alias for rowid, which auto-fills



