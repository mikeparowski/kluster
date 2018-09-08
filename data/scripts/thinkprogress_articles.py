from bs4 import BeautifulSoup
from requests import get
import pymysql.cursors
import pymysql
import json

connection = pymysql.connect('localhost', user='root', password='root', db='kluster')
cursor = connection.cursor(pymysql.cursors.DictCursor)
sql = "SELECT * FROM thinkprogress"# 145,5;"
cursor.execute(sql)

count = 0
for article in cursor:
    count += 1
    print "scraping article {}...".format(count)
    title = article['title'].replace("/", "_")
    author = article['author']
    url = article['url']
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.find('div', 'post__content').find_all('p')
    article = ''
    for paragraph in text:
        article += paragraph.text + ' '
    with open("../articles/"+title[:30]+".tp", 'w') as outfile:
        json.dump({'title': title, 'author': author, 'article': article}, outfile)

