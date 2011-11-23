from sirious import SiriObjects


class SiriousTest(object):
    proxy = None

    def process_plist(self, plist):
        return plist

    def known_intent(self, phrase, plist):
        if phrase.lower().strip() == "are you serious":
            self.proxy.blocking = True
            root = SiriObjects.AddViews()
            root.make_root(ref_id=self.proxy.ref_id)
            root.views.append(SiriObjects.Utterance(text="You're damn right I am. Sirious is up and running!"))
            self.proxy.inject_plist(root.to_dict())

    def unknown_intent(self, phrase, plist):
        pass
