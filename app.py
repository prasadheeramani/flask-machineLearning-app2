import pickle
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
# model = pickle.load(open('model.pkl', 'rb'))

model=pickle.load(open('model.pkl','rb'))
shops = pd.read_csv('shops_data.csv')
shops = shops[['shop_id', 'shop_category', 'shop_city']]

items = pd.read_csv('items_data.csv')
items = items[['item_id', 'item_category_id', 'name2', 'name3',
       'item_price', 'subtype_code', 'type_code']]

@app.route('/')
def home():
    return render_template('index.html')

def ValuePredictor(values):
    keys = ["date_block_num", "shop_id", "item_id"]
#     values = [10,20,30]

    dict_ = dict(zip(keys, values))

#     print(dict_)
    train = pd.DataFrame.from_dict(dict_, orient='index').T
    
    
    train=pd.merge(train,items,on=['item_id'],how='inner')
    train=pd.merge(train,shops,on=['shop_id'],how='inner')
    train.sort_values(["date_block_num", "shop_id", "item_id"], inplace = True )
    train=train.reset_index(drop=True)

    train["month"] = train["date_block_num"] % 12
    days = pd.Series([31,28,31,30,31,30,31,31,30,31,30,31])
    train["days"] = train["month"].map(days).astype(np.int8)
    train["year"] = 2013+(train["date_block_num"]/12).astype(np.int16)
    train['month']=train['month']+1
    
    t = train[['date_block_num', 'shop_id', 'item_id', 'shop_category', 'shop_city',
       'item_category_id', 'name2', 'name3', 'subtype_code', 'type_code', 'days', 'month', 'year',
       'item_price', ]]
    return model.predict(t)




@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [int(x) for x in request.form.values()]
    # final_features = [np.array(int_features)]

    print(int_features)

    prediction = ValuePredictor(int_features)
    print(prediction)

    # output = round(prediction[0], 2)
    # print(output)

    return render_template('index.html', prediction_text='Prediction is: {}'.format(prediction))


if __name__ == "__main__":
    app.run(debug=True)