
# from Classes import cGetMarketData as md
from Robots import cZrobot as zR


class cBookAnalysis (zR.zRobot):

    def __init__(self, symbols):
        super().__init__(symbols)

        # self.bookFilled = {}


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

