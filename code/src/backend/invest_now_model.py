import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
import json
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Current file directory
DATASET_PATH = os.path.join(BASE_DIR, '..')
# Open and read the JSON file
with open('datasets/investment_data.json', 'r') as f:
    documents = json.load(f)

# Global INstance declaration for semantic search engine using faiss
# Load pre-trained transformer model for encoding documents
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# model_dir = 'invest_now_model'
# tokenizer = AutoTokenizer.from_pretrained(model_dir)
# model = AutoModel.from_pretrained(model_dir)
# faiss_index_file = 'invest_now_model.index'
# index = faiss.read_index(faiss_index_file)

def encode_documents(documents):
   
    inputs = tokenizer([doc["content"] for doc in documents], padding=True, truncation=True, return_tensors="pt", max_length=512)
   
    with torch.no_grad():  # Disable gradient calculations
        embeddings = model(**inputs).last_hidden_state.mean(dim=1).cpu().numpy()  
    return embeddings

document_embeddings = encode_documents(documents)

index = faiss.IndexFlatL2(document_embeddings.shape[1])
index.add(np.array(document_embeddings))

def encode_query(query):
    inputs = tokenizer(query, padding=True, truncation=True, return_tensors="pt", max_length=512)
    with torch.no_grad():  # Disable gradient calculations
        query_embedding = model(**inputs).last_hidden_state.mean(dim=1).cpu().numpy()
    return query_embedding

def retrieve_documents(query, top_k=10):
    query_embedding = encode_query(query)
    D, I = index.search(query_embedding, top_k)  
    return [documents[i] for i in I[0]]


def final_investment_list(query,n = 10):
    relevant_docs = retrieve_documents(query,n)
    L = []
    for doc in relevant_docs:
        L.append({"title":doc['title'], "website":doc['website'],"about":doc['about'], "content":doc['content']})
        # print(f"Title: {doc['title']}\n")
    return L

def classify_investment_insight(customer_data, customer_id):
    # Define a list of keywords related to investment and financial interests
    investment_keywords = ["stocks", "bonds", "investments", "retirement", "savings", "home loan", "mortgage", "insurance", "mutual funds"]
    
    # Filter the dataset to focus only on the given customer_id
    customer_row = customer_data[customer_data['Customer_Id'] == customer_id]
    print(customer_row)
    # Initialize a list to hold the insights
    insights = []
    
    if not customer_row.empty:
        # Combine Interests and Preferences for analysis
        combined_text = customer_row.iloc[0]['Interests'].lower() + " " + customer_row.iloc[0]['Preferences'].lower()
        
        # Check for the presence of investment-related keywords
        matched_keywords = [keyword for keyword in investment_keywords if keyword in combined_text]
        
        if matched_keywords:
            insight = f"Customer {customer_id} - {', '.join(matched_keywords)}."
            insights.append(insight)
        else:
            insights.append("")  # If no match, append an empty string
    else:
        insights.append("")
    
    return insights


# final_investment_list("high risk and long term")