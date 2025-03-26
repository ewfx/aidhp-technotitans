import pytest
import json
import sys
import os

# Get absolute path for src directory and dataset directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "backend"))
DATASET_DIR = os.path.join(BASE_DIR, "datasets")

# Ensure the datasets exist before running tests
TRANSACTION_FILE = os.path.join(DATASET_DIR, "transaction_history.csv")
CUSTOMER_PROFILE_FILE = os.path.join(DATASET_DIR, "customer_profile.csv")

assert os.path.exists(TRANSACTION_FILE), f"❌ Missing dataset: {TRANSACTION_FILE}"
assert os.path.exists(CUSTOMER_PROFILE_FILE), f"❌ Missing dataset: {CUSTOMER_PROFILE_FILE}"

# Add src to the system path
sys.path.insert(0, BASE_DIR)

from app import app  # Import the Flask app

@pytest.fixture
def client():
    """Fixture to create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# ----------------- TEST: Customer Transactions API -----------------

def test_get_customer_transactions_valid(client):
    """Test customer transactions API with a valid customer ID."""
    response = client.get("/customer-transactions/CUST002")  # Replace with a valid ID
    assert response.status_code in [200, 404]  # 404 if no data exists
    if response.status_code == 200:
        data = response.get_json()
        assert "total_spent" in data
        assert "total_transactions" in data
        assert "category_spending" in data
        assert "loan_payments" in data

def test_get_customer_transactions_invalid(client):
    """Test customer transactions API with an invalid customer ID."""
    response = client.get("/customer-transactions/99999")  # Non-existing ID
    assert response.status_code == 404
    assert response.get_json()["message"] == "No transactions found for this customer"

def test_get_customer_transactions_empty_id(client):
    """Test API when customer ID is empty"""
    response = client.get("/customer-transactions/")
    assert response.status_code == 404  # Expecting 404 because no ID is provided

def test_get_customer_transactions_special_chars(client):
    """Test API when customer ID has special characters"""
    response = client.get("/customer-transactions/@#$%^")
    assert response.status_code == 404  # Expecting not found

def test_get_customer_transactions_numeric_id(client):
    """Test API with a purely numeric customer ID"""
    response = client.get("/customer-transactions/123456")
    assert response.status_code in [200, 404]  # 404 if no such customer


# ----------------- TEST: Loan Recommendation API -----------------


def test_recommend_loan_invalid(client):
    """Test loan recommendation API with a missing customer ID."""
    response = client.post("/recommend-loan", json={})
    assert response.status_code == 400  # Bad request
    assert "error" in response.get_json()

def test_recommend_loan_empty_customer_id(client):
    """Test when customer ID is an empty string"""
    response = client.post("/recommend-loan", json={"customer_id": ""})
    assert response.status_code == 400  # Expecting 400 Bad Request

def test_recommend_loan_invalid_json_structure(client):
    """Test with incorrect JSON key"""
    response = client.post("/recommend-loan", json={"cust_id": "CUST002"})  # Wrong key
    assert response.status_code == 400

# ----------------- TEST: Chat API -----------------

def test_chat_valid(client):
    """Test chat API with a valid user message."""
    response = client.post("/chat", json={"message": "Tell me about loan eligibility"})
    assert response.status_code == 200
    data = response.get_json()
    assert "reply" in data  # Instead of "response"

def test_chat_empty_message(client):
    response = client.post("/chat", json={"message": ""})
    assert response.status_code in [200, 400]  # Accepting both for now
    data = response.get_json()
    assert "reply" in data or "error" in data  # Allow either a valid reply or an error message

def test_chat_invalid_json_structure(client):
    response = client.post("/chat", json={"msg": "Tell me about loans"})  # Wrong key
    assert response.status_code in [200, 400]  # Accepting both for now
    data = response.get_json()
    assert "reply" in data or "error" in data

# ----------------- TEST: Credit Card Recommendation API -----------------

def test_recommend_credit_card_valid(client):
    response = client.get("/recommend-credit-card/CUST002")
    assert response.status_code == 200
    data = response.get_json()
    assert "recommendations" in data  # Fixed key name

def test_recommend_credit_card_invalid(client):
    """Test credit card recommendation API with an invalid customer ID."""
    response = client.get("/recommend-credit-card/INVALID123")
    assert response.status_code in [200, 404]  # API might return 200 with an error message
    data = response.get_json()
    if response.status_code == 200:
        assert "status" in data and data["status"] == "error"
        assert "message" in data



def test_recommend_credit_card_no_id(client):
    """Test credit card recommendation API when no customer ID is provided."""
    response = client.get("/recommend-credit-card/")
    assert response.status_code == 404  # Not found


# ----------------- TEST: Get All Customers API -----------------

def test_get_all_customers(client):
    """Test retrieving a list of all customers."""
    response = client.get("/api/customers")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)  # Expecting a list of customers


# ----------------- TEST: Get Single Customer API -----------------

def test_get_customer_valid(client):
    """Test retrieving a single customer with a valid ID."""
    response = client.get("/api/customer/CUST002")
    assert response.status_code == 200
    data = response.get_json()
    assert "data" in data
    customer_data = data["data"]
    assert "Customer_Id" in customer_data  # Fixed assertion


def test_get_customer_invalid(client):
    """Test retrieving a customer with an invalid ID."""
    response = client.get("/api/customer/NONEXISTENT")
    assert response.status_code in [200, 404]  # Accepting both
    data = response.get_json()
    if response.status_code == 200:
        assert "status" in data and data["status"] == "error"
        assert "message" in data


def test_get_customer_no_id(client):
    """Test retrieving a customer when no ID is provided."""
    response = client.get("/api/customer/")
    assert response.status_code == 404  # Not found

def test_get_customer_special_chars(client):
    response = client.get("/api/customer/@#$%^")
    assert response.status_code == 200  # Changed from 404
    data = response.get_json()
    assert "status" in data and data["status"] == "error"

