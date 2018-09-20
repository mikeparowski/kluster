from bs4 import BeautifulSoup
from requests import get
import pymysql.cursors
import pymysql
import json

errorfile = open("../error.log", "w")
connection = pymysql.connect('localhost', user='root', password='root', db='kluster')
cursor = connection.cursor(pymysql.cursors.DictCursor)
sql = "SELECT * FROM breitbart;"# LIMIT 145,5;"
print "executing sql..."
cursor.execute(sql)
print "completed sql"

count = 0
for article in cursor:
    count += 1
    print "scraping article {}...".format(count)
    title = article['title'].replace("/", "_")
    author = article['author']
    url = article['url']
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        header = soup.find('div', 'entry-content').h2.text
    except AttributeError as e:
        errorfile.write("url {} HEADER error {}".format(url, str(e)))
        header = ""
    article = header
    try:
        body = soup.find('div', 'entry-content').find_all('p')
        for paragraph in body:
            article += paragraph.text + ' '
    except AttributeError as e:
        errorfile.write("url {} BODY error {}".format(url, str(e)))
        body = ""
    with open("../articles/"+title[:30]+".bb", 'w') as outfile:
        json.dump({'title': title, 'author': author, 'article': article}, outfile)

errorfile.close()

