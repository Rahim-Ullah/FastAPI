from bs4 import BeautifulSoup 
import requests

from fastapi import FastAPI

app =  FastAPI()

@app.get("/scrape")
def scrape_website():
    url = "https://news.ycombinator.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    span = []
    for i in soup.find_all("span"):
        span.append(i.text)
    return span


# applying pagination to the same url
@app.get("/scrape/{page_number}")
def scrape_website_with_pagination(page_number: int):
    page_number = max(0, page_number)  # Ensure page_number is not negative (minimum value is 0)
    url = "https://news.ycombinator.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    span = []
    for i in soup.find_all("span"):
        span.append(i.text)
    return span[page_number*10:(page_number+1)*10] # applying pagination limit of 10 items per page


# alternative method to apply pagination using limit and offset as parameters
# alternative method to apply pagination using limit and page_number as parameters
# @app.get("/scrape/limit/{limit}/offset/{offset}")
# def scrape_website_with_pagination(limit: int, offset: int):

# THIS EXACTLY WORKS AS ABOVE BUT USING LIMIT AND PAGE_NUMBER AS PARAMETERS
@app.get("/scrape/limit/{limit}/page_number/{page_number}")
def scrape_website_using_limit(limit: int, page_number: int):
    page_number = max(0, page_number)  # Ensure page_number is not negative (minimum value is 0)
    url = "https://news.ycombinator.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    span = []
    for i in soup.find_all("span"):
        span.append(i.text)
    return span[page_number*limit:(page_number+1)*limit] # applying pagination limit of 10 items per page




# alternatively pagination has a variety of logic to work with but it depends on your choice and the requirement of the project. like below we would use limit and page number as parameters and then we make the logic of pagination with start and end index
@app.get("/scrape/limit/{limit}/page_number/{page_number}")
def scrape_website_using_pagination_logic(limit: int = 5, page_number: int = 1):
    page_number = max(0, page_number)  # Ensure page_number is not negative (minimum value is 0)
    url = "https://news.ycombinator.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    span = []
    for i in soup.find_all("span"):
        span.append(i.text)
    start_index = (page_number - 1)*limit
    end_index = start_index + limit
    # return span[start_index:end_index] # applying pagination limit of 10 items per page
    return {
        "page_number": page_number,
        "limit": limit,
        "Total": len(span),
        "data": span[start_index:end_index]
    }



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)