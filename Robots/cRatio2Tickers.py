from typing import Any, Union

from Robots import cZrobot as masterR
from Classes import cGetMarketData as md


class cRatio(masterR.zRobot):

    # t0BidPrice: float
    # t1BidPrice: float
    #
    # t0offerPrice: float
    # t1OfferPrice: float
    #
    # t0OfferSize: int
    # t1OfferSize: int
    #
    # t0BidSize: int
    # t1BidSize: int
    #
    # t0Multiplier: int
    # t1Multiplier: int

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

        print("***********  Running Algo", self.algoName)

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

        print("Bid/Offer (", self.myRatioBid, "-", self.myRatioOffer,")", round(self.ratioBidPrice, 2), "/", round(self.ratioOfferPrice, 2),
              " SIZE:", self.availableBid, "/", self.availableOffer)

    def getTickerValues(self):
        pass
        # self.t0Multiplier = self.getContractMultiplier(self.symbols[0])
        # self.t1Multiplier = self.getContractMultiplier(self.symbols[1])

        # self.t0BidPrice = self.getBidPrice(self.symbols[0])
        # self.t0BidSize = self.getBidSize(self.symbols[0])
        # self.t0offerPrice = self.getOfferPrice(self.symbols[0])
        # self.t0OfferSize = self.getOfferSize(self.symbols[0])
        #
        # self.t1BidPrice = self.getBidPrice(self.symbols[1])
        # self.t1BidSize = self.getBidSize(self.symbols[1])
        # self.t1OfferPrice = self.getOfferPrice(self.symbols[1])
        # self.t1OfferSize = self.getOfferSize(self.symbols[1])

    def ratioCalc(self):
        try:

            if self.getOfferPrice(self.symbols[0]) > 0:
                self.ratioBidPrice = self.getBidPrice(self.symbols[1]) / self.getOfferPrice(self.symbols[0])

                if self.getBidPrice(self.symbols[1]) > 0:
                    self.availableBid = min(self.getBidSize(self.symbols[1]), self.getOfferSize(self.symbols[0]))
                    # self.availableBid = int(
                    # round(
                    # min(self.getBidSize(self.symbols[1]) * self.getContractMultiplier(self.symbols[1])
                    # * self.getBidPrice(self.symbols[1]),
                    # self.getOfferPrice(self.symbols[0]) * self.getContractMultiplier(self.symbols[0]) *
                    # self.getOfferSize(self.symbols[0])) \
                    # / self.getBidPrice(self.symbols[1]), 0))

            if self.getBidPrice(self.symbols[0]) > 0:
                self.ratioOfferPrice = self.getOfferPrice(self.symbols[1]) / self.getBidPrice(self.symbols[0])

                if self.getOfferPrice(self.symbols[1]) > 0:
                    self.availableOffer = min(self.getOfferSize(self.symbols[1]), self.getBidSize(self.symbols[0]))
                    # self.availableOffer = int(round(min(self.getOfferPrice(self.symbols[1]) * self.getContractMultiplier(self.symbols[1]) * self.getOfferSize(self.symbols[1]), self.getBidSize(self.symbols[0]) * self.getContractMultiplier(self.symbols[0]) * self.getBidPrice(self.symbols[0]))\
                    #                       / self.getOfferPrice(self.symbols[1]), 0))

        except:
            "cRatio - Some Error ...."

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
                        *self.getContractMultiplier(self.symbols[1])
                        / (self.getBidPrice(self.symbols[0]) * self.getContractMultiplier(self.symbols[0]))
                        , 0)
                )

                self.tradeRatio(self.symbols[1], self.getOfferPrice(self.symbols[1]), min(self.availableOffer, self.tradeSize), self.symbols[0], self.getBidPrice(self.symbols[0]), min(t0Contracts,self.tradeSize))
                self.resetBidOffer(0.997, 0.997)

            except:
                print("error en Buy the Ratio")

        if self.myRatioOffer < self.ratioBidPrice > 0:
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
    myBid   = 900
    myOffer = 990
    tradeContracts = 5
    maxExposition = 100
    suscriptTuple = (ticker1, ticker2)

    r2tickets = cRatio(suscriptTuple, myBid, myOffer, tradeContracts, maxExposition, "Index -> USD")
    r2tickets.start()


else:
    pass