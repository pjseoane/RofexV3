

from Robots import cRatio2Tickers as r2t


class cAY24ccl(r2t.cRatio):

    def __init__(self, symbols, myRatioBid, myRatioOffer, tradeSize, exposition, algoName):

        super().__init__(symbols, myRatioBid, myRatioOffer, tradeSize, exposition, algoName)

    def goRobot(self):
        # Se puede definir cada funcion o hacer override para cada spread en particular
        self.mdOutput()
        self.ratioCalc()
        self.printLineRatio()
        # self.updateBook()
        self.testMyMarket()
        self.balanceBook()

    def buyTheRatio(self):
        print(self.algoName, "*", "Buy the ratio ")
        try:
            t0Contracts = int(
                round(
                    self.getOfferPrice(self.symbols[1]) * self.availableOffer
                    * self.getContractMultiplier(self.symbols[1])
                    / (self.getBidPrice(self.symbols[0]) * self.getContractMultiplier(self.symbols[0]))
                    , 0)
            )

            self.tradeRatio(self.symbols[1], self.getOfferPrice(self.symbols[1]),
                            min(self.availableOffer, self.tradeSize), self.symbols[0],
                            self.getBidPrice(self.symbols[0]), min(t0Contracts, self.tradeSize))
            self.resetBidOffer(0.997, 0.997)
            self.updateBook()

        except:
            print("cRUSDIndx* error en Buy the Ratio")



    def sellTheRatio(self):
        print("self.algoName", "*", "Sell the ratio ")
        print("self.algoName", "*", self.myRatioOffer, self.ratioBidPrice)
        try:
            t0Contracts = int(round(
                self.getBidPrice(self.symbols[1]) * self.availableBid * self.getContractMultiplier(self.symbols[1]) / (
                            self.getOfferPrice(self.symbols[0]) * self.getContractMultiplier(self.symbols[0])), 0))

            self.tradeRatio(self.symbols[0], self.getOfferPrice(self.symbols[0]), min(t0Contracts, self.tradeSize),
                            self.symbols[1], self.getBidPrice(self.symbols[1]),
                            min(self.availableOffer, self.tradeSize))
            self.resetBidOffer(1.003, 1.003)

        except:
            print("self.algoName", "*", " error en Sell the Ratio")


    
if __name__ == '__main__':
    print("AY24 CCL")

    # El algoRatio hace el 2do ticker / el primero, o sea el primer ticker es el de USD
    ticker1 = "AY24DJun19"
    ticker2 = "AY24Jun19"
    myBid   = 0
    myOffer = 0
    tradeContracts = 5
    maxExposition = 100
    suscriptTuple = (ticker1, ticker2)

    ccl1 = cAY24ccl(suscriptTuple, myBid, myOffer, tradeContracts, maxExposition, "AY24 CCL")
    ccl1.start()


else:
    pass