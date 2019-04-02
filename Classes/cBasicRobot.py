from Classes import cGetMarketData as md


class cFutureIndex(md.cGetMarketData):

    def __init__(self, symbols, myIndexBidPrice, myIndexOfferPrice):
        super().__init__(symbols)

        self.indexBidUSD = 0
        self.indexOfferUSD = 0
        self.indexBidSizeUSD = 0
        self.indexOfferSizeUSD = 0
        self.availableBid = 0
        self.availableOffer = 0
        self.midMarket = 0
        self.myIndexBidPrice = myIndexBidPrice
        self.myIndexOfferPrice = myIndexOfferPrice

        self.usdBidPrice = 0
        self.usdBidSize = 0
        self.usdOfferPrice = 0
        self.usdOfferSize = 0

        self.indexBidPrice = 0
        self.indexBidSize = 0
        self.indexOfferPrice = 0
        self.indexOfferSize = 0
        
    def goRobot(self):
        self.usdBidPrice = self.getBidPrice(self.symbols[0])
        self.usdBidSize = self.getBidSize(self.symbols[0])
        self.usdOfferPrice = self.getOfferPrice(self.symbols[0])
        self.usdOfferSize = self.getOfferSize(self.symbols[0])

        self.indexBidPrice = self.getBidPrice(self.symbols[1])
        self.indexBidSize = self.getBidSize(self.symbols[1])
        self.indexOfferPrice = self.getOfferPrice(self.symbols[1])
        self.indexOfferSize = self.getOfferSize(self.symbols[1])
        # print("En goRobot cBasicRobot:")
        # Chequer si el dictionary ya tiene tantos datos como symbols

        if self.marketDataDict.__len__() == len(self.symbols):

            try:
                self.indexOutput()
                self.indexCalc()
                self.tradeIntelligence()

            except:
                # pass
                print("Error goRobot()")
        else:
            print ("Dictionary not completed yet....")

    def indexOutput(self):
        # print ("En cBasicRobot")
        for sym in self.symbols:

            print(sym, "    ", self.getBidPrice(sym), "/", self.getOfferPrice(sym), "----------", self.getBidSize(sym),
                  "/", self.getOfferSize(sym))

    def indexCalc(self):
        usd = self.symbols[0]
        index = self.symbols[1]
        # symbols[1] = Index

        if self.usdOfferPrice != 0:
            self.indexBidUSD = self.indexBidPrice / self.usdOfferPrice

        if self.usdBidPrice != 0:
            self.indexOfferUSD = self.indexOfferPrice / self.usdBidPrice

        if self.usdOfferPrice != 0 and self.indexBidPrice != 0:
            self.availableBid = round(
                min(self.indexBidPrice * self.indexBidSize / self.usdOfferPrice / 1000,
                    self.usdOfferPrice * self.usdOfferSize * 1000 / self.indexBidPrice), 2)

        if self.usdBidPrice != 0 and self.indexOfferPrice != 0:
            self.availableOffer = round(
                min(self.indexOfferPrice * self.indexOfferSize / self.usdBidPrice / 1000,
                    self.usdBidPrice * self.usdBidSize * 1000 / self.indexOfferPrice), 2)

        self.midMarket = (self.indexBidUSD + self.indexOfferUSD) / 2

        print("Index in USD: ", self.indexBidUSD, "/", self.indexOfferUSD, "size :", self.availableBid, "x",
              self.availableOffer, "----->", str(round(self.midMarket * 0.995, 2)), "/",
              str(round(self.midMarket * 1.005, 2)), " SIZE:----> ", str(round(self.availableBid, 0)), "xx",
              str(round(self.availableOffer, 0)))

    def tradeIntelligence(self):
        print("Entrando a Trade Int")
        self.availableOffer=int(round(self.availableOffer, 0))
        self.availableBid = int(round(self.availableBid, 0))

        if self.myIndexBidPrice > self.indexOfferUSD > 0:
            print("Buy indice en USD")
            usdContracts = int(round(self.indexOfferPrice*self.availableOffer/1000,0))

            self.buyIndexUSD(self.symbols[0], self.symbols[1], self.usdBidPrice, self.indexOfferPrice, usdContracts,
                             self.availableOffer)

        if self.indexBidUSD > self.myIndexOfferPrice and self.indexBidUSD > 0:
            print("Sell indice en USD")
            usdContracts = int(round(self.indexBidPrice * self.availableBid / 1000,0))
            self.sellIndexUSD(self.symbols[0], self.symbols[1], self.usdOfferPrice, self.indexBidPrice, usdContracts,
                              self.availableBid)

    def buyIndexUSD(self, tickerUSD, tickerIndex, usdPrice, indexPrice, usdContracts, indexContracts):
        # Buy Index + Sell USD
        # print("Before ex buyIndexUSD",tickerIndex,indexPrice,indexContracts)
        self.singleTrade('BUY', tickerIndex, str(indexPrice), str(indexContracts))
        self.singleTrade('SELL', tickerUSD, str(usdPrice), str(usdContracts))
        print("Buying INDEX: ", "Price / Contracts:", indexPrice, indexContracts)
        print("Selling USD : ", "Price / Contracts:", usdPrice, usdContracts)

    def sellIndexUSD(self, tickerUSD, tickerIndex, usdPrice, indexPrice, usdContracts, indexContracts):
        # Sell Index + Buy USD
        self.singleTrade("SELL", tickerIndex, str(int(indexPrice)), str(int(indexContracts)))
        self.singleTrade("BUY", tickerUSD, str(int(usdPrice)), str(int(usdContracts)))
        print("Selling INDEX: ", "Price / Contracts:", indexPrice, indexContracts)
        print("Buying  USD : ", "Price / Contracts:", usdPrice, usdContracts)


if __name__ == '__main__':

    ticker1 = "DOJun19"
    ticker2 = "RFX20Jun19"
    myBid   =950
    myOffer =964
    suscriptTuple = (ticker1, ticker2)
    suscription = cFutureIndex(suscriptTuple, myBid, myOffer)
    suscription.start()

else:
    pass
