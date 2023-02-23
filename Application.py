import datetime
from flask import Flask, render_template, redirect, url_for, jsonify, request
from ObjectQueue import Queue
from SqlQuerys import FetchMenu

app = Flask(__name__)

queue = Queue()
queue.addObject("Food", "#12")
queue.addObject("Table", "#3")
queue.addObject("Table", "#17")
queue.addObject("Door", "<---")
queue.addObject("Food", "#12")
queue.addObject("Table", "#3")
queue.addObject("Table", "#17")
queue.addObject("Door", "<---")
queue.addObject("Food", "#12")
queue.addObject("Table", "#3")
queue.addObject("Table", "#17")
queue.addObject("Door", "<---")

# Testing Orders queue implementation
orders = Queue()


@app.route('/')
def home():
    return render_template('menu.html')


@app.route('/acceptQueuePing', methods=['POST'])
def acceptQueuePing():
    if request.method == 'POST':
        ping = queue.popFrontObject()
        data = {
            "acceptedPing": ping.getNote1() + " " + ping.getNote2(),
        }
        return jsonify(data)


@app.route('/addPingToQueue', methods=['POST'])
def addPingToQueue():
    if request.method == 'POST':
        data = request.get_json()
        pingType = data.get('pingType')
        tableNo = data.get('tableNo')
        queue.addObject(pingType, tableNo)
        return ('', 204)


@app.route("/updateQueue")
def updateQueue():
    jsonQueue = []
    for i in range(queue.getLength()):
        ping = queue.getObject(i)
        jsonQueue.append({
            "note": ping.getNote1(),
            "tableNo": ping.getNote2()
        })
    return jsonify({
        "queueLength": queue.getLength(),
        "queueItems": jsonQueue
    })


@app.route('/sendToKitchen', methods=['POST'])
def sendToKitchen():
    if request.method == 'POST':
        data = request.get_json()
        order = data.get('order')
        tableNo = data.get('tableNo')
        time = datetime.datetime.now()

        # This is for Maan to deal with :))))
        return ('', 204)


@app.route('/Ring')
def showRing():
    return render_template('Ring.html')


@app.route('/Floor-Staff')
def showFS():
    names, prices = FetchMenu()
    return render_template('Floor-Staff.html', queue=queue, names=names, prices=prices)
from bson import ObjectId
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb+srv://Theamzingu:Socr%40tis123@teamproject14.nnzfaib.mongodb.net/test')
db = client["Kitchen"]
order_collection = db["order_queue"]
accepted_collection = db["accepted_orders"]


@app.route('/kitchen')
def kitchen():
    orders = list(order_collection.find({}, {'_id': False}))
    for order in orders:
        order['items'] = ', '.join(order['items'])
    return render_template('kitchen.html', orders=orders)


@app.route('/order_queue_data')
def order_queue_data():
    orders = list(order_collection.find({}, {'_id': False}))
    for order in orders:
        order['items'] = ', '.join(order['items'])
    return jsonify(orders)

@app.route('/accepted_orders_data')
def accepted_orders_data():
    orders = list(accepted_collection.find({}, {'_id': False}))
    for order in orders:
        order.pop('order_id')
        order['complete_button'] = '<button class="btn btn-success complete-button" data-order-id="' + str(order['order_number']) + '">Complete</button>'
        order['items'] = ', '.join(order['items'])
    return jsonify(orders)


if __name__ == '__main__':
    app.run(debug=True)

