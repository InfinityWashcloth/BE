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
import eventlet

sio = socketio.Server()
app = Flask(__name__, static_url_path='/Users/koobcam/junction/FE')
CORS(app)


# sio.attach(app)


@dataclass
class SessionContext:
    id: str
    filename: str
    file: WavFile

    def __init__(self, sid):
        self.id = sid
        self.filename = "/Users/koobcam/Desktop/device1_channel1_20181021155321.wav"
        self.file = None


sessions_ctx: typing.Dict[str, SessionContext]
sessions_ctx = {}


def new_session(sid):
    new_ctx = SessionContext(sid)
    sessions_ctx[new_ctx.id] = new_ctx
    # sio.emit('id', new_ctx.id)


def get_analysed_data(sid):
    print('Commence: get_analysed_data')
    session = sessions_ctx.get(sid, None)
    if session is None:
        print('Complete: get_analysed_data {}'.format(session))
        sio.emit('error', 'session not found')
        return

    if session.filename is None:
        print('Complete: get_analysed_data file govno')
        sio.emit('error', json.dumps({'error': 'file not selected'}))
        return

    result = {
        'tupo': 'dich galimaya'
    }

    if session.file is None:
        session.file = WavFile(session.filename)

    amplitude_chunk = session.file.get_splitted_audio()
    amplitude, ts, ml_results = _get_ml_result_with_data(amplitude_chunk)

    new_l = [float(i) for i in list(amplitude_chunk)]
    print("type of chunk {0}".format(type(amplitude_chunk)))
    print("chunk {0}".format(amplitude_chunk))


    result = {
        'amplitude': new_l,
        'ts': float(ts),
        'analysis_data': float(ml_results)
    }

    sio.emit('message', {'dima': 'genius'}, sid)
    sio.emit('message', result, sid)
    print("Client {0} uses {1}".format(sid, sio.transport(sid)))


# sio.send(result, sid)
#  yield result


def _get_ml_result_with_data(amplitude: numpy.array) -> typing.Tuple[numpy.array, float, float]:
    ts = time.time()
    ml_results = get_predict(amplitude)
    return amplitude, ts, ml_results
