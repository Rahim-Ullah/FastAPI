from fastapi import FastAPI, Depends, HTTPException, Header
# from fastapi.testclient import TestClient

app = FastAPI()

def common_logic():
    # Placeholder for common logic
    
    return {
        "message":"Common logic executed"
        }

def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return x_token

def get_current_user():
    # Placeholder for getting current user
    return {
        "user": "Rahim",
        "email": "rahimullah@gmail.com"
    }

@app.get("/home")
async def root(data = Depends(common_logic)):
    return data



# reusable logic?
@app.get("/dashboard")
async def dashboard(data = Depends(get_current_user)):
    return data

@app.get("/dashboard/user")
async def dashboard_user(data = Depends(get_current_user)):
    return data


# simple auth 
@app.get("/dashboard/auth")
async def dashboard_auth(x_token = Depends(verify_token)):
    return {
        "message": "Authenticated",
        "token": x_token
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)