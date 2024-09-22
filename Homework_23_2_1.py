import requests
from bs4 import BeautifulSoup
import pandas as pd

def collect_user_rates(user_login):
   page_num = 1
   data = []

   while True:
       url = f'https://www.kinopoisk.ru/user/{user_login}/votes/list/vs/vote/page/{page_num}/#list'
       html_content = requests.get(url).text
       soup = BeautifulSoup(html_content, 'lxml')
       entries = soup.find_all('div', class_='item')
       if len(entries) == 0:  # Признак остановки
           break
       for entry in entries:
           #Считываем название фильма
           nameRus = entry.find('div', class_='nameRus')
           film_name = nameRus.find('a').text
           #в данном списке дата релиза указана в названии, поэтому вытаскиваем год выпуска из названия
           get_values = lambda film_: [i.split(')', 1)[0] for i in film_.split('(')][1:]
           release_date = get_values(film_name)
           release_date = release_date[0]

           #рейтинг пользователя
           vote = entry.find('div', class_='vote').text
           data.append({'film_name': film_name, 'release_date': release_date, 'rating': vote})

       page_num += 1  # Переходим на следующую страницу
   return data

user_rates = collect_user_rates(user_login='182904044') #собираем данные о названии фильма, дате релиза и его рейтинге в файл
df = pd.DataFrame(user_rates)
df.to_excel('user_rates.xlsx')  #Выводим собранные данные в Excel файл
print(df)

