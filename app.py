from flask import Flask, render_template, request
import PingWaiter
app = Flask(__name__)

@app.route('/')

def home():
    return render_template('index.html')
    
@app.route('/background_process_test')

def background_process_test():
    N = PingWaiter.Notifty()
    N.main("Calling for Help")

if __name__== '__main__':
    app.run()
