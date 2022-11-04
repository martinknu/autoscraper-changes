import requests
import pandas as pd
from bs4 import BeautifulSoup


response = requests.get("https://www.dr.dk/nyheder") 
doc = BeautifulSoup(response.text, 'html.parser')

stories = doc.select("article.hydra-latest-news-page-short-news")

rows = []

for story in stories:
    row = {}

    row['title'] = story.select_one('h2').text.strip() #.dre-hyphenate-text

    try:
        row['href'] = story.select_one("a")['href']
    except:
        pass

    try:
        row['tag'] = story.select_one('.media__tag').text.strip()
    except:
        pass

    try:
        mySubjects = story.find_all("p", 'hydra-latest-news-page-short-news__paragraph dre-variables')#.text.strip() # 
        mySubject = str(mySubjects).replace("hydra-latest-news-page-short-news__paragraph dre-variables", "")
        mySubject = mySubject.replace("\"", "")     
        mySubject = mySubject.replace("[<p class=>", "")     
        mySubject = mySubject.replace("<span style=display:inline><span class=dre-glossary-match>", "")     
        mySubject = mySubject.replace("</span></span>", "")     
        mySubject = mySubject.replace("</p>, <p class=>", "")     
        mySubject = mySubject.replace("</p>]", "")     
        mySubject = mySubject.replace("rel=noopener noreferrer target=_blank>", "")     
   
        row['summary'] = mySubject
    except:
        pass

    rows.append(row)

df = pd.DataFrame(rows)
df.to_csv("news.csv", index=True)
