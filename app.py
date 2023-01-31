from flask import Flask, render_template
app = Flask(__name__)

import sqlite3


@app.route('/kitchen')
def kitchen():
    conn = sqlite3.connect("orders.db")
    c = conn.cursor()
    c.execute("SELECT * FROM order_queue")
    orders = c.fetchall()
    conn.close()
    return render_template("kitchen.html", orders=orders)

if __name__ == "__main__":
    app.run(debug=True)