import time
import asyncio
from fastapi import FastAPI

app = FastAPI()



# General synchronous example
def sync_task():
    
    print("Hello World! just random print")
    return "Hello World randomly printed"

# general async example
async def async_task():
    print("Hello World! just random print before 3 seconds of sleep")
    await asyncio.sleep(3)
    print("Hello World! just random print after 3 seconds")
    return "Hello World after 3 seconds"

# async through api
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/async")
async def async_root():
    await asyncio.sleep(3)
    return {"message": "Hello World after 3 seconds"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")