from flask.testing import FlaskClient
import pytest
import sys
import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Fix the path to recognize the src module
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(SCRIPT_DIR, '../src/backend'))

from app import app
# from src.backend.invest_now_model import *

@pytest.fixture
def client():
    """Fixture to create a test client for the Flask app."""
    with app.test_client() as client:
        yield client

def test_invest_now_valid_input(client: FlaskClient):
    """Test with valid inputs and check response."""
    response = client.post('/invest-now/CUST2025B', json={"risk_level": "High", "max_tenure": 10})
    assert response.status_code == 200
    data = response.get_json()
    assert "investment_recommendation" in data
    assert "High risk and long term" in data["query"]

def test_invest_now_short_term(client: FlaskClient):
    """Test for short-term investment suggestion."""
    response = client.post('/invest-now/CUST2025B', json={"risk_level": "Low", "max_tenure": 2, "cus_id": "CUST2025B"})
    assert response.status_code == 200
    data = response.get_json()
    assert "Low risk and short term" in data["query"]

def test_invest_now_missing_customer(client: FlaskClient):
    """Test when customer ID is not found in the dataset."""
    response = client.post('/invest-now', json={"risk_level": "Medium", "max_tenure": 5})
    print(response.status_code)
    assert response.status_code == 404
    assert "error" in response.get_json()

def test_invest_now_missing_tenure(client: FlaskClient):
    """Test with missing tenure, should use the default tenure value."""
    response = client.post('/invest-now/CUST2025B', json={"risk_level": "Medium", "cus_id": "CUST2025B"})
    assert response.status_code == 200
    data = response.get_json()
    assert "medium term" in data["query"]

def test_invest_now_invalid_risk_level(client: FlaskClient):
    """Test with an invalid risk level (handled gracefully)."""
    response = client.post('/invest-now/CUST2025B', json={"risk_level": "UnknownRisk", "max_tenure": 8, "cus_id": "CUST2025B"})
    assert response.status_code == 200
    data = response.get_json()
    assert "UnknownRisk risk and long term" in data["query"]
