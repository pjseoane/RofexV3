# Robot Zero, basico solo suscribe una tupla de symbols y los displaya
#Los demas heredan de este


from Classes import cGetMarketData as md


class zRobot (md.cGetMarketData):

    def __init__(self, symbols):
        super().__init__(symbols)

        self.bookBySymbol = {}

    def goRobot(self):  # Overridable method, cada robot implementa el suyo
        pass

    def mdOutput(self):
        # if self.marketDataDict.__len__() == len(self.symbols):
            #print("Dictionary completed")
            for sym in self.symbols:
                print("zRobot", sym,
                      "    Bid/Ask :", round(self.getBidPrice(sym), 2), "/", round(self.getOfferPrice(sym), 2),
                      "    Last :", round(self.getLastPrice(sym), 2),
                      "    Size :", self.getBidSize(sym), "/", self.getOfferSize(sym))
                # print("Dictionary market close: ",self.marketCloseData [sym])

        # else:
        #     print("Dictionary not completed yet....")

    def singleTrade(self, side, ticker, price, cant):
        self.newSingleOrder(self.marketId_, ticker, price, cant, "LIMIT", side, "DAY", self.account, "FALSE")

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

    def getSUMContractsOpenOrders(self, ticker):
        contratos = 0

        try:
            dOpenOrders = self.getOrdenesOpen(suscription.account)['orders']
            for x in dOpenOrders:
                mult = 1
                if x['instrumentId']['symbol'] == ticker:
                    if x['side'] == 'SELL':
                        mult = -1

                    contratos += x['orderQty'] * mult
                    # sum += x['orderQty'] * x['price'] * mult

            return contratos
        except:
            print("Error getSUMContractsOpenOrders")
            pass

    def getSUMValueOpenOrders(self, ticker):
        contratos=0
        sum=0

        try:
            dOpenOrders=self.getOrdenesOpen(suscription.account)['orders']
            for x in dOpenOrders:
                mult = 1
                if x['instrumentId']['symbol'] == ticker:
                    if x['side'] == 'SELL':
                        mult = -1

                    contratos += x['orderQty']*mult
                    sum += x['orderQty'] * self.getContractMultiplier(ticker) * x['price'] * mult

            return sum

        except:
            print("Error getSUMValueOpenOrders")
            pass


if __name__ == '__main__':

    ticker1 = "DOJun19"
    ticker2 = "RFX20Jun19"
    suscriptTuple = (ticker1, ticker2)
    suscription = zRobot(suscriptTuple)
    # suscription.start()
    suscription.mdOutput()
    # obf = suscription.getOrdenesAll(suscription.account)

    print("High Limit: ", ticker1, suscription.getContractHighLimit(ticker1))
    print("High Limit: ", ticker2, suscription.getContractHighLimit(ticker2))
    print("Multiplier: ", ticker1,  suscription.getContractMultiplier(ticker1))
    print("Multiplier: ", ticker2, suscription.getContractMultiplier(ticker2))


    print("Order Book All:", suscription.getOrdenesAll(suscription.account))
    print("Order Book Open:", suscription.getOrdenesOpen(suscription.account))
    print("Order Book Filled:", suscription.getOrdenesFilled(suscription.account))
    # print("Filled Orders function", suscription.getFilledOrders(ticker1))
    print("Open Contracts / Value", suscription.getSUMContractsOpenOrders(ticker1), suscription.getSUMValueOpenOrders(ticker1))





    # msg = simplejson.loads(message)
else:
    pass