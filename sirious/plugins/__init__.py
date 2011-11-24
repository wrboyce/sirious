from pydispatch import dispatcher

from sirious import SiriObjects


class SiriPlugin(object):
    proxy = None

    def respond(self, text, speakableText=None, dialogueIdentifier='Misc#ident', listenAfterSpeaking=False):
        self.proxy.blocking = True
        root = SiriObjects.AddViews()
        root.make_root(ref_id=self.proxy.ref_id)
        root.views.append(SiriObjects.Utterance(text=text, speakableText=speakableText, dialogueIdentifier=dialogueIdentifier, listenAfterSpeaking=listenAfterSpeaking))
        self.proxy.inject_plist(root.to_dict())

    def ask(self, handler, text, speakableText=None, dialogueIdentifier='Misc#ident'):
        self.respond(text, speakableText, dialogueIdentifier, listenAfterSpeaking=True)
        self.proxy.blocking = 1
        def handle_answer(*a, **kw):
            ## if the question caused unknown intent, we'll get told about it twice
            if kw['plist']['class'] == 'AddViews':
                return
            del(kw['sender'])
            del(kw['signal'])
            handler(*a, **kw)
            dispatcher.disconnect(handle_answer, signal='consume_phrase')
        dispatcher.connect(handle_answer, signal='consume_phrase')

    def plist_from_server(self, plist):
        return plist

    def plist_from_client(self, plist):
        return plist
