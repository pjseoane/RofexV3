from Robots import cZrobot as z2


class cIndex2(z2.zRobot):

    maxTradeQty = 5 # contracts
    maxExposition = 50 # contracts

    def __init__(self, symbols, myIndexBidPrice, myIndexOfferPrice):
        super().__init__(symbols)

        self.myIndexBidPrice = myIndexBidPrice
        self.myIndexOfferPrice = myIndexOfferPrice

        self.usdBidPrice = self.getBidPrice(self.symbols[0])
        self.usdBidSize = self.getBidSize(self.symbols[0])
        self.usdOfferPrice = self.getOfferPrice(self.symbols[0])
        self.usdOfferSize = self.getOfferSize(self.symbols[0])
        self.usdLastPrice = self.getLastPrice(self.symbols[0])

        self.indexBidPrice = self.getBidPrice(self.symbols[1])
        self.indexBidSize = self.getBidSize(self.symbols[1])
        self.indexOfferPrice = self.getOfferPrice(self.symbols[1])
        self.indexOfferSize = self.getOfferSize(self.symbols[1])
        self.indexLastPrice = self.getLastPrice(self.symbols[1])

        self.indexBidUSD = self.myIndexBidPrice
        self.indexOfferUSD = self.myIndexOfferPrice
        self.availableBid = 0
        self.availableOffer = 0
        self.indexPosition = 0
        self.USDPosition = 0
        self.sumIndexValue = 0
        self.sumUSDValue = 0

    def goRobot(self):
        self.mdOutput()
        self.indexCalc()
        self.printLineIndexUSD()
        self.tradeIntelligence()
        self.printBook()

    def indexCalc(self):
        if self.usdOfferPrice > 0:
            self.indexBidUSD = self.indexBidPrice / self.usdOfferPrice

        if self.usdOfferPrice == 0:
            # TODO: calcular y poner nuestro offer
            pass

        if self.usdBidPrice > 0:
            self.indexOfferUSD = self.indexOfferPrice / self.usdBidPrice

        if self.usdBidPrice == 0:
            # TODO: calcular y poner nuestro bid
            pass

        if self.usdOfferPrice > 0 and self.indexBidPrice > 0:
            self.availableBid = round(min(self.indexBidPrice * self.indexBidSize / self.usdOfferPrice / 1000,
                                          self.usdOfferPrice * self.usdOfferSize * 1000 / self.indexBidPrice), 2)

        if self.usdBidPrice > 0 and self.indexOfferPrice > 0:
            self.availableOffer = round(min(self.indexOfferPrice * self.indexOfferSize / self.usdBidPrice / 1000,
                                            self.usdBidPrice * self.usdBidSize * 1000 / self.indexOfferPrice), 2)

    def printLineIndexUSD(self):
        print("Index in USD: ", "(",
              round(self.myIndexBidPrice, 2), "/",
              round(self.myIndexOfferPrice,2), ")",
              round(self.indexBidUSD,2), "/",
              round(self.indexOfferUSD,2), "size :",
              self.availableBid, "x", self.availableOffer) \
              # , "----->",
              #   str(round(self.midMarket * 0.995, 2)), "/",
              #   str(round(self.midMarket * 1.005, 2)), " SIZE:----> ",
              #   str(round(self.availableBid, 0)), "xx",
              #   str(round(self.availableOffer, 0)))

    def printBook(self):
        print("Book-Total trades: ", self.trades,
              "  Index Pos: ", self.indexPosition, ":", round(self.sumIndexValue, 2),
              "  USD Position :", self.USDPosition, ":", round(self.sumUSDValue, 2))

if __name__ == '__main__':

    ticker1 = "DOJun19"
    ticker2 = "RFX20Jun19"
    myBid = 800
    myOffer = 950
    suscriptTuple = (ticker1, ticker2)
    suscription = cIndex2(suscriptTuple, myBid, myOffer)
    suscription.start()

else:
    pass






