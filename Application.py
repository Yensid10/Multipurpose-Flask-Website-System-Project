from flask import Flask, render_template, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb+srv://Theamzingu:Socr%40tis123@teamproject14.nnzfaib.mongodb.net/test')

db = client["Kitchen"]
collection = db["order_queue"]


@app.route('/kitchen')
def kitchen():
    orders = list(collection.find({}, {'_id': False}))
    for order in orders:
        order['items'] = ', '.join(order['items'])
    return render_template('kitchen.html', orders=orders)

@app.route('/order_queue_data')
def order_queue_data():
    orders = list(collection.find({}, {'_id': False}))
    for order in orders:
        order['items'] = ', '.join(order['items'])
    return jsonify(orders)

if __name__ == '__main__':
    app.run(debug=True)