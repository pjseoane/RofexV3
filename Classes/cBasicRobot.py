from Classes import cGetMarketData as md


from time import sleep


class cFutureIndex(md.cGetMarketData):

    def __init__(self, symbols):
        super().__init__(symbols)

        self.indexBid = 0
        self.indexOffer = 0
        self.indexBidSize = 0
        self.indexOfferSize = 0
        self.availableBid = 0
        self.availableOffer = 0
        self.midMarket = 0

    #def suscribeTickers(self):
        # for self.sym in self.symbols:
        #
        #     # Arma diccionario de detalles contratos para este Algo
        #     self.contractDetail[self.sym] = self.instrumentDetail(self.sym, 'ROFX')
        #     self.ws.send(self.buildMessage)
        #     print("Sent Suscription msg for ticker in Suscribe This", self.sym)
        #     sleep(1)

    def goRobot(self):
        print("En goRobot cSuscribeThis:")
        #print("marketDataDict en cSusribeThis : ", self.marketDataDict)
        # Chequer si el dictionary ya tiene tantos datos como symbols
        if self.marketDataDict.__len__() == len(self.symbols):

            try:
                self.indexOutput()
                self.indexCalc()

            except:
                # pass
                print("Error goRobot()")

    def indexOutput(self):
        # print ("En cBasicRobot")
        for sym in self.symbols:

            print(sym, "    ", self.getBidPrice(sym), "/", self.getOfferPrice(sym), "----------", self.getBidSize(sym),
                  "/", self.getOfferSize(sym))

    def indexCalc(self):
        usd = self.symbols[0]
        index = self.symbols[1]
        # symbols[1] = Index

        if self.getOfferPrice(usd) != 0:
            self.indexBid = self.getBidPrice(index) / self.getOfferPrice(usd)

        if self.getBidPrice(usd) != 0:
            self.indexOffer = self.getOfferPrice(index) / self.getBidPrice(usd)

        if self.getOfferPrice(usd) != 0 and self.getBidPrice(index) != 0:
            self.availableBid = round(
                min(self.getBidPrice(index) * self.getBidSize(index) / self.getOfferPrice(usd) / 1000,
                    self.getOfferPrice(usd) * self.getOfferSize(usd) * 1000 / self.getBidPrice(index)), 2)

        if self.getBidPrice(usd) != 0 and self.getOfferPrice(index) != 0:
            self.availableOffer = round(
                min(self.getOfferPrice(index) * self.getOfferSize(index) / self.getBidPrice(usd) / 1000,
                    self.getBidPrice(usd) * self.getBidSize(usd) * 1000 / self.getOfferPrice(index)), 2)

        self.midMarket = (self.indexBid + self.indexOffer) / 2

        print("Index in USD: ", self.indexBid, "/", self.indexOffer, "size :", self.availableBid, "x",
              self.availableOffer, "----->", str(round(self.midMarket * 0.995, 2)), "/",
              str(round(self.midMarket * 1.005, 2)), " SIZE:----> ", str(round(self.availableBid, 0)), "xx",
              str(round(self.availableOffer, 0)))


if __name__ == '__main__':

    ticker1 = "DOJun19"
    ticker2 = "RFX20Jun19"
    suscriptTuple = (ticker1, ticker2)
    suscription = cFutureIndex(suscriptTuple)
    suscription.start()

else:
    pass