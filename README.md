## Sirious, the _totally sirious_ Siri Proxy.


### Usage

First you'll need to install the biplist Python module:

    $ pip install biplist

Due to the way Siri works, you'll need to install a Custom CA onto your iPhone. There is a included script that will do most of the legwork for you, just run:

    $ ./gen_certs.zsh

It'll prompt you for some input, the correct answers are "1234", "1234", "y" and "y".
Once this is done there will be keys/ca.pem - you need to get this file install on your iPhone, email is probably the easiest.
During installation iOS will give you a pretty scary (and rightfully so) warning, you can safely ignore it as this is **your** CA, and hopefully you can trust yourself!

Once this is done, you'll need to redirect the DNS for guzzoni.apple.com to wherever you are running sirious. I'd recommend using dnsmasq for this.
Finally, fire up sirious:

    $ sudo python main.py
