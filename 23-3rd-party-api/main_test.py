from fastapi.testclient import TestClient
from main import app

client = TestClient(app) # Create a test client for the FastAPI app



# @pytest.fixture # This fixture will create a test client for the FastAPI app
# def client():
#     with TestClient(app) as c:
#         yield c




# def test_root(client): # client should be passed just in-case pytest.fixture is enabled, otherwise it will be created automatically



def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}