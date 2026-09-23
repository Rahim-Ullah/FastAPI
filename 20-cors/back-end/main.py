from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow origins using CORS middleware (we can add multiple origins to allow requests from)
# Setup this inside .env file for production and development environment. For now, we will hardcode it here.
origins = [
    "http://localhost:5173", # This is the url where the front-end is running. We can add multiple urls here if we have multiple front-end apps.
    "http://127.0.0.1:5173" # This is the port where the front-end is running.
]
# why both the IP address and localhost? Because some browsers treat localhost and 127.0.0.1 as different origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # This means that the browser will include credentials (like cookies, authorization headers, or TLS client certificates) in requests to the server.
    allow_methods=["*"], # This means that from the allowed oring any method can be used.
    allow_headers=["*"],
)




# Home route
@app.get("/")
async def read_root():
    return {"Backend":"This is from backend fastapi!","message": "CORS enabled FastAPI backend is running!"}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)