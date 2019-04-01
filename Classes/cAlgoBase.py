
class cAlgoBase:
    def __init__(self, marketDataDictionary):

        self.marketDataDict=marketDataDictionary

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

# faltan definir las otras funciones para obtener mas data del dictionary