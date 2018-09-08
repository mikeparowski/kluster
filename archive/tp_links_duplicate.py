from bs4 import BeautifulSoup
from requests import get
import pymysql.cursors
import pymysql

MAX_PAGE = 2

connection = pymysql.connect(host='localhost', user='root', password='root', db='kluster')
sql = "INSERT IGNORE INTO thinkprogress (title, author, url) VALUES (%s, %s, %s)"

class TPCrawler():
    def __init__(self):
        self.url = 'https://www.thinkprogress.org/latest/page/'
        self.page = -1

    def next_page(self):
        self.page += 1
        if self.page == MAX_PAGE:
            return None
        next_page = self.url + str(self.page) + '/'

        return next_page

    def get_links(self, url):
        response = get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article')
        for art in articles:
            url = art.find('header', {'class': 'post__header'}).a.get('href')
            title = art.find('header', {'class': 'post__header'}).a.text.replace(" ", "_").lower()
            title = ''.join([i if ord(i) < 128 else '' for i in title])
            author = art.findAll('span', {'class': 'author vcard'}).text
            # upload to local mysql db
            with connection.cursor() as cursor:
                cursor.execute(sql, (title, author, url))
            connection.commit()


## Main
crawler = TPCrawler()
next_page = crawler.next_page()
while next_page is not None:
    print next_page
    crawler.get_links(next_page)
    next_page = crawler.next_page()

connection.close()
