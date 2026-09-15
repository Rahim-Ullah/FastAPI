from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()



class User(BaseModel):
    name: str
    age: int
    email: str
    password: str


class UserResponse(BaseModel):
    name: str
    age: int
    email: str

@app.get("/user", response_model=UserResponse) #this endpoint will return a user object without the password field as defined by user-response model
async def get_user():
    return {"name": "Rahim", "age": 25, "email": "rahimullah@gmail.com", "password": "123456"} #this will return the user object without the password field as defined by user-response model

