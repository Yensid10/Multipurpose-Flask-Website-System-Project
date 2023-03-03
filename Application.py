from flask import Flask, render_template, redirect, url_for
import sqlite3
from flask import Flask, jsonify, render_template, request
from flask import redirect
from ObjectQueue import Queue
import SqlQuerys
from flask import Response

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
# Colour coordinate these depending on the type of request?

# Testing Orders queue implementation
orders = Queue()


@app.route('/')
def home():
    return render_template('menu.html')


@app.route('/hideDairy', methods=['POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        tableNumber = data['tableNumber']
        allergens = data['allergens']
        print(tableNumber, allergens)
        for i in range(len(allergens)):
            if 'Milk' in allergens:
                print("True")
                data = SqlQuerys.FetchDairy()
                return jsonify({'data': data})

            if 'Gluten' in allergens:
                print("True")
                data = SqlQuerys.FetchGluten()
                return jsonify({'data': data})

            if 'Peanuts' in allergens:
                print("True")
                data = SqlQuerys.FetchPeanuts()
                return jsonify({'data': data})

            if 'Treenuts' in allergens:
                print("True")
                data = SqlQuerys.FetchTreenuts()
                return jsonify({'data': data})

            if 'Celery' in allergens:
                print("True")
                data = SqlQuerys.FetchCelery()
                return jsonify({'data': data})

            if 'Mustard' in allergens:
                print("True")
                data = SqlQuerys.FetchMustard()
                return jsonify({'data': data})

            if 'Eggs' in allergens:
                print("True")
                data = SqlQuerys.FetchEggs()
                return jsonify({'data': data})

            if 'Sesame' in allergens:
                print("True")
                data = SqlQuerys.FetchSesame()
                return jsonify({'data': data})

            if 'Fish' in allergens:
                print("True")
                data = SqlQuerys.FetchFish()
                return jsonify({'data': data})

            if 'Crustaceans' in allergens:
                print("True")
                data = SqlQuerys.FetchCrustaceans()
                return jsonify({'data': data})

            if 'Molluscs' in allergens:
                print("True")
                data = SqlQuerys.FetchMolluscs()
                return jsonify({'data': data})

            if 'Sulphates' in allergens:
                print("True")
                data = SqlQuerys.FetchSulphites()
                return jsonify({'data': data})

            if 'Lupin' in allergens:
                print("True")
                data = SqlQuerys.FetchLupin()
                return jsonify({'data': data})
            #             # if x == 'dairy':
    return jsonify({'success': False})


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
        tableNo = data.get('tableNo')
        queue.addObject("Table ", tableNo)
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


@ app.route("/updateOrder")
def updateOrder():
    jsonQueue = []
    for i in range(orders.getLength()):
        order = orders.getObject(i)
        jsonQueue.append({
            "name": order.getNote1(),
            "note": order.getNote2()
        })
    return jsonify({
        "queueItems": jsonQueue
    })


# @app.route('/background_process_test', methods=['GET', 'POST'])
# def background_process_test():
#     if request.method == "POST":
#         table_number = request.form.get("TableNum")
#         Request = request.form.get("Request")
#         print(table_number)
#         print(Request)
#     if table_number and Request:
#         Queue().add_object(table_number, Request)
#     return redirect('/')


@ app.route('/Ring')
def showRing():
    return render_template('Ring.html')


@ app.route('/Floor-Staff')
def showFS():
    return render_template('Floor-Staff.html', queue=queue)


@ app.route('/kitchen')
def kitchen():
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute("SELECT * FROM order_queue")
    orders = c.fetchall()
    c.execute("SELECT * FROM accepted_orders")
    accepted_orders = c.fetchall()
    conn.close()
    return render_template("kitchen.html", orders=orders, accepted_orders=accepted_orders)


@ app.route('/order_history')
def order_history():
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute("SELECT * FROM order_history")
    order_history = c.fetchall()
    conn.close()
    return render_template('order_history.html', order_history=order_history)


@ app.route('/accept_order/<int:order_id>')
def accept_order(order_id):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM order_queue WHERE id=?", (order_id,))
    order = cursor.fetchone()

    cursor.execute("INSERT INTO accepted_orders (id, table_number, items, status, recipe_url) VALUES (?, ?, ?, ?, ?)",
                   (order_id, order[1], order[2], order[3], order[4]))
    conn.commit()

    cursor.execute("DELETE FROM order_queue WHERE id=?", (order_id,))
    conn.commit()

    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute(
        "UPDATE accepted_orders SET status = '<preparing>' WHERE id=?", (order_id,))
    conn.commit()

    return redirect(url_for('kitchen'))


@ app.route('/complete_order/<int:order_id>')
def complete_order(order_id):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM accepted_orders WHERE id=?", (order_id,))
    order = cursor.fetchone()

    cursor.execute("INSERT INTO order_history (id, table_number, items, status, recipe_url) VALUES (?, ?, ?, ?, ?)",
                   (order_id, order[1], order[2], order[3], order[4]))
    conn.commit()

    cursor.execute("DELETE FROM accepted_orders WHERE id=?", (order_id,))
    conn.commit()

    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute(
        "UPDATE order_history SET status = '<complete>' WHERE id=?", (order_id,))
    conn.commit()

    return redirect(url_for('kitchen'))


if __name__ == "__main__":
    app.run(debug=True)
