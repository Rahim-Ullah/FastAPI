from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()



class Address(BaseModel):
    city: str
    district: str
    postal_code: int
# schema having another embeded schema 
class User(BaseModel):
    name: str
    age: int
    email: str
    address: Address


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/create-users")
async def read_users(user: User):
    return {"message": f"Hello {user.name}", "Here is your details": user}