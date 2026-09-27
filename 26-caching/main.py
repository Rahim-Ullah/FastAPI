from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import time # to check and monitor the speed of response


app = FastAPI()

# cache setup
cached_data = []
last_fetched = 0


@app.get("/")
def home():
    return{
        "Welcome!": "to our fetching with cache system"
    }

# get new (news crawling)
@app.get("/news")
async def news_fetching(page: int = 1, limit: int =10):
    global cached_data, last_fetched # selecting the above variables as global 

    start_time = time.time()
    if time.time() - last_fetched > 60:    
        print("Fetching fresh data!")
        url = "https://news.ycombinator.com/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        cached_data = [
            item.text for item in soup.find_all("span", class_="titleline")
        ]

        last_fetched = time.time()

    else:
        print("Using cache")

    end_time = time.time()

    total_time_taken = round(end_time-start_time, 4)
    print(f"Total time taken: {total_time_taken}")

    return {
        "Time taken": total_time_taken,
        "Data": cached_data[:5]
    }

    title = []

    for i in soup.find_all("span", class_="title_line"):
        title.append(i.text)

    # pagination logic
    # start_page = 
    return {
        "Data": title[:5]
    }
    