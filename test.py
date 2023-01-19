from flask import Flask, render_template
# import mysql.connector

app = Flask(__name__)

# @app.route("/")
# def home():
#     return "Hello, Flask!"


@app.route("/")
# @app.route("/menu/<array>")
# Format will be Name, price, Description, Calories and Allergic/Religious/Dietary requirements.
def menu(array=[["Beans", 12, "Some Cool Beans", 123, "Bean Allergy?"], ["Cheese", 11, "Some Cool Cheese", 1234, "Chesse Allergy?"], ["Soup", 10, "Some Cool Soup", 321, "Soup Allergy?"]]):
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

# export FLASK_APP=test.py python -m flask run
