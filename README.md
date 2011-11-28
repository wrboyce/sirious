# Sirious, the _totally sirious_ Siri Proxy.

## About

Sirious is a tampering proxy server for Apple's Siri Assistant, allowing you to extend Siri to add custom commands/functionality.

_Sirious does **not** allow you to run Siri on an unauthorised (non-iPhone4S) device_


## Support

Not really, but feel free to drop by #sirious on freenode.


## Plugins

The Plugin API should be pretty stable now, until I discover more stuff in the Siri Protocol we can abuse. Take a look at sirious.plugins.sirious_test for a pretty clear example


## Installation/Usage

Install using the usual method:

    $ python setup install.py

Then you will need to run sirious-gencerts to generate your certificates for you. The location of these will be automatically calculated based on how you run/install Sirious.
It will be either:

    ${VIRTUAL_ENV}/.sirious/
    ~/.sirious/

Inside an `ssl` subdir.
If you wish to load plugins, or pass any configuration options, your config file should by `sirious.cfg` in the above directory. A sample config is provided with the package.


## Acknowledgements

* Applidium, without who I wouldn't have really known where to start with the Siri Protocol
* plamoni/SiriProxy, sometimes it's nice to have a reference even in a language you don't speak :)
* chendo, for some (albeit Rubyist) Plugin API inspiration
