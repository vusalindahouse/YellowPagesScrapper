import json
import requests
from bs4 import BeautifulSoup
import gspread
import pandas as pd
sheet_id = "1bYm6xoJb6vp4d7ELTZpLDamsyj4ZXUT_9KgWxjt1dcM"
data = []
list_=[]




class YellowPages:
    def get_html(self, url):
        r = requests.get(url)
        return r.text


    def add_to_sheets(self):
        for page in range(30):
            url = f'https://www.yellowpages.com/search?search_terms=Video%2FFilm%20Production&geo_location_terms=Los%20Angeles%2C%20CA&page={page}'
            r = self.get_html(url)

            soup = BeautifulSoup(r, 'lxml')
            posts = soup.find_all('div', class_='result')

            for p in posts:
                title = p.find('a', class_='business-name').text

                number = p.find('div', class_='phones phone primary')
                if number is not None:
                    number = "".join(p.find('div', class_='phones phone primary').get('href')).replace('tel:', '')
                else:
                    number = None

                adress = p.find('div', class_='street-address')
                if adress is not None:
                    adress = p.find('div', class_='street-address').text
                else:
                    adress = None

                site = p.find('a', class_='track-visit-website')
                if site is not None:
                    site = p.find('a', class_='track-visit-website').get('href')
                else:
                    site = None



                data.append({'title': title,
                             'number': number,
                             'adress': adress,
                             'site': site,
                                             })

                link = 'https://yellowpages.com' + p.find('a', class_='business-name').get('href')
                list_.append(link)

        df = pd.DataFrame(data)

        gc = gspread.service_account(filename='creds.json')
        wks = gc.open("Los Angeles").sheet1
        wks.update([df.columns.values.tolist()] + df.values.tolist())

        return list_



    def get_email(self, html):
        result = pd.DataFrame(columns=['Emails'])
        data = []

        soup = BeautifulSoup(html, 'lxml')
        poct = soup.find('a', class_='email-business')
        if poct is not None:
            poct = soup.find('a', class_='email-business').get('href').replace('mailto:', '')
        elif poct is None:
            poct = None

        print(poct)





yp = YellowPages()
url_list = yp.add_to_sheets()

for url in url_list:
    yp.get_email(yp.get_html(url))