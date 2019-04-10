from Robots import cZrobot as z2


class cRatio2Tickers(z2.zRobot):

    # maxTradeQty = 5 # contracts
    # maxExposition = 50 # contracts

    def __init__(self, symbols):
        super().__init__(symbols)

        self.myRatioBid = 0
        self.myRatioOffer = 0

        self.ratioBidPrice = 0
        self.ratioBidSize = 0
        self.ratioOfferPrice = 0
        self.ratioOfferSize = 0
        self.availableBid = 0
        self.availableOffer = 0
        # self.indexPosition = 0
        # self.USDPosition = 0
        # self.sumIndexValue = 0
        # self.sumUSDValue = 0

        #self.t1Multiplier = self.getContractMultiplier(symbols[1])

    def setMyRatioBid(self, myRatioBid):
        self.myRatioBid = myRatioBid

    def setRatioOffer(self, myRatioOffer):
        self.myRatioOffer = myRatioOffer

    def goRobot(self):
        self.mdOutput()
        self.ratioCalc()
        self.printLineRatio()
        # self.tradeIntelligence()
        # self.printBook()

    def ratioCalc(self):

        t0BidPrice = self.getBidPrice(self.symbols[0])
        t0BidSize = self.getBidSize(self.symbols[0])
        t0offerPrice = self.getOfferPrice(self.symbols[0])
        t0OfferSize = self.getOfferSize(self.symbols[0])
        t0Multiplier = self.getContractMultiplier(self.symbols[0])
        # #
        t1BidPrice = self.getBidPrice(self.symbols[1])
        t1BidSize = self.getBidSize(self.symbols[1])
        t1OfferPrice = self.getOfferPrice(self.symbols[1])
        t1OfferSize = self.getOfferSize(self.symbols[1])
        t1Multiplier = self.t1Multiplier
        # t1Multiplier = 88
        print("in ratio calc", t0Multiplier, t1Multiplier)
        # if t0offerPrice > 0:
        #     self.ratioBidPrice = t1BidPrice / t0offerPrice
        #
        #     if self.t1BidPrice > 0:
        #         self.availableBid = round(min(t1BidPrice * t1BidSize * t1Multiplier / (t0offerPrice * t0Multiplier),
        #                                   t0offerPrice * t0OfferSize * t0Multiplier / t1BidPrice), 2)
        #
        # if t0BidPrice > 0:
        #     self.ratioOfferPrice = t1OfferPrice / t0BidPrice
        #
        #     if self.t1OfferPrice > 0:
        #         self.availableOffer = round(min(t1OfferPrice * t1OfferSize * t1Multiplier / (t0BidPrice*t0Multiplier),
        #                                         t0BidPrice*t0BidSize*t0Multiplier/t1OfferPrice), 2)


    # def ratioCalcOld(self):
    #     if self.usdOfferPrice > 0:
    #         self.indexBidUSD = self.indexBidPrice / self.usdOfferPrice
    #
    #     if self.usdOfferPrice == 0:
    #         # TODO: calcular y poner nuestro offer
    #         pass
    #
    #     if self.usdBidPrice > 0:
    #         self.indexOfferUSD = self.indexOfferPrice / self.usdBidPrice
    #
    #     if self.usdBidPrice == 0:
    #         # TODO: calcular y poner nuestro bid
    #         pass
    #
    #     if self.usdOfferPrice > 0 and self.indexBidPrice > 0:
    #         self.availableBid = round(min(self.indexBidPrice * self.indexBidSize / self.usdOfferPrice / 1000,
    #                                       self.usdOfferPrice * self.usdOfferSize * 1000 / self.indexBidPrice), 2)
    #
    #     if self.usdBidPrice > 0 and self.indexOfferPrice > 0:
    #         self.availableOffer = round(min(self.indexOfferPrice * self.indexOfferSize / self.usdBidPrice / 1000,
    #                                         self.usdBidPrice * self.usdBidSize * 1000 / self.indexOfferPrice), 2)

    def printLineRatio(self):
        print("Index in USD: ", "(",
              round(self.myRatioBid, 2), "/",
              round(self.myRatioOffer, 2), ")",
              round(self.ratioBidPrice, 2), "/",
              round(self.ratioOfferPrice, 2), "size :",
              self.availableBid, "x", self.availableOffer) \
              # , "----->",
              #   str(round(self.midMarket * 0.995, 2)), "/",
              #   str(round(self.midMarket * 1.005, 2)), " SIZE:----> ",
              #   str(round(self.availableBid, 0)), "xx",
              #   str(round(self.availableOffer, 0)))

    # def printBook(self):
    #     print("Book-Total trades: ", self.trades,
    #           "  Index Pos: ", self.indexPosition, ":", round(self.sumIndexValue, 2),
    #           "  USD Position :", self.USDPosition, ":", round(self.sumUSDValue, 2))


if __name__ == '__main__':

    ticker1 = "DOJun19"
    ticker2 = "RFX20Jun19"
    myBid = 800
    myOffer = 950
    suscriptTuple = (ticker1, ticker2)

    r2tickets = cRatio2Tickers(suscriptTuple)
    # r2tickets.start()
    r2tickets.setMyRatioBid(myBid)
    r2tickets.setRatioOffer(myOffer)


else:
    pass






