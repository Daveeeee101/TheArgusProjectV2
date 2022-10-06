import logging

def setupLogging():
    FORMAT = '%(levelname)s: %(asctime)s  %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO, filename='Files/FullLog.log')
    consoleHandle = logging.StreamHandler()
    consoleHandle.setLevel(logging.WARNING)
    logging.getLogger().addHandler(consoleHandle)
