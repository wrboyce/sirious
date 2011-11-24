from sirious import SiriPlugin


class SiriousTest(SiriPlugin):
    def sirious(self, phrase, plist):
        self.respond("You're damn right I am. Sirious is up and running!")
    sirious.triggers = ['are you serious']
