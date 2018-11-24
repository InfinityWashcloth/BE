import sio_handlers
from sio_handlers import app
from aiohttp import web


def connect(sid, env):
    print('new sess')
    sio_handlers.new_session()


def disconnect(sid):
    del sio_handlers.sessions_ctx[sid]


web.run_app(app)
