from flask import Flask, render_template
# import mysql.connector

app = Flask(__name__)

@app.route('/menu/<query>')
def menu(array):
# def menu(query):
    # # Connect to the database
    # conn = mysql.connector.connect(user='username',
    #                                password='password',
    #                                host='host',
    #                                database='database')
    # cursor = conn.cursor()

    # # Execute the SQL query
    # cursor.execute(query)

    # # Fetch the menu items
    # menu_items = cursor.fetchall()

    # # Close the cursor and connection
    # cursor.close()
    # conn.close()

    # # Render the template with the menu items
    return render_template('dynamicMenu.html', menu_items=array)
if name == 'main':
    app.run(debug=True)