from Robots import indexUSD as rob

ticker1 = "DOJun19"
ticker2 = "RFX20Jun19"
myBid = 900
myOffer = 910
suscriptTuple = (ticker1, ticker2)
rob = rob.indexUSD(suscriptTuple, myBid, myOffer)
# TODO: Al constructor agregar parametros de limit vol a acumular en exposicion
rob.start()


