import uuid
import time
from dataclasses import dataclass
import numpy
import typing
from aiohttp import web
import socketio
import json
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


@dataclass
class StreamHandler:
    sessions_ctx: typing.Dict[str, SessionContext]

    def __init__(self):
        self.sessions_ctx = dict()

    def new_session(self):
        new_ctx = SessionContext()
        self.sessions_ctx[new_ctx.id] = new_ctx
        # todo send sid to client

    def get_analysed_data(self, sid):
        session = self.sessions_ctx.get(sid, None)
        if session in None:
            # todo send notFound status
            return

        if session.filename is None:
            # todo not selected file
            return

        for amplitude_chunk in WavFile(session.filename).get_splitted_audio():
            amplitude, ts, ml_results = self._get_ml_result_with_data(amplitude_chunk)

            result = json.dumps({
                'amplitude':      amplitude_chunk,
                'ts':             ts,
                'analysis_data':  ml_results
            })

            sio.emit('update', result)

    def _get_audio_analysis(self, audio_data: numpy.array) -> float:
        # TODO send data for analysis to ML service
        pass

    def _get_ml_result_with_data(self, amplitude: numpy.array) -> typing.Tuple[numpy.array, float, float]:
        ts = time.time()
        ml_results = self._get_audio_analysis(amplitude)
        return amplitude, ts, ml_results

