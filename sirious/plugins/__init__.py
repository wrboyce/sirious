from sirious import SiriObjects


class SiriPlugin(object):
    """ Abstract Plugin Class """
    proxy = None
    logger = None

    def plist_from_server(self, plist):
        """ Called when a plist is received from guzzoni, prior to processing. """
        return plist

    def plist_from_client(self, plist):
        """ Called when a plist is received from an iPhone, prior to processing. """
        return plist

    def block_session(self):
        """ Have the proxy block any further packets from the peer. """
        self.proxy.blocking = True

    def send_object(self, plist):
        """ Inject an object into the conversation. """
        self.proxy.inject_plist(plist)

    def respond(self, text, speakableText=None, dialogueIdentifier='Misc#ident', listenAfterSpeaking=False):
        """ Respond with a simple `Utterance` """
        self.block_session()
        root = SiriObjects.AddViews()
        root.make_root(ref_id=self.proxy.ref_id)
        root.views.append(SiriObjects.Utterance(text=text, speakableText=speakableText, dialogueIdentifier=dialogueIdentifier, listenAfterSpeaking=listenAfterSpeaking))
        self.send_object(root)

    def ask(self, text, speakableText=None, dialogueIdentifier='Misc#ident'):
        """ Respond with an `Utterance` and send the response to `handler`. """
        root = SiriObjects.AddViews()
        root.views.append(SiriObjects.Utterance(text=text, speakableText=speakableText, dialogueIdentifier=dialogueIdentifier, listenAfterSpeaking=True))
        root.make_root(ref_id=self.proxy.ref_id)
        return self.ask_views(root)

    def get_next_phrase(self):
        def _handler(phrase):
            self.__response = phrase
        self.proxy.get_next_phrase(_handler)

    def ask_views(self, views):
        """ Underlying power behind `SiriPlugin.ask` to send request and register for response. """
        self.block_session()
        self.send_object(views)
        self.__response = None
        self.get_next_phrase()
        while self.__response is None:
            pass
        response, self.__response = self.__response, None
        return response

    def confirm(self, text, speakableText=None, dialogueIdentifier='Misc#ident'):
        root = SiriObjects.AddViews()
        root.views.append(SiriObjects.Utterance(text=text, speakableText=speakableText, dialogueIdentifier=dialogueIdentifier, listenAfterSpeaking=True))
        root.make_root(ref_id=self.proxy.ref_id)
        return self.confirm_views(root)

    def confirm_views(self, views):
        return self._confirm(self.ask_views(views))

    def _confirm(self, phrase):
        phrase = phrase.lower().strip()
        if phrase in ['yes', 'ok']:
            return True
        elif phrase in ['no', 'cancel']:
            return False
        return self.confirm("Please respond yes or no.")

    def complete(self):
        """ Sends a `RequestCompleted` response. """
        request_complete = SiriObjects.RequestCompleted()
        request_complete.make_root(self.proxy.ref_id)
        self.send_object(request_complete)
