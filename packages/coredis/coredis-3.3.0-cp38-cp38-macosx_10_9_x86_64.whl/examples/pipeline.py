#!/usr/bin/python

import asyncio
from coredis import Redis


async def pipeline(client):
    async with await client.pipeline(transaction=True) as pipe:
        # will return self to send another command
        pipe = await (await pipe.flushdb()).set("foo", "bar")
        # can also directly send command
        await pipe.set("bar", "foo")
        await pipe.keys("*")
        res = await pipe.execute()
    # results should be in order corresponding to your command
    assert res == (True, True, True, {b"foo", b"bar"}), res


if __name__ == "__main__":
    # default to connect to local redis server at port 6379
    client = Redis()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(pipeline(client))
