from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# testing home route
def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_add_numbers():
    response = client.get("/add?a=1&b=2") # here the data is passes as a query string and hard coded format because we just need to obtain the correct result
    assert response.status_code == 200
    assert response.json() == {"result": 3}