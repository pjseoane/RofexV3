import websocket
import threading
import simplejson

from Classes import cRofexLogin
from time import sleep


class cGetMarketData():

    # messages = []

    def __init__(self, user, symbols):
        self.user = user
        self.symbols = symbols
        self.sym = ""
        self.ws = websocket.WebSocketApp
        self.numMessages = 0
        self.marketDataDict = {}
        self.runWS()

    def runWS(self):
        headers = {'X-Auth-Token:{token}'.format(token=self.user.token)}
        self.ws = websocket.WebSocketApp(self.user.activeWSEndpoint,
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
                self.ws.send(self.buildMessage)
                print("Sent Suscription msg for ticker", self.sym)
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
                print("Tipo de Mensaje Recibido No soportado: " + msg)

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
        return "{\"type\":\"" + self.user.type_ + "\",\"level\":" + self.user.level_ + ", \"entries\":[\"BI\", \"OF\"],\"products\":[{\"symbol\":\"" + self.sym + "\",\"marketId\":\"" + self.user.marketId_ + "\"}]}"

    def getBidPrice(self, ticker):
        msg = self.marketDataDict[ticker]['marketData']['BI'][0]['price']
        return msg if msg else 0

    def getBidSize(self, ticker):
        msg = self.marketDataDict[ticker]['marketData']['BI'][0]['size']
        return msg if msg else 0

    def getOfferPrice(self, ticker):
        msg = self.marketDataDict[ticker]['marketData']['OF'][0]['price']
        return msg if msg else 0

    def getOfferSize(self, ticker):
        msg = self.marketDataDict[ticker]['marketData']['OF'][0]['size']
        return msg if msg else 0
        
    def goRobot(self):
        print("marketDataDict: ", self.marketDataDict)

        try:
            for sym in self.symbols:
                print(sym, "    ", self.getBidPrice(sym), "/", self.getOfferPrice(sym), "----------", self.getBidSize(sym), "/", self.getOfferSize(sym))

        except:
            print("Error goRobot()", sym, self.marketDataDict.__len__())


if __name__ == '__main__':
    user1 = cRofexLogin.cSetUpEnvironment()
    suscription1 = cGetMarketData(user1, ["DoJun19", "RFX20Jun19"])

else:
    pass
