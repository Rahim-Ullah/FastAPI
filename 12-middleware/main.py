from fastapi import FastAPI, Request 
import time

app = FastAPI()


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request took {process_time} seconds to process")
    return response

# logging middleware 
@app.middleware("http")
# async def add_header(request: Request, call_next):
#     response = await call_next(request)
#     response.headers["X-Custom-Header"] = "My custom header"
async def my_middleware(request: Request, call_next):
    print("My middleware is called! request received")
    response = await call_next(request)
    print("My middleware is done! response sent")
    response.headers["X-Custom-Header"] = "My custom header"
    return response


