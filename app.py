import pickle
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

#Load model saved in model.pkl
model=pickle.load(open('model.pkl','rb'))

#load shops_data which have all shops, it is used for merging with another table
shops = pd.read_csv('shops_data.csv')
shops = shops[['shop_id', 'shop_category', 'shop_city']]

#load items_data which have all shops, it is used for merging with another table
items = pd.read_csv('items_data.csv')
items = items[['item_id', 'item_category_id', 'name2', 'name3','item_price', 'subtype_code', 'type_code']]

#Index homepage
@app.route('/')
def home():
    return render_template('index.html')

"""
ValuePredictor function return predicted value for a single tuple
"""
def ValuePredictor(values):
    #Created tuple column name
    keys = ["shop_id", "item_id", "month", "year"]
    dict_ = dict(zip(keys, values))
    persistent_value = pd.DataFrame.from_dict(dict_, orient='index').T
    
    persistent_value['date_block_num'] = (persistent_value['year'] - 2013) * 12 + persistent_value['month'] - 1
    days = pd.Series([31,28,31,30,31,30,31,31,30,31,30,31])
    persistent_value["days"] = persistent_value["month"].map(days).astype(np.int8)

    persistent_value=pd.merge(persistent_value,items,on=['item_id'],how='inner')
    persistent_value=pd.merge(persistent_value,shops,on=['shop_id'],how='inner')
    persistent_value.sort_values(["date_block_num", "shop_id", "item_id"], inplace = True )
    persistent_value=persistent_value.reset_index(drop=True)
    
    test_tuple = persistent_value[['date_block_num', 'shop_id', 'item_id', 'shop_category', 'shop_city',
       'item_category_id', 'name2', 'name3', 'subtype_code', 'type_code', 'days', 'month', 'year',
       'item_price', ]]
    return abs(model.predict(test_tuple))



@app.route('/predict',methods=['POST'])
def predict():
    int_features = [int(x) for x in request.form.values()]
    prediction = ValuePredictor(int_features)
    return render_template('index.html', prediction_text='Predicted Sale is: {}'.format(prediction))

@app.route('/api',methods=['POST'])
def api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    
    int_features = list(data.values())
    prediction = ValuePredictor(int_features)

    print("data:", data)
    print("Prediction:", prediction)

    output = str(prediction[0])
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)