from typing import Any, Union

from Robots import cZrobot as ratioR
from Classes import cGetMarketData as md


class cRatio(md.cGetMarketData):

    t0BidPrice: float
    t1BidPrice: float

    t0offerPrice: float
    t1OfferPrice: float

    t0OfferSize: int
    t1OfferSize: int

    t0BidSize: int
    t1BidSize: int

    t0Multiplier: int
    t1Multiplier: int

    def __init__(self, symbols, myRatioBid, myRatioOffer, tradeSize, exposition, algoName):

        super().__init__(symbols)

        self.algoAlive= True
        self.myRatioBid = myRatioBid
        self.myRatioOffer = myRatioOffer
        self.tradeSize = tradeSize
        self.exposition = exposition
        #self.algoName = algoName

        self.ratioBidPrice = 0
        self.ratioOfferPrice = 0

        self.availableBid: int = 0
        self.availableOffer: int = 0

        self.t1Position = 0
        self.t0Position = 0
        self.sumt1Value = 0
        self.sumt0Value = 0
        self.openAvgPrice = 0



        print("***********  Running Algo", algoName)

    def setMyRatioBid(self, myRatioBid):
        self.myRatioBid = myRatioBid

    def setMyRatioOffer(self, myRatioOffer):
        self.myRatioOffer = myRatioOffer

    def goRobot(self):
        self.mdOutput()
        self.getTickerValues()
        self.ratioCalc()
        self.printLineRatio()
        self.updateBook()
        self.tradePlan()
        self.balanceBook()

    def printLineRatio(self):

        print("Bid/Offer (", self.myRatioBid,"-",self.myRatioOffer,")", round(self.ratioBidPrice, 2), "/", round(self.ratioOfferPrice, 2),
              " SIZE:", self.availableBid, "/", self.availableOffer)

    def getTickerValues(self):
        self.t0Multiplier = self.getContractMultiplier(self.symbols[0])
        self.t1Multiplier = self.getContractMultiplier(self.symbols[1])

        self.t0BidPrice = self.getBidPrice(self.symbols[0])
        self.t0BidSize = self.getBidSize(self.symbols[0])
        self.t0offerPrice = self.getOfferPrice(self.symbols[0])
        self.t0OfferSize = self.getOfferSize(self.symbols[0])

        self.t1BidPrice = self.getBidPrice(self.symbols[1])
        self.t1BidSize = self.getBidSize(self.symbols[1])
        self.t1OfferPrice = self.getOfferPrice(self.symbols[1])
        self.t1OfferSize = self.getOfferSize(self.symbols[1])

    def ratioCalc(self):
        try:

            if self.t0offerPrice > 0:
                self.ratioBidPrice = self.t1BidPrice / self.t0offerPrice

                if self.t1BidPrice > 0:
                    self.availableBid = int(round(min(self.t1BidSize * self.t1Multiplier * self.t1BidPrice,
                                                  self.t0offerPrice * self.t0Multiplier * self.t0OfferSize) \
                                        / self.t1BidPrice,0))

            if self.t0BidPrice > 0:
                self.ratioOfferPrice = self.t1OfferPrice / self.t0BidPrice

                if self.t1OfferPrice > 0:
                    self.availableOffer = int(round(min(self.t1OfferPrice * self.t1Multiplier * self.t1OfferSize, self.t0BidSize * self.t0Multiplier * self.t0BidPrice)\
                                          / self.t1OfferPrice, 0))

        except:
            "cRatio - Some Error ...."

    def tradePlan(self):
        print("In trade plan...")
        self.availableOffer = int(round(self.availableOffer, 0))
        self.availableBid = int(round(self.availableBid, 0))

        if self.myRatioBid > self.ratioOfferPrice > 0:
            print("Buy the ratio ")
            t0Contracts = int(round(self.t1OfferPrice * self.availableOffer *self.t1Multiplier / (self.t0BidPrice * self.t0Multiplier),0))

            self.tradeContracts(self.symbols[1], self.t1OfferPrice, min(self.availableOffer, self.tradeSize), self.symbols[0], self.t0BidPrice, min(t0Contracts,self.tradeSize))
            self.setMyRatioBid(self.myRatioBid * 0.997)

        if self.t0BidPrice > self.myRatioOffer and self.t0BidPrice > 0:
            print("Sell the ratio ")
            t0Contracts = int(round(self.t1BidPrice * self.availableBid*self.t1Multiplier / (self.t0offerPrice * self.t0Multiplier), 0))

            self.tradeContracts(self.symbols[0], self.t0offerPrice, min(t0Contracts, self.tradeSize),
                                self.symbols[1], self.t1BidPrice, min(self.availableOffer, self.tradeSize))

            self.setMyRatioOffer(self.myRatioOffer * 1.003)

    def tradeContracts(self, buyTicker, buyPrice, buyContracts, sellTicker, sellPrice, sellContracts):
        self.singleTrade("BUY", buyTicker, str(buyPrice), str(int(buyContracts)))
        self.singleTrade("SELL", sellTicker, str(sellPrice), str(int(sellContracts)))


if __name__ == '__main__':
    print("cRatio Main")
    ticker1 = "DOJun19"
    ticker2 = "RFX20Jun19"
    myBid   = 930
    myOffer = 940
    tradeContracts = 5
    maxExposition = 100
    suscriptTuple = (ticker1, ticker2)

    r2tickets = cRatio(suscriptTuple, myBid, myOffer, tradeContracts, maxExposition, "Index -> USD")
    r2tickets.start()


else:
    pass