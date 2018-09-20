from newsapi import NewsApiClient
import pymysql.cursors
import pymysql

connection = pymysql.connect(host='localhost', user='root', password='root', db='kluster')
sql = "INSERT IGNORE INTO breitbart (title, author, url) VALUES (%s, %s, %s)"

# VV mparowsk api key. maxed out ptjfa -__- 
newsapi = NewsApiClient(api_key='19735570ecae46fb8998ef350936a542')
testdb = []
for i in xrange(1, 251):
    # newsapi page of 20 articles
    page = newsapi.get_everything(sources='breitbart-news', page=i)['articles']
    # iterate over each article collecting desired data
    for j in xrange(len(page)):
        title = page[j]['title'].replace(" ", "_").lower()
        title = ''.join([i if ord(i) < 128 else '' for i in title])
        author = page[j]['author']
        url = page[j]['url']
        # upload to local mysql db
        with connection.cursor() as cursor:
            cursor.execute(sql, (title, author, url))
        connection.commit()

connection.close()
