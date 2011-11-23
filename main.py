import ConfigParser

from twisted.internet import reactor, ssl

from sirious import SiriProxyFactory


config = ConfigParser.RawConfigParser()
config.read('sirious.cfg')
plugins = []
for plugin, cls in config.items('plugins'):
    try:
        kwargs = dict(config.items(cls))
    except ConfigParser.NoSectionError:
        kwargs = {}
    plugins.append((plugin, cls, kwargs))
reactor.listenSSL(443, SiriProxyFactory(plugins),
        ssl.DefaultOpenSSLContextFactory('keys/server.key', 'keys/server.crt'))
reactor.run()
