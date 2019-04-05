# Robot Zero, basico solo suscribe una tupla de symbols y los displaya
#Los demas heredan de este


from Classes import cGetMarketData as md


class zRobot (md.cGetMarketData):

    def __init__(self, symbols):
        super().__init__(symbols)

    def goRobot(self): # Overridable method, cada robot implementa el suyo
        pass

    def mdOutput(self):
        # print ("En zRobot")
        if self.marketDataDict.__len__() == len(self.symbols):
            print("Dictionary completed")
            for sym in self.symbols:
                print(sym,
                      "    Bid/Ask :", round(self.getBidPrice(sym), 2), "/", round(self.getOfferPrice(sym), 2),
                      "    Last :", round(self.getLastPrice(sym), 2),
                      "    Size :", self.getBidSize(sym), "/", self.getOfferSize(sym))
                # print("Dictionary market close: ",self.marketCloseData [sym])

        else:
            print("Dictionary not completed yet....")

    def getFullMD(self, ticker, depth):
        return self.getMarketData('ROFX', ticker, 'BI', 'OF', 'LA', 'OP', 'CL', 'SE', 'OI', depth)

    def getContractMultiplier(self, ticker):
        return self.contractDetail[ticker]['instrument']['contractMultiplier']

    def getContractLowLimit(self, ticker):
        return self.contractDetail[ticker]['instrument']['lowLimitPrice']

    def getContractHighLimit(self, ticker):
        return self.contractDetail[ticker]['instrument']['highLimitPrice']

    def getContractMinPriceIncrement(self, ticker):
        return self.contractDetail[ticker]['instrument']['minPriceIncrement']

    def getContractMultiplier(self, ticker):
        return self.contractDetail[ticker]['instrument']['contractMultiplier']

    def getMaturityDate(self, ticker):
        return self.contractDetail[ticker]['instrument']['maturityDate']

    def getBidPrice(self, ticker):
        try:
            m = self.marketDataDict[ticker]['marketData']['BI'][0]['price']
        except:
            m = 0
        return m

    def getBidSize(self, ticker):
        try:
            m = self.marketDataDict[ticker]['marketData']['BI'][0]['size']
        except:
            m = 0
        return m

    def getOfferPrice(self, ticker):
        try:
            m = self.marketDataDict[ticker]['marketData']['OF'][0]['price']
        except:
            m = 0
        return m

    def getOfferSize(self, ticker):
        try:
            m = self.marketDataDict[ticker]['marketData']['OF'][0]['size']
        except:
            m = 0
        return m

    def getLastPrice(self, ticker):
        try:
            m = self.marketCloseData[ticker]['marketData']['LA']['price']
        except:
            m = 0
        return m

if __name__ == '__main__':

    ticker1 = "DOJun19"
    ticker2 = "RFX20Jun19"
    suscriptTuple = (ticker1, ticker2)
    suscription = zRobot(suscriptTuple)
    suscription.start()
    suscription.mdOutput()
    print("High Limit: ", ticker1, suscription.getContractHighLimit(ticker1))

else:
    pass