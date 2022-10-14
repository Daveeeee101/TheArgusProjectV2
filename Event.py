
class Event:
    def __init__(self, openseaEventData):
        self.badEvent = False
        self.collection = openseaEventData['collection']['slug']
        try:
            self.assetName = openseaEventData['item']['name']
            self.address = openseaEventData['item']['assetContract']['address']
            self.link = openseaEventData['item']['assetContract']['blockExplorerLink']
        except Exception:
            self.badEvent = True
            return
        self.tokenId = openseaEventData['item']['tokenId']
        self.timestamp = openseaEventData['eventTimestamp']
        self.eventType = openseaEventData['eventType']
        self.creatorFee = openseaEventData['creatorFee']
        self.ethPrice = openseaEventData['perUnitPrice']['eth']
        self.dollarPrice = openseaEventData['perUnitPrice']['usd']
        try:
            self.sellerAddress = openseaEventData['seller']['address']
        except Exception:
            self.badEvent = True
            return
        if self.eventType == 'SUCCESSFUL':
            self.buyerAddress = openseaEventData['winnerAccount']['address']
            self.paymentType = openseaEventData['payment']['symbol']
        else:
            self.buyerAddress = None
            self.paymentType = None
            self.wasOfferAccepted = None
        self.eventSpecific = self.eventType

    def setEventSpecific(self, eventSpecific):
        self.eventSpecific = eventSpecific

    def __str__(self):
        return f"{self.eventType} event for collection {self.collection} happened at {self.timestamp} for {self.ethPrice} (tokenId = {self.tokenId})"
