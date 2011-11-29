from lxml.cssselect import CSSSelector
import lxml.html

from sirious import SiriPlugin


class LFCFixtures(SiriPlugin):
    def get_next_game(self, phrase, match_groups):
        location = 'H' if match_groups[0].lower() == 'home' else 'A'
        url = "http://www.liverpoolfc.tv/match/fixtures"
        root = lxml.html.parse(url)
        fixtable = CSSSelector('table.fixtures')(root)[0]
        for row in CSSSelector('tr.EvenR, tr.OddB')(fixtable):
            cols = CSSSelector('td')(row)
            if cols[3].text_content() == location and not cols[5].text_content().strip():
                date, time, team = cols[0].text_content().strip(), cols[4].text_content().strip(), cols[2].text_content().strip()
                break
        response = "The next %s game is %s at %s on %s." % ("home" if location is 'H' else "away", team, time, date)
        self.respond(response)
        self.complete()
    get_next_game.triggers = ['next (home|away) game']
