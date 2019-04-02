import websocket
import threading
import simplejson

from Classes import cRofexLogin as rLogin
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
        #self.runWS()

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
            self.suscribeTickers()

    def suscribeTickers(self):
        # overridable method
        #pass
        for self.sym in self.symbols:

            # Arma diccionario de detalles contratos para este Algo
            self.contractDetail[self.sym] = self.instrumentDetail(self.sym, 'ROFX')
            self.ws.send(self.buildMessage)
            print("Sent Suscription msg for ", self.sym)
            sleep(1)

    def on_message(self, message):
        self.numMessages += 1

        try:
            msg = simplejson.loads(message)
            msgType = msg['type'].upper()

            if msgType == 'MD':
                # Arma y carga el Dictionary
                self.sym = msg['instrumentId']['symbol']
                self.marketDataDict[self.sym] = msg

                self.goRobot()

            elif msgType == 'OR':
                print("En Mensaje OR")
                print(msg)
            else:
                print("Tipo de Mensaje Recibido No soportado: ", msg)

        except:
            print("Error al procesar mensaje recibido:--->>> ", msg)

    def on_error(self, error):
        print("Salio por error: ", error)
        self.ws.close()

    @staticmethod
    def on_close():
        print("### connection closed ###")

    def on_open(self):
        pass
        # print("WS Conection Open...")

    @property
    def buildMessage(self):
        return "{\"type\":\"" + self.type_ + "\",\"level\":" + self.level_ + ", \"entries\":[\"BI\", \"OF\"],\"products\":[{\"symbol\":\"" + self.sym + "\",\"marketId\":\"" + self.marketId_ + "\"}]}"

    def getContractLowLimit(self, ticker):
        return self.contractDetail[ticker]['instrument']['lowLimitPrice']

    def getContractHighLimit(self, ticker):
        return self.contractDetail[ticker]['instrument']['highLimitPrice']

    def getContractMinPriceIncrement(self, ticker):
        return self.contractDetail[ticker]['instrument']['minPriceIncrement']

    def getContractMultiplier(self, ticker):
        return self.contractDetail[ticker]['instrument']['contractMultiplier']

    def getMaturityDate(self, ticker):
        return self.contractDetail[ticker]['instrument']['maturityDate']

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

    def goRobot(self):
        # Overridable Method
        pass
        # # print("marketDataDict: ", self.marketDataDict)
        # # Chequer si el dictionary ya tiene tantos datos como symbols
        # if self.marketDataDict.__len__() == len(self.symbols):
        #
        #     try:
        #
        #         rob1 = cAlgoIndex.cAlgoIndex(self.marketDataDict, self.symbols)
        #         rob1.indexOutput()
        #         rob1.indexCalc()
        #
        #     except:
        #         #pass
        #         print("Error goRobot()")


if __name__ == '__main__':
    #newUser = cRofexLogin.cSetUpEnvironment()

    ticker1 = "DOJun19"
    ticker2 = "RFX20Jun19"
    suscriptTuple = (ticker1, ticker2)
    # print(newUser.instrumentDetail(ticker1, 'ROFX'))
    suscription1 = cGetMarketData(suscriptTuple)


else:
    pass
