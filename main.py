import ConfigParser

from twisted.internet import reactor, ssl

from sirious import SiriProxyFactory


config = ConfigParser.RawConfigParser()
config.read('sirious.cfg')
plugins = [plugin for (plugin, state) in config.items('plugins') if state == 'enabled']
reactor.listenSSL(443, SiriProxyFactory(plugins), ssl.DefaultOpenSSLContextFactory(
    'keys/server.key', 'keys/server.crt'))
reactor.run()
