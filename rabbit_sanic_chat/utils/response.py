from .compat import complex_json


async def ws_send(ws, message):
    data = complex_json.dumps({'message': message})
    await ws.send(data)
