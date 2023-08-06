import sys
import asyncio
from EventHub import Send

async def Run():
    await Send.run()


loop = asyncio.get_event_loop()
loop.run_until_complete(Run())


