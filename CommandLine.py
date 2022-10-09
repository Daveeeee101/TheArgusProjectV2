from typing import Dict
from Collection import Collection
import aioconsole
from datetime import datetime, timedelta


async def getInput(collections: Dict[str, Collection]):
    while True:
        lineInput: str = await aioconsole.ainput()
        inputList = lineInput.split()
        try:
            collection = inputList[0]
            collectionObject = collections[collection]
            if inputList[1] == 'events':
                if inputList[2] == 'all':
                    if inputList[3] == 'last':
                        lastSeconds = int(inputList[4])
                        currTime = datetime.utcnow()
                        out = collectionObject.getEventsAfterTime(currTime-timedelta(seconds=lastSeconds))
                        for i in out:
                            print(i)

            elif inputList[1] == 'assets':
                if inputList[2] == 'top':
                    count = int(inputList[3])
                    assets = collectionObject.getAssetsFromFloor(2)[0:count]
                    for i in assets:
                        print(i)
                if inputList[2] == 'percent':
                    percent = float(inputList[3])
                    assets = collectionObject.getAssetsFromFloor(1+percent)
                    for i in assets:
                        print(i)
        except:
            print('invalid operation')
