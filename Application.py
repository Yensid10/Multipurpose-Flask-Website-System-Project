import datetime
from bson import ObjectId
from flask import Flask, render_template, jsonify, request, json
from pymongo import MongoClient
from ObjectQueue import Queue
from SqlQuerys import FetchMenu
import paypalrestsdk
import logging

# import os

paypalrestsdk.configure({
    "mode": "sandbox",  # sandbox or live
    "client_id": "AfzWV6H8HbQPiOb0a3B-ty24yYWRllM8s34zjYgsgjpnIqlunb3vkmZrJ5KSvLB5XjRXOoAQP6nriEOA",
    "client_secret": "EA4HmZS-IacWkAx8U0pOwRTlfNawZ_c3wZh87F8oXvxfWK2St54c1CAbdy1_qodhY1OUbz3loVpbwa89"})


app = Flask(__name__)
# app.config['AfzWV6H8HbQPiOb0a3B-ty24yYWRllM8s34zjYgsgjpnIqlunb3vkmZrJ5KSvLB5XjRXOoAQP6nriEOA'] = os.environ.get(
#     'AfzWV6H8HbQPiOb0a3B-ty24yYWRllM8s34zjYgsgjpnIqlunb3vkmZrJ5KSvLB5XjRXOoAQP6nriEOA')
# app.config['EA4HmZS-IacWkAx8U0pOwRTlfNawZ_c3wZh87F8oXvxfWK2St54c1CAbdy1_qodhY1OUbz3loVpbwa89'] = os.environ.get(
#     'EA4HmZS-IacWkAx8U0pOwRTlfNawZ_c3wZh87F8oXvxfWK2St54c1CAbdy1_qodhY1OUbz3loVpbwa89')

client = MongoClient(
    'mongodb+srv://Theamzingu:Socr%40tis123@teamproject14.nnzfaib.mongodb.net/test')
db = client["Kitchen"]
order_collection = db["order_queue"]
accepted_collection = db["accepted_orders"]

queue = Queue()
# queue.addObject("Food", "#12")
# queue.addObject("Table", "#3")
# queue.addObject("Table", "#17")
queue.addObject("Door", "<---")
# queue.addObject("Food", "#12")
# queue.addObject("Table", "#3")
# queue.addObject("Table", "#17")
# queue.addObject("Door", "<---")
# queue.addObject("Food", "#12")
# queue.addObject("Table", "#3")
# queue.addObject("Table", "#17")
# queue.addObject("Door", "<---")

# Testing Orders queue implementation
orders = Queue()


@app.route('/')
def home():
    return render_template('menu.html')


@app.route('/billTemplate')
def billTemplate():
    return render_template('billTemplate.html')


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
        time = datetime.datetime.now()
        order = data.get('order')
        tableNo = data.get('tableNo')
        if orders.getSpecificOrder(tableNo) == False:
            orders.addObject(tableNo, order)
        else:
            tempOrder = orders.popSpecificOrder(tableNo).getNote2()[
                'queue'] + order['queue']
            orders.addObject(tableNo, tempOrder)

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


# @ app.route('/getBill', methods=['POST'])
# def getBill():
#     if request.method == 'POST':
#         tableNo = request.form['tableNo']
#         if orders.getSpecificOrder(tableNo) == False:
#             return render_template('bills.html', data="No order found")
#         return render_template('bills.html', data=orders.getSpecificOrder(tableNo))

@ app.route('/getBill', methods=['POST'])
def getBill():
    if request.method == 'POST':
        tableNo = request.form['tableNo']
        order = orders.getSpecificOrder(tableNo)
        if order == False:
            return render_template('billTemplate.html', data="No order found")
        return render_template('billTemplate.html', data={'queue': order['queue']})


@ app.route('/makePayment', methods=['POST'])
def makePayment():
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": "10.00",
                "currency": "USD"
            },
            "description": "This is the payment transaction description."
        }],
        "redirect_urls": {
            "return_url": "http://localhost:5000/payment/success",
            "cancel_url": "http://localhost:5000/payment/cancel"
        }
    })
    if payment.create():
        print("Payment created successfully")
    else:
        print(payment.error)
    # Get the payment URL from the Payment object
    payment_url = None
    for link in payment.links:
        if link.method == "REDIRECT":
            payment_url = link.href
            break

    # Return the payment URL as a JSON response
    return jsonify({'payment_url': payment_url})


@ app.route('/testPayment')
def testPayment():
    return render_template('payTemplate.html')


@ app.route('/Ring')
def showRing():
    return render_template('Ring.html')


@ app.route('/faqPage')
def faqPage():
    return render_template('faq.html')


@ app.route('/loginPage')
def loginPage():
    return render_template('loginpage.html')


@ app.route('/Floor-Staff')
def showFS():
    names, prices = FetchMenu()
    return render_template('Floor-Staff.html', queue=queue, names=names, prices=prices)


@ app.route('/kitchen')
def kitchen():
    orders = list(order_collection.find())
    for order in orders:
        order['_id'] = str(order['_id'])

    accepted_orders = list(accepted_collection.find())
    for order in accepted_orders:
        order['_id'] = str(order['_id'])

    print(orders)
    return render_template('kitchen.html', orders=orders, accepted_orders=accepted_orders)


@ app.route('/accept_order', methods=['POST'])
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


if __name__ == '__main__':
    app.run(debug=True)
