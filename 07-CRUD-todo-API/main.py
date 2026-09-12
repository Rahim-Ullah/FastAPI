from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Todo(BaseModel):
    id: int
    title: str = "My-Todo"
    description: Optional[str] = None
    status: Optional[str] = "pending"
    completed: bool = False

# db simulator list
todos = []
@app.get("/")
def read_root():
    return {"Hello": "Welcome to our TODO app!"}

@app.post("/todos")
def create_todo(todo: Todo):
    todos.append(todo)
    return {"message": "Todo created successfully!", "Todo-Data": todo}


@app.get("/todos")
def read_todos():
    if len(todos) == 0:
        return {"message": "No todos found!"}
    return {"message": "Todos retrieved successfully!", "Todo-Data": todos}

# fetch a single todo
@app.get("/todos/{id}")
def read_todo(id: int):
    for todo in todos:
        if todo.id == id:
            return {"message": "Todo retrieved successfully!", "Todo-Data": todo}
    return {"message": "Todo not found!"}


# update a single todo [the better choice for update is PUT/PATCH?]
# to update a single todo, we should use patch method, put method can also work but it will update the whole todo object as it's primary purpose is create a new todo
# if the client sends a complete replacement object. then put method will replace the whole todo object with the new one so put is useful when complete data replacement is expected
@app.put("/todos/{id}")
def update_todo(id: int, new_todo: Todo): # here the new todo should be passed with different vriable name to the function argument (function arg != todo form the list or db inside the loop) [the concept behind is variable scoping]
    for todo in todos:
        if todo.id == id:
            todo.id = new_todo.id
            todo.title = new_todo.title
            todo.description = new_todo.description
            todo.status = new_todo.status
            todo.completed = new_todo.completed
            return {"message": "Todo updated successfully!", "Todo-Data": new_todo}
    return {"message": "Todo not found!"}


# delete a single todo
@app.delete("/todos/{id}")
def delete_todo(id: int):
    for todo in todos:
        if todo.id == id:
            todos.remove(todo)
            return {"message": "Todo deleted successfully!"}
    return {"message": "Todo not found!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)