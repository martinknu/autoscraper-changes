import requests

import pandas as pd
from bs4 import BeautifulSoup

response = requests.get("https://www.dr.dk/nyheder") #https://www.bbc.com/ : https://www.dr.dk/nyheder/
doc = BeautifulSoup(response.text, 'html.parser')

#print(doc.prettify())

#articles = doc.find_all("article")[0]

#print(articles)


stories = doc.select("article.hydra-latest-news-page-short-news")

#print(stories)

rows = []

for story in stories:
    row = {}

    row['title'] = story.select_one('h2').text.strip() #.dre-hyphenate-text

    try:
        row['href'] = story.select_one('.dre-share-link-copy-url')['href']
    except:
        pass

    try:
        row['tag'] = story.select_one('.media__tag').text.strip()
    except:
        pass

    try:
        mySubjects = story.find_all(["p ", "span"], "hydra-latest-news-page-short-news__paragraph dre-variables", "display:inline")#.text.strip() # 
        #myResult = ""
        #for mySubject in mySubjects:
        #    myResult += mySubject
        #    print(myResult)
            
        row['summary'] = story.find_all(["p", "span"], "hydra-latest-news-page-short-news__paragraph dre-variables")
    except:
        pass

    rows.append(row)

#print(rows)
df = pd.DataFrame(rows)
df.to_csv("bbc-headlines.csv", index=True)
