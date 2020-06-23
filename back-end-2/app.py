from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'FIXME: Generate secret key'
socketio = SocketIO(app)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == '__main__':
    socketio.run(app)

@socketio.on('connection')
def handle_connect():
    print('NICE')
    send('hello world')

@socketio.on('sendMessage')
def handle_message(message):
    print('received: ' + message)
    response = 'fixme: response'
    send(msg)

@socketio.on('disconnect')
def handle_disconnect():
    # clean up
    print('user left')