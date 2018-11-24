from flask import send_from_directory
from flask import request, redirect
import sio_handlers
from sio_handlers import flask_app, sio
import socketio
import eventlet
import os


@sio.on('connect')
def connect(sid, env):
    print('new sess {}'.format(sid))
    sio_handlers.new_session(sid)
    # sio_handlers.get_analysed_data(sid)


@sio.on('start')
def start_analysis(sid):
    sio_handlers.get_analysed_data(sid)


@flask_app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('./static', path)


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect')
    sio_handlers.sessions_ctx.__delitem__(sid)


@flask_app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        raise ValueError('files not found')
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        raise ValueError('Bad file')
    filename = file.filename
    fullpath = os.path.join(flask_app.config['UPLOAD_FOLDER'], filename)
    file.save(fullpath)

    for sid in sio_handlers.sessions_ctx.keys():
        sio_handlers.sessions_ctx[sid].filename = fullpath
        sio_handlers.sessions_ctx[sid].file = None

    return redirect('/static/index.html')


if __name__ == '__main__':
    # wrap Flask application with socketio's middleware
    app = socketio.Middleware(sio, flask_app)
    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8080)), app)

