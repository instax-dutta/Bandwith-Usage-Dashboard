from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import psutil

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit_bandwidth_usage()

def emit_bandwidth_usage():
    net_io_counters = psutil.net_io_counters()
    bytes_sent = net_io_counters.bytes_sent
    bytes_recv = net_io_counters.bytes_recv

    # Convert bytes to gigabytes
    gigabytes_sent = bytes_sent / (1024 ** 3)
    gigabytes_recv = bytes_recv / (1024 ** 3)

    socketio.emit('bandwidth_update', {
        'gigabytes_sent': gigabytes_sent,
        'gigabytes_recv': gigabytes_recv
    })

if __name__ == '__main__':
    socketio.run(app, debug=True)