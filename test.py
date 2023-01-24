from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/menu')
def menu():
    conn = sqlite3.connect('dummybase2.db')
    c = conn.cursor()
    c.execute("SELECT * FROM menu_items")
    menu_items = c.fetchall()
    conn.close()
    return render_template('menu.html', menu_items=menu_items)

if __name__ == '__main__':
    app.run(debug=True)
