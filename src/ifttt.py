import requests

class ifttt_webhooks:
    base_url = 'https://maker.ifttt.com/trigger/{}/with/key/{}'

    def __init__(self, key):
        self.key = key

    def trig(self, event_name):
        url = base_url.format(event_name, self.key)
        r = requests.get(url)
