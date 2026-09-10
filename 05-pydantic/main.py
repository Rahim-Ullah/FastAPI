from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict

app = FastAPI()


# this is the generic and unsafe method, the modern and safe method to post request is to use the pydantic model
# remember to test post, put and patch through postman or swagger or maybe another alternative...
@app.post("/create-user")
def create_user(name: str, age: int):
    return {"name": name, "age": age}

# here we can send a json dictionary to the server
@app.post("/create-user-json")
def create_user_json(user: dict):
    return user

# we are able to pass this data to the server
"""
{
"Name": "Rahim Ullah",
"Age": 22,
"Dev": "Python",
"Skill": ["cpp", "js", "fastapi"]
}
"""



# creating the exact same function but using the pydantic model
# now if we send some extra fields during testing they will be skipped automatically! But if you want to throw error instead of skipping the fields you can use the pydantic model
    # This configuration blocks extra fields completely
    # model_config = ConfigDict(extra="forbid") ...inside out the pydantic model
class User(BaseModel):
    # model_config = ConfigDict(extra="forbid") 
    name: str
    age: int


@app.post("/create-user-pydantic")
def create_user_pydantic(user: User): # this is the pydantic model which defines the data types and the data model that will be sent to the server
    # return {"name": user.name, "age": user.age} # below is the alternative to avoid using .name and .age
    return user

# this block checks if the file is being called directly and not imported to another file as library then the uvicorn will be imported to run the server otherwise it will skipped the server to run the library
# this block of code is always is written in a file where we run our server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)