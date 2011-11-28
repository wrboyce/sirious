import ConfigParser
import logging
import os
from pkg_resources import resource_filename

from twisted.internet import reactor, ssl

from sirious import SiriProxyFactory


def get_paths():
    cfg_dirs = [os.path.expanduser('~/.sirious/'), '/etc/sirious']
    if os.getenv('VIRTUAL_ENV'):
        cfg_dirs.insert(0, os.path.expandvars('${VIRTUAL_ENV}/.sirious/'))
    return cfg_dirs

def gen_certs():
    path = get_paths()[0]
    os.system('mkdir -p %s/ssl' % path)
    os.chdir(path)
    filename = resource_filename(__name__, "scripts/gen_certs.zsh")
    print "You will shortly be asked four questions. The correct answers are 1234, 1234, y, y."
    os.system(filename)

def start_proxy():
    ## Find & Parse the config files
    config = ConfigParser.RawConfigParser()
    cfg_dirs = get_paths()
    for dir in cfg_dirs[::-1]:  # Cfg files are parsed in the order /etc/sirious/sirious.cfg, ~/.sirious/sirious.cfg, ${VIRTUAL_ENV}/.sirious/sirious.cfg
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
        logging.getLogger('sirious').info('Registering plugin %s.%s...' % (plugin, cls))
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
