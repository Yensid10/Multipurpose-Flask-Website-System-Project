import threading
from flask import Flask, render_template, request
from flask import redirect
from ObjectQueue import Queue
app = Flask(__name__)


@app.route('/')
def home():
    t = threading.Thread(target=Queue().Check_queue)
    t.start()
    return render_template('index.html')


@app.route('/background_process_test')
def background_process_test():
    Queue().add_object('14', "Table Needs Assistance")
    return redirect('/')


if __name__ == '__main__':
    app.run()
