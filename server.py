import sio_handlers
from sio_handlers import app, sio
import socketio
import eventlet


@sio.on('connect')
def connect(sid, env):
    print('new sess {}'.format(sid))
    sio_handlers.new_session(sid)
    sio_handlers.get_analysed_data(sid)


# @sio.on('update')
# def update(sid):
#     sio_handlers.get_analysed_data(sid)


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect')
    sio_handlers.sessions_ctx.__delitem__(sid)


if __name__ == '__main__':
    # wrap Flask application with socketio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8080)), app)
