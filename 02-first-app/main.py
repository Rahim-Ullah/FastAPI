from fastapi import FastAPI

ourApp = FastAPI()

@ourApp.get("/")
def read_root():
	return {"message": "Welcome to our first FasAPI app!"}

@ourApp.get("/about")
async def about_page():
	return {"message": "This is the about page"}

@ourApp.get("/members")
def read_members():
	return {"message": "This is the members page",
		 "Members": ["Rahim Ullah", "Ahmed", "Mohammed"]}