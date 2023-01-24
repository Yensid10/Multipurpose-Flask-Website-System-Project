from flask import Flask, request
import sqlite3

app = Flask(__name__)

# Connect to the database
def get_db():
    conn = sqlite3.connect('menu.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return 'Welcome to the menu app'

# Create the menu_items table
@app.route('/create_table', methods=['GET'])
def create_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS menu_items (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        description TEXT,
                        price REAL,
                        restrictions TEXT
                    )''')
    conn.commit()
    return 'Table created'

# Add a menu item
@app.route('/add_item', methods=['POST'])
def add_item():
    conn = get_db()
    cursor = conn.cursor()
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    restrictions = request.form['restrictions']
    cursor.execute("INSERT INTO menu_items (name, description, price, restrictions) VALUES (?,?,?,?)", (name, description, price, restrictions))
    conn.commit()
    return 'Menu item added'