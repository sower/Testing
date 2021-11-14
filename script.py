import requests
import json
import re


class CloudJson(object):
    host = 'https://json.extendsclass.com'
    session = requests.Session()
    response = None

    def __init__(self, security_key: str = None):
        if security_key:
            self.session.headers.update({"Security-key": security_key})

    # decorator
    def log(func):
        def wrapper(self, *args, **kwargs):
            print('running', func.__name__)
            res = func(self, *args, **kwargs)
            if self.response.status_code >= 400:
                print('request error')
            else:
                print('successfully request with', self.response.request.body)

            print(json.dumps(res, indent=2))
            return res
        return wrapper

    @log
    def obtain(self, id: str):
        self.response = self.session.get(f'{self.host}/bin/{id}')
        return self.response.json()

    @log
    def update(self, id: str, data):
        self.response = self.session.put(f'{self.host}/bin/{id}', data=data)
        return self.response.json()

    @log
    def partially_update(self, id: str, data):
        headers = {"Content-type": "application/json-patch+json"}
        self.response = self.session.patch(f'{self.host}/bin/{id}',
                                           data=data, headers=headers)
        return self.response.json()


def query(id):
    response = requests.get('https://www.ghxi.com/chrome.html')
    chrome = re.search('<title>(.+)</title>', response.text).group(1)

    cj = CloudJson('ec')
    software = cj.obtain(id)['software']

    if software.get('chrome', None) == chrome:
        print('No found new version')
        return False

    data = f'[{{"op":"add","path":"/software/chrome","value":"{chrome}"}}]'
    r = cj.partially_update(id, data.encode('utf-8'))
    return chrome


if __name__ == '__main__':
    key = input()
    try:
        ver = query(key)
    except Exception as e:
        print(e)
        ver = e

    if ver:
        content = f"""
            <h1> Chrome Update Notification </h1>
            <h3>{ver}</h3>
            <h3>GUI url: https://www.ghxi.com/chrome.html</h3>
        """
        with open(r'result.html', 'w', encoding='utf-8') as f:
            f.write(content)
