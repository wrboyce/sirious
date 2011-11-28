import ConfigParser
import logging
import os

from twisted.internet import reactor, ssl

from sirious import SiriProxyFactory


## Find & Parse the config files
## Cfg files are parsed in the order /etc/sirious/sirious.cfg, ~/.sirious/sirious.cfg, ${VIRTUAL_ENV}/.sirious/sirious.cfg
config = ConfigParser.RawConfigParser()
cfg_dirs = [os.path.expanduser('~/.sirious/'), '/etc/sirious']
if os.getenv('VIRTUAL_ENV'):
    cfg_dirs.insert(0, os.path.expandvars('${VIRTUAL_ENV}/.sirious/'))
for dir in cfg_dirs[::-1]:
    config.read('sirious.cfg')
## Grab core settings
try:
    core_settings = config.items('core')
except ConfigParser.NoSectionError:
    core_settings = {}
settings = {}
settings['root'] = root = cfg_dirs[0]  # ${VIRTUAL_ENV}/.sirious or ~/.sirious
## Configure logging
try:
    loglevel_name = core_settings['loglevel']
    loglevel = getattr(logging, loglevel_name.upper())
except (KeyError, AttributeError):
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
settings['plugins'] = plugins
## Start the Proxy
logging.getLogger('sirious').info('Starting up...')
reactor.listenSSL(443, SiriProxyFactory(**settings),
    ssl.DefaultOpenSSLContextFactory(
        os.path.join(root, 'ssl', 'server.key'),
        os.path.join(root, 'ssl', 'server.crt')
    )
)
reactor.run()
