import websocket
import threading
from Classes import cRofexLogin
from time import sleep


class cGetMarketData():

    messages = []

    def __init__(self, user, symbols):
        self.user = user
        self.symbols = symbols
        self.sym = ""
        self.ws = websocket.WebSocketApp
        self.numMessages = 0
        self.messages = []
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
            print("Calling cRofexMessage ")
            # q = rMsg.cRofexMessage(message)
            print("Nro Mensajes",self.numMessages)
            print("Mensaje recibido:", message)
            self.messages.append(message)

            # self.md.append(q.getLastMessage())
            # print("Len md en cSuscriptV2:", len(self.md))

        except:
            # print("Error al procesar mensaje recibido:--->>> " + msg)
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
        return "{\"type\":\"" + self.user.type_ + "\",\"level\":" + self.user.level_ + ", \"entries\":[\"BI\", \"OF\"],\"products\":[{\"symbol\":\"" + self.sym + "\",\"marketId\":\"" + self.user.marketId_ + "\"}]}"


if __name__ == '__main__':
    user1 = cRofexLogin.cSetUpEnvironment()
    md1 = cGetMarketData(user1, ["DoJun19", "RFX20Jun19"])

else:
    pass