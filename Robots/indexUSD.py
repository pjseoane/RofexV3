from Robots import zRobot as zR


class indexUSD(zR.zRobot):

    USDPosition: int
    # factor:float

    def __init__(self, symbols, myIndexBidPrice, myIndexOfferPrice):

        super().__init__(symbols)

        self.indexBidUSD = False
        self.indexOfferUSD = False
        self.indexBidSizeUSD = 0
        self.indexOfferSizeUSD = 0
        self.availableBid = False
        self.availableOffer = False
        self.midMarket = False
        self.myIndexBidPrice = myIndexBidPrice
        self.myIndexOfferPrice = myIndexOfferPrice
        #
        self.usdBidPrice = False
        self.usdBidSize = 0
        self.usdOfferPrice = False
        self.usdOfferSize = 0

        self.indexBidPrice = False
        self.indexBidSize = 0
        self.indexOfferPrice = False
        self.indexOfferSize = 0
        self.indexPosition=0
        self.USDPosition=0
        self.sumIndexValue=0
        self.sumUSDValue=0

    def goRobot(self):
        # print("En goRobot indexUSD")
        self.mdOutput()
        self.usdBidPrice = self.getBidPrice(self.symbols[0])
        self.usdBidSize = self.getBidSize(self.symbols[0])
        self.usdOfferPrice = self.getOfferPrice(self.symbols[0])
        self.usdOfferSize = self.getOfferSize(self.symbols[0])

        self.indexBidPrice = self.getBidPrice(self.symbols[1])
        self.indexBidSize = self.getBidSize(self.symbols[1])
        self.indexOfferPrice = self.getOfferPrice(self.symbols[1])
        self.indexOfferSize = self.getOfferSize(self.symbols[1])
        # Chequer si el dictionary ya tiene tantos datos como symbols

        if self.marketDataDict.__len__() == len(self.symbols):
            self.indexCalc()
            self.printLineIndexUSD()
            self.tradeIntelligence()
            self.printBook()

        #TODO: Desarrollar un BookStatus method, ver limites, balancear etc
        else:
            print(" indexUSD Dictionary not completed yet....")

    def indexCalc(self):
        # # usd = self.symbols[0]
        # # index = self.symbols[1]
        # # # symbols[1] = Index
        #
        if self.usdOfferPrice != 0:
            self.indexBidUSD = self.indexBidPrice / self.usdOfferPrice

        if self.usdBidPrice != 0:
            self.indexOfferUSD = self.indexOfferPrice / self.usdBidPrice

        if self.usdOfferPrice != 0 and self.indexBidPrice != 0:
            self.availableBid = round(min(self.indexBidPrice * self.indexBidSize / self.usdOfferPrice / 1000,
                                          self.usdOfferPrice * self.usdOfferSize * 1000 / self.indexBidPrice), 2)

        if self.usdBidPrice != 0 and self.indexOfferPrice != 0:
            self.availableOffer = round(min(self.indexOfferPrice * self.indexOfferSize / self.usdBidPrice / 1000,
                                            self.usdBidPrice * self.usdBidSize * 1000 / self.indexOfferPrice), 2)

        self.midMarket = (self.indexBidUSD + self.indexOfferUSD) / 2

    def printLineIndexUSD(self):
        print("Index in USD: ", "(",
              round(self.myIndexBidPrice, 2), "/",
              round(self.myIndexOfferPrice,2), ")",
              round(self.indexBidUSD,2), "/",
              round(self.indexOfferUSD,2), "size :",
              self.availableBid, "x", self.availableOffer, "----->",
              str(round(self.midMarket * 0.995, 2)), "/",
              str(round(self.midMarket * 1.005, 2)), " SIZE:----> ",
              str(round(self.availableBid, 0)), "xx",
              str(round(self.availableOffer, 0)))

    def printBook(self):
        print("Book-Total trades: ", self.trades,
              "  Index Pos: ", self.indexPosition, ":", round(self.sumIndexValue, 2),
              "  USD Position :", self.USDPosition, ":", round(self.sumUSDValue,2))

    def tradeIntelligence(self):
        # print("Entrando a Trade Int")

        # Opera de a 1 contrato, sino
        self.availableOffer = int(round(self.availableOffer, 0))
        self.availableBid = int(round(self.availableBid, 0))

        if self.myIndexBidPrice > self.indexOfferUSD > 0:
            print("Buy indice en USD")
            usdContracts = int(round(self.indexOfferPrice*self.availableOffer/ (self.usdBidPrice*1000), 0))

            # TODO mandar ordenes de 1 contrato nada mas
            self.buyIndexUSD(self.symbols[0], self.symbols[1], self.usdBidPrice, self.indexOfferPrice, usdContracts,
                             self.availableOffer)

            self.myIndexBidPrice=self.decreaseBidPrice(0.997)
            # self.myIndexBidPrice *= 0.997

        if self.indexBidUSD > self.myIndexOfferPrice and self.indexBidUSD > 0:
            print("Sell indice en USD")
            usdContracts = int(round(self.indexBidPrice * self.availableBid / (self.usdOfferPrice*1000), 0))
            self.sellIndexUSD(self.symbols[0], self.symbols[1], self.usdOfferPrice, self.indexBidPrice, usdContracts,
                              self.availableBid)

            self.myIndexOfferPrice=self.increaseOfferPrice(1.003)

    def decreaseBidPrice(self, factor):
        self.myIndexBidPrice *= factor
        return self.myIndexBidPrice

    def increaseOfferPrice(self, factor):
        """

        :type factor: float
        """
        self.myIndexOfferPrice *= factor
        return self.myIndexOfferPrice

    def buyIndexUSD(self, tickerUSD, tickerIndex, usdPrice, indexPrice, usdContracts, indexContracts):
        # Buy Index + Sell USD
        # print("Before ex buyIndexUSD",tickerIndex,indexPrice,indexContracts)
        self.singleTrade('BUY', tickerIndex, str(indexPrice), str(indexContracts))
        self.singleTrade('SELL', tickerUSD, str(usdPrice), str(usdContracts))
        self.indexPosition += indexContracts
        self.USDPosition -= usdContracts
        self.sumIndexValue += indexPrice * indexContracts
        self.sumUSDValue -= usdPrice * usdContracts *1000

        print("Buying INDEX: ", "Price / Contracts:", str(indexPrice), str(indexContracts))
        print("Selling USD : ", "Price / Contracts:", str(usdPrice), str(usdContracts))

    def sellIndexUSD(self, tickerUSD, tickerIndex, usdPrice, indexPrice, usdContracts, indexContracts):
        # Sell Index + Buy USD
        self.singleTrade("SELL", tickerIndex, str(int(indexPrice)), str(int(indexContracts)))
        self.singleTrade("BUY", tickerUSD, str(int(usdPrice)), str(int(usdContracts)))
        self.indexPosition -= indexContracts
        self.USDPosition += usdContracts
        self.sumIndexValue -= indexPrice * indexContracts
        self.sumUSDValue += usdPrice * usdContracts * 1000

        print(".....Selling INDEX: ", indexPrice, "vol:", indexContracts,
              "Buying USD: ", usdPrice, "vol ", usdContracts,)
        #print("Buying  USD : ", "Price / Contracts:", usdPrice, usdContracts)


if __name__ == '__main__':

    ticker1 = "DOJun19"
    ticker2 = "RFX20Jun19"
    myBid   = 900
    myOffer = 915
    suscriptTuple = (ticker1, ticker2)
    suscription = indexUSD(suscriptTuple, myBid, myOffer)
    suscription.start()

else:
    pass

