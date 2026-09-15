from fastapi import FastAPI, status as status_code, HTTPException

app = FastAPI()



@app.post("/create_user", status_code=status_code.HTTP_201_CREATED) # we have a bunch of status codes in fastapi, we can use them to return the appropriate status code for our endpoints
async def create_user():
    return {"message": "User created successfully"}


# custom response
@app.get("/get_users", status_code=status_code.HTTP_200_OK)
async def get_users():
    return {"message": "Users retrieved successfully", "status_code": status_code.HTTP_200_OK, }

# get root with id
@app.get("/get_users/{user_id}")
async def get_user(user_id: int):
    if user_id < 1:
        raise HTTPException(status_code=status_code.HTTP_400_BAD_REQUEST, detail="Invalid user ID Passed!") # the code inside raised will not be shown to user instead the details of the error will be
    return {"message": f"User with ID {user_id} retrieved successfully", "status_code": status_code.HTTP_200_OK}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)