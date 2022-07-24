from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
from pprint import pprint
import time

client = MongoClient('127.0.0.1', 27017)
db = client['m_video']
m_video_db = db.m_video

s = Service('c:\Program Files\Google\Chrome\Application\chromedriver.exe')
driver = webdriver.Chrome(service=s)
time.sleep(2)
driver.get('https://www.mvideo.ru/')

html = driver.find_element(By.CSS_SELECTOR, 'html')
while True:
    try:
        button_in_trend = driver.find_element(By.XPATH, ".//span[contains(text(),'В тренде')]/../..")
        button_in_trend.click()
        time.sleep(2)
        break
    except NoSuchElementException:
        html.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)

cards_in_trend = driver.find_elements(By.XPATH, "//mvid-shelf-group//mvid-product-cards-group//div[@class='title']")
for card in cards_in_trend:
    name = card.text
    link = card.find_element(By.XPATH, "./a").get_attribute('href')
    if not m_video_db.find_one({'name': name}):
        m_video_db.insert_one({'name': name, 'link': link})

for item in m_video_db.find({}):
    pprint(item)
