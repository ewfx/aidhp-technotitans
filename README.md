# 🚀 Project Name

## 📌 Table of Contents
- [Introduction](#-introduction)
- [Demo](#-demo)
- [Inspiration](#-inspiration)
- [What It Does](#-what-it-does)
- [How We Built It](#-how-we-built-it)
- [Challenges We Faced](#-challenges-we-faced)
- [How to Run](#-how-to-run)
- [Tech Stack](#-tech-stack)
- [Team](#-team)

---

## 🎯 Introduction
Our Hyper-Personalized Financial Recommendation System integrates advanced AI and machine learning to provide deeply individualized financial solutions that enhance user experience and drive business growth. The system features a multi-modal chatbot, offering text and voice-based interactions for instant, personalized financial guidance, making it accessible to all users. Personalized loan recommendations tailor loan options to users’ financial profiles and behavior, reducing rejection rates and increasing conversion. The customized content recommendation engine delivers relevant financial articles, videos, and tips, keeping users engaged and fostering long-term loyalty. The AI-driven credit card recommendation system suggests credit cards that maximize rewards based on individual spending habits, further enhancing satisfaction. Additionally, the churn prediction model analyzes user data to proactively identify at-risk customers and deliver targeted offers or discounts, boosting retention. By combining these features into one integrated platform, the system provides real-time, relevant, and actionable recommendations that improve customer satisfaction, increase conversions, and promote long-term engagement.

## 🎥 Demo
📹 [Video Demo](https://github.com/ewfx/aidhp-technotitans/tree/main/artifacts/demo) (if applicable)  


## 💡 Inspiration
The inspiration for this project stemmed from the growing demand for more personalized, user-centric services in the financial industry. Many users struggle with generic recommendations from traditional financial systems, leading to a lack of engagement and missed opportunities. We wanted to create a solution that goes beyond surface-level personalization and dives deeper into user behaviors, preferences, and needs. By harnessing the power of AI and machine learning, we aimed to build a hyper-personalized recommendation system that delivers tailored financial solutions, improving user engagement, decision-making, and satisfaction.

## ⚙️ What It Does
Our Hyper-Personalized Recommendation System transforms the way users interact with their finances by offering real-time, AI-driven recommendations that are uniquely tailored to each user. Key features include:

- Personalized Loan Recommendations: The system identifies suitable loan options based on users' financial profiles, spending behavior, and lifestyle patterns.
- Customized Content Delivery: Users receive financial content (articles, videos, etc.) that aligns with their interests and financial goals.
- AI-driven Finance Chatbot: Offers instant, personalized support and financial advice through both text and voice interactions, making it accessible for all users.
- Personalized Investment Suggestions: Recommends investment opportunities based on user risk profiles and financial objectives.
- User Activity Dashboard: Provides comprehensive spending analysis and insights, allowing users to make more informed financial decisions.
- Churn Prediction & Mitigation: Analyzes user data to predict potential churn and sends personalized recommendations to enhance retention.
- AI-driven Credit Card Recommendations: Suggests credit cards that maximize rewards based on the user's spending patterns.

## 🛠️ How We Built It

We combined cutting-edge technologies to deliver a seamless, AI-driven recommendation system:

- Backend: Built with Python, leveraging FAISS for efficient similarity search and finally RAG models, SerpAPI and Open AI API for recommendation systems 
- Frontend: Angular for a responsive and user-friendly interface, with Bootstrap for styling and Chart.js for displaying financial data and insights.
- AI: OpenAI API for natural language processing in the chatbot and DistilBERT for personalized investment suggestions.
- Automation: pywin32 for automating personalized email communication and machine learning models to predict churn.

## 🚧 Challenges We Faced
1. Technical Challenges:
   - Ensuring real-time, accurate personalization with minimal latency required fine-tuning our AI models and integrating them seamlessly into the system.
   - Developing a scalable system capable of processing and analyzing large amounts of data that too in a short span of time.
     
2. Non-Technical Challenges:
   - Striking a balance between offering personalized recommendations with limited resource and ensuring user privacy by not providing user's sensitive data to models.
   - Ensuring not to overwhelm users with too many recommendations or content, which could lead to decision fatigue

## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/ewfx/aidhp-technotitans.git
   ```
2. Install dependencies  
   Terminal 1 (Frontend)
   ```sh
   cd code/src/frontend
   ```
   ```sh
   npm install  
   ```
   Terminal 2 (Backend)
   ```sh
   cd code/src/backend
   ```
   ```sh
   pip install -r requirements.txt (for Python)
   ```
4. Run the project
   Terminal 1 (Frontend)
   ```sh
   cd code/src/frontend
   ```
   ```sh
   npm start  # or python app.py
   ```
   Terminal 2 (Backend)
   ```sh
   cd code/src/backend
   ```
   ```sh
   python app.py
   ```
   Terminal 3 (Scheduler)
   ```sh
   cd code/src/backend
   ```
   ```sh
   python churn_predictions.py
   ```

## 🏗️ Tech Stack
- 🔹 Frontend: Angular
- 🔹 Backend: Python
- 🔹 Other: OpenAI API / ChromaDB / FAISS / SerpAPI

## 👥 Team
- **Anjaneyulu Macherla** - [GitHub](https://github.com/amacherla) | [LinkedIn](https://www.linkedin.com/in/anjaneyulu-macherla/)
- **Aditilakshmi S** - [GitHub](https://github.com/The-coderlearner) | [LinkedIn](https://in.linkedin.com/in/aditi-lakshmi-s-47089b226)
- **Bhavaneda Subramani** - [GitHub](https://github.com/bhavaneda) | [LinkedIn](https://www.linkedin.com/in/bhavaneda)
- **Valarmathi Balakrishna** - [GitHub](https://github.com/valar03) | [LinkedIn](https://www.linkedin.com/in/valarmathi-b-1b2286227/)
