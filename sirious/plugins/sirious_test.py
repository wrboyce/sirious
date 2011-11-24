from sirious import SiriPlugin


class SiriousTest(SiriPlugin):
    def known_intent(self, phrase, plist):
        if phrase.lower().strip() == "are you serious":
            self.proxy.blocking = True
            self.respond("You're damn right I am. Sirious is up and running!")
