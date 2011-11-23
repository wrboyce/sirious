from binascii import hexlify, unhexlify
import zlib

from biplist import readPlistFromString, writePlistToString
from twisted.internet import protocol, reactor, ssl
from twisted.protocols.basic import LineReceiver
from twisted.protocols.portforward import ProxyClientFactory


class SiriProxy(LineReceiver):
    peer = None

    def setPeer(self, peer):
        self.peer = peer

    def lineReceived(self, line):
        self.peer.sendLine(line)
        if not line:
            self.setRawMode()

    def connectionLost(self, reason):
        if self.peer:
            self.peer.transport.loseConnection()
            self.setPeer(None)

class SiriProxyClient(SiriProxy):
    raw_header = False

    def __init__(self):
        self.buffer = ""
        self.zlib_d = zlib.decompressobj()
        self.zlib_c = zlib.compressobj()

    def connectionMade(self):
        self.peer.setPeer(self)
        self.peer.transport.resumeProducing()

    def rawDataReceived(self, data):
        if self.zlib_d.unconsumed_tail:
            data = self.zlib_d.unconsumed_tail + data
        if not self.raw_header:
            self.peer.transport.write(data[0:4])
            data = data[4:]
            self.raw_header = True
        ## Add `data` to decompress stream
        udata = self.zlib_d.decompress(data)
        if udata:
            ## If we get decompressed output, process it
            header = hexlify(udata[0:5])
            if header[1] in [3,4]:
                ## Ping/Pong packets - pass them straight through
                return self.transport.write(data)
            size = int(header[2:], 16)
            body = udata[5:size+5]
            if body:
                plist = readPlistFromString(body)
                plist = self.process_plist(plist)
                self.inject_plist(plist)

    def process_plist(self, plist):
        phrase = ''
        if plist['class'] == 'AddViews':
            if plist['properties']['views'][0]['properties']['dialogIdentifier'] == 'Common#unknownIntent':
                phrase = plist['properties']['views'][1]['properties']['commands'][0]['properties']['commands'][0]['properties']['utterance'].split('^')[3]
                return self.process_unknown_intent(phrase, plist)
        if plist['class'] == 'SpeechRecognized':
            for phrase_plistect in plist['properties']['recognition']['properties']['phrases']:
                for token in phrase_plistect['properties']['interpretations'][0]['properties']['tokens']:
                    if token['properties']['removeSpaceBefore']:
                        phrase = phrase[:-1]
                    phrase += token['properties']['text']
                    if not token['properties']['removeSpaceAfter']:
                        phrase += ' '
            return self.process_known_intent(phrase, plist)
        return plist

    def inject_plist(self, plist):
        data = writePlistToString(plist)
        data_len = len(data)
        if data_len > 0:
            header = hex(0x0200000000 + int(hex(data_len), 16)).split('x')[1].rjust(10, '0')
            data = self.zlib_c.compress(unhexlify(header) + data)
            #data += self.zlib_c.flush(zlib.Z_FULL_FLUSH)
            self.peer.transport.write(data)
            self.peer.transport.write(self.zlib_c.flush(zlib.Z_FULL_FLUSH))

    def process_unknown_intent(self, phrase, plist):
        ## TODO: plugins
        return plist

    def process_known_intent(self, phrase, plist):
        ## TODO: plugins
        return plist

class SiriProxyClientFactory(ProxyClientFactory):
    protocol = SiriProxyClient

class SiriProxyServer(SiriProxy):
    clientProtocolFactory = SiriProxyClientFactory

    def connectionMade(self):
        self.transport.pauseProducing()
        client = self.clientProtocolFactory()
        client.setServer(self)
        reactor.connectSSL('17.174.4.4', self.factory.port, client, ssl.DefaultOpenSSLContextFactory(
            'keys/server.key', 'keys/server.crt'))

    def rawDataReceived(self, data):
        self.peer.transport.write(data)

class SiriProxyFactory(protocol.Factory):
    protocol = SiriProxyServer

    def __init__(self):
        self.host = '17.174.4.44'
        self.port = 443


if __name__ == '__main__':
    reactor.listenSSL(443, SiriProxyFactory(), ssl.DefaultOpenSSLContextFactory(
        'keys/server.key', 'keys/server.crt'))
    reactor.run()
