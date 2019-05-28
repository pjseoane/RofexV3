import websocket
import threading
import simplejson

from Classes import cRofexLoginWS as rLogin
from time import sleep


class cGetMarketData(rLogin.cSetUpEnvironment):

    def __init__(self, symbols):
        super().__init__()

        self.symbols = symbols
        self.sym = ""
        self.ws = websocket.WebSocketApp
        self.numMessages = 0
        self.marketDataDict = {}
        self.contractDetail = {}
        self.marketCloseData = {}

        # self.runWS()

    def start(self):
        self.runWS()

    def runWS(self):
        headers = {'X-Auth-Token:{token}'.format(token=self.token)}
        self.ws = websocket.WebSocketApp(self.activeWSEndpoint,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close,
                                         on_open=self.on_open,
                                         header=headers)

        wst = threading.Thread(target=self.ws.run_forever, kwargs={"ping_interval": 5})
        wst.start()
        # Esperamos a que la conexion ws se establezca
        conn_timeout = 5
        # conn_timeout = 50 #y nada
        sleep(1)

        while not self.ws.sock.connected and conn_timeout:
            sleep(1)
            conn_timeout -= 1
        else:

            for self.sym in self.symbols:

                # Arma diccionario de detalles contratos para este Algo
                self.contractDetail[self.sym] = self.instrumentDetail(self.sym, 'ROFX')
                self.marketCloseData[self.sym] = self.getMarketData('ROFX', self.sym,
                                                                "LA", "CL", "SE", "OI", "", "", "", str(1))
                self.ws.send(self.buildMessage)

                print("cGetMarketData - Sent Suscription msg for: ", self.sym)
                sleep(1)

    def on_message(self, message):
        self.numMessages += 1

        try:
            msg = simplejson.loads(message)
            msgType = msg['type'].upper()

            if msgType == 'MD':
                # print("cgetMarketData New msg MD->: ", msg)
                # Arma y carga el Dictionary
                # Busca de que sym es el mensaje que viene y lo coloca en el Dictionary
                self.marketDataDict[msg['instrumentId']['symbol']] = msg

                if self.marketDataDict.__len__() == len(self.symbols):
                    print("cGetMarketData - Dict OK, New Msg")
                    try:
                        self.goRobot()
                    except:
                        print("Problem in goRobot()")

                # else:
                #     print("cGetMarketData - Dictionary not completed yet....")

            elif msgType == 'OR':
                print("En Mensaje OR")
                print(msg)
            else:
                print("Tipo de Mensaje Recibido No soportado: ", msg)

        except:
            print("Error al procesar mensaje recibido:--->>> ", message)

    def on_error(self, error):
        print("Salio por error: ", error)
        self.ws.close()

    @staticmethod
    def on_close():
        print("### connection closed ###")

    @staticmethod
    def on_open():
        # pass
        print("WS Conection Open...")

    @property
    def buildMessage(self):
        # 'BI', 'OF', 'LA', 'OP', 'CL', 'SE', 'OI'
        return "{\"type\":\"" + self.type_ + "\",\"level\":" + self.level_ +\
               ", \"entries\":[\"BI\", \"OF\",\"LA\"],\"products\":[{\"symbol\":\"" +\
               self.sym + "\",\"marketId\":\"" + self.marketId_ + "\"}]}"

    def goRobot(self):
        # Overridable Method
        pass

    def mdOutput(self):

        for sym in self.symbols:
            print("cGetMarketData*", sym,
                        "    Bid/Ask :", round(self.getBidPrice(sym), 2), "/", round(self.getOfferPrice(sym), 2),
                        "    Last :", round(self.getLastPrice(sym), 2),
                        "    Size :", self.getBidSize(sym), "/", self.getOfferSize(sym))

    def getFullMD(self, ticker, depth):
        return self.getMarketData('ROFX', ticker, 'BI', 'OF', 'LA', 'OP', 'CL', 'SE', 'OI', depth)

    def getContractMultiplier(self, ticker):
        return self.contractDetail[ticker]['instrument']['contractMultiplier']

    def getContractLowLimit(self, ticker):
        return self.contractDetail[ticker]['instrument']['lowLimitPrice']

    def getContractHighLimit(self, ticker):
        return self.contractDetail[ticker]['instrument']['highLimitPrice']

    def getContractMinPriceIncrement(self, ticker):
        return self.contractDetail[ticker]['instrument']['minPriceIncrement']

    def getMaturityDate(self, ticker):
        return self.contractDetail[ticker]['instrument']['maturityDate']

    def getBidPrice(self, ticker):
        try:
            m = self.marketDataDict[ticker]['marketData']['BI'][0]['price']
        except:
            m = 0
        return m

    def getBidSize(self, ticker) -> int:
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

    def getLastPrice(self, ticker):
        try:
            m = self.marketCloseData[ticker]['marketData']['LA']['price']
        except:
            m = 0
        return m

    def singleTrade(self, side, ticker, price, cant):
        self.newSingleOrder(self.marketId_, ticker, price, cant, "LIMIT", side, "DAY", self.account, "FALSE")


if __name__ == '__main__':

    ticker1 = "DOJun19"
    ticker2 = "RFX20Jun19"
    suscriptTuple = (ticker1, ticker2)
    suscrip = cGetMarketData(suscriptTuple)
    suscrip.start()
    suscrip.mdOutput()

    print("High Limit: ", ticker1, suscrip.getContractHighLimit(ticker1))
    print("High Limit: ", ticker2, suscrip.getContractHighLimit(ticker2))
    print("Multiplier: ", ticker1, suscrip.getContractMultiplier(ticker1))
    print("Multiplier: ", ticker2, suscrip.getContractMultiplier(ticker2))

    # suscrip.start()

else:
    pass
