### Imports ###

import datetime
import re
import paypalrestsdk
from bson import ObjectId
from flask import Flask, render_template, jsonify, request, json
from pymongo import MongoClient
import SqlQuerys
from ObjectQueue import Queue
from SqlQuerys import FetchMenu


### Configurations ###

# Sets up the paypal api in sandbox mode (to allow for testing)
paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": "AfzWV6H8HbQPiOb0a3B-ty24yYWRllM8s34zjYgsgjpnIqlunb3vkmZrJ5KSvLB5XjRXOoAQP6nriEOA",
    "client_secret": "EA4HmZS-IacWkAx8U0pOwRTlfNawZ_c3wZh87F8oXvxfWK2St54c1CAbdy1_qodhY1OUbz3loVpbwa89"})

client = MongoClient(
    'mongodb+srv://Theamzingu:Socr%40tis123@teamproject14.nnzfaib.mongodb.net/test')
db = client["Kitchen"]
order_collection = db["order_queue"]
accepted_collection = db["accepted_orders"]
complete_collection = db["complete_orders"]

app = Flask(__name__)


### Variables ###

queue = Queue()  # Used for pings
orders = Queue()  # Used for orders


### Routes ###

@app.route('/')
def home():
    # Displays Home page
    return render_template('index.html')


@app.route('/Menu')
def menu():
    # Displays Menu page
    return render_template('menu.html')


@app.route('/about')
def about_us():
    # Displays About-us page
    return render_template('about.html')


@app.route('/contact')
def contact_us():
    # Displays Contact-us page
    return render_template('contact.html')


@app.route('/hideDairy', methods=['POST'])
def index():
    if request.method == 'POST':
        # Get the JSON data from the request
        data = request.get_json()
        # Get the list of allergens from the JSON data
        allergens = data['allergens']
        # Initialize an empty list to store the query results
        results = []
        # Loop through the list of allergens and fetch the corresponding data from the database
        for allergen in allergens:
            if allergen == 'Milk':
                results.extend(SqlQuerys.FetchDairy())
                print(results)
            elif allergen == 'Gluten':
                results.extend(SqlQuerys.FetchGluten())

            elif allergen == 'Peanuts':
                results.extend(SqlQuerys.FetchPeanuts())

            elif allergen == 'Treenuts':
                results.extend(SqlQuerys.FetchTreenuts())

            elif allergen == 'Celery':
                results.extend(SqlQuerys.FetchCelery())

            elif allergen == 'Mustard':
                results.extend(SqlQuerys.FetchMustard())

            elif allergen == 'Eggs':
                results.extend(SqlQuerys.FetchEggs())

            elif allergen == 'Sesame':
                results.extend(SqlQuerys.FetchSesame())

            elif allergen == 'Fish':
                results.extend(SqlQuerys.FetchFish())

            elif allergen == 'Crustaceans':
                results.extend(SqlQuerys.FetchCrustaceans())

            elif allergen == 'Molluscs':
                results.extend(SqlQuerys.FetchMolluscs())

            elif allergen == 'Sulphates':
                results.extend(SqlQuerys.FetchSulphites())

            elif allergen == 'Lupin':
                results.extend(SqlQuerys.FetchLupin())
        # Check if there are any query results
        if results:
            return jsonify({'data': results})
        else:
            return jsonify({'success': False})


@app.route('/billTemplate')
def billTemplate():
    # Displays Bills page
    return render_template('billTemplate.html')


@app.route('/acceptQueuePing', methods=['POST'])
def acceptQueuePing():
    # Pop top ping in queue and return it
    if request.method == 'POST':
        ping = queue.popFrontObject()
        data = {
            "acceptedPing": ping.getNote1() + " " + ping.getNote2(),
        }
        return jsonify(data)


@app.route('/addPingToQueue', methods=['POST'])
def addPingToQueue():
    # Add ping to bottom of queue
    if request.method == 'POST':
        data = request.get_json()
        pingType = data.get('pingType')
        tableNo = data.get('tableNo')
        queue.addObject(pingType, tableNo)
        return ('', 204)


@app.route('/sendCancel', methods=['POST'])
def sendCancel():
    # Needs to be completed
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
    # Returns the queue as a json object
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
    # Send an order to the kitchen database and store it in the order queue
    if request.method == 'POST':
        data = request.get_json()
        time = datetime.datetime.now()
        order = data.get('order')
        tableNo = data.get('tableNo')
        if orders.getSpecificOrder(tableNo) == False:
            orders.addObject(tableNo, order)
        else:
            # If the table already has an order, add the new order to the old one
            tempOrder = {
                'queue': orders.popSpecificOrder(tableNo)['queue']
                + order['queue']}
            print(tempOrder)
            orders.addObject(tableNo, tempOrder)

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
                # Save the order ID for each item
                'order_index': item['order_index'],
                'items': order_items,
                'note': note,
                'status': 'Taken',
                'time': time
            })
        return ('', 204)


@app.route('/getBill', methods=['POST'])
def getBill():
    # Get the bill for a specific table
    if request.method == 'POST':
        tableNo = request.form['tableNo']
        order = orders.getSpecificOrder(tableNo)
        if order == False:
            return render_template('billTemplate.html', data="No order found")
        subtotal = sum(float(item['price']) for item in order['queue'])
        return render_template('billTemplate.html',
                               data={'queue': order['queue'], 'subtotal': subtotal, 'tableNo': tableNo})


@app.route('/makePayment', methods=['POST'])
def makePayment():
    # Make a payment using paypal api
    if request.method == 'POST':
        tableNo = request.json['tableNo']
        bill = orders.getSpecificOrder(tableNo)
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": sum(float(item['price']) for item in bill['queue']),
                    "currency": "GBP"
                },
                "description": "Payment for table {}".format(tableNo) + " at " + str(datetime.datetime.now()),
                "item_list": {
                    "items": [{
                        "name": item['Note1'],
                        "quantity": 1,
                        "price": item['price'],
                        "currency": "GBP"
                    } for item in bill['queue']]
                }
            }],
            "redirect_urls": {
                "return_url": "http://localhost:5000/success",
                "cancel_url": "http://localhost:5000/Menu"
            }
        })
        payment.create()
        paymentUrl = next(
            (link.href for link in payment.links if link.method == "REDIRECT"), None)
        return jsonify({'paymentUrl': paymentUrl})


@app.route('/checkPayment', methods=['POST'])
def checkPayment():
    # Check if a payment has been made/if an order exists
    if request.method == 'POST':
        tableNo = request.json['tableNo']
        check = orders.getSpecificOrder(tableNo)
        if check == False:
            return jsonify({'check': "False"})
        return jsonify({'check': "True"})


@app.route('/success')
def success():
    # After a successful order, add it to the completed orders database
    pattern = r"Payment for table (\d+) at"
    payment_id = request.args.get("paymentId")
    payer_id = request.args.get("PayerID")
    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        match = re.search(pattern, payment.transactions[0].description)
        tableNo = match.group(1)
        order = orders.popSpecificOrder(tableNo)['queue']
        time = datetime.datetime.now()

        complete_collection.insert_one({
            '_id': ObjectId(),
            'table_number': tableNo,
            'items': order,
            'time': time
        })
    else:
        print(payment.error)
    return render_template('menu.html')


@app.route('/faqPage')
def faqPage():
    # Render the FAQ page
    return render_template('faq.html')


@app.route('/doorPage')
def DoorPage():
    # Render the Door page
    return render_template('DoorPage.html')


@app.route('/loginPage')
def loginPage():
    # Render the Login page
    return render_template('loginpage.html')


@app.route('/Floor-Staff')
def showFS():
    # Render the Floor Staff page, passing in the relevent information
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


### MAIN ###

if __name__ == '__main__':
    # Run the app
    app.run(debug=True)
