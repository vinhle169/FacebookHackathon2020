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
    print('NICE')
    print(request.cookies.get('username'))
    user_ids.setdefault(request.cookies.get('username'), conversation(''))


@socketio.on('sendMessage')
def handle_message(message):
    global user_ids
    print(message)
    print(request.cookies.get('username') + ': ' + message['message'])
    user_ids[request.cookies.get('username')].update_utterance(message['message'])
    emit('response', {'message': user_ids[request.cookies.get('username')].parse_convo()})


@socketio.on('disconnect')
def handle_disconnect():
    global user_ids
    del user_ids[request.cookies.get('username')]
    print('user left')


if __name__ == '__main__':
    socketio.run(app, debug=True)
