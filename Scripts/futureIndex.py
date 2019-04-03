from Robots import indexUSD as rob

ticker1 = "DOJun19"
ticker2 = "RFX20Jun19"
myBid = 950
myOffer = 964
suscriptTuple = (ticker1, ticker2)
rob = rob.indexUSD(suscriptTuple, myBid, myOffer)
rob.start()


