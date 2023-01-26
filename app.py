from ObjectQueue import Queue
import threading
from flask import Flask, render_template, request
from flask import redirect
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('menu.html')


@app.route('/background_process_test', methods=['GET', 'POST'])
def background_process_test():
    if request.method == "POST":
        table_number = request.form.get("TableNum")
        Request = request.form.get("Request")
        print(table_number)
        print(Request)
    if table_number and Request:
        Queue().add_object(table_number, Request)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
