from pydispatch import dispatcher

from sirious import SiriObjects


class SiriPlugin(object):
    """ Abstract Plugin Class """
    proxy = None
    logger = None

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

    def ask(self, handler, text, speakableText=None, dialogueIdentifier='Misc#ident', handler_kwargs={}):
        """ Respond with an `Utterance` and send the response to `handler`. """
        root = SiriObjects.AddViews()
        root.views.append(SiriObjects.Utterance(text=text, speakableText=speakableText, dialogueIdentifier=dialogueIdentifier, listenAfterSpeaking=True))
        root.make_root(ref_id=self.proxy.ref_id)
        self.ask_views(handler, root, handler_kwargs)

    def ask_views(self, handler, views, handler_kwargs={}):
        """ Underlying power behind `SiriPlugin.ask` to send request and register for response. """
        self.block_session()
        self.send_object(views)
        def handle_answer(*a, **kw):
            del(kw['sender'])
            del(kw['signal'])
            handler_kwargs.update(kw)
            handler(*a, **handler_kwargs)
            dispatcher.disconnect(handle_answer, signal='consume_phrase')
        dispatcher.connect(handle_answer, signal='consume_phrase')

    def confirm(self, handler, text, speakableText=None, dialogueIdentifier='Misc#ident', handler_kwargs={}):
        root = SiriObjects.AddViews()
        root.views.append(SiriObjects.Utterance(text=text, speakableText=speakableText, dialogueIdentifier=dialogueIdentifier, listenAfterSpeaking=True))
        root.make_root(ref_id=self.proxy.ref_id)
        self.confirm_views(handler, root, handler_kwargs)

    def confirm_views(self, handler, views, handler_kwargs={}):
        """ Wrapper around `SiriPlugin.ask` which handles yes/no responses. """
        def handle_confirm(phrase, plist, **kwargs):
            phrase = phrase.lower().strip()
            print 'confirm: "%s"' % phrase
            confirmed = None
            if phrase in ['yes', 'ok']:
                confirmed = True
            elif phrase in ['no', 'cancel']:
                confirmed = False
            if confirmed is None:
                self.confirm(handler, "Please respond yes or no.", views, handler_kwargs)
            else:
                handler(confirmed, phrase, plist, **kwargs)
        self.ask_views(handle_confirm, views, handler_kwargs)

    def complete(self):
        """ Sends a `RequestCompleted` response. """
        request_complete = SiriObjects.RequestCompleted()
        request_complete.make_root(self.proxy.ref_id)
        self.send_object(request_complete)

    def plist_from_server(self, plist):
        """ Called when a plist is received from guzzoni, prior to processing. """
        return plist

    def plist_from_client(self, plist):
        """ Called when a plist is received from an iPhone, prior to processing. """
        return plist
