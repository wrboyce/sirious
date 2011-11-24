from sirious import SiriObjects


class SiriPlugin(object):
    proxy = None

    def respond(self, text, speakableText=None, dialogueIdentifier='Misc#ident', listenAfterSpeaking=False):
        self.proxy.blocking = True
        root = SiriObjects.AddViews()
        root.make_root(ref_id=self.proxy.ref_id)
        root.views.append(SiriObjects.Utterance(text=text, speakableText=speakableText, dialogueIdentifier=dialogueIdentifier, listenAfterSpeaking=listenAfterSpeaking))
        self.proxy.inject_plist(root.to_dict())

    def ask(self, text, speakableText=None, dialogueIdentifier='Misc#ident', listenAfterSpeaking=True):
        self.respond(text, speakableText, dialogueIdentifier, listenAfterSpeaking)

    def plist_from_server(self, plist):
        return plist

    def plist_from_client(self, plist):
        return plist
