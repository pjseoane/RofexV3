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
        self.marketCloseData = {}
        self.runWS()

    # def start(self):
    #     self.runWS()

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
        for self.sym in self.symbols:

            # Arma diccionario de detalles contratos para este Algo
            self.contractDetail[self.sym] = self.instrumentDetail(self.sym, 'ROFX')
            self.marketCloseData[self.sym] = self.getMarketData('ROFX', self.sym,
                                                                "LA", "CL", "SE", "OI", "", "", "", str(1))

            self.ws.send(self.buildMessage)
            # print("(cGetMarketData)", self.contractDetail[self.sym])
            print("(cGetMarketData) Sent Suscription msg for: ", self.sym)
            sleep(1)

    def on_message(self, message):
        self.numMessages += 1

        try:
            msg = simplejson.loads(message)
            msgType = msg['type'].upper()

            if msgType == 'MD':
                # print("cgetMarketData New msg MD->: ", msg)
                # Arma y carga el Dictionary
                self.sym = msg['instrumentId']['symbol']
                self.marketDataDict[self.sym] = msg

                if self.marketDataDict.__len__() == len(self.symbols):
                    print("cGetMarketData - Dictionary completed")
                    self.goRobot()
                else:
                    print("cGetMarketData - Dictionary not completed yet....")

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

    def on_open(self):
        pass
        # print("WS Conection Open...")

    @property
    def buildMessage(self):
        # 'BI', 'OF', 'LA', 'OP', 'CL', 'SE', 'OI'
        return "{\"type\":\"" + self.type_ + "\",\"level\":" + self.level_ +\
               ", \"entries\":[\"BI\", \"OF\",\"LA\"],\"products\":[{\"symbol\":\"" +\
               self.sym + "\",\"marketId\":\"" + self.marketId_ + "\"}]}"

    def goRobot(self):
        # Overridable Method
        pass


if __name__ == '__main__':

    ticker1 = "DOJun19"
    ticker2 = "RFX20Jun19"
    suscriptTuple = (ticker1, ticker2)
    suscrip = cGetMarketData(suscriptTuple)
    # suscrip.start()

else:
    pass
