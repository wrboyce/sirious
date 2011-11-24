from lxml.cssselect import CSSSelector
import lxml.html
import re

from sirious import SiriPlugin


class LFCFixtures(SiriPlugin):
    def get_next_game(self, home):
        url = "http://www.liverpoolfc.tv/match/fixtures"
        root = lxml.html.parse(url)
        fixtable = CSSSelector('table.fixtures')(root)[0]
        for row in CSSSelector('tr.EvenR, tr.OddB')(fixtable):
            cols = CSSSelector('td')(row)
            if cols[3].text_content() == ('H' if home else 'A') and not cols[5].text_content().strip():
                return cols[0].text_content().strip(), cols[4].text_content().strip(), cols[2].text_content().strip()

    def known_intent(self, phrase, plist):
        if re.search('next (home|away) game', phrase, re.I):
            self.proxy.blocking = True
            home = True if 'home' in phrase.lower() else False
            date, time, team = self.get_next_game(home)
            response = "The next %s game is %s at %s on %s." % ("home" if home else "away", team, time, date)
            self.respond(response)
