from flask import Flask

app = Flask(__name__)

@app.route('/', methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
def index():
    return "Hello, Techstars! <a href='/cool'>Click here to go to the cool page.</a>"

@app.route('/cool')
def cool():
    return "You are cool!"
