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
    result = scrape_website_using_pagination_logic(limit=5, page_number=1)
    assert isinstance(result, dict)
    assert result["page_number"] == 1
    assert result["limit"] == 5
    assert "Total" in result
    assert "data" in result
    assert isinstance(result["data"], list)
    assert len(result["data"]) <= 5
