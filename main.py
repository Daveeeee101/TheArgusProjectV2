import logging
import Logging
import EventLoop
from Collection import Collection

if __name__ == '__main__':
    Logging.setupLogging()
    logging.info("starting logging")
    EventLoop.eventLoop({'probablyalabel': Collection('probablyalabel')})
