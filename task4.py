from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['news']
news_db = db.news

header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 '
                        'Safari/537.36'}
url = 'https://lenta.ru/'
session = requests.Session()
response = session.get(url, headers=header)
dom = html.fromstring(response.text)

items = dom.xpath("//a[contains(@class,'_topnews')]")
for item in items:
    new = {}
    title = item.xpath("./*[contains(@class, 'card-')]//*[contains(@class, '__title')]/text()")[0]
    time = item.xpath(".//*[contains(@class, '__date')]/text()")[0]
    href = item.xpath("./@href")
    if href[0][0] == '/':
        href = url[:-1] + href[0]
        source = url
    else:
        source = href[0][:href[0].find('/news') + 1]
    new['1_source'] = source
    new['2_title'] = title
    new['3_href'] = href
    new['4_time'] = time

    if not news_db.find_one({'2_title': title}):
        news_db.insert_one(new)


for item in news_db.find({}):
    pprint(item)
