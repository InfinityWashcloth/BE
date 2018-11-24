import json
import time
import typing
import uuid
from dataclasses import dataclass
import numpy
import socketio
from aiohttp import web

from audio_analysis import WavFile

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


@dataclass
class SessionContext:
    id: str
    filename: str

    def __init__(self):
        self.id = uuid.uuid4().hex
        self.filename = None


sessions_ctx: typing.Dict[str, SessionContext]


def new_session():
    new_ctx = SessionContext()
    sessions_ctx[new_ctx.id] = new_ctx
    sio.emit('id', new_ctx.id)


def get_analysed_data(sid):
    session = sessions_ctx.get(sid, None)
    if session in None:
        sio.emit('session not found')
        return

    if session.filename is None:
        sio.emit('error', 'file not selected')
        return

    for amplitude_chunk in WavFile(session.filename).get_splitted_audio():
        amplitude, ts, ml_results = _get_ml_result_with_data(amplitude_chunk)

        result = json.dumps({
            'amplitude': amplitude_chunk,
            'ts': ts,
            'analysis_data': ml_results
        })

        sio.emit('update', result)


def _get_audio_analysis(audio_data: numpy.array) -> float:
    # TODO send data for analysis to ML service
    pass


def _get_ml_result_with_data(amplitude: numpy.array) -> typing.Tuple[numpy.array, float, float]:
    ts = time.time()
    ml_results = _get_audio_analysis(amplitude)
    return amplitude, ts, ml_results
