# app.py

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Dictionary to store text for each session
sessions = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<session_id>')
def join_session(session_id):
    return render_template('index.html', session_id=session_id)


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@socketio.on('join_session')
def join_session(data):
    session_id = data['session_id']
    if session_id not in sessions:
        sessions[session_id] = ""
    emit('update_text', {'text': sessions[session_id]})


@socketio.on('update_text')
def update_text(data):
    session_id = data['session_id']
    text = data['text']
    sessions[session_id] = text
    emit('update_text', {'text': text}, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

