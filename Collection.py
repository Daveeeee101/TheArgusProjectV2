import logging
from typing import List, Dict
from Event import Event
from Asset import Asset


class Collection:

    def __init__(self, slug):
        self.slug = slug
        self.eventHistory: List[Event] = []
        self.assetDict: Dict[str, Asset] = {}

    def updateEventHistory(self, newEvent: Event):
        self.eventHistory.append(newEvent)
        logging.info('new event of type %s for collection %s added to history, tokenId=%s',
                     newEvent.eventType, newEvent.collection, newEvent.tokenId)
        if newEvent.eventType == 'CREATED':
            if newEvent.tokenId in self.assetDict:
                logging.warning('Token (id=%s) listed but already in collection (collection=%s)! Prev price: %s, new price: %s',
                                newEvent.tokenId, newEvent.collection, self.assetDict[newEvent.tokenId].price, newEvent.ethPrice)
                self.assetDict[newEvent.tokenId].price = float(newEvent.ethPrice)
            else:
                newAsset = Asset(id=newEvent.tokenId, name=newEvent.assetName, price=newEvent.ethPrice,
                                 usdPrice=newEvent.dollarPrice, seller=newEvent.sellerAddress)
                self.assetDict[newEvent.tokenId] = newAsset
        elif newEvent.eventType == 'SUCCESSFUL':
            if newEvent.tokenId not in self.assetDict:
                logging.warning('Token (id=%s) sold but not in collection (collection=%s)!',
                                newEvent.tokenId, newEvent.collection)
            else:
                self.assetDict.pop(newEvent.tokenId)
        elif newEvent.eventType == 'CANCELLED':
            if newEvent.tokenId not in self.assetDict:
                logging.warning('Token (id=%s) cancelled but not in collection (collection=%s)!',
                                newEvent.tokenId, newEvent.collection)
            else:
                self.assetDict.pop(newEvent.tokenId)

    def addInitialAssets(self, assets: List[Asset]):
        for asset in assets:
            self.assetDict[asset.assetId] = asset

    def __str__(self):
        return f"{self.slug}\n------------\n" + ''.join(map(lambda x: str(x)+"\n", sorted(self.assetDict.values(), key=lambda x: x.price))) + "#####################\n"

    def getFloorPrice(self) -> float:
        return sorted(self.assetDict.values(), key=lambda x: x.price)[0].price

    def getAssetsFromFloor(self, multipleAboveFloor) -> List[Asset]:
        return [x for x in sorted(self.assetDict.values(), key=lambda x: x.price) if x.price < self.getFloorPrice() * multipleAboveFloor]