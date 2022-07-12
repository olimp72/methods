import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
import json
import pandas as pd
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 '
                         'Safari/537.36'}
url = 'https://hh.ru/search/vacancy'
params = {'page': '0', 'text': input('Введите название специальности: ')}
session = requests.Session()
response = session.get(url, params=params, headers=headers)
dom = BeautifulSoup(response.text, 'html.parser')
last_page = dom.find('a', {'data-qa': 'pager-next'})
if last_page:
    last_page = int(last_page.previous_sibling.find('a', {'data-qa': 'pager-page'}).text)
else:
    last_page = -1
articles_list = []
for i in range(0, int(last_page) + 1):
    print(f'scrapping page {i}')
    params['page'] = i
    response = session.get(url, params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    articles = dom.find_all('div', {'class': 'vacancy-serp-item-body__main-info'})
    for article in articles:
        pay_min, pay_max, currency = None, None, None
        article_data = {}
        name = article.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        href = name.get('href')
        name = name.text
        cost = article.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if cost:
            cost = re.sub(r'\u202f', '', cost.text).replace('–', '').split()
            if cost[0] == 'от':
                pay_min = int(cost[1])
            if cost[0] == 'до':
                pay_max = int(cost[1])
            if cost[0].isdigit():
                pay_min = int(cost[0])
                pay_max = int(cost[1])
            currency = cost[2]
        article_data['1_name'] = name
        article_data['2.1_pay_min'] = pay_min
        article_data['2.2_pay_max'] = pay_max
        article_data['2.3_currency'] = currency
        article_data['3_href'] = href
        article_data['4_source'] = 'https://hh.ru'
        articles_list.append(article_data)
# pprint(articles_list)
df = pd.DataFrame(articles_list)
pprint(df)
df.to_csv('job.csv', encoding='utf-8', sep=';')
# df.to_json('job1.json', force_ascii=False)
print('Количество найденных вакансий:', len(articles_list))
with open('job.json', 'w', encoding='utf-8') as f:
    json.dump(articles_list, f, ensure_ascii=False, indent=4)
