import chromadb
import pandas as pd
from sentence_transformers import SentenceTransformer
import os

# Load dataset
csv_path = "datasets/credit_card_dataset.csv"  # Make sure this file exists in your directory
df = pd.read_csv(csv_path)

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="chroma_db")  # Stores embeddings persistently
collection = chroma_client.get_or_create_collection(name="credit_cards")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")  # Efficient transformer for text embeddings

# Insert credit card information into ChromaDB
for idx, row in df.iterrows():
    card_name = row["Name"]
    card_details = f"Category: {row['Category']}, Interest Rate: {row['Interest_Rate (%)']}%, Annual Fee: ${row['Annual_Fee ($)']}, Cashback: {row['Cashback (%)']}%, Rewards: {row['Rewards']}, Minimum Income: ${row['Min_Income ($)']}, Best For: {row['Best_For']}"
    
    # Generate embeddings
    embedding = model.encode(card_details).tolist()
    
    # Store in ChromaDB
    collection.add(
        ids=[str(idx)],  # Unique ID
        embeddings=[embedding],
        metadatas=[{"Name": card_name, "Details": card_details}]
    )

print("✅ Credit card embeddings stored in ChromaDB!")

# ✅ Load dataset
loan_csv_path = "datasets/loan.csv"
if not os.path.exists(loan_csv_path):
    raise FileNotFoundError(f"Dataset file not found: {csv_path}")
loan_df = pd.read_csv(loan_csv_path)

# ✅ create collection to store loan data
collection = chroma_client.get_or_create_collection(name="loans")

existing_ids = set(collection.get()["ids"])  # Fetch existing IDs

# ✅ Insert loan information into ChromaDB
for idx, row in loan_df.iterrows():
    loan_name = row["LoanID"]
    if str(idx) in existing_ids:
        continue  # Skip duplicate loan IDs
    loan_details = (
        f"Type: {row['LoanType']}, Interest Rate: {row['InterestRate']}%, "
        f"Min Credit Score: {row['MinCreditScore']}, Max Loan Amount: ${row['MaxLoanAmount']}, "
        f"Repayment Period: {row['RepaymentPeriod']} months, Income Requirement: ${row['IncomeRequirement']}, "
        f"Employment Type: {row['EmploymentType']}, Risk Level: {row['RiskLevel']}, "
        f"Processing Time: {row['ProcessingTime']} days, Early Repayment Benefits: {row['EarlyRepaymentBenefits']}, "
        f"Special Offers: {row['SpecialOffers']}, Flexible Repayment Options: {row['FlexibleRepaymentOptions']}, "
        f"User-friendly Description: {row['LoanDescription']}"
    )
    
    # Generate embeddings
    embedding = model.encode(loan_details).tolist()
    
    # Store in ChromaDB
    collection.add(
        ids=[str(idx)],
        embeddings=[embedding],
        metadatas=[{"LoanID": loan_name, "Details": loan_details}]
    )

print("✅ Loan embeddings stored in ChromaDB!")