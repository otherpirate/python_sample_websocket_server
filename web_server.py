import sys

from twisted.web.static import File
from twisted.python import log
from twisted.web.server import Site
from twisted.internet import reactor

from autobahn.twisted.resource import WebSocketResource

from protocol import Protocol
from factory import Factory

if __name__ == "__main__":
    log.startLogging(sys.stdout)

    factory = Factory(u"ws://0.0.0.0:8080", debug=True)
    factory.protocol = Protocol
    resource = WebSocketResource(factory)

    # static file server seving index.html as root
    root = File(".")

    # websockets resource on "/ws" path
    root.putChild(u"ws", resource)

    site = Site(root)
    reactor.listenTCP(8080, site)
    reactor.run()