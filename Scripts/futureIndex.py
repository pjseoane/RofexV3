from Robots import indexUSD as rob

ticker1 = "DOJun19"
ticker2 = "RFX20Jun19"
myBid = 934
myOffer = 945
suscriptTuple = (ticker1, ticker2)
rob = rob.indexUSD(suscriptTuple, myBid, myOffer)
# TODO: Al constructor agregaar parametros de limit vol a acumular en exposicion
rob.start()


