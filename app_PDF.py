import requests
from bs4 import BeautifulSoup

import app_WEB

session = requests.session()
site = 'https://www.miit.ru'
session.post(site)

print(requests.get('https://www.miit.ru/timetable/216259', headers=app_WEB.headers).text)
if __name__ == "__main__":
    print(1)