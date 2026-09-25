import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI


"""
# Crawling in PYTHON

# Site url to be crawled 
url = 'https://www.python.org/'

# Requesting the website
response = requests.get(url)

# Beautiful soup is used to parse the html content
soup = BeautifulSoup(response.content, 'html.parser')

# Finding all the links on the page
links = soup.find_all('a')

# getting the title of the web page
title = soup.title.get_text() if soup.title else 'No title found'
print(f'Title of the page is {title}')

for link in links:
    print(link.get('href'))
"""


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the web crawler API!"}

@app.get("/news")
def read_news():
    # url = 'https://www.python.org/blogs/'
    # url = "https://www.dawn.com/"
    url = "https://www.bbc.com/urdu"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = []
    for t in soup.find_all('h1'):
        title.append(t.get_text())
    return title



    # using on page class
    # title = []
    #     for t in soup.find_all('h1', class_='some_title_class'):
    #         title.append(t.get_text())
    #        # title.append(t.text)
    #     return title


    # title = soup.title.get_text() if soup.title else 'No title found'
    # print(f'Title of the page is {title}')



    # links = soup.find_all('a')
    # for link in links:
    #     print(link.get('href'))
    # return {"message": "Welcome to the web crawler API!"}






if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)