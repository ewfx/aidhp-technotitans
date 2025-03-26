import pandas as pd
import numpy as np
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from win32com.client import Dispatch
import logging
import pythoncom  # Required for COM initialization
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from app import *
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def predict_churn():
    """
    Perform churn prediction based on transaction data and save results to CSV.
    """
    logging.info("Running churn prediction...")

    # Load transaction data (path adjusted)
    data = pd.read_csv("datasets/transaction_history.csv")

    # Convert transaction date to datetime format
    data['Transaction_Date'] = pd.to_datetime(data['Transaction_Date'], format="%d-%m-%Y")

    # Identify and classify inactivity patterns
    def detect_inactivity_pattern(transaction_dates):
        sorted_dates = transaction_dates.sort_values()
        inactivity_periods = (sorted_dates.diff().dt.days > 60).sum()  # Count inactivity gaps over 60 days
        return 1 if inactivity_periods > 1 else 0

    # Add churn based on inactivity patterns
    data['Churn_Inactivity'] = data.groupby('Customer_ID')['Transaction_Date'].transform(detect_inactivity_pattern)

    # Aggregate customer transaction data
    df_agg = data.groupby('Customer_ID').agg({
        'Transaction_ID': 'count',
        'Transaction_Amount': 'mean',
        'Transaction_Date': lambda x: (x.max() - x.min()).days,
        'Outstanding_Debt': 'mean',
        'Income_to_Expense_Ratio': 'mean',
        'Churn_Inactivity': 'max'
    }).reset_index()

    # Rename columns for better understanding
    df_agg.columns = [
        'Customer_ID', 'Total_Transactions', 'Avg_Transaction_Amount', 'Transaction_Days_Span',
        'Avg_Outstanding_Debt', 'Avg_Income_Expense_Ratio', 'Churn_Inactivity'
    ]

    # Assign churn labels based on inactivity or transactional features
    df_agg['Predicted_Churn'] = np.where(
        (df_agg['Total_Transactions'] < 10) & (df_agg['Avg_Outstanding_Debt'] > 15000) |
        (df_agg['Churn_Inactivity'] == 1),
        1, 0
    )

    # Prepare additional customer features like rewards and credit score
    df_features = data.groupby('Customer_ID').agg({
        'Rewards_Earned': 'sum',
        'Credit_Score_Impact': lambda x: x.mode()[0] if not x.empty else 'Unknown'
    }).reset_index()

    # Merge features with aggregated customer data
    final_df = pd.merge(df_agg, df_features, on='Customer_ID', how='left')

    # Display churned customers (for log purpose)
    churned_customers = final_df[final_df['Predicted_Churn'] == 1]
    logging.info("List of customers predicted to churn:")
    logging.info(churned_customers[['Customer_ID', 'Total_Transactions', 'Avg_Outstanding_Debt', 'Churn_Inactivity']])

    # Save churn predictions to CSV
    final_df.to_csv("datasets/Mllm_churn_predictions.csv", index=False)
    logging.info("Churn predictions saved to 'datasets/Mllm_churn_predictions.csv'.")


def check_and_send_churn_alert():
    """
    Function to check customer churn and send emails to churned customers using Outlook.
    """
    logging.info("Running weekly churn check...")

    # Load churn prediction CSV and customer dataset Excel
    churn_df = pd.read_csv("datasets/Mllm_churn_predictions.csv")
    customer_dataset = pd.read_excel("datasets/customer_dataset.xlsx")

    # Identify churned customers and filter their details
    churned_customer_ids = churn_df[churn_df['Predicted_Churn'] == 1]['Customer_ID'].tolist()

    if churned_customer_ids:
        # Filter churned customers from the customer dataset
        churned_customers = customer_dataset[customer_dataset['Customer_Id'].isin(churned_customer_ids)]

        # Loop through churned customers and send an email to each one
        for _, row in churned_customers.iterrows():
            customer_email = row['Email']
            customer_name = row['Customer_Id']
            interests = row['Interests']
            # try:
            #     recommendation = suggest_best_card(customer_name)
            #     print(recommendation)
            #     send_outlook_email(customer_email, customer_name, interests, recommendation)

            # except:
            send_outlook_email(customer_email, customer_name, interests,customer_name)    # BHAVANEDAAA - send_outlook_email(customer_email, customer_name, interests, suggest_best_card(customer_name)) POTTU RUN PANNAU
    else:
        logging.info("No churn detected this week.")


def send_outlook_email(email, name, interests, customer_id):
    """
    Sends an email using Outlook to churned customers with personalized suggestions.
    """
    pythoncom.CoInitialize() 
    outlook = Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)

    # Fetch the recommended credit card dynamically
    recommendation = recommend_credit_cards(customer_id)
    recommendation = format_recommendation_email(recommendation)
    # Configure recipient, subject, and message with enhanced CSS styling
    mail.To = email
    mail.Subject = "We Miss You! Personalized Recommendations Inside"
    mail.HTMLBody = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    padding: 20px;
                    color: #333;
                }}
                .email-container {{
                    background-color: #fff;
                    border-radius: 10px;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                    padding: 20px;
                    max-width: 600px;
                    margin: auto;
                }}
                .header {{
                    background-color: red;
                    color: white;
                    padding: 10px 0;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .button {{
                    display: inline-block;
                    padding: 10px 20px;
                    font-size: 16px;
                    font-weight: bold;
                    text-align: center;
                    color: white;
                    background-color: red;
                    text-decoration: none;
                    border-radius: 5px;
                    margin-top: 20px;
                }}
                .footer {{
                    font-size: 12px;
                    text-align: center;
                    color: #777;
                    padding-top: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <h2>We Miss You, {name}!</h2>
                </div>
                <p>We noticed that you haven't been engaging with us as much lately, and we wanted to check in.</p>
                <p>As someone with an interest in <strong>{interests}</strong>, we want to ensure you're getting the most out of your experience with us.</p>

                <p><strong>Personalized CreditCard Suggestions:</strong></p>
                <p>{recommendation}</p>

                <a href="https://www.wellsfargo.com" class="button">Re-Engage with Us</a>

                <div class="footer">
                    <p>The wellsfargo Team | Contact Us: aditilakshmis@outlook.com</p>
                </div>
            </div>
        </body>
        </html>
        """
    mail.Send()
    logging.info(f"Churn alert email sent to {email}!")

def format_recommendation_email(recommendation):
    if recommendation["status"] != "success":
        return "<p>We couldn't find any credit card recommendations at this time.</p>"

    email_content = ""
    
    for idx, card in enumerate(recommendation["recommendations"], start=1):
        email_content += f"""
        <p><strong>🔹 {idx}. {card['card_name']}</strong><br>
        <em>🏆 Why Recommended:</em> {card['why_recommended']}<br>
        <em>✅ Key Benefits:</em></p>
        <ul>
        """
        for benefit in card["key_benefits"]:
            email_content += f"<li>{benefit}</li>"
        email_content += "</ul>"

    return email_content



def schedule_cron_job():
    """
    Schedules the churn prediction and email job to run weekly.
    """
    scheduler = BlockingScheduler()
    scheduler.add_job(lambda: (predict_churn(), check_and_send_churn_alert()), 'cron', day_of_week='wed', hour=21, minute=10) 
    
    logging.info("Scheduler set up: Churn detection job will run every Wednesday.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Scheduler stopped.")


if __name__ == "__main__":
    schedule_cron_job()