from rabbit_sanic_chat.rabbit_sanic_chat import app
from rabbit_sanic_chat.utils import sanic_config_manager
from rabbit_sanic_chat.plugin.opentracing import setup_opentracing

# setup_opentracing(app=app)

sanic_config_manager(app, prefix="SANIC_")

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        workers=4,
    )
