import requests
import html
import re
import json


def query(key):
    url = f'https://www.ghxi.com/{key}.html'
    response = requests.get(url)
    data = {}
    data[key] = re.search('<title>(.+)</title>', response.text).group(1)

    response = requests.get('https://note.ms/chrometest')

    json_str = re.search(
        '<textarea class="content">(.+)</textarea>', response.text).group(1)

    store = json.loads(html.unescape(json_str))

    if store.get(key, None) == data[key]:
        print('false')
        return False

    store[key] = data[key]
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
    requests.post(url="https://note.ms/chrometest",
                  headers=HEADERS,
                  data=f"&t={json.dumps(store,ensure_ascii=False,sort_keys=True)}".encode())
    print('true')
    return store


if __name__ == '__main__':
    key = input()
    data = query(key)
    if data:
        title = "Chrome Update Notification"
        content = f"""
            <h1>Chrome had Update!</h1>
            <h3>{data[key]}</h3>
            <h3>GUI url: https://www.ghxi.com/{key}.html</h3>
        """
        with open(r'result.html', 'w', encoding='utf-8') as f:
            f.write(content)
