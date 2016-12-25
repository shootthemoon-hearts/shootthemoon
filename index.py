#!/usr/bin/env python3

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__, template_folder='client')
socketio = SocketIO(app)
DIR = os.path.dirname(os.path.realpath(__file__))

@app.route("/")
def index():
    return render_template('index.html', template_folder=os.path.join(DIR, 'client'))

@socketio.on('connect')
def test_connect():
    print ("connnected")
    emit('connected', 1500)

if __name__ == "__main__":
    socketio.run(app)
