import asyncio
from functools import partial
import os

from sanic.blueprints import Blueprint
from sanic.response import file, json

from ...utils.compat import complex_json
from ...utils.response import ws_send
from ...utils.asyncio import await_many_dispatch
from .aio_rabbit import MQClient

chat = Blueprint('chat', url_prefix='/chat/')
BASE_DIR = os.path.split(os.path.abspath(__file__))[0]


@chat.route('')
async def index(request):
    return await file(os.path.join(BASE_DIR, 'index.html'))


async def heart_beat(ws=None, interval=5):
    await asyncio.sleep(interval)
    await ws_send(ws, '[server] heart beat')


async def receive(ws=None, mq_client=None):
    data = await ws.recv()
    decoded_json_data = complex_json.loads(data)
    message = decoded_json_data['message']
    await ws_send(ws, '[you] ' + message)
    await mq_client.publish('[broadcast] ' + message)


@chat.websocket('ws')
async def chat_feed(request, ws):
    await ws_send(ws, '[server] Hello')
    client = MQClient()
    client.websocket = ws
    await client.start()
    local_heart_beat = partial(heart_beat, ws=ws)
    local_receive = partial(receive, ws=ws, mq_client=client)
    await await_many_dispatch([local_heart_beat, local_receive])
