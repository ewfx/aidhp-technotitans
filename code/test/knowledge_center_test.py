from flask.testing import FlaskClient
import pytest
import sys
import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Fix the path to recognize the src module
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(SCRIPT_DIR, '../src/backend'))

from app import app
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_valid_customer_id(client):
    response = client.get('/knowledge_center/CUST2025A')
    assert response.status_code == 200
    assert "Articles" in response.get_json()
    assert "Videos" in response.get_json()
    assert "PDFs" in response.get_json()

def test_missing_customer_id(client):
    response = client.get('/knowledge_center/')
    assert response.status_code == 404

def test_none_customer_id(client):
    response = client.get('/knowledge_center/None')
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid customer ID"}


def test_search_exception(client, mocker):
    # Simulate exception in search_results function
    mocker.patch('app.search_results', side_effect=Exception("Search failure"))
    response = client.get('/knowledge_center/CUST456')
    assert response.status_code == 200
    assert "error" in response.get_json()
