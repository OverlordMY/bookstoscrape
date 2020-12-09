from bs4 import BeautifulSoup
import requests
import pandas as pd


def book_scraping():

    global df
    web_page = r'http://books.toscrape.com/'
    sectioned_next_page_url = r'catalogue/page-'
    page_number = 1
    page_html = '.html'

    titles = []
    book_price = []
    star_rating = []
    book_status = []

    while True:
        try:
            link = web_page + sectioned_next_page_url + str(page_number) + page_html
            connect = requests.get(link, 'lxml')

            web_url = web_page+sectioned_next_page_url+str(page_number)+page_html

            requesting = requests.get(web_url).text

            soup = BeautifulSoup(requesting, 'lxml')

            for row in soup.find_all('img'):
                titles.append(row['alt'])

            for row in soup.find_all('p', class_='price_color'):
                book_price.append(row.text[2:])

            for row in soup.find_all('p', class_='instock availability'):
                book_status.append(row.text.strip())

            for row in soup.find_all('p', {'class': 'star-rating'}):
                star_rating.append(row['class'][1])

            df = pd.DataFrame(titles, columns=['Titles'])
            df['Book Price'] = book_price
            df['Star Rating'] = star_rating
            df['Book Status'] = book_status

            page_number += 1
            if connect.ok is False:
                break
        except Exception as e:
            print(e)


book_scraping()

df.to_csv('bookstoscrape.csv')







