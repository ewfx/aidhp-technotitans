
from flask import Flask, request, jsonify
from invest_now_model import *
import pandas as pd
from flask import jsonify, request
# we integrate api for invest now
from knowledge_base_model import *
import requests
import json
import re
from gtts import gTTS
from flask_cors import CORS
import openai
import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
load_dotenv()
import logging
logging.getLogger("chromadb").setLevel(logging.WARNING)
openai.api_key = os.getenv("openai.api_key")

app = Flask(__name__)
CORS(app)

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # src/backend directory
DATASET_DIR = os.path.join(BASE_DIR, "datasets")

TRANSACTION_FILE = os.path.join(DATASET_DIR, "transaction_history.csv")
CUSTOMER_PROFILE_FILE = os.path.join(DATASET_DIR, "customer_profile.csv")

df = pd.read_csv(TRANSACTION_FILE)  # Now using absolute path

@app.route('/invest-now/<cus_id>', methods=['POST'])
def invest_now(cus_id):
    try:
        # Get parameters from the query string instead of JSON
        risk_level = request.json.get("risk", "Medium")
        max_tenure = int(request.json.get("tenure", 5))
        print("hihihih",risk_level, max_tenure)
        # Determine term preference based on max_tenure
        if max_tenure > 7:
            ten_str = "long"
        elif 3 < max_tenure <= 7:
            ten_str = "medium"
        else:
            ten_str = "short"

        # Load the customer dataset
        file_path = "./datasets/customer_dataset.xlsx"
        try:
            l = pd.read_excel(file_path)
            print(l.head())
            try:
                DATA = classify_investment_insight(l, cus_id)
                print(DATA)
            except:
                DATA = ""
        except Exception as e:
            return jsonify({"error": f"Failed to read customer dataset: {e}"}), 500
        if risk_level == 'low':
            text = f"{risk_level} risk and {ten_str} term"
        else:
            text = f"{risk_level} risk and {ten_str} term and {DATA[0]}"
        L = final_investment_list(text)
        return jsonify({"query": text, "investment_recommendation": L})
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/knowledge_center/<customer_id>', methods=['GET'])
def search(customer_id):
    print(customer_id)
    if not customer_id or customer_id == "None":
        return jsonify({"error": "Invalid customer ID"}), 400

    try:
        print("here")
        search_result = search_results(customer_id)
        print(search_result)
    except Exception as e:
        return jsonify({"error": f"Error: {e}"})
    
    # Return summarized search results
    return search_result

openai.api_base = "https://api.groq.com/openai/v1"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"  

# ✅ Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection(name="credit_cards")

@app.route('/customer-transactions/<customer_id>', methods=['GET'])
def get_customer_transactions(customer_id):
    # Read transaction data
    df = pd.read_csv(TRANSACTION_FILE)
    
    # Convert customer_id to string for safe comparison
    customer_id = str(customer_id)

    # Filter transactions for this customer
    customer_data = df[df['Customer_ID'] == customer_id]

    if customer_data.empty:
        return jsonify({"message": "No transactions found for this customer"}), 404

    # Compute statistics
    total_spent = customer_data['Transaction_Amount'].sum()
    total_transactions = len(customer_data)
    
    # Group by Category and sum Transaction_Amount
    category_spending = customer_data.groupby('Category')['Transaction_Amount'].sum().to_dict()
    
    # Filter loan payments and group by Transaction_Date
    loan_payments = customer_data[customer_data['Transaction_Type'] == 'Loan Payment'].groupby('Transaction_Date')['Transaction_Amount'].sum().to_dict()

    # Response JSON
    response = {
        "total_spent": round(total_spent, 2),
        "total_transactions": total_transactions,
        "category_spending": category_spending,
        "loan_payments": loan_payments
    }

    return jsonify(response)


def suggest_best_card(customer_id):
    """Suggest the best credit card based on customer profile and transaction history."""
    
    # ✅ Load customer profile & transactions
    customer_profile, transaction_data = load_customer_data(customer_id)
    if not customer_profile:
        return {"status": "error", "message": f"No customer data found for {customer_id}."}

    # ✅ Extract transaction insights
    spending_categories, avg_spending, top_payment_method, credit_impact = analyze_transactions(transaction_data)

    # ✅ Retrieve relevant credit cards
    retrieved_cards = []
    for category in spending_categories:
        cards = get_relevant_credit_cards(customer_profile, spending_categories, avg_spending, top_payment_method, credit_impact)
        retrieved_cards.extend(cards)

    # ✅ Remove duplicates
    retrieved_cards = list(set(retrieved_cards))

    if not retrieved_cards:
        return {"status": "error", "message": "No relevant credit cards found."}

    # ✅ Format retrieved cards for prompt
    retrieved_cards_text = "\n".join([f"- {card}" for card in retrieved_cards])

    prompt = f"""
### 🏦 Customer Credit Card Recommendation

#### 📌 Customer Profile:
- **Age:** {customer_profile['Age']}
- **Gender:** {customer_profile['Gender']}
- **Location:** {customer_profile['Location']}
- **Interests:** {customer_profile['Interests']}
- **Preferences:** {customer_profile['Preferences']}
- **Income per Year:** ${customer_profile['Income per year']}
- **Occupation:** {customer_profile['Occupation']}

#### 💳 Spending Behavior:
- **Top Spending Categories:** {spending_categories}
- **Average Transaction Amount:** ${avg_spending:.2f}
- **Preferred Payment Method:** {top_payment_method}
- **Credit Score Impact:** {credit_impact}

---

### 🏆 **Recommended Credit Cards**
Based on the customer’s financial profile and spending habits, here are the top 6 credit card recommendations:

{retrieved_cards_text}

**Return ONLY JSON (without extra text), following this format:**  
```json
{{
  "status": "success",
  "recommendations": [
    {{"card_name": "Credit Card 1", "why_recommended": "Reason 1", "key_benefits": ["Benefit 1", "Benefit 2"]}},
    {{"card_name": "Credit Card 2", "why_recommended": "Reason 2", "key_benefits": ["Benefit 1", "Benefit 2"]}},
    {{"card_name": "Credit Card 3", "why_recommended": "Reason 3", "key_benefits": ["Benefit 1", "Benefit 2"]}}
    {{"card_name": "Credit Card 4", "why_recommended": "Reason 4", "key_benefits": ["Benefit 1", "Benefit 2"]}},
    {{"card_name": "Credit Card 5", "why_recommended": "Reason 5", "key_benefits": ["Benefit 1", "Benefit 2"]}},
    {{"card_name": "Credit Card 6", "why_recommended": "Reason 6", "key_benefits": ["Benefit 1", "Benefit 2"]}}
  ]
}}

""" 
        # ✅ Call AI Model
    response = openai.ChatCompletion.create(
        model="mistral-saba-24b",
        messages=[{"role": "user", "content": prompt}]
        )

    response_text = response["choices"][0]["message"]["content"]

# Remove Markdown code block notation if AI includes it
    response_text = re.sub(r"```json|```", "", response_text).strip()

    try:
        recommendations_json = json.loads(response_text)
    except json.JSONDecodeError:
        recommendations_json = {"status": "error", "message": "AI response was not valid JSON", "raw_response": response_text}
    return recommendations_json

def load_customer_data(customer_id):
    """Fetch customer profile & transaction history from CSV files."""
    profile_df = pd.read_csv(CUSTOMER_PROFILE_FILE)
    transactions_df = pd.read_csv(TRANSACTION_FILE)

    # ✅ Get customer profile
    customer_row = profile_df[profile_df["Customer_Id"] == customer_id]
    if customer_row.empty:
        return None, None
    customer_profile = customer_row.iloc[0].to_dict()

    # ✅ Get customer transaction history
    customer_transactions = transactions_df[transactions_df["Customer_ID"] == customer_id]

    return customer_profile, customer_transactions

def analyze_transactions(transactions_df):
    """Extract insights from customer transaction history."""
    if transactions_df.empty:
        return ["Unknown"], 0, "Unknown", "Neutral"

    # ✅ Identify spending categories (return top 3)
    category_spending = transactions_df.groupby("Category")["Transaction_Amount"].sum()
    top_categories = category_spending.nlargest(min(3, len(category_spending))).index.tolist()

    if not top_categories:
        top_categories = ["General"]  # Fallback category

    # ✅ Calculate average transaction amount
    avg_transaction_amount = transactions_df["Transaction_Amount"].mean()

    # ✅ Identify preferred payment method
    top_payment_method = transactions_df["Payment_Method"].mode()[0] if not transactions_df["Payment_Method"].isna().all() else "Unknown"

    # ✅ Determine credit score impact
    credit_impact = transactions_df["Credit_Score_Impact"].mode()[0] if not transactions_df["Credit_Score_Impact"].isna().all() else "Neutral"

    return top_categories, avg_transaction_amount, top_payment_method, credit_impact

def get_relevant_credit_cards(customer_profile, spending_categories, avg_spending, payment_method, credit_impact):
    """Retrieve relevant credit cards using ChromaDB."""
    
    retrieved_cards = set()  # Use a set to avoid duplicates

    for category in spending_categories:
        query_text = f"""
        Customer spends mostly on {category}, earns {customer_profile['Income per year']}, 
        prefers {customer_profile['Preferences']}, usually pays with {payment_method}, 
        has a credit score impact of {credit_impact}, and makes average transactions of {avg_spending}.
        """
        query_vector = embedder.encode(query_text).tolist()
        results = collection.query(query_embeddings=[query_vector], n_results=3)

        if results["documents"] and results["documents"][0]:
            for doc in results["documents"][0]:
                retrieved_cards.add(doc if doc else "Unknown Card")

    if not retrieved_cards:
        retrieved_cards.add("Standard Cashback Card")  # Default suggestion

    return list(retrieved_cards)

@app.route('/recommend-loan', methods=['POST'])
def recommend_loan():
    data = request.json
    # Check if customer_id is missing or empty
    if not data or "customer_id" not in data or not data["customer_id"].strip():
        return jsonify({"error": "customer_id is required"}), 400  # Return 400 Bad Request
    customer_id = data.get("customer_id")
    return suggest_best_loan(customer_id) 

def suggest_best_loan(customer_id):
    """Suggest the best loan based on customer profile and transaction history."""
    customer_profile, transaction_data = load_customer_data(customer_id)
    if not customer_profile:
        return jsonify({"error": f"No customer data found for {customer_id}."})

    spending_categories, avg_spending, top_payment_method, credit_impact = analyze_transactions(transaction_data)
    retrieved_loans = get_relevant_loans(customer_profile, spending_categories, avg_spending, top_payment_method, credit_impact)
    
    if not retrieved_loans:
        return jsonify({"error": "No relevant loans found."})

    retrieved_loans_str = "\n".join([f"- {loan}" for loan in retrieved_loans])

    prompt = f"""
    ### Customer Loan Recommendation

    #### 📌 Customer Profile:
    - **Age:** {customer_profile['Age']}
    - **Gender:** {customer_profile['Gender']}
    - **Location:** {customer_profile['Location']}
    - **Interests:** {customer_profile['Interests']}
    - **Preferences:** {customer_profile['Preferences']}
    - **Income per year:** ${customer_profile['Income per year']}
    - **Occupation:** {customer_profile['Occupation']}

    #### 📊 Financial Behavior:
    - **Top Spending Category:** {spending_categories}
    - **Average Transaction Amount:** ${avg_spending:.2f}
    - **Preferred Payment Method:** {top_payment_method}
    - **Credit Score Impact:** {credit_impact}

    #### 🏦 Available Loans for Consideration:
    Below are the loans retrieved based on the customer’s financial profile and spending habits:

    {retrieved_loans_str}

    #### 🎯 Task:
    **Recommend the top 6 best loans from the above list.**
    **Provide additional benefits, unique selling points, and why each loan suits the user.**
    **Return the response in JSON format only. Do NOT include any additional text.**
    **There must be 6 loans recommended for sure.**
    
    **Response format:**
    {{
      "loans": [
        {{
          "loan_type": "Loan Name",
          "benefits": "Why this loan is suitable for the user",
          "special_offers": "Any discounts or benefits included",
          "processing_time": "How fast the loan is processed"
        }},
        ...
      ]
    }}
    """

    response = openai.ChatCompletion.create(
        model="mistral-saba-24b",
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract raw response
    response_text = response["choices"][0]["message"]["content"]
    print("DEBUG: Raw OpenAI Response:\n", response_text)  # Debugging

    import re

    # Ensure the response is valid JSON
    try:
        clean_response = re.sub(r"```json|```", "", response_text).strip()  # Remove markdown code block
        loan_recommendations = json.loads(clean_response)
        return jsonify(loan_recommendations)
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse AI response.", "raw_response": response_text})


def get_relevant_loans(customer_profile, spending_categories, avg_spending, payment_method, credit_impact):
    """Retrieve relevant loans based on spending categories using ChromaDB."""
    retrieved_loans = set()

    for category in spending_categories:
        query_text = f"Customer spends mostly on {category}, earns {customer_profile['Income per year']}, usually pays with {payment_method}, has a credit score impact of {credit_impact}, and makes average transactions of {avg_spending}."
        query_vector = embedder.encode(query_text).tolist()
        results = collection.query(query_embeddings=[query_vector], n_results=3)

        if results and "documents" in results and results["documents"]:
            for doc in results["documents"][0]:
                if doc:
                    retrieved_loans.add(doc)

    return list(retrieved_loans) if retrieved_loans else ["Basic Personal Loan"]

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').strip()

    if not user_message:
        return jsonify({"reply": "Please ask a valid question.", "audio_url": None})

    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-saba-24b",
        "messages": [
            {"role": "system", "content": "You are a financial chatbot. Answer only financial-related questions. If the question is unrelated to finance, respond with: 'I can only answer financial-related questions.'"},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 200,
        "temperature": 0.7,
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        response_json = response.json()

        if response.status_code == 200 and "choices" in response_json:
            reply = response_json["choices"][0]["message"]["content"]
        else:
            print("Groq API Error:", response_json)
            reply = "Sorry, I couldn't process your request."

    except Exception as e:
        print("Request Error:", str(e))
        reply = "Sorry, an error occurred while processing your request."

    # Generate TTS audio
    tts = gTTS(text=reply, lang='en')
    audio_filename = "response.mp3"
    tts.save(audio_filename)

    return jsonify({"reply": reply, "audio_url": f"http://localhost:5000/audio/{audio_filename}"})


@app.route('/recommend-credit-card/<customer_id>', methods=['GET'])
def recommend_credit_card(customer_id):
    """API Endpoint: Get recommended credit cards for a given customer."""
    result = suggest_best_card(customer_id)
    return jsonify(result)

def recommend_credit_cards(customer_id):
      # Ensure Flask's app context is available
    result = suggest_best_card(customer_id)
    return result 

def load_login_details():
    df = pd.read_csv(CUSTOMER_PROFILE_FILE)
    
    # Strip spaces from column names to avoid mismatches
    df.columns = df.columns.str.strip()

    # Ensure correct column names match
    if "Customer_Id" in df.columns and "Password" in df.columns:
        customers = df[["Customer_Id", "Password"]].copy()
        customers.rename(columns={"Customer_Id": "username", "Password": "password"}, inplace=True)
        
        # Convert to string to prevent type mismatches
        customers["username"] = customers["username"].astype(str)
        customers["password"] = customers["password"].astype(str)

        return customers.to_dict(orient="records")
    else:
        print("Error: Column names do not match!")
        return []

@app.route('/api/customers', methods=['GET'])
def get_customers():
    return jsonify(load_login_details())

@app.route('/api/customer/<customer_id>', methods=['GET'])
def get_customer_details(customer_id):
    df = pd.read_csv(CUSTOMER_PROFILE_FILE)
    user_data = df[df['Customer_Id'] == customer_id].to_dict(orient='records')
    if user_data:
        user_data[0].pop('Password', None)  # Remove password field
        return jsonify({"status": "success", "data": user_data[0]})
    else:
        return jsonify({"status": "error", "message": "User not found"})

if __name__ == '__main__':
    app.run(debug=True)
