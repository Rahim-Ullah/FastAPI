from fastapi import FastAPI, status as status_codes, HTTPException as http_exception

app = FastAPI()


class UserNotFoundException(Exception):
    def __init__(self, user_name: str): # we can create our own exceptions and raise them using raise kw, and the exception is initialize by constructor and we can pass the user_id to it
        self.user_name = user_name

@app.post("/create_user", status_code=status_codes.HTTP_201_CREATED) # we have a bunch of status codes in fastapi, we can use them to return the appropriate status code for our endpoints
async def create_user():
    return {"message": "User created successfully"}


# custom response
@app.get("/get_users", status_code=status_codes.HTTP_200_OK)
async def get_users():
    return {"message": "Users retrieved successfully", "status_code": status_codes.HTTP_200_OK, }

# get root with id
# @app.get("/get_users/{user_id}")
# async def get_user(user_id: int):
#     if user_id < 1:
#         raise http_exception(status_code=status_code.HTTP_400_BAD_REQUEST, detail="Invalid user ID Passed!") # the code inside raised will not be shown to user instead the details of the error will be
#     return {"message": f"User with ID {user_id} retrieved successfully", "status_code": status_code.HTTP_200_OK}


# Errors handling code custom, exceptions and global error handlers 
@app.get("/get_users/{user_id}", status_code=status_codes.HTTP_404_NOT_FOUND)
async def get_user(user_id: int):
    if user_id < 1:
        raise http_exception(status_code=400, detail="Invalid user ID Passed!")
    return {"message": f"User with ID {user_id} retrieved successfully", "status_code": status_codes.HTTP_200_OK}


# Custom error handler [for that creating a model for the error is a good practice]
# @app.exception_handler(UserNotFoundException)
# async def user_not_found_exception_handler(request, exc):
#     return {"message": f"User with name {exc.user_name} not found", "status_code": status_codes.HTTP_404_NOT_FOUND}

    
@app.get("/get_users/{user_name}")
async def get_user(user_name: str):
    # try:
    if user_name != "rahim":
        raise UserNotFoundException(user_name)
    return {"message": f"User with name {user_name} retrieved successfully", "status_code": status_codes.HTTP_200_OK}





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)