import ConfigParser
import logging

from twisted.internet import reactor, ssl

from sirious import SiriProxyFactory


## Parse config file
config = ConfigParser.RawConfigParser()
config.read('sirious.cfg')
## Configure logging
try:
    loglevel_name = config.items('sirious')['loglevel']
    loglevel = getattr(logging, loglevel_name.upper())
except (ConfigParser.NoSectionError, KeyError, AttributeError):
    loglevel = logging.INFO
finally:
    logging.basicConfig(
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        level=loglevel)
## Configure plugins
plugins = []
for plugin, cls in config.items('plugins'):
    try:
        kwargs = dict(config.items(cls))
    except ConfigParser.NoSectionError:
        kwargs = {}
    plugins.append((plugin, cls, kwargs))

## Start the Proxy
reactor.listenSSL(443, SiriProxyFactory(plugins),
        ssl.DefaultOpenSSLContextFactory('keys/server.key', 'keys/server.crt'))
reactor.run()
