from flask import Flask
from flask_socketio import SocketIO, emit
import g4f
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


@socketio.on("send_prompt")
def handle_prompt(data):
    prompt = data["prompt"]
    print(prompt)
    start = time.time()

    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    for message in response:
        emit("response", {"content": message}, namespace="/")


if __name__ == "__main__":
    socketio.run(app)
