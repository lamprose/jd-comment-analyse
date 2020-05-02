import requests


class SpiderBase:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)'
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }

    def getData(self):
        pass
