import requests

from sirious import SiriPlugin


class RedAlert(SiriPlugin):
    """ A plugin for Philips Hue assisted awesome. """
    def __init__(self, hostname, username):
        self.host = hostname
        self.user = username

    def red_alert(self, phrase):
        _red_alert_state = {'on': True, 'bri': 255, 'hue': 0, 'sat': 255, 'alert': 'lselect'}
        self.respond("Awoooga! Awoooga!")
        for id in requests.get('http://{}/api/{}/lights'.format(self.host, self.user)).json().iterkeys():
            requests.put('http://{}/api/{}/lights/{}/state'.format(self.host, self.user, id), _red_alert_state)
    red_alert.triggers = ['Red alert']
