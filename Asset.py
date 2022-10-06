class Asset:

    def __init__(self, **kwargs):
        if len(kwargs) == 1:
            openseaAssetData = kwargs['openseaAssetData']
            self.assetId: str = openseaAssetData['tokenId']
            self.assetName: str = openseaAssetData['name']
            try:
                self.price: float = float(openseaAssetData['orderData']['bestAskV2']['priceType']['eth'])
                self.priceInDollars: float = float(openseaAssetData['orderData']['bestAskV2']['priceType']['usd'])
                self.seller: str = openseaAssetData['orderData']['bestAskV2']['maker']['address']
            except TypeError:
                self.price: float = 0.0
                self.priceInDollars: float = 0.0
                self.seller: str = "NO SELLER"
        else:
            self.assetId: str = kwargs['id']
            self.assetName: str = kwargs['name']
            self.price: float = float(kwargs['price'])
            self.priceInDollars: float = float(kwargs['usdPrice'])
            self.seller = kwargs['seller']

    def __str__(self):
        return f"id: {self.assetId}, price:{self.price}"

    def __eq__(self, other):
        return self.assetId == other.assetId and self.price == other.price and self.seller == other.seller
