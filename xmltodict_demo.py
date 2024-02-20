import json

import requests
import xmltodict

rss_url = "https://www.opennet.ru/opennews/opennews_all_utf.rss"
response = requests.get(rss_url)
#print(response.text)
rss = xmltodict.parse(response.text)
rss_json = json.dumps(rss, ensure_ascii=False).encode('utf8')
print(rss['rss']['channel']['item'][0]['title'])

