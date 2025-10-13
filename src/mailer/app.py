from typing import Any

from faststream import FastStream
from faststream.asgi import AsgiResponse, get

from src.adapters.broker import broker
from src.mailer import handlers as handlers
from src.mailer.db import init_db
from src.mailer.smtp import smtp_client


@get
async def liveness_ping(scope: Any) -> AsgiResponse:  # noqa: ARG001
    return AsgiResponse(b"", status_code=200)


app = FastStream(broker).as_asgi(asgi_routes=[("/liveness", liveness_ping)])


@app.on_startup
async def startup_event() -> None:
    await init_db()
    await smtp_client.connect()


@app.on_shutdown
async def shutdown_event() -> None:
    await smtp_client.quit()
