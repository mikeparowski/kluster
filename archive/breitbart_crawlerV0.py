from bs4 import BeautifulSoup
from requests import get

MAX_PAGE = 99

class BbCrawler():
    def __init__(self):
        self.url = 'http://www.breitbart.com/news/page/'
        self.articles = []
        self.num_articles = 0
        self.page = 0

    def _soupify(self, url):
        #print url
        return BeautifulSoup(get(url).text, 'html.parser')

    def get_num_articles(self):
        return self.num_articles

    def next_page(self):
        if self.page == MAX_PAGE:
            return None
        self.page += 1
        print "crawling page {}/{}".format(self.page, MAX_PAGE)
        next_page = self.url + str(self.page) + '/'

        return next_page

    def crawl(self, url):
        soup = self._soupify(url)
        links = soup.find_all('article')
        for link in links:
            link = link.a.get('href')
            self.articles.append(link)

        return self._extract(self.articles)

    def _writefile(self, title, text):
        with open(title+".bb", "w") as output:
            output.write("{}".format(text.encode('utf-8')))

    def _extract(self, articles):
        for page in articles:
            self.num_articles += 1
            soup = self._soupify(page)
            title = soup.h1.text[:30].replace(" ", "_").lower()
            title = ''.join([i if ord(i) < 128 else 'u' for i in title])
            paragraphs = soup.find('div', {'class': 'entry-content'}).find_all('p')
            text = ' '.join([paragraph.text for paragraph in paragraphs])
            self._writefile(title, text)

crawler = BbCrawler()
page = crawler.next_page()
while page is not None:
    crawler.crawl(page)
    page = crawler.next_page()

print "Crawled {} articles and saved to individual files".format(crawler.get_num_articles())

