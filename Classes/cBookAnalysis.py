
# from Classes import cGetMarketData as md
from Robots import cZrobot as zR


class cBookAnalysis (zR.zRobot):

    def __init__(self, symbols):
        super().__init__(symbols)

        self.bookFilled = {}

    def updateBook(self):
        print ("In updateBook :")

        for sym in self.symbols:
            filledContracts = self.getFilledContracts(sym)
            filledValue = self.getFilledValue(sym)/self.getContractMultiplier(sym)

            self.bookFilled['symbol'] = sym
            self.bookFilled['contracts'] = filledContracts
            self.bookFilled['avg'] = filledValue / filledContracts

            print("Ticker :", sym, "Contracts: ", self.bookFilled['contracts'], "Avg :", self.bookFilled['avg'])
            #print("Dict   :", self.bookFilled)

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
                    # sum += x['orderQty'] * x['price'] * mult

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


if __name__ == '__main__':

    ticker1 = "DOJun19"
    ticker2 = "RFX20Jun19"
    suscriptTuple = (ticker1, ticker2)
    suscription = cBookAnalysis(suscriptTuple)
    suscription.start()
    suscription.mdOutput()
    obf = suscription.getOrdenesAll(suscription.account)

    # print("High Limit: ", ticker1, suscription.getContractHighLimit(ticker1))
    # print("Order Book All:", suscription.getOrdenesAll(suscription.account))
    # print("Order Book Open:", suscription.getOrdenesOpen(suscription.account))
    # print("Order Book Filled:", suscription.getOrdenesFilled(suscription.account))
    # # print("Filled Orders function", suscription.getFilledOrders(ticker1))
    # print("Open Contracts / Value: ", ticker1, suscription.getSUMContractsOpenOrders(ticker1), suscription.getSUMValueOpenOrders(ticker1))

    suscription.updateBook()

    # msg = simplejson.loads(message)
else:
    pass

