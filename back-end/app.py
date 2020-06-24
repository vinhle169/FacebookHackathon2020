from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from conversation_handler import conversation

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins=["https://heal-bot.netlify.app"])
user_ids = {}


@app.route("/")
def home():
    return render_template("index.html")


@socketio.on('connect')
def handle_connect():
    global user_ids
    print('NICE')
    print(request.sid)
    user_ids.setdefault(request.sid, conversation(''))


@socketio.on('sendMessage')
def handle_message(message):
    global user_ids
    print(message)
    print(request.sid + ': ' + message['message'])
    user_ids[request.sid].update_utterance(message['message'])
    emit('response', {'message': user_ids[request.sid].parse_convo()})


@socketio.on('disconnect')
def handle_disconnect():
    global user_ids
    del user_ids[request.sid]
    print('user left')


if __name__ == '__main__':
    socketio.run(app, debug=True)
