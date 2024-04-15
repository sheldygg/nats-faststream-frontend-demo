from contextlib import asynccontextmanager
from faststream import FastStream, ContextRepo
from faststream.nats import NatsBroker
from aiohttp import ClientSession

from .consumers import setup_consumers


@asynccontextmanager
async def lifespan(context: ContextRepo):
    aiohttp_session = ClientSession()
    context.set_global("aiohttp_session", aiohttp_session)

    yield

    await aiohttp_session.close()


broker = NatsBroker()
broker.include_router(setup_consumers())

app = FastStream(broker=broker, lifespan=lifespan)
