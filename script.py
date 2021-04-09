import requests
import time
import math
import re


def query():
    url = 'https://api.shuax.com/v2/chrome'
    response = requests.post(url)
    data = response.json()['win_stable_x64']
    chrome = {}
    chrome['update_time'] = math.floor(
        (time.time()*1000 - data['time'])/86400000)
    chrome['size'] = round(data['size'] / 1024 ** 2, 2)
    chrome['version'] = data['version']
    chrome['download_url'] = data['urls'][4]

    response = requests.get('https://note.ms/chrometest')
    current = re.search(
        '<textarea class="content">(.+)</textarea>', response.text).group(1)

    if current == chrome['version']:
        return False

    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
    requests.post(url="https://note.ms/chrometest",
                  headers=HEADERS, data=f"&t={chrome['version']}")
    return chrome


if __name__ == '__main__':
    chrome = query()
    if chrome:
        title = "Chrome Update Notification"
        content = f"""
            <h1>Chrome had Update!<h1>
            <h3>GUI url: {'https://tools.shuax.com/chrome/'}<h3>
            <h3>latest version: {chrome['version']}<h3>
            <h3>File size: {chrome['size']} MB<h3>
            <h3>Updated: {chrome['update_time']}天前<h3>
            <h3>download link: {chrome['download_url']}<h3>
        """
        with open(r'result.html', 'w', encoding='utf-8') as f:
            f.write(content)
