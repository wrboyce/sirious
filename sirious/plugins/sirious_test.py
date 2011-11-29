from sirious import SiriPlugin


class SiriousTest(SiriPlugin):
    def sirious(self, phrase, plist):
        self.respond("You're damn right I am. Sirious is up and running!")
        self.complete()
    sirious.triggers = ['are you serious']

    def ask_test(self, phrase, plist):
        self.ask(self.ask_test_response, "Do you think this is a test?")
    ask_test.triggers = ['is this a test']

    def ask_test_response(self, phrase, plist):
        self.respond("Well, you've failed.")
        self.complete()
