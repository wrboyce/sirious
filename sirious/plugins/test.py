from sirious import SiriPlugin


class SiriousTest(SiriPlugin):
    def respond_test(self, phrase, plist):
        self.respond("You're damn right I am. Sirious is up and running!")
        self.complete()
    respond_test.triggers = ['Are you serious']

    def ask_test(self, phrase, plist):
        self.ask(self.ask_test_response, "Do you think this is a test?")
    ask_test.triggers = ['Is this a test']

    def ask_test_handler(self, phrase, plist):
        self.respond("Well, you've failed.")
        self.complete()

    def confirm_test(self, phrase, plist):
        self.confirm(self.confirm_test_handler, "Please confirm")
    confirm_test.triggers = ['Do something']

    def confirm_test_handler(self, confirmed, phrase, plist):
        self.respond('Confirmed.' if confirmed else 'OK, cancelled.')
        self.complete()
