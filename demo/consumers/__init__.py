from faststream.nats import NatsRouter

from . import price


def setup_consumers() -> NatsRouter:
    router = NatsRouter()
    router.include_router(price.router)

    return router
