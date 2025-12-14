from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.status_code == 200

def test_flights():
    res = client.get("/flights?from_city=IST&to_city=AMS")
    assert res.status_code == 200
