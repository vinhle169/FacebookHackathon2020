from gevent import monkey as curious_george
curious_george.patch_all(thread=False, select=False)
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from conversation_handler import conversation

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ASDJOAIHJFLKAGNALKGBNAJKLBG'
socketio = SocketIO(app, cors_allowed_origins="*")
user_ids = {}


@app.route("/")
def home():
    return render_template("index.html")


@socketio.on('connect')
def handle_connect():
    global user_ids
    print('USER CONNECTED')
    print(request.sid)
    user_ids.setdefault(request.sid, conversation(''))


@socketio.on('sendMessage')
def handle_message(message):
    global user_ids
    print('MENSAJE: ', message)
    print(request.sid + ': ' + message['message'])
    user_ids[request.sid].update_utterance(message['message'])
    emit('response', {'message': user_ids[request.sid].parse_convo()})


@socketio.on('disconnect')
def handle_disconnect():
    global user_ids
    del user_ids[request.sid]
    print('USER LEFT')


if __name__ == '__main__':
    socketio.run(app, debug=True)
