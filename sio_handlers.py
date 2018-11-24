import json
import time
import typing
from dataclasses import dataclass
import numpy
import socketio
from audio_analysis import WavFile
from mock_ml import get_predict
from flask import Flask
from flask_cors import CORS

sio = socketio.Server()
flask_app = Flask(__name__, static_url_path='')
CORS(flask_app)

UPLOAD_FOLDER = './data'
ALLOWED_EXTENSIONS = set(['wav'])
flask_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# sio.attach(app)


@dataclass
class SessionContext:
    id: str
    filename: str
    file: WavFile

    def __init__(self, sid):
        self.id = sid
        self.filename = "./data/test.wav"
        self.file = None


sessions_ctx: typing.Dict[str, SessionContext]
sessions_ctx = {}


def new_session(sid):
    new_ctx = SessionContext(sid)
    sessions_ctx[new_ctx.id] = new_ctx
    # sio.emit('id', new_ctx.id)


def get_analysed_data(sid):
    session = sessions_ctx.get(sid, None)
    if session is None:
        sio.emit('error', 'session not found')
        return

    if session.filename is None:
        sio.emit('error', json.dumps({'error': 'file not selected'}))
        return

    if session.file is None:
        session.file = WavFile(session.filename)

    amplitude_chunk = session.file.get_average_amplitude()
    amplitude, ml_results = _get_ml_result_with_data(amplitude_chunk)

    # new_l = [float(i) for i in list(amplitude_chunk)]

    result = {
        'amplitude': float(amplitude_chunk),
        'ts': float(session.file.offset),
        'analysis_data': float(ml_results)
    }

    sio.emit('tupo dich galimaya', {'dima': 'genius'}, sid)
    sio.emit('update', result, sid)


# sio.send(result, sid)
#  yield result


def _get_ml_result_with_data(amplitude: numpy.array) -> typing.Tuple[numpy.array, float]:
    ml_results = get_predict(amplitude)
    return amplitude, ml_results
