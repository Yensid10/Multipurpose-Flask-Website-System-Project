import time
from ObjectQueue import Queue
from flask import redirect
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

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
# Colour coordinate these depending on the type of request?


@app.route('/')
def home():
    return render_template('menu.html')


# @app.route('/')
# def home():
#     return render_template('Floor-Staff.html', queue=queue)

@app.route('/acceptQueuePing', methods=['POST'])
def acceptQueuePing():
    if request.method == 'POST':
        queue.popFrontObject()
        return ('', 204)


@app.route('/addPingToQueue', methods=['POST'])
def addPingToQueue():
    if request.method == 'POST':
        data = request.get_json()
        tableNo = data.get('tableNo')
        queue.addObject("Table ", tableNo)
        return ('', 204)


@app.route("/updateQueue")
def updateQueue():
    jsonQueue = []
    for i in range(queue.getLength()):
        order = queue.getObject(i)
        jsonQueue.append({
            "note": order.getNote(),
            "tableNo": order.getTableNo()
        })
    return jsonify({
        "queueLength": queue.getLength(),
        "queueItems": jsonQueue
    })


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


@app.route('/Ring')
def showRing():
    return render_template('Ring.html')


@app.route('/Floor-Staff')
def showFS():
    return render_template('Floor-Staff.html', queue=queue)


if __name__ == '__main__':
    app.run(debug=True)
