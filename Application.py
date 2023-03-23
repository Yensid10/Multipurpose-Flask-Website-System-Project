### Imports ###

import datetime
import re
import paypalrestsdk
from bson import ObjectId
from flask import Flask, render_template, jsonify, request, json, redirect, url_for
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

complete_collection = db["complete_orders"]

app = Flask(__name__)


### Variables ###

queue = Queue()  # Used for pings
orders = Queue()  # Used for orders


### Routes ###

@app.route('/')
def home():
    """Displays the home page.

    Returns:
        str: HTML for the home page.
    """
    # Displays Home page
    return render_template('index.html')


@app.route('/Menu')
def menu():
    """
    Displays the menu page.

    Returns:
        str: HTML for the menu page.
    """
    return render_template('menu.html')


@app.route('/about')
def about_us():
    """
    Displays the about-us page.

    Returns:
        str: HTML for the about-us page.
    """
    return render_template('about.html')


@app.route('/contact')
def contact_us():
    """
    Displays the contact-us page.

    Returns:
        str: HTML for the contact-us page.
    """
    return render_template('contact.html')


@app.route('/hideDairy', methods=['POST'])
def index():
    """Endpoint that returns a list of food items that do not contain specified allergens.

    This endpoint takes in a JSON object in the request body that contains a list of allergens to exclude from the query.
    It then fetches the corresponding data from a database and returns a list of food items that do not contain any of the specified allergens.

    Returns:
        A JSON object with a 'data' key that contains a list of food items that do not contain any of the specified allergens, or a 'success' key with a value of False if there are no query results.
    """
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


@app.route('/acceptQueuePing', methods=['POST'])
def acceptQueuePing():
    # Pop top ping in queue and return it
    """
    The acceptQueuePing function is called by the client when a user clicks on the Accept button.
        The function pops off the top ping in queue and returns it to be displayed on screen.

    :return: The ping that was accepted
    """
    if request.method == 'POST':
        ping = queue.popFrontObject()
        data = {
            "acceptedPing": ping.getNote1() + " " + ping.getNote2(),
        }
        return jsonify(data)


@app.route('/addPingToQueue', methods=['POST'])
def addPingToQueue():
    # Add ping to bottom of queue
    """
        The addPingToQueue function is used to add a ping to the queue.
            It takes in a POST request with JSON data containing two fields:
                - pingType (string) : The type of ping that needs to be added.
                - tableNo (int) : The number of the table that needs service.

        :return: A 204 status code which means that the request has been successfully processed and the response is intentionally blank
        """
    if request.method == 'POST':
        data = request.get_json()
        pingType = data.get('pingType')
        tableNo = data.get('tableNo')
        queue.addObject(pingType, tableNo)
        return ('', 204)


@app.route('/sendCancel', methods=['POST'])
def sendCancel():
    # When an order item is cancelled in the kitchen, it also needs to be deleted in the order queue
    """
    The sendCancel function is called when an order item is cancelled in the kitchen.
        It deletes the corresponding order item from the queue of orders for that table.

        Args:
            data (dict): A dictionary containing a table number and index number, which are used to identify which order item to delete from the queue of orders for that table.

    :return: A 204 status code, which means that the request has been successfully processed and the response is intentionally blank
    """
    if request.method == 'POST':
        data = request.get_json()
        tableNo = data.get('tableNo')[1:]
        indexNumber = int(data.get("indexNo"))
        tempOrder = orders.popSpecificOrder(tableNo)['queue']
        tempOrder[indexNumber] = "CANCELLED"
        if all(item == "CANCELLED" for item in tempOrder):
            # Skip adding the order back into orders if all items are cancelled
            pass
        else:
            tempOrder = {'queue': tempOrder}
            orders.addObject(tableNo, tempOrder)
        return ('', 204)


@app.route("/updateQueue")
def updateQueue():
    # Returns the queue as a json object
    """
    The updateQueue function returns the queue as a json object.
        The function is called by the client to update its view of the queue.

        Returns:
            A json object containing two fields: &quot;queueLength&quot; and &quot;queueItems&quot;.

    :return: The queue as a json object
    """
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
    """
    The sendToKitchen function is used to send the order from the table to the kitchen.
    It takes in a JSON object with two keys: 'order' and 'tableNo'. The value of 'order' is an array of objects, each containing information about one item on the order.
    The value of 'tableNo' is a string representing which table this order belongs to.

    :return: A 204 status code, which means that the request was received and understood but no response is needed
    """
    if request.method == 'POST':
        data = request.get_json()
        time = datetime.datetime.now()
        order = data.get('order')
        tableNo = data.get('tableNo')

        # Get the highest order index for the table
        max_order_index = 0
        existing_orders = order_collection.find({'table_number': tableNo})
        for existing_order in existing_orders:
            order_index = int(existing_order['order_index'].split('-')[-1])
            if order_index > max_order_index:
                max_order_index = order_index + 1

        if orders.getSpecificOrder(tableNo) == False:
            orders.addObject(tableNo, order)
        else:
            # If the table already has an order, add the new order to the old one
            tempOrder = {
                'queue': orders.popSpecificOrder(tableNo)['queue']
                + order['queue']}
            orders.addObject(tableNo, tempOrder)

        queue = order.get('queue', [])

        # Add an order ID to each item in the order
        for i, item in enumerate(queue):
            next_order_index = max_order_index + i
            item['order_index'] = f"{tableNo}-{next_order_index}"

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
    """
    Retrieve the bill for a specific table.

    :return: The rendered HTML template for displaying the bill information.
    """
    # Get the bill for a specific table
    if request.method == 'POST':
        tableNo = request.form['tableNo']
        order = orders.getSpecificOrder(tableNo)
        if order == False:
            return render_template('billTemplate.html', data="No order found")
        subtotal = sum(float(item['price'])
                       for item in order['queue'] if item != "CANCELLED")
        return render_template('billTemplate.html',
                               data={'queue': order['queue'], 'subtotal': subtotal, 'tableNo': tableNo})


@app.route('/makePayment', methods=['POST'])
def makePayment():
    # Make a payment using paypal api
    """
    The makePayment function is used to create a payment object using the paypal api.
    The function takes in a table number and uses this to get the bill for that table from
    the bill database. The total price of all items on the bill is then calculated and passed into
    the payment object along with other information such as currency, description, item list etc.
    A redirect url is also created which will be used by paypal when it redirects back to our website.

    :return: A paymenturl which is a link to the paypal website
    """
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
                    "total": sum(float(item['price']) for item in bill['queue'] if item != "CANCELLED"),
                    "currency": "GBP"
                },
                "description": "Payment for table {}".format(tableNo) + " at " + str(datetime.datetime.now()),
                "item_list": {
                    "items": [{
                        "name": item['Note1'],
                        "quantity": 1,
                        "price": item['price'],
                        "currency": "GBP"
                    } for item in bill['queue'] if item != "CANCELLED"]
                }

            }],
            "redirect_urls": {
                "return_url": "https://group14projectoaxaca-357.azurewebsites.net/success",
                "cancel_url": "https://group14projectoaxaca-357.azurewebsites.net/Menu"
            }
        })
        payment.create()
        paymentUrl = next(
            (link.href for link in payment.links if link.method == "REDIRECT"), None)
        return jsonify({'paymentUrl': paymentUrl})


@app.route('/checkPayment', methods=['POST'])
def checkPayment():
    # Check if a payment has been made/if an order exists
    """
    The checkPayment function is used to check if a payment has been made for an order.
        This function takes in the table number of the order and checks if there is an existing
        order with that table number. If there isn't, it returns False, else it returns True.

    :return: A boolean value that determines whether or not a payment has been made
    """
    if request.method == 'POST':
        tableNo = request.json['tableNo']
        check = orders.getSpecificOrder(tableNo)
        if check == False:
            return jsonify({'check': "False"})
        return jsonify({'check': "True"})

# stores order with all items in database and clears the order of the table number


@app.route('/success')
def success():
    # After a successful order, add it to the completed orders database
    """
    The success function is called when the user has successfully paid for their order.
    It takes the payment ID and payer ID from PayPal, then uses them to execute a payment.
    If this is successful, it will add an entry to the completed orders database with
    the table number, items ordered and time of completion.

    :return: To the menu page
    """
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
    return render_template('index.html')


@app.route('/faqPage')
def faqPage():
    # Render the FAQ page
    """
    The faqPage function renders the FAQ page.

    :return: The rendered faq page
    """
    return render_template('faq.html')


@app.route('/doorPage')
def DoorPage():
    # Render the Door page
    """
    The DoorPage function renders the DoorPage.html template, which is a page that allows users to open and close the door.

    :return: The doorpage
    """
    return render_template('DoorPage.html')


@app.route('/loginPage')
def loginPage():
    # Render the Login page
    """
    The loginPage function renders the login page for the user to enter their credentials.
        Args: None
        Returns: The rendered template of the login page.

    :return: The loginpage
    """
    return render_template('loginpage.html')


@app.route('/Floor-Staff')
def showFS():
    # Render the Floor Staff page, passing in the relevant information
    """
    The showFS function is used to render the Floor Staff page, passing in the relevant information.
        It takes no arguments and returns a rendered template of the Floor Staff page.

    :return: The floor staff page
    """
    names, prices = FetchMenu()
    return render_template('Floor-Staff.html', queue=queue, names=names, prices=prices)


@app.route('/kitchen')
def kitchen():
    """
    The kitchen function is the route for the kitchen page.
    It queries all orders from the order collection and accepted orders from
    the accepted_orders collection, then renders them to a template.

    :return: A list of all orders in the order collection and a list of accepted orders from the accepted_collection
    """
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
    """
    The accept_order function is called when the user clicks on the accept button for a given order.
    It takes in an order_data object, which contains all of the information about that particular order.
    The function then inserts this data into the accepted_orders collection and removes it from
    the orders_queue collection.

    :return: A success response, but the client doesn't do anything with it
    """
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
    """
    The complete_order function is called when the user clicks on the Complete Order button.
    It takes in an order ID from a POST request and uses it to find the corresponding order in
    the accepted_orders collection. If it finds one, then it inserts that data into the complete_orders
    collection and removes that data from accepted_orders.

    :return: A success response
    """
    order_id = request.form['order_id']

    # Get the order from the accepted_orders collection
    order = accepted_collection.find_one({'_id': ObjectId(order_id)})

    if order:
        # Insert the order data into the complete_orders collection
        complete_collection.insert_one(order)
        complete_collection.update_one({'_id': ObjectId(order_id)}, {
                                       '$set': {'status': 'Completed', 'completed_time': datetime.datetime.now()}})
        # Remove the order from the accepted_orders collection
        accepted_collection.delete_one({'_id': ObjectId(order_id)})

    # Return a success response
    return jsonify({'success': True})


@app.route('/cancel_order', methods=['POST'])
def cancel_order():
    """
    The cancel_order function is called when a user clicks the cancel button on an order.
    It removes the order from either the accepted orders collection or the order queue collection, depending on whether it has been accepted yet.

    :return: A success response
    """
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


@app.route('/completed')
def completed():
    """
    The completed function is a route that renders the completed.html template, which displays all orders in the
    completed_orders collection of MongoDB. The function first finds all documents in the collection and stores them as a list
    in completed_orders. Then, it iterates through each order and converts its ObjectId to a string so that it can be displayed
    on the page.

    :return: The completed orders page
    """
    completed_orders = list(complete_collection.find())
    for order in completed_orders:
        order['_id'] = str(order['_id'])

    return render_template('completed.html', completed_orders=completed_orders)


@app.route('/clear_completed_orders', methods=['POST'])
def clear_completed_orders():
    """
    The clear_completed_orders function clears the completed orders collection in MongoDB.
        It is called when the user clicks on the 'Clear Completed Orders' button on the /completed page.

    :return: The completed page
    """
    complete_collection.delete_many({})
    return redirect(url_for('completed'))

### MAIN ###


if __name__ == '__main__':
    # Run the app
    app.run(debug=True)
