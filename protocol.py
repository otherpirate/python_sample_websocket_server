from autobahn.twisted.websocket import WebSocketServerProtocol

class Protocol(WebSocketServerProtocol):
    def onOpen(self):
        self.factory.register(self)
        self.factory.findPartner(self)

    def connectionLost(self, reason):
        self.factory.unregister(self)

    def onMessage(self, payload, isBinary):
        self.factory.communicate(self, payload, isBinary)