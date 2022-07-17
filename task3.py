import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
from pymongo import MongoClient
from pymongo import errors


def check_new_vacancy(uncheck_vacancy):
    count = 0
    try:
        jobs.insert_one(uncheck_vacancy)
        count = 1
        print(f"Document with id = {uncheck_vacancy['_id']} was added")
    except errors.DuplicateKeyError:
        print(f"Document with id = {uncheck_vacancy['_id']} is already exists")
    return count


def check_pay_vacancy(pay):
    gt_pay = 0
    for item in jobs.find({'$or': [{'2_1_pay_min': {'$gt': pay}}, {'2_2_pay_max': {'$gt': pay}}]}):
        gt_pay += 1
        pprint(item)
    print(f'Найдено {gt_pay} вакансии(й) с зарплатой более {pay}')


count_all = 0
client = MongoClient('127.0.0.1', 27017)
db = client['task3']
jobs = db.jobs
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
        if href.find('https://hh.ru/vacancy/') > -1:
            vacancy = int(href.replace('https://hh.ru/vacancy/', '').replace(href[href.find('?'):], ''))
        else:
            vacancy = int(href.replace('https://hhcdn.ru/click?b=', '').replace(href[href.find('&'):], ''))
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
        article_data['_id'] = vacancy
        article_data['1_name'] = name
        article_data['2_1_pay_min'] = pay_min
        article_data['2_2_pay_max'] = pay_max
        article_data['2_3_currency'] = currency
        article_data['3_href'] = href
        article_data['4_source'] = 'https://hh.ru'
        count_all += check_new_vacancy(article_data)
print(f'Добавлено {count_all} новых записей')
check_pay_vacancy(int(input('Введите размер заработной платы: ')))
