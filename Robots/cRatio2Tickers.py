

from Robots import cZrobot as masterR


class cRatio(masterR.zRobot):

    def __init__(self, symbols, myRatioBid, myRatioOffer, tradeSize, exposition, algoName):

        super().__init__(symbols, algoName)

        self.algoAlive = True
        self.myRatioBid = myRatioBid
        self.myRatioOffer = myRatioOffer
        self.tradeSize = tradeSize
        self.exposition = exposition

        self.ratioBidPrice = 0
        self.ratioOfferPrice = 0

        self.availableBid: int = 0
        self.availableOffer: int = 0

        self.t1Position = 0
        self.t0Position = 0
        self.sumt1Value = 0
        self.sumt0Value = 0
        self.openAvgPrice = 0

        print("***********  Algo Name:", self.algoName)

    def setRatioMarket(self,bid,offer,size):
        self.myRatioBid = bid
        self.myRatioOffer = offer
        self.tradeSize = size

    def setMyRatioBid(self, myRatioBid):
        self.myRatioBid = myRatioBid

    def setMyRatioOffer(self, myRatioOffer):
        self.myRatioOffer = myRatioOffer

    def goRobot(self):
        self.mdOutput()
        self.ratioCalc()
        self.printLineRatio()
        self.updateBook()
        self.tradePlan()
        self.balanceBook()

    def printLineRatio(self):

        print("cR2t*","Bid/Offer (", self.myRatioBid, "-", self.myRatioOffer,")", round(self.ratioBidPrice, 2), "/", round(self.ratioOfferPrice, 2),
              " SIZE:", self.availableBid, "/", self.availableOffer)

    def ratioCalc(self):
        try:

            if self.getOfferPrice(self.symbols[0]) > 0:
                self.ratioBidPrice = self.getBidPrice(self.symbols[1]) / self.getOfferPrice(self.symbols[0])

                if self.getBidPrice(self.symbols[1]) > 0:
                    self.availableBid = min(self.getBidSize(self.symbols[1]), self.getOfferSize(self.symbols[0]))

            if self.getBidPrice(self.symbols[0]) > 0:
                self.ratioOfferPrice = self.getOfferPrice(self.symbols[1]) / self.getBidPrice(self.symbols[0])

                if self.getOfferPrice(self.symbols[1]) > 0:
                    self.availableOffer = min(self.getOfferSize(self.symbols[1]), self.getBidSize(self.symbols[0]))

        except:
            "CR2t* - Some Error ...."

    def tradePlan(self):
        print("In trade plan...")
        self.availableOffer = int(round(self.availableOffer, 0))
        self.availableBid = int(round(self.availableBid, 0))

        if self.myRatioBid > self.ratioOfferPrice > 0:
            print("Buy the ratio ")
            try:
                t0Contracts = int(
                    round(
                        self.getOfferPrice(self.symbols[1]) * self.availableOffer
                        * self.getContractMultiplier(self.symbols[1])
                        / (self.getBidPrice(self.symbols[0]) * self.getContractMultiplier(self.symbols[0]))
                        , 0)
                )

                self.tradeRatio(self.symbols[1], self.getOfferPrice(self.symbols[1]), min(self.availableOffer, self.tradeSize), self.symbols[0], self.getBidPrice(self.symbols[0]), min(t0Contracts,self.tradeSize))
                self.resetBidOffer(0.997, 0.997)

            except:
                print("error en Buy the Ratio")

        if self.ratioBidPrice > self.myRatioOffer > 0:
            print("Sell the ratio ")
            print("***", self.myRatioOffer, self.ratioBidPrice)
            try:
                t0Contracts = int(round(self.getBidPrice(self.symbols[1]) * self.availableBid*self.getContractMultiplier(self.symbols[1]) / (self.getOfferPrice(self.symbols[0]) * self.getContractMultiplier(self.symbols[0])), 0))

                self.tradeRatio(self.symbols[0], self.getOfferPrice(self.symbols[0]), min(t0Contracts, self.tradeSize),
                                self.symbols[1], self.getBidPrice(self.symbols[1]), min(self.availableOffer, self.tradeSize))
                self.resetBidOffer(1.003, 1.003)

            except:
                print("error en Sell the Ratio")

    def resetBidOffer(self, factorDown, factorUp):
        self.myRatioBid *= factorDown
        self.myRatioOffer *= factorUp

    def tradeRatio(self, buyTicker, buyPrice, buyContracts, sellTicker, sellPrice, sellContracts):
        self.singleTrade("BUY", buyTicker, str(buyPrice), str(int(buyContracts)))
        self.singleTrade("SELL", sellTicker, str(sellPrice), str(int(sellContracts)))


if __name__ == '__main__':
    print("cRatio Main")

    # El algoRatio hace el 2do ticker / el primero, o sea el primer ticker es el de USD
    ticker1 = "DOJun19"
    ticker2 = "RFX20Jun19"

    # ticker1 = "AY24DJun19"
    # ticker2 = "AY24Jun19"
    myBid   = 0
    myOffer = 0
    tradeContracts = 5
    maxExposition = 100
    suscriptTuple = (ticker1, ticker2)

    r2tickets = cRatio(suscriptTuple, myBid, myOffer, tradeContracts, maxExposition, "cRatioTicker")
    r2tickets.start()


else:
    pass