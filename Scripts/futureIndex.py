from Classes import cBasicRobot as rob


ticker1 = "DOJun19"
ticker2 = "RFX20Jun19"
suscriptTuple = (ticker1, ticker2)
rob1=rob.cFutureIndex(suscriptTuple)
rob1.start()


