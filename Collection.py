import logging
from typing import List, Dict
from Event import Event
from Asset import Asset
from datetime import datetime


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
            newEvent.setEventSpecific('LISTING')
            if newEvent.tokenId in self.assetDict:
                newEvent.setEventSpecific('RELIST')
                logging.warning('Token (id=%s) listed but already in collection (collection=%s)! Prev price: %s, new price: %s',
                                newEvent.tokenId, newEvent.collection, self.assetDict[newEvent.tokenId].price, newEvent.ethPrice)
                self.assetDict[newEvent.tokenId].price = float(newEvent.ethPrice)
            else:
                newAsset = Asset(id=newEvent.tokenId, name=newEvent.assetName, price=newEvent.ethPrice,
                                 usdPrice=newEvent.dollarPrice, seller=newEvent.sellerAddress)
                self.assetDict[newEvent.tokenId] = newAsset
        elif newEvent.eventType == 'SUCCESSFUL':
            if newEvent.paymentType == "WETH":
                newEvent.setEventSpecific('OFFER_ACCEPTED')
                logging.info('Token (id=%s) sold with an offer', newEvent.tokenId)
            else:
                newEvent.eventType = 'BUY_NOW'
            if newEvent.tokenId not in self.assetDict:
                if newEvent.eventSpecific == 'OFFER_ACCEPTED':
                    logging.info('Token (id=%s) sold with an offer', newEvent.tokenId)
                else:
                    logging.warning('Token (id=%s) sold but not in collection (collection=%s)!',
                                newEvent.tokenId, newEvent.collection)
            else:
                self.assetDict.pop(newEvent.tokenId)
        elif newEvent.eventType == 'CANCELLED':
            if newEvent.eventSpecific != 'CANCELLED_FALSE':
                newEvent.eventSpecific = 'CANCELLED'
            if newEvent.tokenId not in self.assetDict:
                logging.warning('Token (id=%s) cancelled but not in collection (collection=%s)!',
                                newEvent.tokenId, newEvent.collection)
            else:
                if self.assetDict[newEvent.tokenId].seller == newEvent.sellerAddress:
                    self.assetDict.pop(newEvent.tokenId)
                else:
                    print("cancellation not from owner of token")
                    logging.warning("token id %s had cancellation from %s but currently listed by %s", newEvent.tokenId, newEvent.sellerAddress, self.assetDict[newEvent.tokenId].seller)

    def addInitialAssets(self, assets: List[Asset]):
        for asset in assets:
            self.assetDict[asset.assetId] = asset

    def __str__(self):
        return f"{self.slug}\n------------\n" + ''.join(map(lambda x: str(x)+"\n", sorted(self.assetDict.values(), key=lambda x: x.price))) + "#####################\n"

    def getFloorPrice(self) -> float:
        return sorted(self.assetDict.values(), key=lambda x: x.price)[0].price

    def getAssetsFromFloor(self, multipleAboveFloor) -> List[Asset]:
        return [x for x in sorted(self.assetDict.values(), key=lambda x: x.price) if x.price < self.getFloorPrice() * multipleAboveFloor]

    def getEventsAfterTime(self, inputTime):
        return [x for x in self.eventHistory if datetime.fromisoformat(x.timestamp) > inputTime]

