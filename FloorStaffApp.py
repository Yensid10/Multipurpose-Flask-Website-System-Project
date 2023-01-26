import time
from ObjectQueue import Queue
from flask import Flask, render_template, request
from flask import redirect
from threading import Thread

app = Flask(__name__)


def checkQueue():
    while True:
        if queue.checkQueue() == "Changed":
            return redirect('/')
        time.sleep(1)


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
# Colour coordinate these depending on the type of request


@app.route('/', methods=['GET', 'POST'])
def home():
    thread = Thread(target=checkQueue)
    thread.start()
    if request.method == 'POST':
        if request.form.get('popQueue') == 'Accept':
            queue.popFrontObject()
            return redirect('/')
    return render_template('Floor-Staff.html', queue=queue)


# @app.route('/background_process_test', methods=['GET', 'POST'])
# def background_process_test():

#     #     table_number = request.form.get("TableNum")
#     #     Request = request.form.get("Request")
#     #     print(table_number)
#     #     print(Request)
#     # if table_number and Request:
#     #     Queue().add_object(table_number, Request)
#     return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
