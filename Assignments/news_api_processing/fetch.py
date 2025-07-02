import requests

URL="https://newsapi.org/v2/everything"
API_KEY="224aed70fc5e450e93a7b2c745e7efd9"
COUNT=10
page=2

def fetch_news():
    all_articles=[]
    for page in range(1,page+1):
        params={"apiKey":API_KEY,"pageSize":COUNT,"q":"bitcoin","page":page}
        news_api=requests.get(URL,params=params)
        news_api.raise_for_status()
        response=news_api.json()
        if "articles" in  response:
            all_articles.extend(response["articles"])
        else:
            print(f"no articles found in page {page}")
    return all_articles
       
if __name__=="__main__":
    articles=fetch_news()  # r else fetch_news(API_KEY,COUNT)
    print(f"\nno of articles fetched: {len(articles)}")
    for article in articles:
        print("\n")
        print(article)


# DIFFERENCE BTW PAGESIZE AND PAGE

# pageSize--> no of articles u want  page--->from which page(pagination index).max no of articles per page is 100
# if u take params{page=2} u'll get 10 art from page 2
# r if want many so u can loop through pages