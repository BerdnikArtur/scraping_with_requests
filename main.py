import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import lxml
import json

def serch_data(town):
    user = UserAgent()
    headers = {"Accept": "*/*",
               "User-Agent": user.random}
    data = list()
    
    try:
        req = requests.get(url='https://www.ticketland.ru/', headers=headers)
    except Exception as ex:
        print(f'Error: {ex} --- code: {req.status_codes} --- second request')

    with open('data.html', 'w') as file:
        file.write(req.text)

    with open('data.html', 'r') as file:
        soup = BeautifulSoup(file, 'lxml')

    list_of_towns = soup.find('ul', {'class': 'dropdown__list'}).find_all('li', {'class': 'dropdown__item'})
    list_of_abbreviation = {}
    
    for i in list_of_towns:
        list_of_abbreviation[i.text.strip()] = i.get('data-js-dd-item').split('/')[2]
        if town == 'Москва':
            path = 'https://ticketland.ru/'
        elif i.text.strip() == town:
            abb = i.get('data-js-dd-item').split('/')[2]
            path = f'https://{abb}.ticketland.ru/'

    number = 0
    offset = 0

    while True:
        try:
            if offset == 0:
                req_of_town = requests.get(url=f"https://{list_of_abbreviation[town]}.ticketland.ru/", headers=headers)
            else:
                req_of_town = requests.get(url=f"https://{list_of_abbreviation[town]}.ticketland.ru/show/jsGetPopular/?offset={offset}", headers=headers)
        except Exception as ex:
            print(f'Error: {ex} --- code: {req_of_town.status_codes} --- second request')

        soup = BeautifulSoup(req_of_town.text, 'lxml')

        items = soup.find_all('div', {'class': 'col d-flex mb-3'})

        if items == []:
            break

        for item in items:
            name = item.find('div', {'class': 'card__title-text'}).text.strip()
            date_and_time = item.find('div', {'class': 'tag tag--white card__date'}).text.strip()
            place = item.find('a', {'class': 'card__building pb-1 text-truncate'}).text.strip()
            price = item.find('p', {'class': 'card__price'}).text.strip()
            link = f'https://{list_of_abbreviation[town]}.ticketland.ru' + item.find('a', {'class': 'card__title pb-1 pt-1'}).get('href')

            data.append({
                'name': name,
                'date_and_time': date_and_time,
                'place': place,
                'price': price,
                'link': link
            })
        
            print(f'{number} item is done')
            number += 1

        offset += 24

    with open(f'data_of_{list_of_abbreviation[town]}.json', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    

if __name__=='__main__':
    town = input('enter the town you need: ')
    serch_data(town)