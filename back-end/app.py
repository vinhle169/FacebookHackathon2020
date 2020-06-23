from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'FIXME: Generate secret key'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def home():
    return render_template("index.html")

@socketio.on('connect')
def handle_connect():
    print('NICE')
    print(request.sid)
    emit('response', {'message': 'hello world'})

@socketio.on('sendMessage')
def handle_message(message):
    print(message)
    print('received: ' + message['message'])
    response = 'fixme: response'
    emit('response', {'message': message['message']})

@socketio.on('disconnect')
def handle_disconnect():
    # clean up
    print('user left')

if __name__ == '__main__':
    socketio.run(app)