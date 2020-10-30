from sanic import Sanic
from sanic.response import redirect
from .blueprint.chat import chat

app = Sanic(__name__)

app.blueprint(chat)


@app.route('/')
async def default(request):
    return redirect('/chat')
