import json
import os
import requests
import uuid

URL="https://newsapi.org/v2/everything"
API_KEY="224aed70fc5e450e93a7b2c745e7efd9"
COUNT=10

def fetch_news():
    all_articles=[]
    params={"apiKey":API_KEY,"pageSize":COUNT,"q":"bitcoin"}
    news_api=requests.get(URL,params=params)
    news_api.raise_for_status()
    response=news_api.json()
    if "articles" in response:
        all_articles.extend(response["articles"])
    else:
        print("no article found")
    return all_articles

def save_article(Articles):
    for article in Articles:
        article_id=str(uuid.uuid4())
        file_path=os.path.join("queue",f"{article_id}.json")   # f"arcticle_{i+1}.json"
        with open (file_path,"w")as f:
            json.dump(article,f,indent=4)
        
if __name__=="__main__":
    articles=fetch_news()   # r else fetch_news(API_KEY,COUNT)
    #print(articles)
    save_article(articles)