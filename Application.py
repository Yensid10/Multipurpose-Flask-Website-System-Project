import SqlQuerys
import datetime
from bson import ObjectId
from flask import Flask, render_template, jsonify, request, json
from pymongo import MongoClient
from ObjectQueue import Queue
from SqlQuerys import FetchMenu
import paypalrestsdk
import re

paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": "AfzWV6H8HbQPiOb0a3B-ty24yYWRllM8s34zjYgsgjpnIqlunb3vkmZrJ5KSvLB5XjRXOoAQP6nriEOA",
    "client_secret": "EA4HmZS-IacWkAx8U0pOwRTlfNawZ_c3wZh87F8oXvxfWK2St54c1CAbdy1_qodhY1OUbz3loVpbwa89"})

app = Flask(__name__)

client = MongoClient(
    'mongodb+srv://Theamzingu:Socr%40tis123@teamproject14.nnzfaib.mongodb.net/test')
db = client["Kitchen"]
order_collection = db["order_queue"]
accepted_collection = db["accepted_orders"]
complete_collection = db["complete_orders"]


orders = Queue()
queue = Queue()


@app.route('/Menu')
def menu():
    return render_template('menu.html')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/hideDairy', methods=['POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        # tableNumber = data['tableNumber']
        allergens = data['allergens']
        # print(tableNumber, allergens)
        results = []
        for allergen in allergens:
            if allergen == 'Milk':
                results.extend(SqlQuerys.FetchDairy())

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

        if results:
            return jsonify({'data': results})
        else:
            return jsonify({'success': False})


@app.route('/billTemplate')
def billTemplate():
    return render_template('billTemplate.html')


@ app.route('/acceptQueuePing', methods=['POST'])
def acceptQueuePing():
    if request.method == 'POST':
        ping = queue.popFrontObject()
        data = {
            "acceptedPing": ping.getNote1() + " " + ping.getNote2(),
        }
        return jsonify(data)


@ app.route('/addPingToQueue', methods=['POST'])
def addPingToQueue():
    if request.method == 'POST':
        data = request.get_json()
        pingType = data.get('pingType')
        tableNo = data.get('tableNo')
        queue.addObject(pingType, tableNo)
        return ('', 204)


@ app.route('/addItemToOrder', methods=['POST'])
def addPingToOrder():
    if request.method == 'POST':
        data = request.get_json()
        orderItem = data.get('orderItem')
        orderNotes = data.get('orderNotes')
        orders.addObject(orderItem, orderNotes)
        return ('', 204)


@ app.route("/updateQueue")
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


@ app.route('/sendToKitchen', methods=['POST'])
def sendToKitchen():
    if request.method == 'POST':
        data = request.get_json()
        time = datetime.datetime.now()
        order = data.get('order')
        tableNo = data.get('tableNo')
        if orders.getSpecificOrder(tableNo) == False:
            orders.addObject(tableNo, order)
        else:
            tempOrder = orders.popSpecificOrder(tableNo)[
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


@ app.route('/getBill', methods=['POST'])
def getBill():
    if request.method == 'POST':
        tableNo = request.form['tableNo']
        order = orders.getSpecificOrder(tableNo)
        if order == False:
            return render_template('billTemplate.html', data="No order found")
        subtotal = sum(float(item['price']) for item in order['queue'])
        return render_template('billTemplate.html', data={'queue': order['queue'], 'subtotal': subtotal, 'tableNo': tableNo})


@ app.route('/makePayment', methods=['POST'])
def makePayment():
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
                "cancel_url": "http://localhost:5000/"
            }
        })
        payment.create()
        paymentUrl = next(
            (link.href for link in payment.links if link.method == "REDIRECT"), None)
        return jsonify({'paymentUrl': paymentUrl})


@ app.route('/testPayment')
def testPayment():
    return render_template('payTemplate.html')

# stores order with all items in database and clears the order of the table number


@ app.route('/success')
def success():
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


@  app.route('/Ring')
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


@ app.route('/order_history')
def order_history():
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute("SELECT * FROM order_history")
    order_history = c.fetchall()
    conn.close()
    return render_template('order_history.html', order_history=order_history)


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
