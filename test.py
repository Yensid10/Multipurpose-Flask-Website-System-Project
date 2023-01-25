from flask import Flask, render_template
# import mysql.connector

app = Flask(__name__)

# @app.route("/")
# def home():
#     return "Hello, Flask!"


@app.route("/")
def menu(array=[["Beans", 12, "Some Cool Beans", 123, "Bean Allergy?"],
                ["Cheese", 11, "Some Cool Cheese", 1234, "Chesse Allergy?"],
                ["Soup", 10, "Some Cool Soup", 321, "Soup Allergy?"]]):

    return render_template('dynamicMenu.html', menu_items=array)


if __name__ == '__main__':
    app.run(debug=True)

# FLASK_APP=test.py flask --debug run
