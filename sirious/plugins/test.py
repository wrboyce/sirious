from sirious import SiriPlugin


class SiriousTest(SiriPlugin):
    def respond_test(self, phrase):
        self.respond("You're damn right I am. Sirious is up and running!")
        self.complete()
    respond_test.triggers = ['Are you serious']

    def ask_test(self, phrase):
        self.logger.info('Asking question...')
        response = self.ask("Do you think this is a test?")
        self.logger.info('Got answer: %s' % response)
        self.respond("Well, you've failed.")
        self.complete()
    ask_test.triggers = ['Is this a test']

    def confirm_test(self, phrase):
        if self.confirm("Please confirm"):
            self.respond("Confirmed.")
        else:
            self.respond("Ok, cancelled.")
        self.complete()
    confirm_test.triggers = ['Do something']
