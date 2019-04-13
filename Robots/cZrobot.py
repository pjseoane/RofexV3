# Robot Zero, basico solo suscribe una tupla de symbols y los displaya
#Los demas heredan de este


from Classes import cGetMarketData as md


class zRobot (md.cGetMarketData):

    def __init__(self, symbols, algoName):
        super().__init__(symbols)

        self.algoName = algoName
        self.bookFilled = {}
        self.netExposition = 0
        self.algoAlive = True

    def goRobot(self):  # Overridable method, cada robot implementa el suyo
        pass

    def updateBook(self):
        print("In updateBook :")
        self.netExposition = 0

        for sym in self.symbols:
            filledContracts = self.getFilledContracts(sym)
            filledV = self.getFilledValue(sym)
            filledValue = filledV/self.getContractMultiplier(sym)
            self.netExposition += filledV

            if filledContracts:
                self.bookFilled['symbol'] = sym
                self.bookFilled['contracts'] = filledContracts
                self.bookFilled['avg'] = filledValue / filledContracts

                print("Ticker :", sym, "Contracts: ", self.bookFilled['contracts'], "Avg :", self.bookFilled['avg'])

            else:
                print(sym ,"...empty book")

    def getFilledContracts(self, ticker):
        contratos = 0

        try:
            bookFilled = self.getOrdenesFilled(self.account)['orders']
            for order in bookFilled:
                mult = 1
                if order['instrumentId']['symbol'] == ticker:
                    if order['side'] == 'SELL':
                        mult = -1

                    contratos += order['orderQty'] * mult

            return contratos
        except:
            print("Error getFilledContracts")
            pass

    def getFilledValue(self, ticker):
        contratos = 0
        sum = 0

        try:
            bookFilled = self.getOrdenesFilled(self.account)['orders']
            for order in bookFilled:
                mult = 1
                if order['instrumentId']['symbol'] == ticker:
                    if order['side'] == 'SELL':
                        mult = -1

                    contratos += order['orderQty'] * mult
                    sum += order['orderQty'] * self.getContractMultiplier(ticker) * order['price'] * mult
            return sum

        except:
            print("Error getFilledValue")
            pass

    def balanceBook(self):
        print("Net Exposition....... :", self.netExposition)

        try:
            if self.netExposition !=0:
                if self.netExposition < 0:
                    # buy 1st ticket
                    contractsToBalance = int(abs(self.netExposition/self.getContractMultiplier(self.symbols[0])/self.getOfferPrice(self.symbols[0])))
                    if contractsToBalance >0:
                        print("Contracts to Buy ...:", contractsToBalance)
                        self.singleTrade("BUY", self.symbols[0], str(self.getOfferPrice(self.symbols[0])), str(contractsToBalance))

                else:
                    # sell 1st ticket
                    contractsToBalance = int(abs(self.netExposition / self.getContractMultiplier(self.symbols[0]) / self.getBidPrice(self.symbols[0])))
                    if contractsToBalance > 0:
                        print("Contracts to Sell...:", contractsToBalance)
                        self.singleTrade("SELL", self.symbols[0], str(self.getBidPrice(self.symbols[0])), str(contractsToBalance))

        except:
            print("error en balanceBook")


if __name__ == '__main__':

    ticker1 = "DOJun19"
    ticker2 = "RFX20Jun19"
    suscriptTuple = (ticker1, ticker2)
    suscription = zRobot(suscriptTuple, "Robot Zero")
    # suscription.start()
    suscription.mdOutput()
    print(suscription.algoName)
    # obf = suscription.getOrdenesAll(suscription.account)

    print("Order Book All:", suscription.getOrdenesAll(suscription.account))
    print("Order Book Open:", suscription.getOrdenesOpen(suscription.account))
    print("Order Book Filled:", suscription.getOrdenesFilled(suscription.account))
    # print("Filled Orders function", suscription.getFilledOrders(ticker1))





    # msg = simplejson.loads(message)
else:
    pass