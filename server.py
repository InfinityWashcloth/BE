from flask import send_from_directory

import sio_handlers
from sio_handlers import app, sio
import socketio
import eventlet


@sio.on('connect')
def connect(sid, env):
    print('new sess {}'.format(sid))
    sio_handlers.new_session(sid)
    # sio_handlers.get_analysed_data(sid)


@sio.on('start')
def start_analysis(sid):
    sio_handlers.get_analysed_data(sid)


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('/Users/koobcam/junction/FE', path)


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect')
    sio_handlers.sessions_ctx.__delitem__(sid)


if __name__ == '__main__':
    # wrap Flask application with socketio's middleware
    app = socketio.Middleware(sio, app)
    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8080)), app)

