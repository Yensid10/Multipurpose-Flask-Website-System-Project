from flask import Flask, render_template
# import mysql.connector

app = Flask(__name__)

# @app.route("/")
# def home():
#     return "Hello, Flask!"

@app.route("/")
# @app.route("/menu/<array>")
def menu(array = [["beans", 12, "Bean Allergy", 123, "this is the quantity, the item is nice"], ["cheese", 11, "cheese Allergy"], ["soup", 10, "soup Allergy"]]):
# # def menu(query):
#     # # Connect to the database
#     # conn = mysql.connector.connect(user='username',
#     #                                password='password',
#     #                                host='host',
#     #                                database='database')
#     # cursor = conn.cursor()

#     # # Execute the SQL query
#     # cursor.execute(query)

#     # # Fetch the menu items
#     # menu_items = cursor.fetchall()

#     # # Close the cursor and connection
#     # cursor.close()
#     # conn.close()

#     # # Render the template with the menu items
    return render_template('dynamicMenu.html', menu_items=array)

# if name == 'main':
#     app.run(debug=True)

# export FLASK_APP=test.py 
# python -m flask run