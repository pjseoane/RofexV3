from Robots import cAY24ccl as ccl

print("AY24 CCL")

# El algoRatio hace el 2do ticker / el primero, o sea el primer ticker es el de USD
ticker1 = "AY24DJun19"
ticker2 = "AY24Jun19"
myBid = 0
myOffer = 0
tradeContracts = 5
maxExposition = 100
suscriptTuple = (ticker1, ticker2)

ccl1 = ccl.cAY24ccl(suscriptTuple, myBid, myOffer, tradeContracts, maxExposition, "AY24 CCL")
ccl1.start()
