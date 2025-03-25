from invest_now_model import *
import pandas as pd

# we integrate api for invest now

def invest_now(cus_id = "CUST2025B"):
    risk_level = input("Risk level: ")
    max_tenure = int(input("Tenure: "))
    if(max_tenure >7):
        ten_str = "long"
    elif (max_tenure<=7 or max_tenure>3):
        ten_str = "medium"
    else:
        ten_str = "short"
    file_path = '../datasets/customer_dataset.xlsx'
    try:
        l = pd.read_excel(file_path) 
        DATA = classify_investment_insight(l, cus_id)
    except:
        DATA = ""
    text = str(risk_level) + " risk and " + ten_str + " term" + " and " + DATA[0]
    print(text)
    op = final_investment_list(text)
    print(op)
    return op
invest_now()