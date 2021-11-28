import asyncio

from api.jobs import background


asyncio.run(background(None))
