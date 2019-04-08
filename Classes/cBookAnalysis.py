
# from Classes import cGetMarketData as md
from Robots import cZrobot as zR

class cBookAnalysis (zR.zRobot):

    def __init__(self, symbols):
        super().__init__(symbols)


    def getSUMContractsOpenOrders(self, ticker):
        contratos = 0

        try:
            dOpenOrders = self.getOrdenesOpen(self.account)['orders']
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
            dOpenOrders=self.getOrdenesOpen(self.account)['orders']
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
    suscription = cBookAnalysis(suscriptTuple)
    suscription.start()
    suscription.mdOutput()
    obf = suscription.getOrdenesAll(suscription.account)

    # print("High Limit: ", ticker1, suscription.getContractHighLimit(ticker1))
    print("Order Book All:", suscription.getOrdenesAll(suscription.account))
    print("Order Book Open:", suscription.getOrdenesOpen(suscription.account))
    print("Order Book Filled:", suscription.getOrdenesFilled(suscription.account))
    # print("Filled Orders function", suscription.getFilledOrders(ticker1))
    print("Open Contracts / Value", suscription.getSUMContractsOpenOrders(ticker1), suscription.getSUMValueOpenOrders(ticker1))

    # msg = simplejson.loads(message)
else:
    pass

