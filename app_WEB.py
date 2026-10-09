import requests
from bs4 import BeautifulSoup
import threading
import json


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'https://google.com'
}

session = requests.session()
site = 'https://www.miit.ru'
session.post(site, headers=headers)


def study_group_numbers():
    with open("post_WEB.json", "r", encoding="utf-8") as f:
        post = json.load(f)

    response = session.get(site + '/timetable', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []

    for i in soup.find('div', class_='info-block info-block_collapse show', id=post["institute"]).find_all('a', class_='dropdown-item'):
        data.append((i.text.replace('\r\n', '').replace(' ', ''), i.get("href").split('/')[-1]))

    return data

def get_all_audiences(group, k):
    for i in range(k, len(group)-k, 10):
        response = session.get(site+"/timetable/"+group[i][1], headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        for j in soup.find_all('tr'):
            days = [k.text[:k.text.find('\r\n')] for k in j.find_all('th')]
            if not days:
                schedule = [j.find('td', class_='text-right').text[1:].replace('\r\n                    ', '')]
                for l in j.find_all('td', class_='timetable__grid-day'):
                    if l.find_all('div', class_='mb-2'):
                        schedule.append(l.find_all('div', class_='mb-2')[-1].text.replace("\n\n\n\n", '').replace("\r\n", '').replace('Аудитория ', '').replace(' ', ''))
                    else:
                        schedule.append('')
                print(schedule)
            else:
                print(days)



if __name__ == "__main__":
    group = study_group_numbers()
    print(len(group)//100+1)
    print(len(group))
    for j in range(10):
        threading.Thread(target=get_all_audiences, args=(group, j,)).start()
