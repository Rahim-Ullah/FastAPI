from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

users = []
class User(BaseModel):
    # id: Optional[int] = 1 # if we do not provide the user id still we can find a user by id using id there the id provided my be less than len(users)
    name: str
    age: int

@app.post("/users")
def create_user(user: User):
    users.append(user)
    return {"message": "User created", "user": user}

@app.get("/users")
def read_users():
    return users

# @app.get("/users/{user_id}")
# def read_user(user_id: int, q: Optional[str] = None):
#     for user in users:
#         if user.name == q:
#             return user
#     return {"message": "User not found"}

@app.put("/users/update-by-name")
def update_user(user: User, notify: bool = False):
    for i, u in enumerate(users):
        if u.name == user.name:
            users[i] = user
            return {"message": "User updated", "user": user, "notify": notify}
    return {"message": "User not found"}


@app.put("/users/{user_id}")
def update_user(user_id: int, user: User, notify: bool = False):
    # for i, u in enumerate(users):
    #     if u.user_id == user_id:
    if user_id < len(users):
            users[user_id] = user
            return {"message": "User updated", "user": user, "notify": notify}
    return {"message": "User not found"}
