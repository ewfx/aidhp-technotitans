import chromadb
import pandas as pd
from sentence_transformers import SentenceTransformer

# Load dataset
csv_path = "credit_card_dataset.csv"  # Make sure this file exists in your directory
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
