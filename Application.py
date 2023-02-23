import datetime
from flask import Flask, render_template, redirect, url_for
import sqlite3
from flask import Flask, jsonify, render_template, request
from flask import redirect
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


@app.route('/kitchen')
def kitchen():
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute("SELECT * FROM order_queue")
    orders = c.fetchall()
    c.execute("SELECT * FROM accepted_orders")
    accepted_orders = c.fetchall()
    conn.close()
    return render_template("kitchen.html", orders=orders, accepted_orders=accepted_orders)


@app.route('/order_history')
def order_history():
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute("SELECT * FROM order_history")
    order_history = c.fetchall()
    conn.close()
    return render_template('order_history.html', order_history=order_history)


@app.route('/accept_order/<int:order_id>')
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


@app.route('/complete_order/<int:order_id>')
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
