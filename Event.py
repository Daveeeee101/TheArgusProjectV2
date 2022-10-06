class Event:

    def __init__(self, openseaEventData):
        self.collection = openseaEventData['collection']['slug']
        self.assetName = openseaEventData['item']['name']
        self.address = openseaEventData['item']['assetContract']['address']
        self.link = openseaEventData['item']['assetContract']['blockExplorerLink']
        self.tokenId = openseaEventData['item']['tokenId']
        self.timestamp = openseaEventData['eventTimestamp']
        self.eventType = openseaEventData['eventType']
        self.creatorFee = openseaEventData['creatorFee']
        self.ethPrice = openseaEventData['perUnitPrice']['eth']
        self.dollarPrice = openseaEventData['perUnitPrice']['usd']
        self.sellerAddress = openseaEventData['seller']['address']
        if self.eventType == 'SUCCESSFUL':
            self.buyerAddress = openseaEventData['winnerAccount']['address']
        else:
            self.buyerAddress = None

    def __str__(self):
        return f"{self.eventType} event for collection {self.collection} happened at {self.timestamp} for {self.ethPrice} (tokenId = {self.tokenId})"