import requests

class ifttt_webhooks:
        def __init__(self, key):
        self.key = key

    def trig(self, event_name):
        base_url = 'https://maker.ifttt.com/trigger/{}/with/key/{}'
        url = base_url.format(event_name, self.key)
        r = requests.get(url)
