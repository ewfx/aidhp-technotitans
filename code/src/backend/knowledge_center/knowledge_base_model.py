from flask import Flask, request, jsonify
import pandas as pd
from transformers import pipeline, PegasusForConditionalGeneration, PegasusTokenizer
import requests
from bs4 import BeautifulSoup
import torch

app = Flask(__name__)

# Load datasets
social_media_data = pd.read_excel("/mnt/data/social_media_sentiment_dataset.xlsx")
customer_data = pd.read_excel("/mnt/data/customer_dataset.xlsx")

# Initialize Hugging Face sentiment analysis and intent classification pipelines
sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
intent_pipeline = pipeline("text-classification", model="bhadresh-savani/bert-base-go-emotion", return_all_scores=True)

# Initialize Pegasus summarization model
model_name = "google/pegasus-xsum"
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)

# Google Scraping Function
def google_search(query, num_results=5):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        search_url = f"https://www.google.com/search?q={query}&num={num_results}"
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        results = []
        for item in soup.find_all("div", class_="tF2Cxc"):
            title = item.find("h3").text if item.find("h3") else "No Title"
            link = item.find("a")['href'] if item.find("a") else "No Link"
            results.append((title, link))

        return results

    except Exception as e:
        print(f"Error scraping Google: {e}")
        return []

# Summarization function
def summarize_text(text):
    batch = tokenizer([text], truncation=True, padding="longest", return_tensors="pt").to(device)
    translated = model.generate(**batch)
    return tokenizer.batch_decode(translated, skip_special_tokens=True)[0]

# @app.route('/search', methods=['GET'])
def search_results():
    customer_id = input()

    # Validate customer ID
    if customer_id is None or not customer_id.isdigit():
        return jsonify({"error": "Invalid customer ID"}), 400

    customer_id = int(customer_id)
    if customer_id >= len(customer_data):
        return jsonify({"error": "Customer ID not found"}), 404

    # Get customer preferences
    customer_interests = customer_data.iloc[customer_id]['Preferences']

    # Perform searches based on customer preferences
    article_results = google_search(f"Finance and Banking {customer_interests}")
    video_results = google_search(f"Finance and Banking {customer_interests} filetype:mp4")
    pdf_results = google_search(f"Finance and Banking {customer_interests} filetype:pdf")

    # Summarize and prepare the results
    summarized_articles = [{"title": summarize_text(title), "url": url} for title, url in article_results]
    summarized_videos = [{"title": summarize_text(title), "url": url} for title, url in video_results]
    summarized_pdfs = [{"title": summarize_text(title), "url": url} for title, url in pdf_results]

    # Return the search results
    return jsonify({
        "articles": summarized_articles,
        "videos": summarized_videos,
        "pdfs": summarized_pdfs
    })
