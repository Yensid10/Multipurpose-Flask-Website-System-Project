from ObjectQueue import Queue
from flask import Flask, render_template, request
from flask import redirect

app = Flask(__name__)


@app.route('/')
def home():
    queue = Queue()
    queue.add_object("Food", "#12")
    queue.add_object("Table", "#3")
    queue.add_object("Table", "#17")
    queue.add_object("Door", "<---")
    queue.add_object("Food", "#12")
    queue.add_object("Table", "#3")
    queue.add_object("Table", "#17")
    queue.add_object("Door", "<---")
    queue.add_object("Food", "#12")
    queue.add_object("Table", "#3")
    queue.add_object("Table", "#17")
    queue.add_object("Door", "<---")
    # Colour coordinate these depending on the type of request
    return render_template('Floor-Staff.html', queue=queue.getQueue())


# @app.route('/background_process_test', methods=['GET', 'POST'])
# def background_process_test():
#     if request.method == "POST":
#         table_number = request.form.get("TableNum")
#         Request = request.form.get("Request")
#         print(table_number)
#         print(Request)
#     if table_number and Request:
#         Queue().add_object(table_number, Request)
#     return redirect('/')


if __name__ == '__main__':
    app.run()
