from fastapi.testclient import TestClient
from app.main import app
from app.database import init_database
from scripts.seed_data import seed_sample_data

# Initialize DB and seed data before tests
init_database()
seed_sample_data()

client = TestClient(app)

def test_get_classes():
    response = client.get("/api/v1/classes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)