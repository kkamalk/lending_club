from flask import Flask, jsonify, request
import joblib
from functions import *

app = Flask(__name__)

interest_rate_regressor = joblib.load("lightgbm_model_v1.pkl")


@app.route('/loan/interest', methods=['POST'])
def loan_interest():
    content = request.json

    # Create the interest_rate_prediction_inputs DataFrame with modified column names
    interest_rate_prediction_columns = [
        'emp_length_1 year',
        'emp_length_10+ years',
        'emp_length_2 years',
        'emp_length_3 years',
        'emp_length_4 years',
        'emp_length_5 years',
        'emp_length_6 years',
        'emp_length_7 years',
        'emp_length_8 years',
        'emp_length_9 years',
        'emp_length_< 1 year',
        'purpose_car',
        'purpose_credit_card',
        'purpose_debt_consolidation',
        'purpose_educational',
        'purpose_home_improvement',
        'purpose_house',
        'purpose_major_purchase',
        'purpose_medical',
        'purpose_moving',
        'purpose_other',
        'purpose_renewable_energy',
        'purpose_small_business',
        'purpose_vacation',
        'purpose_wedding',
        'annual_inc',
        'fico_range_low',
        'fico_range_high',
        'revol_util',
        'loan_amnt',
        'dti',
        'inq_last_6mths',
        'pub_rec',
        'pub_rec_bankruptcies',
        'open_acc',
        'total_acc',
        'credit_line_year',
        'issue_month',
        'credit_line_month'
    ]

    # Convert column values to float
    for column in ['annual_inc', 'fico_range_low', 'fico_range_high', 'revol_util', 'loan_amnt',
                   'dti', 'inq_last_6mths', 'pub_rec', 'pub_rec_bankruptcies', 'open_acc',
                   'total_acc', 'credit_line_year', 'issue_month', 'credit_line_month']:
        content[column] = float(content[column])

    # Create the new DataFrame with the request content
    new_inputs = pd.DataFrame(data=[content], columns=interest_rate_prediction_columns)

    # Initialize interest_rate_prediction_inputs if it is not already initialized
    if 'interest_rate_prediction_inputs' not in globals():
        interest_rate_prediction_inputs = pd.DataFrame(columns=interest_rate_prediction_columns)

    # Concatenate the new DataFrame with the existing interest_rate_prediction_inputs DataFrame
    interest_rate_prediction_inputs = pd.concat([interest_rate_prediction_inputs, new_inputs], ignore_index=True)

    interest_rate_res = interest_rate_regressor.predict(interest_rate_prediction_inputs)
    interest_rate = round(interest_rate_res[0], 2)

    return jsonify({
        'interest_rate': interest_rate,
    })



# ...


@app.route('/')
def index():
    return 'Welcome to the Loan Status API'

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)


