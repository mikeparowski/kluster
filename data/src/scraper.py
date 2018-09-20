import newspaper
from newspaper import news_pool
from Tokenizer import Tokenizer
import os, string

print("building fox")
foxnews = newspaper.build('http://foxnews.com', language='en')
print("building breitbart")
breitbart = newspaper.build('https://www.breitbart.com', language='en')
print("building thinkprogress")
thinkprogress = newspaper.build('https://thinkprogress.org', language='en')
print("buildling cnn")
cnn = newspaper.build('https://www.cnn.com')
print("building atlantic")
atlantic = newspaper.build('https://www.theatlantic.com', language='en')
print("building vice")
vice = newspaper.build('https://www.vice.com/en_us', language='en')
print("building blaze")
blaze = newspaper.build('https://www.theblaze.com', language='en')
print("building federalist")
federalist = newspaper.build('http://thefederalist.com', language='en')
print("building wsj")
wsj = newspaper.build('https://www.wsj.com', language='en')
print("buildling nyt")
nyt = newspaper.build('https://www.nytimes.com', language='en')
#print("building huffpost")
#huffpost = newspaper.build('https://www.huffingtonpost.com/?country=US', language='en')

extensions = {
    foxnews: ".fx",
    breitbart: ".bb",
    thinkprogress: ".tp",
    cnn: ".cnn",
    atlantic: ".atl",
    vice: ".vc",
    blaze: ".blz",
    federalist: ".fd",
    wsj: ".wsj",
    nyt: ".nyt",
    #huffpost: ".huf"
}

papers = [foxnews, breitbart, thinkprogress, cnn, atlantic, vice, blaze, federalist, wsj, nyt]#, huffpost]
news_pool.set(papers, threads_per_source=5)
news_pool.join()

translator = str.maketrans('', '', string.punctuation)
tk = Tokenizer()
for source in papers:
    name = source.domain.split(".")
    if name[0] == "www":
        name = name[1]
    else:
        name = name[0]
    print("beginning {} crawl".format(name))
    directory = '../articles/'+name
    if not os.path.exists(directory):
        os.makedirs(directory)
    for article in source.articles:
        article.parse()
        title = article.title.translate(translator)
        title = title.lower().replace(" ", "_")
        title += extensions[source]
        text = tk.clean(article.text)
        with open(os.path.join(directory, title), 'w+') as f:
            f.write(text)


total = foxnews.size() + breitbart.size() + thinkprogress.size() + cnn.size() + atlantic.size() + vice.size() + blaze.size() + federalist.size() + wsj.size() + nyt.size()# + huffpost.size()
print("Total: {}".format(total))
print("FoxNews: {}%".format(round(foxnews.size()/total*100)))
print("Breitbart: {}%".format(round(breitbart.size()/total*100)))
print("ThinkProgress: {}%".format(round(thinkprogress.size()/total*100)))
print("TheAtlantic: {}%".format(round(atlantic.size()/total*100)))
print("CNN: {}%".format(round(cnn.size()/total*100)))
print("Vice: {}%".format(round(vice.size()/total*100)))
print("Blaze: {}%".format(round(blaze.size()/total*100)))
print("TheFederalist: {}%".format(round(federalist.size()/total*100)))
print("WSJ: {}%".format(round(wsj.size()/total*100)))
print("NYTimes: {}%".format(round(nyt.size()/total*100)))
#print("HuffPost: {}%".format(round(huffpost.size()/total*100)))
