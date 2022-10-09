import logging
import Logging
import EventLoop
from Collection import Collection
import CommandLine
import asyncio

async def main(colls):
    await asyncio.gather(
        EventLoop.eventLoop(colls)
    )
    """CommandLine.getInput(colls)"""

if __name__ == '__main__':
    Logging.setupLogging()
    logging.info("starting logging")
    collections = {'the-chimpsons-official': Collection('the-chimpsons-official')}
    asyncio.run(main(collections))
