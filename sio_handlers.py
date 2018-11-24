import json
import time
import typing
from dataclasses import dataclass
import numpy
import socketio
from aiohttp import web
import random
from audio_analysis import WavFile

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


@dataclass
class SessionContext:
    id: str
    filename: str

    def __init__(self, sid):
        self.id = sid
        self.filename = "/Users/koobcam/Desktop/device1_channel1_20181021155321.wav"


sessions_ctx: typing.Dict[str, SessionContext]
sessions_ctx = {}


async def new_session(sid):
    new_ctx = SessionContext(sid)
    sessions_ctx[new_ctx.id] = new_ctx
    await sio.emit('id', new_ctx.id)


async def get_analysed_data(sid):
    print('Commence: get_analysed_data')
    session = sessions_ctx.get(sid, None)
    if session is None:
        print('Complete: get_analysed_data {}'.format(session))
        await sio.emit('error', 'session not found')
        return

    if session.filename is None:
        print('Complete: get_analysed_data file govno')
        await sio.emit('error', json.dumps({'error': 'file not selected'}))
        return

    for amplitude_chunk in WavFile(session.filename).get_splitted_audio():
        amplitude, ts, ml_results = _get_ml_result_with_data(amplitude_chunk)

        new_l = [float(i) for i in amplitude_chunk]

        result = json.dumps({
            'amplitude': new_l,
            'ts': float(ts),
            'analysis_data': float(ml_results)
        })

        print('Complete: get_analysed_data ok')
        await sio.emit('update', result)


def _get_audio_analysis(audio_data: numpy.array) -> float:
    return random.randint(1, 10)


def _get_ml_result_with_data(amplitude: numpy.array) -> typing.Tuple[numpy.array, float, float]:
    ts = time.time()
    ml_results = _get_audio_analysis(amplitude)
    return amplitude, ts, ml_results
