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
