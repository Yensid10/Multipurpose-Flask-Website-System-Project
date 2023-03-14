import datetime

from bson import ObjectId
from flask import Flask, render_template, jsonify, request, json
from pymongo import MongoClient

from ObjectQueue import Queue
from SqlQuerys import FetchMenu

app = Flask(__name__)

client = MongoClient('mongodb+srv://Theamzingu:Socr%40tis123@teamproject14.nnzfaib.mongodb.net/test')
db = client["Kitchen"]
order_collection = db["order_queue"]
accepted_collection = db["accepted_orders"]
complete_collection = db["complete_orders"]


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


@app.route('/sendCancel', methods=['POST'])
def sendCancel():
    if request.method == 'POST':
        data = request.get_json()
        pingType = data.get('pingType')
        tableNo = data.get('tableNo')
        indexNumber = data.get("indexNo")
        print(pingType)
        print(tableNo)
        print(indexNumber)
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

        # Add an order ID to each item in the order
        for i, item in enumerate(queue):
            item['order_index'] = f"{tableNo}-{i + 1}"

            order_items = item.get('Note1')
            note = item.get('Note2')

            # Insert the order into the order queue in MongoDB
            order_collection.insert_one({
                '_id': ObjectId(),
                'table_number': tableNo,
                'order_index': item['order_index'],  # Save the order ID for each item
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
    orders = list(order_collection.find())
    for order in orders:
        order['_id'] = str(order['_id'])

    accepted_orders = list(accepted_collection.find())
    for order in accepted_orders:
        order['_id'] = str(order['_id'])

    return render_template('kitchen.html', orders=orders, accepted_orders=accepted_orders)


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

    # Get the order from the accepted_orders collection
    order = accepted_collection.find_one({'_id': ObjectId(order_id)})

    if order:
        # Insert the order data into the complete_orders collection
        complete_collection.insert_one(order)

        # Remove the order from the accepted_orders collection
        accepted_collection.delete_one({'_id': ObjectId(order_id)})

    # Return a success response
    return jsonify({'success': True})


@app.route('/cancel_order', methods=['POST'])
def cancel_order():
    # Get the order index and order ID from the POST request
    order_index = request.form['order_index']
    order_id = request.form['order_id']

    # Check if the order is in the order queue collection
    order = order_collection.find_one({'order_index': order_index})
    if order:
        # If the order is in the order queue collection, remove it
        order_collection.delete_one({'order_index': order_index})
    else:
        # If the order is not in the order queue collection, it must be in the accepted orders collection
        accepted_collection.delete_one({'_id': ObjectId(order_id)})

    # Return a success response
    return jsonify({'success': True})




if __name__ == '__main__':
    app.run(debug=True)
