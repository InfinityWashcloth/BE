import sio_handlers
from sio_handlers import app, sio
from aiohttp import web


@sio.on('connect')
def connect(sid, env):
    print('new sess')
    sio_handlers.new_session()


@sio.on('update')
def update(sid):
    sio_handlers.get_analysed_data(sid)


@sio.on('disconnect')
def disconnect(sid):
    del sio_handlers.sessions_ctx[sid]


web.run_app(app)
