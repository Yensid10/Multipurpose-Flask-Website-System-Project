import time
from ObjectQueue import Queue
from flask import Flask, jsonify, render_template, request
from flask import redirect
from threading import Thread

app = Flask(__name__)


# def checkQueue():
#     while True:
#         if queue.checkQueue() == "Changed":
#             return redirect('/')
#         time.sleep(1)


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


@app.route('/')
def home():
    # thread = Thread(target=checkQueue)
    # thread.start()
    # if request.method == 'POST':
    #     if request.form.get('popQueue') == 'Accept':
    #         queue.popFrontObject()
    #         return redirect('/')
    return render_template('Floor-Staff.html', queue=queue)


@app.route('/page')
def page():
    # thread = Thread(target=checkQueue)
    # thread.start()
    # if request.method == 'POST':
    #     if request.form.get('popQueue') == 'Accept':
    #         queue.popFrontObject()
    #         return redirect('/')
    return render_template('page.html')


@app.route('/test', methods=['POST'])
def test():
    if request.method == 'POST':
        queue.popFrontObject()
        # print("popped")
        return ('', 204)


@app.route('/addToQueueTest', methods=['POST'])
def addToQueueTest():
    print("help")
    if request.method == 'POST':
        data = request.get_json()
        tableNo = data.get('tableNo')
        queue.addObject("Table ", tableNo)
        return ('', 204)


@ app.route('/background_process_test', methods=['GET', 'POST'])
def background_process_test():

    if request.method == "POST":
        table_number = request.form.get("TableNum")
        note = request.form.get("Note")
        print(table_number)
        print(note)
    if table_number and note:
        queue.addObject(note, table_number)
    return redirect('/')


@app.route("/updateQueue")
def updateQueue():
    queueItems = []
    for i in range(queue.getLength()):
        order = queue.getOrder(i)
        queueItems.append({
            "note": order.getNote(),
            "tableNo": order.getTableNo()
        })
    return jsonify({
        "queueLength": queue.getLength(),
        "queueItems": queueItems
    })


if __name__ == '__main__':
    app.run(debug=True)
