# FastAPI Web Scraping & Pagination API

A lightweight FastAPI service demonstrating how to scrape web data using **BeautifulSoup4** and **Requests**, implementing four different pagination patterns.

---

## Project Structure

```text
25-pagination/
├── main.py        # FastAPI app with scraping routes & pagination logic
├── README.md      # Project documentation and route tests
└── .venv/         # Python virtual environment
```

---

## Setup & Running

### 1. Activate Virtual Environment
```powershell
.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```bash
pip install fastapi uvicorn requests beautifulsoup4 pytest httpx
```

### 3. Start the Server
```bash
python main.py
```
Or with Uvicorn hot-reload:
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
Interactive API docs are available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

## Explanation of `main.py`

[main.py](file:///C:/Users/rahim_ullah/Downloads/FastAPI/25-pagination/main.py) defines the FastAPI application instance and four route handlers demonstrating progressive pagination techniques:

### 1. Route 1: Baseline Unpaginated Scrape
- **Path**: `GET /scrape`
- **Handler**: [`scrape_website`](file:///C:/Users/rahim_ullah/Downloads/FastAPI/25-pagination/main.py#L9-L16)
- **Logic**: Sends an HTTP GET request to `https://news.ycombinator.com`, parses the HTML DOM with BeautifulSoup, extracts the inner text of all `<span>` tags into a list, and returns the full unpaginated list.

### 2. Route 2: Fixed-Size Page-Number Pagination
- **Path**: `GET /scrape/{page_number}`
- **Handler**: [`scrape_website_with_pagination`](file:///C:/Users/rahim_ullah/Downloads/FastAPI/25-pagination/main.py#L21-L29)
- **Logic**: Accepts a 0-indexed `page_number` path parameter. Enforces a non-negative value via `max(0, page_number)`. Slices the results with a hardcoded page size of 10 items (`span[page_number*10 : (page_number+1)*10]`).

### 3. Route 3: Dynamic Limit & Page-Number Pagination
- **Path**: `GET /scrape/limit/{limit}/page_number/{page_number}`
- **Handler**: [`scrape_website_using_limit`](file:///C:/Users/rahim_ullah/Downloads/FastAPI/25-pagination/main.py#L39-L48)
- **Logic**: Accepts dynamic `limit` and `page_number` path parameters. Computes chunk bounds dynamically using `span[page_number*limit : (page_number+1)*limit]`.

### 4. Route 4: Structured Metadata Envelope Pagination
- **Path**: `GET /scrape/limit/{limit}/page_number/{page_number}`
- **Handler**: [`scrape_website_using_pagination_logic`](file:///C:/Users/rahim_ullah/Downloads/FastAPI/25-pagination/main.py#L54-L70)
- **Logic**: Employs standard 1-indexed pagination logic (`start_index = (page_number - 1) * limit`, `end_index = start_index + limit`). Returns a structured JSON response dictionary containing pagination metadata:
  ```json
  {
    "page_number": 1,
    "limit": 5,
    "Total": 120,
    "data": ["item1", "item2", "..."]
  }
  ```
> [!NOTE]
> **FastAPI Route Precedence**: Because Route 3 and Route 4 declare the exact same path (`/scrape/limit/{limit}/page_number/{page_number}`), FastAPI's router evaluates requests against the first declared handler ([`scrape_website_using_limit`](file:///C:/Users/rahim_ullah/Downloads/FastAPI/25-pagination/main.py#L39-L48)). Route 4's handler function ([`scrape_website_using_pagination_logic`](file:///C:/Users/rahim_ullah/Downloads/FastAPI/25-pagination/main.py#L54-L70)) represents an alternative architectural style and can be tested directly as a unit test or assigned a distinct path (e.g. `/scrape/v2/limit/{limit}/page_number/{page_number}`).

---

### Route Testing Code

Below is the complete testing suite using `pytest` and FastAPI's `TestClient` to verify all 4 routes:

```python
from fastapi.testclient import TestClient
from main import app, scrape_website_using_pagination_logic

client = TestClient(app)


def test_route_1_scrape_all():
    """Route 1: GET /scrape"""
    response = client.get("/scrape")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_route_2_fixed_pagination():
    """Route 2: GET /scrape/{page_number}"""
    response = client.get("/scrape/0")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10


def test_route_3_dynamic_limit():
    """Route 3: GET /scrape/limit/{limit}/page_number/{page_number}"""
    response = client.get("/scrape/limit/5/page_number/0")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5


def test_route_4_pagination_logic_metadata():
    """Route 4: scrape_website_using_pagination_logic handler"""
    # Directly invokes the handler to test the structured envelope logic
    result = scrape_website_using_pagination_logic(limit=5, page_number=1)
    assert isinstance(result, dict)
    assert result["page_number"] == 1
    assert result["limit"] == 5
    assert "Total" in result
    assert "data" in result
    assert isinstance(result["data"], list)
    assert len(result["data"]) <= 5
```

#### Test Explanations:
1. **`test_route_1_scrape_all`**: Sends a request to `/scrape`, verifies HTTP 200 status, and confirms the response body is a non-empty list of scraped elements.
2. **`test_route_2_fixed_pagination`**: Requests page 0 (`/scrape/0`), verifying that status is 200 and the returned list adheres to the 10-item limit.
3. **`test_route_3_dynamic_limit`**: Requests custom limit 5 and page 0 (`/scrape/limit/5/page_number/0`), asserting status 200 and list length `<= 5`.
4. **`test_route_4_pagination_logic_metadata`**: Directly tests [`scrape_website_using_pagination_logic`](file:///C:/Users/rahim_ullah/Downloads/FastAPI/25-pagination/main.py#L54-L70), verifying that the returned dictionary contains the expected metadata keys (`page_number`, `limit`, `Total`, `data`) and that sliced data matches the specified limit.
