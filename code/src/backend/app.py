from flask import Flask, request, jsonify
from invest_now_model import *
import pandas as pd
from flask import jsonify, request
# we integrate api for invest now
from knowledge_base_model import *
app = Flask(__name__)

# Home Route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the dummy Flask API!"})

@app.route('/invest-now/<cus_id>', methods=['POST'])
def invest_now(cus_id):
    try:
        # Get parameters from the query string instead of JSON
        risk_level = request.json.get("risk_level", "Medium")
        max_tenure = int(request.json.get("max_tenure", 5))

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

        text = f"{risk_level} risk and {ten_str} term and {DATA[0]}"
        L = final_investment_list(text)
        return jsonify({"query": text, "investment_recommendation": L})
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/knowledge_center/<customer_id>', methods=['GET'])
def search(customer_id):
    if not customer_id or customer_id == "None":
        return jsonify({"error": "Invalid customer ID"}), 400

    try:
        search_result = search_results(customer_id)
        print(search_result)
    except Exception as e:
        return jsonify({"error": f"Error: {e}"})
    
    # Return summarized search results
    return search_result


if __name__ == '__main__':
    app.run(debug=True)
