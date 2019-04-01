from Classes import cAlgoBase as alg


class cAlgoIndex(alg.cAlgoBase):
    def __init__ (self, marketDataDictionary, symbols):

        super().__init__(marketDataDictionary)

        self.symbols=symbols

        self.indexBid = 0
        self.indexOffer = 0
        self.indexBidSize = 0
        self.indexOfferSize = 0
        self.availableBid = 0
        self.availableOffer=0
        self.midMarket=0

    def indexOutput(self):
        print ("En cGoRobotIndex")
        for sym in self.symbols:
            print ("ticker from cAlgoIndex: ",sym)
            print(sym, "    ", self.getBidPrice(sym), "/", self.getOfferPrice(sym), "----------", self.getBidSize(sym),
                   "/", self.getOfferSize(sym))

    def indexCalc(self):
        usd=self.symbols[0]
        index=self.symbols[1]
        # symbols[1] = Index


        if self.getOfferPrice(usd) !=0:
            self.indexBid = self.getBidPrice(index)/self.getOfferPrice(usd)

        if self.getBidPrice(usd) !=0:
            self.indexOffer = self.getOfferPrice(index)/self.getBidPrice(usd)

        if self.getOfferPrice(usd) !=0 and self.getBidPrice(index) !=0:
            self.availableBid = min(self.getBidPrice(index)*self.getBidSize(index)/self.getOfferPrice(usd)/1000,
                                      self.getOfferPrice(usd)*self.getOfferSize(usd)*1000/self.getBidPrice(index))

        if self.getBidPrice(usd) !=0 and self.getOfferPrice(index) !=0:
            self.availableOffer = min(self.getOfferPrice(index)*self.getOfferSize(index)/self.getBidPrice(usd)/1000,
                                            self.getBidPrice(usd)*self.getBidSize(usd)*1000/self.getOfferPrice(index))

        self.midMarket = (self.indexBid + self.indexOffer) / 2

        print ("Index in USD: ",self.indexBid, "/", self.indexOffer,"size :",self.availableBid , "x",self.availableOffer,"----->",str(round(self.midMarket*0.995,2)),"/",str(round(self.midMarket*1.005,2))," SIZE:----> " ,str(round(self.availableBid,0)),"xx",str(round(self.availableOffer,0)))
