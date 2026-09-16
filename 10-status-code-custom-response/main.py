from fastapi import FastAPI, HTTPException as http_exception, Request, status as status_codes
from fastapi.responses import JSONResponse

app = FastAPI()


# 1. FIXED: Added 'detail' to the constructor so it matches how you raise it below
class UserNotFoundException(Exception):

  def __init__(self, user_name: str, detail: str = None):
    self.user_name = user_name
    self.detail = detail


@app.post("/create_user", status_code=status_codes.HTTP_201_CREATED)
async def create_user():
  return {"message": "User created successfully"}


@app.get("/get_users", status_code=status_codes.HTTP_200_OK)
async def get_users():
  return {
      "message": "Users retrieved successfully",
      "status_code": status_codes.HTTP_200_OK,
  }


# 2. FIXED: Exception handlers MUST return a Response object (like JSONResponse)
@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(
    request: Request, exc: UserNotFoundException
):
  return JSONResponse(
      status_code=status_codes.HTTP_404_NOT_FOUND,
      content={
          "message": f"User with name {exc.user_name} not found",
          "detail": exc.detail,
          "status_code": status_codes.HTTP_404_NOT_FOUND,
      },
  )


# 3. FIXED: Changed route path to '/get_users/by_name/{user_name}' to avoid matching conflicts
@app.get("/get_users/by_name/{user_name}")
async def get_user_by_name(user_name: str):
  if user_name != "rahim":
    # This now works perfectly because __init__ accepts 'detail'
    raise UserNotFoundException(
        user_name, detail="Invalid user name Passed!"
    )
  return {
      "message": f"User with name {user_name} retrieved successfully",
      "status_code": status_codes.HTTP_200_OK,
  }


# 4. FIXED: Changed route path to '/get_users/by_id/{user_id}' and renamed function to prevent overwriting
@app.get("/get_users/by_id/{user_id}")
async def get_user_by_id(user_id: int):
  if user_id != 1:
    raise http_exception(
        status_code=400, detail="Invalid user ID Passed! The ID should be 1"
    )
  return {
      "message": f"User with ID {user_id} retrieved successfully",
      "status_code": status_codes.HTTP_200_OK,
  }


if __name__ == "__main__":
  import uvicorn

  uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)