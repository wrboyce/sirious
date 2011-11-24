# Sirious, the _totally sirious_ Siri Proxy.

## About

Sirious is a tampering proxy server for Apple's Siri Assistant, allowing you to extend Siri to add custom commands/functionality.

_Sirious does **not** allow you to run Siri on an unauthorised (non-iPhone4S) device_


## Support

Not really, but feel free to drop by #sirious on freenode.


## Plugins

The Plugin API should be pretty stable now, until I discover more stuff in the Siri Protocol we can abuse. Take a look at sirious.plugins.sirious_test for a pretty clear example


## Usage

First you'll need to install the biplist Python module:

    $ pip install biplist

Due to the way Siri works, you'll need to install a Custom CA onto your iPhone. There is a included script that will do most of the legwork for you, just run:

    $ ./gen_certs.zsh

It'll prompt you for some input, the correct answers are "1234", "1234", "y" and "y".

Once this is done there will be keys/ca.pem - you need to get this file installed on your iPhone, email is probably the easiest.
During installation iOS will give you a pretty scary (and rightfully so) warning, you can safely ignore it.

Once this is done, you'll need to redirect the DNS for guzzoni.apple.com to wherever you are running sirious. I'd recommend using dnsmasq for this.

Finally, fire up sirious:

    $ sudo python main.py


## Acknowledgements

* Applidium, without who I wouldn't have really known where to start with the Siri Protocol
* plamoni/SiriProxy, sometimes it's nice to have a reference even in a language you don't speak :)
