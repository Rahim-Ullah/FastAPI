from fastapi import FastAPI
import requests # pip install requests 

response_url = "https://jsonplaceholder.typicode.com/posts"

app = FastAPI()

response = requests.get(response_url)

response_data = response.json()


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/post_item")
async def post_item():
    return {"message": response_data[5]}

@app.get("/post_item_title")
async def post_item_title():
    return {"message": response_data[0]['title']}


@app.get("/post_item_4fields")
async def post_items_4fields():
    return {"message": response_data[:4]}



# A better way

@app.get("/posts")
async def posts():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    return response.json()
# use post id
@app.get("/post/{post_id}")
async def post(post_id):
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    response = requests.get(url)
    return response.json()





if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=9000)