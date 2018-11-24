import sio_handlers
from sio_handlers import app, sio
from aiohttp import web


@sio.on('connect')
async def connect(sid, env):
    print('new sess {}'.format(sid))
    await sio_handlers.new_session(sid)
    await sio_handlers.get_analysed_data(sid)


# @sio.on('update')
# def update(sid):
#     sio_handlers.get_analysed_data(sid)


@sio.on('disconnect')
async def disconnect(sid):
    print('disconnect')
    sio_handlers.sessions_ctx.__delitem__(sid)


web.run_app(app)
