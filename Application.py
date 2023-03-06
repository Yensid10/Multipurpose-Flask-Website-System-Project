import datetime
import time

from bson import ObjectId
from flask import Flask, render_template, jsonify, request, json, session
from pymongo import MongoClient

from ObjectQueue import Queue
from SqlQuerys import FetchMenu

app = Flask(__name__)

client = MongoClient('mongodb+srv://Theamzingu:Socr%40tis123@teamproject14.nnzfaib.mongodb.net/test')
db = client["Kitchen"]
order_collection = db["order_queue"]
accepted_collection = db["accepted_orders"]

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

        queue = order.get('queue', [])

        for item in queue:
            order_items = item.get('Note1')
            note = item.get('Note2')

            # Insert the order into the order queue in MongoDB
            order_collection.insert_one({
                '_id': ObjectId(),
                'table_number': tableNo,
                'items': order_items,
                'note': note,
                'status': 'Taken',
                'time': time
            })

        return ('', 204)


@app.route('/Ring')
def showRing():
    return render_template('Ring.html')


@app.route('/Floor-Staff')
def showFS():
    names, prices = FetchMenu()
    return render_template('Floor-Staff.html', queue=queue, names=names, prices=prices)


@app.route('/kitchen')
def kitchen():
    # Get the current time
    current_time = int(time.time())

    # Render the kitchen.html template with the current time
    orders = list(order_collection.find())
    for order in orders:
        order['_id'] = str(order['_id'])

    accepted_orders = list(accepted_collection.find())
    for order in accepted_orders:
        order['_id'] = str(order['_id'])

    return render_template('kitchen.html', orders=orders, accepted_orders=accepted_orders, current_time=current_time)


@app.route('/accept_order', methods=['POST'])
def accept_order():
    # Get the order data from the POST request
    order_data = json.loads(request.form['order_data'])

    order_data['time'] = int(request.form['time'])

    print(order_data)

    # Insert the order data into the accepted_orders collection
    accepted_collection.insert_one(order_data)

    # Remove the order data from the order_queue collection
    order_collection.delete_one({'_id': ObjectId(order_data['old_id'])})

    # Return a success response
    return jsonify({'success': True})

@app.route('/complete_order', methods=['POST'])
def complete_order():
    # Get the order ID from the POST request
    order_id = request.form['order_id']

    # Remove the order from the accepted_orders collection
    accepted_collection.delete_one({'_id': ObjectId(order_id)})

    # Return a success response
    return jsonify({'success': True})

@app.route('/kitchen/data')
def kitchen_data():
    # Get the last updated timestamp from the request parameters
    last_updated = int(request.args.get('last_updated'))

    # Get the current time
    current_time = int(time.time())

    # Query the MongoDB database for new orders since the last updated timestamp
    new_orders = list(order_collection.find({'time': {'$gt': last_updated}}))

    # Convert the ObjectId to string for JSON serialization
    for order in new_orders:
        order['_id'] = str(order['_id'])

    # Return a JSON response with the current time and the new orders
    response = {
        'current_time': current_time,
        'new_orders': bool(new_orders)
    }
    return jsonify(response)



if __name__ == '__main__':
    app.run(debug=True)
