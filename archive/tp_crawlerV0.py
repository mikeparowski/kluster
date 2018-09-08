from bs4 import BeautifulSoup
from requests import get
import json

MAX_PAGE = 500

class TPCrawler():
    def __init__(self):
        self.url = 'https://www.thinkprogress.org/latest/page/'
        self.articles = {}
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
            url = art.findAll("header", {"class": "post__header"})[0].a.get("href")
            title = art.findAll("header", {"class": "post__header"})[0].a.text
            author = art.findAll("span", {"class": "author vcard"})[0].text
            self.articles[url] = (title, author)

        return self.articles

## Main
links = []
crawler = TPCrawler()
next_page = crawler.next_page()
while next_page is not None:
    print next_page
    links.append(crawler.get_links(next_page))
    next_page = crawler.next_page()

with open('thinkprogressive.dat', 'wb') as f:
    f.write(json.dumps(links))

