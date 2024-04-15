from aiohttp import ClientSession
from faststream import Context
from faststream.nats import NatsRouter, NatsMessage
from faststream.nats.annotations import NatsBroker

router = NatsRouter()


async def get_price(aiohttp_session: ClientSession, coin: str = "KAS") -> str:
    async with aiohttp_session.get(
        f"https://api.mexc.com/api/v3/ticker/price?symbol={coin}USDT"
    ) as response:
        return (await response.json())["price"]


@router.subscriber("crypto.price", "workers")
async def cryptoprice(
    msg: NatsMessage,
    broker: NatsBroker,
    aiohttp_session: ClientSession = Context("aiohttp_session"),
):
    price = await get_price(aiohttp_session, msg.decoded_body.decode())
    await broker.publish(message=price, subject=msg.reply_to)
