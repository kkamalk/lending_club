import requests
import json

url = 'http://localhost:5000/loan/status'
payload = {
    "annual_inc": 50000,
    "emp_length": 2,
    "purpose": "debt_consolidation",
    "fico_range_low": 700,
    "fico_range_high": 710,
    "dti": 25,
    "loan_amnt": 10000
}

response = requests.post(url, json=payload)
print(response.status_code)  # Print the HTTP status code
print(response.text)  # Print the response content as text
