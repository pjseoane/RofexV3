
class cGoRobot():
    def __init__(self,marketDataDictionary):
        self.marketDataDictionary=marketDataDictionary

    def RobOutput(self):

        for sym in self.marketDataDictionary:
            print ("ticker from goRobot Class: ",sym)
            # print(sym, "    ", self.getBidPrice(sym), "/", self.getOfferPrice(sym), "----------", self.getBidSize(sym),
            #       "/", self.getOfferSize(sym))
            # print(sym, "Low limit: ", self.getContractLowLimit(sym), "High Limit: ", self.getContractHighLimit(sym),
            #       "Maturity: ", self.getMaturityDate(sym))
