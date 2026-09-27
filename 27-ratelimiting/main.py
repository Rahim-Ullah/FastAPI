from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

app = FastAPI()

# limiter setup
limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter

# errors handling
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exception_handler(request = Request, exc = RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"message": "Too many requests. Please try again later."},
    )


# rate limiter api
@app.get("/data")
@limiter.limit("5/minute") # 5 requests per minute
async def rate_limiter(request: Request):
    # await request.state.limiter.hit(request.state.remote_address) #optional: record the hit for the remote address
    return {"message": "Rate limiter api"}
