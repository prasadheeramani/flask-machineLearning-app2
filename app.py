# from flask import Flask, render_template, request
from flask import Flask, request, jsonify,render_template

import pandas as pd
import numpy as np
# from sklearn.externals import joblib

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            ID = int(request.form['ID'])
            Shop_ID = int(request.form['Shop_ID'])
            Item_ID = int(request.form['Item_ID'])
            pred_args = [ID, Shop_ID, Item_ID]
            print(pred_args)

        except valueError:
            return "Please check values"



# @app.route('/predict', methods=['GET', 'POST'])
# def predict():
#     if request.method == 'POST':
#         try:
#             ID = int(request.form['ID'])
#             Shop_ID = int(request.form['Shop_ID'])
#             Item_ID = int(request.form['Item_ID'])
#             pred_args = [ID, Shop_ID, Item_ID]
#             pred_args_array = np.array(pred_args)
#             pred_args_array = pred_args_array.reshape((1,-1))

#             model = open('model.pkl', 'rb')
#             ml_model = joblib.load(model)

#             model_prediction = ml_model.predict(pred_args_array)
            
#         except valueError:
#             return "Please check if all values are correct."

#     return render_template('predict.html', prediction=model_prediction)


if __name__ == "__main__":
    app.run()