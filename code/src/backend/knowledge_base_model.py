import pandas as pd
from serpapi import GoogleSearch
from flask import jsonify
import os
import logging
# Function to search Google using SerpAPI
from dotenv import load_dotenv
load_dotenv()
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

def serpapi_search(query, search_type="web", num_results=5):
    """
    Perform a Google search using SerpAPI and return results.
    
    Args:
        query (str): The search query.
        search_type (str): Type of search - "web", "videos", or "pdfs".
        num_results (int): Number of search results to return.
        
    Returns:
        list: Titles and URLs of search results.
    """
    # Hardcoded API Key (replace with your key or env variable if required)
    # SERPAPI_API_KEY = SERPAPI_API_KEY
    if not SERPAPI_API_KEY:
        logging.error("SerpAPI API Key not found.")
        return [("Error", "No API key found. Please configure your SERPAPI_API_KEY.")]

    params = {
        "q": query,
        "hl": "en",
        "num": num_results,
        "api_key": SERPAPI_API_KEY
    }

    # Modify search parameters based on the search type
    if search_type == "videos":
        params["tbm"] = "vid"
    elif search_type == "pdfs":
        params["q"] += " filetype:pdf"

    search = GoogleSearch(params)
    results = search.get_dict()

    output = []
    if search_type in ["web", "pdfs"]:
        for result in results.get("organic_results", []):
            output.append((result.get("title"), result.get("link")))
    elif search_type == "videos":
        for video in results.get("video_results", []):
            output.append((video.get("title"), video.get("link")))

    return output

# Main function that performs the search for a given customer
def search_results(customer_id):
    """
    Perform searches based on a customer's preferences and return relevant finance-related results.
    
    Args:
        customer_id (str): The customer ID whose preferences are to be searched.
        
    Returns:
        dict: Dictionary containing article, video, and PDF search results.
    """
    customer_data = pd.read_excel('datasets/customer_dataset.xlsx')
    try:
        customer_interests = customer_data[customer_data['Customer_Id'] == customer_id]['Preferences'].values[0]
        article_results = serpapi_search(f"Finance and Banking {customer_interests}", search_type="web")
        video_results = serpapi_search(f"Finance and Banking {customer_interests}", search_type="videos")
        pdf_results = serpapi_search(f"Finance and Banking {customer_interests}", search_type="pdfs")
        
        return jsonify({
            "Articles": article_results,
            "Videos": video_results,
            "PDFs": pdf_results
        })
    except:
        print("here")
        article_results = serpapi_search(f"Finance and Banking wells fargo", search_type="web")
        video_results = serpapi_search(f"Finance and Banking wells fargo youtube", search_type="videos")
        pdf_results = serpapi_search(f"Finance and Banking wells fargo", search_type="pdfs")
    
        return jsonify({
                "Articles": article_results,
                "Videos": video_results,
                "PDFs": pdf_results
            })
    

