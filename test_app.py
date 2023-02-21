import json
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_objects_endpoint():
    response = client.get("/objects?start_date=2023-01-10&end_date=2023-01-20")
    assert response.status_code == 200
    response_data = json.loads(response.text)
    print(response_data)
    assert isinstance(response_data, list)
    assert len(response_data) > 0
    for obj in response_data:
        assert "name" in obj
        assert "size" in obj
        assert "closest_approach_date" in obj
        assert "closest_approach_distance" in obj
