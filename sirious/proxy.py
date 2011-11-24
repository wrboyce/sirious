from binascii import hexlify, unhexlify
import re
import sys
import zlib

from biplist import readPlistFromString, writePlistToString
from twisted.internet import protocol, reactor, ssl
from twisted.protocols.basic import LineReceiver
from twisted.protocols.portforward import ProxyClientFactory


class SiriProxy(LineReceiver):
    peer = None
    blocking = False
    ref_id = None

    def __init__(self, plugins=[], triggers=[]):
        self.buffer = ""
        self.zlib_d = zlib.decompressobj()
        self.zlib_c = zlib.compressobj()
        self.plugins = plugins
        self.triggers = triggers

    def setPeer(self, peer):
        self.peer = peer

    def lineReceived(self, line):
        self.peer.sendLine(line)
        if not line:
            self.setRawMode()

    def rawDataReceived(self, data):
        if self.zlib_d.unconsumed_tail:
            data = self.zlib_d.unconsumed_tail + data
        if hexlify(data[0:4]) == 'aaccee02':
            self.peer.transport.write(data[0:4])
            data = data[4:]
        ## Add `data` to decompress stream
        udata = self.zlib_d.decompress(data)
        if udata:
            ## If we get decompressed output, process it
            header = hexlify(udata[0:5])
            if header[1] in [3, 4]:
                ## Ping/Pong packets - pass them straight through
                return self.peer.transport.write(data)
                pass
            size = int(header[2:], 16)
            body = udata[5:(size + 5)]
            if body:
                plist = readPlistFromString(body)
                plist = self.process_plist(plist)
                if plist:
                    if self.blocking and self.ref_id != plist['refId']:
                        self.blocking = False
                    if not self.blocking:
                        self.inject_plist(plist)
                        pass
                    return plist

    def process_plist(self, plist):
        ## Offer plugins a chance to intercept plists
        for plugin in self.plugins:
            plugin.proxy = self
            if self.__class__ == SiriProxyServer:
                plist = plugin.plist_from_client(plist)
            if self.__class__ == SiriProxyClient:
                plist = plugin.plist_from_server(plist)
            ## If a plugin returns None, the plist has been blocked
            if not plist:
                return
        return plist

    def inject_plist(self, plist):
        ref_id = plist.get('refId', None)
        if ref_id:
            self.ref_id = ref_id
        data = writePlistToString(plist)
        data_len = len(data)
        if data_len > 0:
            header = '{:x}'.format(0x0200000000 + data_len).rjust(10, '0')
            data = self.zlib_c.compress(unhexlify(header) + data)
            self.peer.transport.write(data)
            self.peer.transport.write(self.zlib_c.flush(zlib.Z_FULL_FLUSH))

    def connectionLost(self, reason):
        if self.peer:
            self.peer.transport.loseConnection()
            self.setPeer(None)


class SiriProxyClient(SiriProxy):
    def connectionMade(self):
        self.peer.setPeer(self)
        self.peer.transport.resumeProducing()

    def rawDataReceived(self, data):
        plist = SiriProxy.rawDataReceived(self, data)
        if plist:
            self.process_speech(plist)

    def process_speech(self, plist):
        phrase = None
        if plist['class'] == 'AddViews':
            phrase = ''
            if plist['properties']['views'][0]['properties']['dialogIdentifier'] == 'Common#unknownIntent':
                phrase = plist['properties']['views'][1]['properties']['commands'][0]['properties']['commands'][0]['properties']['utterance'].split('^')[3]
        if plist['class'] == 'SpeechRecognized':
            phrase = ''
            for phrase_plistect in plist['properties']['recognition']['properties']['phrases']:
                for token in phrase_plistect['properties']['interpretations'][0]['properties']['tokens']:
                    if token['properties']['removeSpaceBefore']:
                        phrase = phrase[:-1]
                    phrase += token['properties']['text']
                    if not token['properties']['removeSpaceAfter']:
                        phrase += ' '
        if phrase:
            #print '[Speech Recognised] %s' % phrase
            for trigger, function in self.triggers:
                if trigger.search(phrase):
                    function(phrase, plist)


class SiriProxyClientFactory(ProxyClientFactory):
    protocol = SiriProxyClient


class SiriProxyServer(SiriProxy):
    clientProtocolFactory = SiriProxyClientFactory

    def connectionMade(self):
        self.transport.pauseProducing()
        client = self.clientProtocolFactory()
        client.setServer(self)
        client.plugins = self.plugins
        client.triggers = self.triggers
        reactor.connectSSL(self.factory.host, self.factory.port, client, ssl.DefaultOpenSSLContextFactory(
            'keys/server.key', 'keys/server.crt'))

    def rawDataReceived(self, data):
        SiriProxy.rawDataReceived(self, data) ## returning a value seems to upset Twisted


class SiriProxyFactory(protocol.Factory):
    protocol = SiriProxyServer

    def __init__(self, plugins):
        self.host = '17.174.4.4'
        self.port = 443
        self.plugins = []
        for mod_name, cls_name, kwargs in plugins:
            __import__(mod_name)
            mod = sys.modules[mod_name]
            self.plugins.append((getattr(mod, cls_name), kwargs))

    def _get_plugin_triggers(self, instance):
        for attr_name in dir(instance):
            attr = getattr(instance, attr_name)
            if callable(attr) and hasattr(attr, 'triggers'):
                yield attr

    def buildProtocol(self, addr):
        protocol = self.protocol()
        for cls, plugin_kwargs in self.plugins:
            instance = cls(**plugin_kwargs)
            protocol.plugins.append(instance)
            for function in self._get_plugin_triggers(instance):
                for trigger in function.triggers:
                    trigger_re = re.compile(trigger, re.I)
                    protocol.triggers.append((trigger_re, function))
        protocol.factory = self
        return protocol
